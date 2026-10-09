# Copyright 2021-2026 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
TLS and mutual TLS, end to end, through the SDK's real ``Client`` and ``AsyncClient``.

The SIP clients never build a channel themselves: ``ServicesInterface`` / ``AsyncServicesInterface``
hand the config to ``ondewo-client-utils``, which presents ``grpc_client_cert`` / ``grpc_client_key``.
These tests prove that wiring against a real in-process gRPC server with certificates minted per
module (no private key is committed): an RPC that reaches the servicer-less server answers
``UNIMPLEMENTED``, which means the handshake succeeded; a refused handshake answers ``UNAVAILABLE``. The clients
run with their default channel options (every SIP method is outside the idempotent retry policy).
"""

import asyncio
import datetime
from concurrent import futures
from typing import (
    Callable,
    Iterator,
    List,
    Optional,
)

import grpc
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import (
    ExtendedKeyUsageOID,
    NameOID,
)

from ondewo.sip.client.async_client import AsyncClient
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig
from ondewo.sip.sip_pb2 import SipRegisterAccountRequest

SERVER_NAME: str = "localhost"
PASSWORD: str = "sip-login-password"


class Pki:
    """One throwaway CA with a server leaf (SAN ``localhost``) and a client leaf, all PEM bytes."""

    def __init__(self, name: str) -> None:
        self._ca_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        self.ca_cert: bytes = self._issue(f"{name}-ca", self._ca_key.public_key(), ca=True, issuer=None)
        ca: x509.Certificate = x509.load_pem_x509_certificate(self.ca_cert)
        server_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        self.server_key: bytes = _pem_key(server_key)
        self.server_cert: bytes = self._issue(
            f"{name}-server", server_key.public_key(), False, ca, ExtendedKeyUsageOID.SERVER_AUTH, SERVER_NAME
        )
        client_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        self.client_key: bytes = _pem_key(client_key)
        self.client_cert: bytes = self._issue(
            f"{name}-client", client_key.public_key(), False, ca, ExtendedKeyUsageOID.CLIENT_AUTH
        )

    def _issue(
        self,
        subject: str,
        public_key: ec.EllipticCurvePublicKey,
        ca: bool,
        issuer: Optional[x509.Certificate],
        usage: Optional[x509.ObjectIdentifier] = None,
        san: Optional[str] = None,
    ) -> bytes:
        now: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        name: x509.Name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject)])
        builder: x509.CertificateBuilder = (
            x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name if issuer is None else issuer.subject)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=30))
            .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True)
        )
        if usage is not None:
            builder = builder.add_extension(x509.ExtendedKeyUsage([usage]), critical=False)
        if san is not None:
            builder = builder.add_extension(x509.SubjectAlternativeName([x509.DNSName(san)]), critical=False)
        return builder.sign(self._ca_key, hashes.SHA256()).public_bytes(serialization.Encoding.PEM)


def _pem_key(key: ec.EllipticCurvePrivateKey) -> bytes:
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


@pytest.fixture(scope="module")
def pki() -> Pki:
    return Pki("deployment")


@pytest.fixture(scope="module")
def foreign() -> Pki:
    return Pki("foreign")


def _server_credentials(pki: Pki, require_client_auth: bool) -> grpc.ServerCredentials:
    return grpc.ssl_server_credentials(
        [(pki.server_key, pki.server_cert)],
        root_certificates=pki.ca_cert if require_client_auth else None,
        require_client_auth=require_client_auth,
    )


@pytest.fixture
def server() -> Iterator[Callable[[Pki, bool], int]]:
    """Start a servicer-less TLS server on an ephemeral port; ``(pki, require_client_auth) -> port``."""
    servers: List[grpc.Server] = []

    def start(pki: Pki, require_client_auth: bool) -> int:
        grpc_server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        port: int = grpc_server.add_secure_port("localhost:0", _server_credentials(pki, require_client_auth))
        grpc_server.start()
        servers.append(grpc_server)
        return port

    yield start
    for grpc_server in servers:
        grpc_server.stop(grace=None)


def _config(
    port: int,
    trust: Pki,
    identity: Optional[Pki] = None,
    crlf: bool = False,
) -> ClientConfig:
    """A SIP config trusting ``trust``'s CA, presenting ``identity``'s client leaf when given."""

    def pem(value: bytes) -> str:
        return (value.replace(b"\n", b"\r\n") if crlf else value).decode()

    return ClientConfig(
        host=SERVER_NAME,
        port=str(port),
        grpc_cert=pem(trust.ca_cert),
        grpc_client_cert=None if identity is None else pem(identity.client_cert),
        grpc_client_key=None if identity is None else pem(identity.client_key),
        user_name="tech-user@example.com",
        password=PASSWORD,
    )


def _sync_call(config: ClientConfig) -> grpc.StatusCode:
    """Make one real RPC through ``Client`` and return its status code."""
    client: Client = Client(config=config, use_secure_channel=True)
    try:
        with pytest.raises(grpc.RpcError) as error:
            client.services.sip.register_account(SipRegisterAccountRequest(account_name="a", password="p"))
        code: grpc.StatusCode = error.value.code()  # type: ignore[attr-defined]
        return code
    finally:
        client.disconnect()


def _async_call(config: ClientConfig) -> grpc.StatusCode:
    """Make one real RPC through ``AsyncClient`` (built inside the running loop) and return its status code."""

    async def call() -> grpc.StatusCode:
        client: AsyncClient = AsyncClient(config=config, use_secure_channel=True)
        try:
            with pytest.raises(grpc.aio.AioRpcError) as error:
                await client.services.sip.register_account(SipRegisterAccountRequest(account_name="a", password="p"))
            return error.value.code()
        finally:
            await client.services.sip.grpc_channel.close()

    return asyncio.run(call())


CALLS: List[Callable[[ClientConfig], grpc.StatusCode]] = [_sync_call, _async_call]
CALL_IDS: List[str] = ["Client", "AsyncClient"]


@pytest.mark.parametrize("call", CALLS, ids=CALL_IDS)
class TestHandshakes:
    def test_plain_tls_reaches_the_server(
        self, call: Callable[[ClientConfig], grpc.StatusCode], server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        assert call(_config(server(pki, False), pki)) is grpc.StatusCode.UNIMPLEMENTED

    def test_mutual_tls_reaches_a_server_requiring_client_certs(
        self, call: Callable[[ClientConfig], grpc.StatusCode], server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        assert call(_config(server(pki, True), pki, identity=pki)) is grpc.StatusCode.UNIMPLEMENTED

    def test_crlf_pems_complete_the_mutual_tls_handshake(
        self, call: Callable[[ClientConfig], grpc.StatusCode], server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        assert call(_config(server(pki, True), pki, identity=pki, crlf=True)) is grpc.StatusCode.UNIMPLEMENTED

    def test_empty_identity_on_both_is_plain_tls(
        self, call: Callable[[ClientConfig], grpc.StatusCode], server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        config: ClientConfig = ClientConfig(
            host=SERVER_NAME,
            port=str(server(pki, False)),
            grpc_cert=pki.ca_cert.decode(),
            grpc_client_cert="",
            grpc_client_key="",
            user_name="tech-user@example.com",
            password=PASSWORD,
        )
        assert call(config) is grpc.StatusCode.UNIMPLEMENTED

    def test_no_identity_is_refused_by_a_server_requiring_client_certs(
        self, call: Callable[[ClientConfig], grpc.StatusCode], server: Callable[[Pki, bool], int], pki: Pki
    ) -> None:
        assert call(_config(server(pki, True), pki)) is grpc.StatusCode.UNAVAILABLE

    def test_an_identity_from_an_unrelated_ca_is_refused(
        self,
        call: Callable[[ClientConfig], grpc.StatusCode],
        server: Callable[[Pki, bool], int],
        pki: Pki,
        foreign: Pki,
    ) -> None:
        assert call(_config(server(pki, True), pki, identity=foreign)) is grpc.StatusCode.UNAVAILABLE

    def test_a_server_from_an_untrusted_ca_is_refused(
        self,
        call: Callable[[ClientConfig], grpc.StatusCode],
        server: Callable[[Pki, bool], int],
        pki: Pki,
        foreign: Pki,
    ) -> None:
        assert call(_config(server(pki, False), foreign)) is grpc.StatusCode.UNAVAILABLE


@pytest.mark.parametrize("dropped", ["grpc_client_cert", "grpc_client_key"])
def test_half_a_client_identity_is_refused_by_the_config(pki: Pki, dropped: str) -> None:
    """Half a pair would make grpc core abort the process; the config raises before any channel exists."""
    identity: dict = {"grpc_client_cert": pki.client_cert.decode(), "grpc_client_key": pki.client_key.decode()}
    identity[dropped] = None
    with pytest.raises(ValueError, match="set both to use mutual TLS, or neither") as refusal:
        ClientConfig(
            host=SERVER_NAME,
            port="1",
            grpc_cert=pki.ca_cert.decode(),
            user_name="tech-user@example.com",
            password=PASSWORD,
            **identity,
        )
    assert "PRIVATE KEY" not in str(refusal.value)
    assert "CERTIFICATE" not in str(refusal.value)


@pytest.mark.parametrize("client_class", [Client, AsyncClient], ids=CALL_IDS)
def test_an_insecure_channel_is_refused_for_a_client_identity(pki: Pki, client_class: type) -> None:
    """``use_secure_channel=False`` would drop the identity silently; both clients refuse instead."""
    config: ClientConfig = _config(1, pki, identity=pki)

    async def build() -> None:
        client_class(config=config, use_secure_channel=False)

    with pytest.raises(ValueError, match="use a secure channel") as refusal:
        asyncio.run(build())
    assert "PRIVATE KEY" not in str(refusal.value)
    assert PASSWORD not in str(refusal.value)


def test_repr_and_str_never_render_the_key_or_the_password(pki: Pki) -> None:
    config: ClientConfig = _config(1, pki, identity=pki)
    for rendered in (repr(config), str(config)):
        assert "PRIVATE KEY" not in rendered
        assert pki.client_key.decode() not in rendered
        assert PASSWORD not in rendered
        assert "grpc_client_key='***REDACTED***'" in rendered
        assert "password='***REDACTED***'" in rendered
