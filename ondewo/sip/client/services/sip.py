# Copyright 2021-2024 ONDEWO GmbH
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
from ondewo.utils.base_services_interface import BaseServicesInterface

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


class Sip(BaseServicesInterface):
    """
    Exposes the sip endpoints of ONDEWO sip in a user-friendly way.

    See sip.proto.
    """

    @property
    def stub(self) -> SipStub:
        stub: SipStub = SipStub(channel=self.grpc_channel)
        return stub

    def start_session(self, request: SipStartSessionRequest) -> SipStatus:
        response: SipStatus = self.stub.SipStartSession(request)
        return response

    def end_session(self) -> SipStatus:
        response: SipStatus = self.stub.SipEndSession(Empty())
        return response

    def register_account(self, request: SipRegisterAccountRequest) -> SipStatus:
        response: SipStatus = self.stub.SipRegisterAccount(request)
        return response

    def start_call(self, request: SipStartCallRequest) -> SipStatus:
        response: SipStatus = self.stub.SipStartCall(request)
        return response

    def end_call(self, request: SipEndCallRequest) -> SipStatus:
        response: SipStatus = self.stub.SipEndCall(request)
        return response

    def transfer_call(self, request: SipTransferCallRequest) -> SipStatus:
        response: SipStatus = self.stub.SipTransferCall(request)
        return response

    def get_sip_status(self) -> SipStatus:
        response: SipStatus = self.stub.SipGetSipStatus(Empty())
        return response

    def get_sip_status_history(self) -> SipStatusHistoryResponse:
        response: SipStatusHistoryResponse = self.stub.SipGetSipStatusHistory(Empty())
        return response

    def play_wav_files(self, request: SipPlayWavFilesRequest) -> SipStatus:
        response: SipStatus = self.stub.SipPlayWavFiles(request)
        return response

    def mute(self) -> SipStatus:
        response: SipStatus = self.stub.SipMute(Empty())
        return response

    def un_mute(self) -> SipStatus:
        response: SipStatus = self.stub.SipUnMute(Empty())
        return response
