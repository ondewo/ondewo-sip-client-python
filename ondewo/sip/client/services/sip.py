# Copyright 2021 ONDEWO GmbH
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

from ondewo.utils.base_services_interface import BaseServicesInterface
from google.protobuf.empty_pb2 import Empty

from ondewo.sip.sip_pb2 import (
    StartSessionRequest,
    StartCallRequest,
    StartCallResponse,
    RegisterAccountRequest,
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

    def start_session(self, request: StartSessionRequest) -> Empty:
        response: Empty = self.stub.StartSession(request)
        return response

    def start_call(self, request: StartCallRequest) -> StartCallResponse:
        response: StartCallResponse = self.stub.StartCall(request)
        return response

    def register_account(self, request: RegisterAccountRequest) -> Empty:
        response: Empty = self.stub.RegisterAccount(request)
        return response
