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
from google.protobuf.empty_pb2 import Empty
from ondewo.utils.async_base_services_interface import AsyncBaseServicesInterface

from ondewo.sip.sip_pb2 import (
    SipEndCallRequest,
    SipPlayWavFilesRequest,
    SipRegisterAccountRequest,
    SipStartCallRequest,
    SipStartSessionRequest,
    SipStatus,
    SipStatusHistoryResponse,
    SipTransferCallRequest,
)
from ondewo.sip.sip_pb2_grpc import SipStub


class Sip(AsyncBaseServicesInterface):
    """
    Exposes the sip endpoints of ONDEWO sip in a user-friendly way.

    See sip.proto.
    """

    @property
    def stub(self) -> SipStub:
        stub: SipStub = SipStub(channel=self.grpc_channel)
        return stub

    async def start_session(self, request: SipStartSessionRequest) -> SipStatus:
        response: SipStatus = await self.stub.SipStartSession(request)
        return response

    async def end_session(self) -> SipStatus:
        response: SipStatus = await self.stub.SipEndSession(Empty())
        return response

    async def register_account(self, request: SipRegisterAccountRequest) -> SipStatus:
        response: SipStatus = await self.stub.SipRegisterAccount(request)
        return response

    async def start_call(self, request: SipStartCallRequest) -> SipStatus:
        response: SipStatus = await self.stub.SipStartCall(request)
        return response

    async def end_call(self, request: SipEndCallRequest) -> SipStatus:
        response: SipStatus = await self.stub.SipEndCall(request)
        return response

    async def transfer_call(self, request: SipTransferCallRequest) -> SipStatus:
        response: SipStatus = await self.stub.SipTransferCall(request)
        return response

    async def get_sip_status(self) -> SipStatus:
        response: SipStatus = await self.stub.SipGetSipStatus(Empty())
        return response

    async def get_sip_status_history(self) -> SipStatusHistoryResponse:
        response: SipStatusHistoryResponse = await self.stub.SipGetSipStatusHistory(Empty())
        return response

    async def play_wav_files(self, request: SipPlayWavFilesRequest) -> SipStatus:
        response: SipStatus = await self.stub.SipPlayWavFiles(request)
        return response

    async def mute(self) -> SipStatus:
        response: SipStatus = await self.stub.SipMute(Empty())
        return response

    async def un_mute(self) -> SipStatus:
        response: SipStatus = await self.stub.SipUnMute(Empty())
        return response
