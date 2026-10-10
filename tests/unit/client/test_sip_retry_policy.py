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
"""Only the side-effect-free SIP reads are retried by the client's gRPC channel.

sip-api 5.5.0 declares ``idempotency_level = NO_SIDE_EFFECTS`` on ``SipGetSipStatus`` and
``SipGetSipStatusHistory``; ondewo-client-utils derives the channel's per-method retry policy from
that declaration. These tests pin the declaration in the generated code, the service config the
sync and async ``Sip`` services build, and the behaviour through ``Client`` / ``AsyncClient``
against a real in-process server: a status read that fails ``UNAVAILABLE`` once is re-sent, while
``SipEndCall`` (a side effect) reaches the server exactly once.
"""

import asyncio
import json
from concurrent import futures
from typing import (
    Any,
    Dict,
    FrozenSet,
    Iterator,
    List,
    Set,
)

import grpc
import pytest
from google.protobuf.descriptor import MethodDescriptor
from google.protobuf.descriptor_pb2 import MethodOptions
from google.protobuf.empty_pb2 import Empty
from ondewo.utils.grpc_retry_policy import service_config_json_for

import ondewo.sip.sip_pb2 as sip_pb2
from ondewo.sip.client.async_client import AsyncClient
from ondewo.sip.client.client import Client
from ondewo.sip.client.client_config import ClientConfig
from ondewo.sip.client.services.async_sip import Sip as AsyncSip
from ondewo.sip.client.services.sip import Sip as SyncSip
from ondewo.sip.sip_pb2_grpc import (
    SipServicer,
    add_SipServicer_to_server,
)

SERVICE_FULL_NAME: str = "ondewo.sip.Sip"
RETRIED_METHODS: FrozenSet[str] = frozenset({"SipGetSipStatus", "SipGetSipStatusHistory"})


class _FailOnceServicer(SipServicer):
    """Counts every request; each RPC answers ``UNAVAILABLE`` on its first attempt only."""

    def __init__(self) -> None:
        self.calls: Dict[str, int] = {}

    def _count(self, name: str, context: grpc.ServicerContext) -> None:
        self.calls[name] = self.calls.get(name, 0) + 1
        if self.calls[name] == 1:
            context.abort(grpc.StatusCode.UNAVAILABLE, "transient")

    def SipGetSipStatus(self, request: Empty, context: grpc.ServicerContext) -> sip_pb2.SipStatus:
        self._count("SipGetSipStatus", context)
        return sip_pb2.SipStatus(account_name="ok")

    def SipGetSipStatusHistory(self, request: Empty, context: grpc.ServicerContext) -> sip_pb2.SipStatusHistoryResponse:
        self._count("SipGetSipStatusHistory", context)
        return sip_pb2.SipStatusHistoryResponse(status_history=[sip_pb2.SipStatus(account_name="ok")])

    def SipEndCall(self, request: sip_pb2.SipEndCallRequest, context: grpc.ServicerContext) -> sip_pb2.SipStatus:
        self._count("SipEndCall", context)
        return sip_pb2.SipStatus()


@pytest.fixture
def server() -> Iterator[Any]:
    servicer: _FailOnceServicer = _FailOnceServicer()
    grpc_server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    add_SipServicer_to_server(servicer, grpc_server)
    port: int = grpc_server.add_insecure_port("127.0.0.1:0")
    grpc_server.start()
    try:
        yield servicer, ClientConfig(host="127.0.0.1", port=str(port), user_name="user", password="password")
    finally:
        grpc_server.stop(None)


def _methods() -> List[MethodDescriptor]:
    return list(sip_pb2.DESCRIPTOR.services_by_name["Sip"].methods)


def _retried_methods(service_class: type) -> Set[str]:
    config: Dict[str, Any] = json.loads(service_config_json_for(service_class))
    return {
        name["method"]
        for method_config in config["methodConfig"]
        if "retryPolicy" in method_config
        for name in method_config["name"]
        if name.get("service") == SERVICE_FULL_NAME
    }


def test_generated_code_declares_the_status_reads_side_effect_free() -> None:
    declared: Set[str] = {
        method.name
        for method in _methods()
        if method.GetOptions().idempotency_level == MethodOptions.IdempotencyLevel.NO_SIDE_EFFECTS
    }
    assert declared == RETRIED_METHODS


@pytest.mark.parametrize("service_class", [SyncSip, AsyncSip], ids=["sync", "async"])
def test_service_config_retries_exactly_the_status_reads(service_class: type) -> None:
    retried: Set[str] = _retried_methods(service_class)
    assert retried == RETRIED_METHODS
    not_retried: Set[str] = {method.name for method in _methods()} - retried
    assert {"SipEndCall", "SipStartCall", "SipTransferCall", "SipSetCallMediaControl"} <= not_retried


def test_sync_client_retries_a_status_read_but_not_end_call(server: Any) -> None:
    servicer, config = server
    client: Client = Client(config=config, use_secure_channel=False)
    try:
        assert client.services.sip.get_sip_status().account_name == "ok"
        assert len(client.services.sip.get_sip_status_history().status_history) == 1
        with pytest.raises(grpc.RpcError) as raised:
            client.services.sip.end_call(sip_pb2.SipEndCallRequest())
        assert raised.value.code() == grpc.StatusCode.UNAVAILABLE
    finally:
        client.disconnect()
    assert servicer.calls == {"SipGetSipStatus": 2, "SipGetSipStatusHistory": 2, "SipEndCall": 1}


def test_async_client_retries_a_status_read_but_not_end_call(server: Any) -> None:
    servicer, config = server

    async def run() -> None:
        client: AsyncClient = AsyncClient(config=config, use_secure_channel=False)
        try:
            assert (await client.services.sip.get_sip_status()).account_name == "ok"
            assert len((await client.services.sip.get_sip_status_history()).status_history) == 1
            with pytest.raises(grpc.aio.AioRpcError) as raised:
                await client.services.sip.end_call(sip_pb2.SipEndCallRequest())
            assert raised.value.code() == grpc.StatusCode.UNAVAILABLE
        finally:
            await client.disconnect()

    asyncio.run(run())
    assert servicer.calls == {"SipGetSipStatus": 2, "SipGetSipStatusHistory": 2, "SipEndCall": 1}
