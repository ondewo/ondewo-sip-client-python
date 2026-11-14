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
from typing import (
    Iterator,
    Optional,
    Sequence,
    Tuple,
)

from google.protobuf.empty_pb2 import Empty

from ondewo.sip.client.services_interface import ServicesInterface
from ondewo.sip.sip_pb2 import (
    SipCallAudioRequest,
    SipCallAudioResponse,
    SipEndCallRequest,
    SipPlayWavFilesRequest,
    SipRegisterAccountRequest,
    SipReportAnsweringMachineDetectedRequest,
    SipSendDtmfRequest,
    SipSetCallMediaControlRequest,
    SipStartCallRequest,
    SipStartSessionRequest,
    SipStatus,
    SipStatusHistoryResponse,
    SipTransferCallRequest,
)
from ondewo.sip.sip_pb2_grpc import SipStub


class Sip(ServicesInterface):
    """
    Exposes the sip endpoints of ONDEWO sip in a user-friendly way.

    See sip.proto.
    """

    @property
    def stub(self) -> SipStub:
        stub: SipStub = SipStub(channel=self.grpc_channel)
        return stub

    def start_session(self, request: SipStartSessionRequest) -> SipStatus:
        response: SipStatus = self.stub.SipStartSession(request, metadata=self.metadata)
        return response

    def end_session(self) -> SipStatus:
        response: SipStatus = self.stub.SipEndSession(Empty(), metadata=self.metadata)
        return response

    def register_account(self, request: SipRegisterAccountRequest) -> SipStatus:
        response: SipStatus = self.stub.SipRegisterAccount(request, metadata=self.metadata)
        return response

    def start_call(self, request: SipStartCallRequest) -> SipStatus:
        response: SipStatus = self.stub.SipStartCall(request, metadata=self.metadata)
        return response

    def end_call(self, request: SipEndCallRequest, metadata: Optional[Sequence[Tuple[str, str]]] = None) -> SipStatus:
        response: SipStatus = self.stub.SipEndCall(request, metadata=self.call_metadata(metadata))
        return response

    def transfer_call(
        self, request: SipTransferCallRequest, metadata: Optional[Sequence[Tuple[str, str]]] = None
    ) -> SipStatus:
        response: SipStatus = self.stub.SipTransferCall(request, metadata=self.call_metadata(metadata))
        return response

    def get_sip_status(self) -> SipStatus:
        response: SipStatus = self.stub.SipGetSipStatus(Empty(), metadata=self.metadata)
        return response

    def get_sip_status_history(self) -> SipStatusHistoryResponse:
        response: SipStatusHistoryResponse = self.stub.SipGetSipStatusHistory(Empty(), metadata=self.metadata)
        return response

    def play_wav_files(
        self, request: SipPlayWavFilesRequest, metadata: Optional[Sequence[Tuple[str, str]]] = None
    ) -> SipStatus:
        response: SipStatus = self.stub.SipPlayWavFiles(request, metadata=self.call_metadata(metadata))
        return response

    def mute(self, metadata: Optional[Sequence[Tuple[str, str]]] = None) -> SipStatus:
        response: SipStatus = self.stub.SipMute(Empty(), metadata=self.call_metadata(metadata))
        return response

    def un_mute(self, metadata: Optional[Sequence[Tuple[str, str]]] = None) -> SipStatus:
        response: SipStatus = self.stub.SipUnMute(Empty(), metadata=self.call_metadata(metadata))
        return response

    def report_answering_machine_detected(self, request: SipReportAnsweringMachineDetectedRequest) -> SipStatus:
        response: SipStatus = self.stub.SipReportAnsweringMachineDetected(request, metadata=self.metadata)
        return response

    def set_call_media_control(
        self, request: SipSetCallMediaControlRequest, metadata: Optional[Sequence[Tuple[str, str]]] = None
    ) -> SipStatus:
        response: SipStatus = self.stub.SipSetCallMediaControl(request, metadata=self.call_metadata(metadata))
        return response

    def send_dtmf(self, request: SipSendDtmfRequest, metadata: Optional[Sequence[Tuple[str, str]]] = None) -> SipStatus:
        response: SipStatus = self.stub.SipSendDtmf(request, metadata=self.call_metadata(metadata))
        return response

    def stream_call_audio(
        self,
        request_iterator: Iterator[SipCallAudioRequest],
        metadata: Optional[Sequence[Tuple[str, str]]] = None,
    ) -> Iterator[SipCallAudioResponse]:
        response_iterator: Iterator[SipCallAudioResponse] = self.stub.SipStreamCallAudio(
            request_iterator,
            metadata=self.call_metadata(metadata),
        )
        return response_iterator
