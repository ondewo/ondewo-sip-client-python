# @generated by generate_proto_mypy_stubs.py.  Do not edit!
import sys
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from google.protobuf.timestamp_pb2 import (
    Timestamp as google___protobuf___timestamp_pb2___Timestamp,
)

from typing import (
    Iterable as typing___Iterable,
    List as typing___List,
    Mapping as typing___Mapping,
    MutableMapping as typing___MutableMapping,
    Optional as typing___Optional,
    Text as typing___Text,
    Tuple as typing___Tuple,
    Union as typing___Union,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int
builtin___str = str
if sys.version_info < (3,):
    builtin___buffer = buffer
    builtin___unicode = unicode


class EndCallRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    hard_hangup = ... # type: builtin___bool

    def __init__(self,
        *,
        hard_hangup : typing___Optional[builtin___bool] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> EndCallRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> EndCallRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"hard_hangup",b"hard_hangup"]) -> None: ...
global___EndCallRequest = EndCallRequest

class StartCallRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class HeadersEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key = ... # type: typing___Text
        value = ... # type: typing___Text

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[typing___Text] = None,
            ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(cls, s: builtin___bytes) -> StartCallRequest.HeadersEntry: ...
        else:
            @classmethod
            def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> StartCallRequest.HeadersEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    global___HeadersEntry = HeadersEntry

    callee_id = ... # type: typing___Text

    @property
    def headers(self) -> typing___MutableMapping[typing___Text, typing___Text]: ...

    def __init__(self,
        *,
        callee_id : typing___Optional[typing___Text] = None,
        headers : typing___Optional[typing___Mapping[typing___Text, typing___Text]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> StartCallRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> StartCallRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"callee_id",b"callee_id",u"headers",b"headers"]) -> None: ...
global___StartCallRequest = StartCallRequest

class RegisterAccountRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    account_name = ... # type: typing___Text
    password = ... # type: typing___Text

    def __init__(self,
        *,
        account_name : typing___Optional[typing___Text] = None,
        password : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> RegisterAccountRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> RegisterAccountRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_name",b"account_name",u"password",b"password"]) -> None: ...
global___RegisterAccountRequest = RegisterAccountRequest

class StartSessionRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    account_name = ... # type: typing___Text
    auto_answer_interval = ... # type: builtin___int

    def __init__(self,
        *,
        account_name : typing___Optional[typing___Text] = None,
        auto_answer_interval : typing___Optional[builtin___int] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> StartSessionRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> StartSessionRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_name",b"account_name",u"auto_answer_interval",b"auto_answer_interval"]) -> None: ...
global___StartSessionRequest = StartSessionRequest

class TransferCallRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class HeadersEntry(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        key = ... # type: typing___Text
        value = ... # type: typing___Text

        def __init__(self,
            *,
            key : typing___Optional[typing___Text] = None,
            value : typing___Optional[typing___Text] = None,
            ) -> None: ...
        if sys.version_info >= (3,):
            @classmethod
            def FromString(cls, s: builtin___bytes) -> TransferCallRequest.HeadersEntry: ...
        else:
            @classmethod
            def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> TransferCallRequest.HeadersEntry: ...
        def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"key",b"key",u"value",b"value"]) -> None: ...
    global___HeadersEntry = HeadersEntry

    transfer_id = ... # type: typing___Text

    @property
    def headers(self) -> typing___MutableMapping[typing___Text, typing___Text]: ...

    def __init__(self,
        *,
        transfer_id : typing___Optional[typing___Text] = None,
        headers : typing___Optional[typing___Mapping[typing___Text, typing___Text]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> TransferCallRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> TransferCallRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"headers",b"headers",u"transfer_id",b"transfer_id"]) -> None: ...
global___TransferCallRequest = TransferCallRequest

class SipStatus(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class StatusType(builtin___int):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        @classmethod
        def Name(cls, number: builtin___int) -> builtin___str: ...
        @classmethod
        def Value(cls, name: builtin___str) -> 'SipStatus.StatusType': ...
        @classmethod
        def keys(cls) -> typing___List[builtin___str]: ...
        @classmethod
        def values(cls) -> typing___List['SipStatus.StatusType']: ...
        @classmethod
        def items(cls) -> typing___List[typing___Tuple[builtin___str, 'SipStatus.StatusType']]: ...
        no_session = typing___cast('SipStatus.StatusType', 0)
        registered = typing___cast('SipStatus.StatusType', 1)
        ready = typing___cast('SipStatus.StatusType', 2)
        incoming_call_initiated = typing___cast('SipStatus.StatusType', 3)
        outgoing_call_initiated = typing___cast('SipStatus.StatusType', 4)
        outgoing_call_connected = typing___cast('SipStatus.StatusType', 5)
        incoming_call_connected = typing___cast('SipStatus.StatusType', 6)
        transfer_call_initiated = typing___cast('SipStatus.StatusType', 7)
        soft_hangup_initiated = typing___cast('SipStatus.StatusType', 8)
        hard_hangup_initiated = typing___cast('SipStatus.StatusType', 9)
        incoming_call_failed = typing___cast('SipStatus.StatusType', 10)
        outgoing_call_failed = typing___cast('SipStatus.StatusType', 11)
        incoming_call_finished = typing___cast('SipStatus.StatusType', 12)
        outgoing_call_finished = typing___cast('SipStatus.StatusType', 13)
    no_session = typing___cast('SipStatus.StatusType', 0)
    registered = typing___cast('SipStatus.StatusType', 1)
    ready = typing___cast('SipStatus.StatusType', 2)
    incoming_call_initiated = typing___cast('SipStatus.StatusType', 3)
    outgoing_call_initiated = typing___cast('SipStatus.StatusType', 4)
    outgoing_call_connected = typing___cast('SipStatus.StatusType', 5)
    incoming_call_connected = typing___cast('SipStatus.StatusType', 6)
    transfer_call_initiated = typing___cast('SipStatus.StatusType', 7)
    soft_hangup_initiated = typing___cast('SipStatus.StatusType', 8)
    hard_hangup_initiated = typing___cast('SipStatus.StatusType', 9)
    incoming_call_failed = typing___cast('SipStatus.StatusType', 10)
    outgoing_call_failed = typing___cast('SipStatus.StatusType', 11)
    incoming_call_finished = typing___cast('SipStatus.StatusType', 12)
    outgoing_call_finished = typing___cast('SipStatus.StatusType', 13)
    global___StatusType = StatusType

    account_name = ... # type: typing___Text
    status_type = ... # type: global___SipStatus.StatusType
    callee_id = ... # type: typing___Text
    transfer_call_id = ... # type: typing___Text

    @property
    def timestamp(self) -> google___protobuf___timestamp_pb2___Timestamp: ...

    def __init__(self,
        *,
        account_name : typing___Optional[typing___Text] = None,
        timestamp : typing___Optional[google___protobuf___timestamp_pb2___Timestamp] = None,
        status_type : typing___Optional[global___SipStatus.StatusType] = None,
        callee_id : typing___Optional[typing___Text] = None,
        transfer_call_id : typing___Optional[typing___Text] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SipStatus: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SipStatus: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def HasField(self, field_name: typing_extensions___Literal[u"timestamp",b"timestamp"]) -> builtin___bool: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"account_name",b"account_name",u"callee_id",b"callee_id",u"status_type",b"status_type",u"timestamp",b"timestamp",u"transfer_call_id",b"transfer_call_id"]) -> None: ...
global___SipStatus = SipStatus

class SipStatusHistoryResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...

    @property
    def status_history(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[global___SipStatus]: ...

    def __init__(self,
        *,
        status_history : typing___Optional[typing___Iterable[global___SipStatus]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> SipStatusHistoryResponse: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> SipStatusHistoryResponse: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"status_history",b"status_history"]) -> None: ...
global___SipStatusHistoryResponse = SipStatusHistoryResponse

class PlayWavFilesRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    wav_files = ... # type: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___bytes]

    def __init__(self,
        *,
        wav_files : typing___Optional[typing___Iterable[builtin___bytes]] = None,
        ) -> None: ...
    if sys.version_info >= (3,):
        @classmethod
        def FromString(cls, s: builtin___bytes) -> PlayWavFilesRequest: ...
    else:
        @classmethod
        def FromString(cls, s: typing___Union[builtin___bytes, builtin___buffer, builtin___unicode]) -> PlayWavFilesRequest: ...
    def MergeFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def CopyFrom(self, other_msg: google___protobuf___message___Message) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"wav_files",b"wav_files"]) -> None: ...
global___PlayWavFilesRequest = PlayWavFilesRequest
