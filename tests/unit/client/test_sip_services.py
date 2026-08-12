# Copyright 2021-2025 ONDEWO GmbH
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
"""Behavioural tests proving every SIP service method attaches the right gRPC metadata.

Both the sync (`ondewo.sip.client.services.sip.Sip`) and async
(`ondewo.sip.client.services.async_sip.Sip`) wrappers are exercised without any network:
the Keycloak token provider is built with a fake HTTP transport and the generated `SipStub`
is replaced by a recording fake. Every one of the 11 RPC wrappers is asserted to forward the
bearer metadata under the Keycloak path and an empty metadata list under the non-Keycloak
path — the two branches of the `metadata` property.
"""

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
)

import pytest

import ondewo.sip.client.async_services_interface as async_base_module
import ondewo.sip.client.services.async_sip as async_sip_module
import ondewo.sip.client.services.sip as sync_sip_module
import ondewo.sip.client.services_interface as sync_base_module
import ondewo.sip.sip_pb2 as sip
from ondewo.sip.client.client_config import ClientConfig
from ondewo.sip.client.services.async_sip import Sip as AsyncSip
from ondewo.sip.client.services.sip import Sip as SyncSip
from ondewo.sip.utils.keycloak import KeycloakTokenProvider

# Bound exactly once so a refactor that changes only an input or only an expectation cannot
# silently make an assertion tautological.
HOST: str = "localhost"
PORT: str = "50055"
USERNAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t"
KEYCLOAK_URL: str = "https://kc.example.com/auth"
REALM: str = "ondewo-ccai-platform"
CLIENT_ID: str = "ondewo-sip-cai-sdk-public"
ACCESS_TOKEN: str = "acc-1"
EXPECTED_KEYCLOAK_METADATA: List[Tuple[str, str]] = [("authorization", f"Bearer {ACCESS_TOKEN}")]
EXPECTED_EMPTY_METADATA: List[Tuple[str, str]] = []

# Service wrapper method -> the generated stub RPC it must call. Covers all 11 SIP RPCs.
STUB_METHOD_NAMES: Dict[str, str] = {
    "start_session": "SipStartSession",
    "end_session": "SipEndSession",
    "register_account": "SipRegisterAccount",
    "start_call": "SipStartCall",
    "end_call": "SipEndCall",
    "transfer_call": "SipTransferCall",
    "get_sip_status": "SipGetSipStatus",
    "get_sip_status_history": "SipGetSipStatusHistory",
    "play_wav_files": "SipPlayWavFiles",
    "mute": "SipMute",
    "un_mute": "SipUnMute",
}
SERVICE_METHODS: List[str] = list(STUB_METHOD_NAMES)

# Service methods that take a request message; the rest send an `Empty`.
_REQUEST_FACTORIES: Dict[str, Any] = {
    "start_session": sip.SipStartSessionRequest,
    "register_account": sip.SipRegisterAccountRequest,
    "start_call": sip.SipStartCallRequest,
    "end_call": sip.SipEndCallRequest,
    "transfer_call": sip.SipTransferCallRequest,
    "play_wav_files": sip.SipPlayWavFilesRequest,
}

_SENTINEL_RESPONSE: sip.SipStatus = sip.SipStatus()


class _FakeResponse:
    """Minimal `requests.Response` stand-in satisfying the provider's `TokenResponse`."""

    def __init__(self, status_code: int, body: Dict[str, Any]) -> None:
        """Store the canned HTTP status code and JSON body.

        Args:
            status_code (int):
                The HTTP status code the provider reads on `response.status_code`.
            body (Dict[str, Any]):
                The JSON body returned by `json()` and reflected in `text`.
        """
        self.status_code: int = status_code
        self._body: Dict[str, Any] = body

    def json(self) -> Dict[str, Any]:
        """Return the canned JSON body.

        Returns:
            Dict[str, Any]:
                The stored response body.
        """
        return self._body

    @property
    def text(self) -> str:
        """Return the raw body representation used in error messages.

        Returns:
            str:
                `repr()` of the stored body.
        """
        return repr(self._body)


class _FakeTransport:
    """Fake token endpoint that replays a single canned login response with no network."""

    def __init__(self, response: _FakeResponse) -> None:
        """Store the canned login response.

        Args:
            response (_FakeResponse):
                The response returned for the one-time ROPC login POST.
        """
        self._response: _FakeResponse = response

    def post(self, url: str, data: Dict[str, str], timeout: float) -> _FakeResponse:
        """Return the canned response, ignoring the request (no network is touched).

        Args:
            url (str):
                The token-endpoint URL (unused).
            data (Dict[str, str]):
                The form-encoded request parameters (unused).
            timeout (float):
                The request timeout (unused).

        Returns:
            _FakeResponse:
                The canned login response.
        """
        return self._response


def _build_fake_provider() -> KeycloakTokenProvider:
    """Build a `KeycloakTokenProvider` logged in via a fake transport, background refresh off.

    Returns:
        KeycloakTokenProvider:
            A provider whose `bearer_metadata()` yields `EXPECTED_KEYCLOAK_METADATA`.
    """
    transport: _FakeTransport = _FakeTransport(
        _FakeResponse(
            200,
            {
                "access_token": ACCESS_TOKEN,
                "refresh_token": "off-1",
                "expires_in": 300,
                "token_type": "Bearer",
            },
        ),
    )
    return KeycloakTokenProvider(
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
        username=USERNAME,
        password=PASSWORD,
        transport=transport,
        start_background_refresh=False,
    )


def _keycloak_config() -> ClientConfig:
    """Build a Keycloak-flagged client config (`use_keycloak` is True).

    Returns:
        ClientConfig:
            A config carrying the full Keycloak triple.
    """
    return ClientConfig(
        host=HOST,
        port=PORT,
        user_name=USERNAME,
        password=PASSWORD,
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
    )


def _non_keycloak_config() -> ClientConfig:
    """Build a non-Keycloak client config (`use_keycloak` is False).

    Returns:
        ClientConfig:
            A config with only `user_name`/`password` set.
    """
    return ClientConfig(host=HOST, port=PORT, user_name=USERNAME, password=PASSWORD)


def _make_fake_stub_cls(recorder: Dict[str, Optional[List[Tuple[str, str]]]], is_async: bool) -> Type[Any]:
    """Build a fake `SipStub` class whose RPC methods record the metadata they receive.

    The real `stub` property constructs this per access, so recorded calls are written into the
    shared `recorder` dict rather than onto the (transient) stub instance.

    Args:
        recorder (Dict[str, Optional[List[Tuple[str, str]]]]):
            Sink mapping the called stub RPC name to the metadata it was passed.
        is_async (bool):
            Whether the RPC methods must be awaitable (async wrapper) or plain (sync wrapper).

    Returns:
        Type[Any]:
            A stub class accepting `channel=` and exposing every RPC via `__getattr__`.
    """

    class _FakeStub:
        """Records the metadata of each RPC call and returns the sentinel response."""

        def __init__(self, channel: Any) -> None:
            """Store the channel handed in by the `stub` property.

            Args:
                channel (Any):
                    The gRPC channel the real `stub` property passes through.
            """
            self._channel: Any = channel

        def __getattr__(self, name: str) -> Any:
            """Return a recorder callable standing in for the named stub RPC.

            Args:
                name (str):
                    The stub RPC attribute being accessed (e.g. `SipStartSession`).

            Returns:
                Any:
                    A sync or async callable that records `(name, metadata)` and returns the
                    sentinel response.
            """

            def _sync_call(request: Any, metadata: Optional[List[Tuple[str, str]]] = None) -> sip.SipStatus:
                recorder[name] = metadata
                return _SENTINEL_RESPONSE

            async def _async_call(request: Any, metadata: Optional[List[Tuple[str, str]]] = None) -> sip.SipStatus:
                recorder[name] = metadata
                return _SENTINEL_RESPONSE

            return _async_call if is_async else _sync_call

    return _FakeStub


def _invoke_sync(service: SyncSip, method_name: str) -> None:
    """Call a sync service wrapper method with a fresh request when one is required.

    Args:
        service (SyncSip):
            The sync SIP service wrapper under test.
        method_name (str):
            The wrapper method to invoke.
    """
    method = getattr(service, method_name)
    request_factory = _REQUEST_FACTORIES.get(method_name)
    if request_factory is not None:
        method(request=request_factory())
    else:
        method()


async def _invoke_async(service: AsyncSip, method_name: str) -> None:
    """Await an async service wrapper method with a fresh request when one is required.

    Args:
        service (AsyncSip):
            The async SIP service wrapper under test.
        method_name (str):
            The wrapper method to invoke.
    """
    method = getattr(service, method_name)
    request_factory = _REQUEST_FACTORIES.get(method_name)
    if request_factory is not None:
        await method(request=request_factory())
    else:
        await method()


@pytest.mark.parametrize("method_name", SERVICE_METHODS)
def test_sync_keycloak_methods_attach_bearer_metadata(
    monkeypatch: pytest.MonkeyPatch,
    method_name: str,
) -> None:
    """Under Keycloak auth every sync RPC forwards the `Authorization: Bearer` metadata.

    Args:
        monkeypatch (pytest.MonkeyPatch):
            Fixture used to inject the fake provider and the recording stub.
        method_name (str):
            The service wrapper method under test.
    """
    provider: KeycloakTokenProvider = _build_fake_provider()
    monkeypatch.setattr(sync_base_module, "get_keycloak_token_provider", lambda config: provider)
    recorder: Dict[str, Optional[List[Tuple[str, str]]]] = {}
    monkeypatch.setattr(sync_sip_module, "SipStub", _make_fake_stub_cls(recorder, is_async=False))

    service: SyncSip = SyncSip(config=_keycloak_config(), use_secure_channel=False)
    _invoke_sync(service, method_name)

    assert recorder[STUB_METHOD_NAMES[method_name]] == EXPECTED_KEYCLOAK_METADATA


@pytest.mark.parametrize("method_name", SERVICE_METHODS)
def test_sync_non_keycloak_methods_attach_empty_metadata(
    monkeypatch: pytest.MonkeyPatch,
    method_name: str,
) -> None:
    """Without Keycloak auth every sync RPC forwards an empty metadata list.

    Args:
        monkeypatch (pytest.MonkeyPatch):
            Fixture used to inject the recording stub.
        method_name (str):
            The service wrapper method under test.
    """
    recorder: Dict[str, Optional[List[Tuple[str, str]]]] = {}
    monkeypatch.setattr(sync_sip_module, "SipStub", _make_fake_stub_cls(recorder, is_async=False))

    service: SyncSip = SyncSip(config=_non_keycloak_config(), use_secure_channel=False)
    _invoke_sync(service, method_name)

    assert recorder[STUB_METHOD_NAMES[method_name]] == EXPECTED_EMPTY_METADATA


@pytest.mark.asyncio
@pytest.mark.parametrize("method_name", SERVICE_METHODS)
async def test_async_keycloak_methods_attach_bearer_metadata(
    monkeypatch: pytest.MonkeyPatch,
    method_name: str,
) -> None:
    """Under Keycloak auth every async RPC forwards the `Authorization: Bearer` metadata.

    Args:
        monkeypatch (pytest.MonkeyPatch):
            Fixture used to inject the fake provider and the recording stub.
        method_name (str):
            The service wrapper method under test.
    """
    provider: KeycloakTokenProvider = _build_fake_provider()
    monkeypatch.setattr(async_base_module, "get_keycloak_token_provider", lambda config: provider)
    recorder: Dict[str, Optional[List[Tuple[str, str]]]] = {}
    monkeypatch.setattr(async_sip_module, "SipStub", _make_fake_stub_cls(recorder, is_async=True))

    service: AsyncSip = AsyncSip(config=_keycloak_config(), use_secure_channel=False)
    await _invoke_async(service, method_name)

    assert recorder[STUB_METHOD_NAMES[method_name]] == EXPECTED_KEYCLOAK_METADATA


@pytest.mark.asyncio
@pytest.mark.parametrize("method_name", SERVICE_METHODS)
async def test_async_non_keycloak_methods_attach_empty_metadata(
    monkeypatch: pytest.MonkeyPatch,
    method_name: str,
) -> None:
    """Without Keycloak auth every async RPC forwards an empty metadata list.

    Args:
        monkeypatch (pytest.MonkeyPatch):
            Fixture used to inject the recording stub.
        method_name (str):
            The service wrapper method under test.
    """
    recorder: Dict[str, Optional[List[Tuple[str, str]]]] = {}
    monkeypatch.setattr(async_sip_module, "SipStub", _make_fake_stub_cls(recorder, is_async=True))

    service: AsyncSip = AsyncSip(config=_non_keycloak_config(), use_secure_channel=False)
    await _invoke_async(service, method_name)

    assert recorder[STUB_METHOD_NAMES[method_name]] == EXPECTED_EMPTY_METADATA
