from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.sip.sip_pb2 import (
    StartSessionRequest,
    StartSessionResponse,
    StartCallRequest,
    StartCallResponse,
    RegisterAccountRequest,
    RegisterAccountResponse,
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

    def start_session(self, request: StartSessionRequest) -> StartSessionResponse:
        response: StartSessionResponse = self.stub.StartSession(request)
        return response

    def start_call(self, request: StartCallRequest) -> StartCallResponse:
        response: StartCallResponse = self.stub.StartCall(request)
        return response

    def register_account(self, request: RegisterAccountRequest) -> RegisterAccountResponse:
        response: RegisterAccountResponse = self.stub.RegisterAccount(request)
        return response
