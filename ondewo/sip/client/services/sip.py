from google.protobuf.empty_pb2 import Empty
from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.t2s.text_to_speech_pb2 import (
    ListT2sPipelinesRequest,
    ListT2sPipelinesResponse,
    SynthesizeRequest,
    SynthesizeResponse,
    T2sPipelineId,
    Text2SpeechConfig,
)
from ondewo.t2s.text_to_speech_pb2_grpc import Text2SpeechStub


class Text2Speech(BaseServicesInterface):
    """
    Exposes the t2s endpoints of ONDEWO t2s in a user-friendly way.

    See text_to_speech.proto.
    """

    @property
    def stub(self) -> Text2SpeechStub:
        stub: Text2SpeechStub = Text2SpeechStub(channel=self.grpc_channel)
        return stub

    def synthesize(self, request: SynthesizeRequest) -> SynthesizeResponse:
        response: SynthesizeResponse = self.stub.Synthesize(request)
        return response

    def get_t2s_pipeline(self, request: T2sPipelineId) -> Text2SpeechConfig:
        response: Text2SpeechConfig = self.stub.GetT2sPipeline(request)
        return response

    def create_t2s_pipeline(self, request: Text2SpeechConfig) -> T2sPipelineId:
        response: T2sPipelineId = self.stub.CreateT2sPipeline(request)
        return response

    def delete_t2s_pipeline(self, request: T2sPipelineId) -> Empty:
        response: Empty = self.stub.DeleteT2sPipeline(request)
        return response

    def update_t2s_pipeline(self, request: Text2SpeechConfig) -> Empty:
        response: Empty = self.stub.UpdateT2sPipeline(request)
        return response

    def list_t2s_pipelines(self, request: ListT2sPipelinesRequest) -> ListT2sPipelinesResponse:
        response: ListT2sPipelinesResponse = self.stub.ListT2sPipelines(request)
        return response
