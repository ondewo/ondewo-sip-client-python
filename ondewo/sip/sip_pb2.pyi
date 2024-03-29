"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class SipEndCallRequest(google.protobuf.message.Message):
    """Ends an ongoing call of the active SIP session of the active SIP account"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    HARD_HANGUP_FIELD_NUMBER: builtins.int
    hard_hangup: builtins.bool
    """Set to <code>True</code> to forcefully hang up the call"""

    def __init__(self,
        *,
        hard_hangup: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["hard_hangup",b"hard_hangup"]) -> None: ...
global___SipEndCallRequest = SipEndCallRequest

class SipStartCallRequest(google.protobuf.message.Message):
    """Request to start the call with the active SIP session of the active SIP account"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class HeadersEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: typing.Text
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    CALLEE_ID_FIELD_NUMBER: builtins.int
    HEADERS_FIELD_NUMBER: builtins.int
    callee_id: typing.Text
    """SIP account name"""

    @property
    def headers(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Headers to include when starting the call"""
        pass
    def __init__(self,
        *,
        callee_id: typing.Text = ...,
        headers: typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["callee_id",b"callee_id","headers",b"headers"]) -> None: ...
global___SipStartCallRequest = SipStartCallRequest

class SipRegisterAccountRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ACCOUNT_NAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    AUTH_USERNAME_FIELD_NUMBER: builtins.int
    OUTBOUND_PROXY_FIELD_NUMBER: builtins.int
    account_name: typing.Text
    """Account name of the sip user. Usually something like <code>sip-user-1@mydomain.com</code> or
    <code>sip-user-1@192.168.123.123</code> which uses the default SIP port <code>5060</code>.
    Also a non-default SIP port can be specified via <code>sip-user-1@mydomain.com:5099</code> to connect
    to a SIP server running on port <code>5099</code>
    """

    password: typing.Text
    """Password of the account"""

    auth_username: typing.Text
    """Optional: authentication user name"""

    outbound_proxy: typing.Text
    """Optional: outbound proxy address, e.g. <code>my.outbound.proxy.com</code>"""

    def __init__(self,
        *,
        account_name: typing.Text = ...,
        password: typing.Text = ...,
        auth_username: typing.Text = ...,
        outbound_proxy: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_name",b"account_name","auth_username",b"auth_username","outbound_proxy",b"outbound_proxy","password",b"password"]) -> None: ...
global___SipRegisterAccountRequest = SipRegisterAccountRequest

class SipStartSessionRequest(google.protobuf.message.Message):
    """Request for starting a new SIP session for a specified account"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ACCOUNT_NAME_FIELD_NUMBER: builtins.int
    AUTO_ANSWER_INTERVAL_FIELD_NUMBER: builtins.int
    account_name: typing.Text
    """Account name of the sip user. Usually something like <code>sip-user-1@mydomain.com</code> or
    <code>sip-user-1@192.168.123.123</code> which uses the default SIP port <code>5060</code>.
    Also a non-default SIP port can be specified via <code>sip-user-1@mydomain.com:5099</code> to connect
    to a SIP server running on port <code>5099</code>
    """

    auto_answer_interval: builtins.int
    """answer interval"""

    def __init__(self,
        *,
        account_name: typing.Text = ...,
        auto_answer_interval: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_name",b"account_name","auto_answer_interval",b"auto_answer_interval"]) -> None: ...
global___SipStartSessionRequest = SipStartSessionRequest

class SipTransferCallRequest(google.protobuf.message.Message):
    """Request for transferring a call with or without headers"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class HeadersEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: typing.Text
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    TRANSFER_ID_FIELD_NUMBER: builtins.int
    HEADERS_FIELD_NUMBER: builtins.int
    transfer_id: typing.Text
    """The account name or phone number to transfer the call to"""

    @property
    def headers(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """The headers to include when transferring the call"""
        pass
    def __init__(self,
        *,
        transfer_id: typing.Text = ...,
        headers: typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["headers",b"headers","transfer_id",b"transfer_id"]) -> None: ...
global___SipTransferCallRequest = SipTransferCallRequest

class SipStatus(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _StatusType:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _StatusTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[SipStatus._StatusType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        NO_SESSION: SipStatus._StatusType.ValueType  # 0
        """No session is currently active"""

        REGISTERED: SipStatus._StatusType.ValueType  # 1
        """SIP account is registered at a SIP server"""

        READY: SipStatus._StatusType.ValueType  # 2
        """SIP account is ready to call"""

        INCOMING_CALL_INITIATED: SipStatus._StatusType.ValueType  # 3
        """SIP account is being called, i.e. inbound/incoming call"""

        OUTGOING_CALL_INITIATED: SipStatus._StatusType.ValueType  # 4
        """SIP account starts calling, i.e. outbound/outgoing call"""

        OUTGOING_CALL_CONNECTED: SipStatus._StatusType.ValueType  # 5
        """SIP account outbound call is connected"""

        INCOMING_CALL_CONNECTED: SipStatus._StatusType.ValueType  # 6
        """SIP account incoming call is connected"""

        TRANSFER_CALL_INITIATED: SipStatus._StatusType.ValueType  # 7
        """SIP account starts transferring the call"""

        SOFT_HANGUP_INITIATED: SipStatus._StatusType.ValueType  # 8
        """SIP account hangs up the ongoing call"""

        HARD_HANGUP_INITIATED: SipStatus._StatusType.ValueType  # 9
        """SIP account forcefully hangs up by terminating the SIP program"""

        INCOMING_CALL_FAILED: SipStatus._StatusType.ValueType  # 10
        """SIP account cannot accept the incoming call"""

        OUTGOING_CALL_FAILED: SipStatus._StatusType.ValueType  # 11
        """SIP account cannot do an outbound call"""

        INCOMING_CALL_FINISHED: SipStatus._StatusType.ValueType  # 12
        """SIP account finished the ongoing incoming call"""

        OUTGOING_CALL_FINISHED: SipStatus._StatusType.ValueType  # 13
        """SIP account finished the ongoing outgoing call"""

        SESSION_REGISTRATION_FAILED: SipStatus._StatusType.ValueType  # 14
        """Registration of SIP account to SIP server failed"""

        SESSION_STARTED: SipStatus._StatusType.ValueType  # 15
        """SIP account started a new SIP session via a SIP server"""

        SESSION_ENDED: SipStatus._StatusType.ValueType  # 16
        """SIP account ended active sip session with SIP server"""

        TRANSFER_CALL_FAILED: SipStatus._StatusType.ValueType  # 17
        """SIP account cannot transfer the call"""

        MICROPHONE_MUTED: SipStatus._StatusType.ValueType  # 18
        """Microphone is muted"""

        MICROPHONE_UNMUTED: SipStatus._StatusType.ValueType  # 19
        """Microphone is unmuted"""

        MICROPHONE_WAV_FILES_PLAYED: SipStatus._StatusType.ValueType  # 20
        """Microphone has played wav files"""

        NO_ONGOING_CALL: SipStatus._StatusType.ValueType  # 21
        """No ongoing call"""

    class StatusType(_StatusType, metaclass=_StatusTypeEnumTypeWrapper):
        """Types of status"""
        pass

    NO_SESSION: SipStatus.StatusType.ValueType  # 0
    """No session is currently active"""

    REGISTERED: SipStatus.StatusType.ValueType  # 1
    """SIP account is registered at a SIP server"""

    READY: SipStatus.StatusType.ValueType  # 2
    """SIP account is ready to call"""

    INCOMING_CALL_INITIATED: SipStatus.StatusType.ValueType  # 3
    """SIP account is being called, i.e. inbound/incoming call"""

    OUTGOING_CALL_INITIATED: SipStatus.StatusType.ValueType  # 4
    """SIP account starts calling, i.e. outbound/outgoing call"""

    OUTGOING_CALL_CONNECTED: SipStatus.StatusType.ValueType  # 5
    """SIP account outbound call is connected"""

    INCOMING_CALL_CONNECTED: SipStatus.StatusType.ValueType  # 6
    """SIP account incoming call is connected"""

    TRANSFER_CALL_INITIATED: SipStatus.StatusType.ValueType  # 7
    """SIP account starts transferring the call"""

    SOFT_HANGUP_INITIATED: SipStatus.StatusType.ValueType  # 8
    """SIP account hangs up the ongoing call"""

    HARD_HANGUP_INITIATED: SipStatus.StatusType.ValueType  # 9
    """SIP account forcefully hangs up by terminating the SIP program"""

    INCOMING_CALL_FAILED: SipStatus.StatusType.ValueType  # 10
    """SIP account cannot accept the incoming call"""

    OUTGOING_CALL_FAILED: SipStatus.StatusType.ValueType  # 11
    """SIP account cannot do an outbound call"""

    INCOMING_CALL_FINISHED: SipStatus.StatusType.ValueType  # 12
    """SIP account finished the ongoing incoming call"""

    OUTGOING_CALL_FINISHED: SipStatus.StatusType.ValueType  # 13
    """SIP account finished the ongoing outgoing call"""

    SESSION_REGISTRATION_FAILED: SipStatus.StatusType.ValueType  # 14
    """Registration of SIP account to SIP server failed"""

    SESSION_STARTED: SipStatus.StatusType.ValueType  # 15
    """SIP account started a new SIP session via a SIP server"""

    SESSION_ENDED: SipStatus.StatusType.ValueType  # 16
    """SIP account ended active sip session with SIP server"""

    TRANSFER_CALL_FAILED: SipStatus.StatusType.ValueType  # 17
    """SIP account cannot transfer the call"""

    MICROPHONE_MUTED: SipStatus.StatusType.ValueType  # 18
    """Microphone is muted"""

    MICROPHONE_UNMUTED: SipStatus.StatusType.ValueType  # 19
    """Microphone is unmuted"""

    MICROPHONE_WAV_FILES_PLAYED: SipStatus.StatusType.ValueType  # 20
    """Microphone has played wav files"""

    NO_ONGOING_CALL: SipStatus.StatusType.ValueType  # 21
    """No ongoing call"""


    class HeadersEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        value: typing.Text
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    ACCOUNT_NAME_FIELD_NUMBER: builtins.int
    TIMESTAMP_FIELD_NUMBER: builtins.int
    STATUS_TYPE_FIELD_NUMBER: builtins.int
    CALLEE_ID_FIELD_NUMBER: builtins.int
    TRANSFER_CALL_ID_FIELD_NUMBER: builtins.int
    HEADERS_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    EXCEPTION_NAME_FIELD_NUMBER: builtins.int
    EXCEPTION_TRACEBACK_FIELD_NUMBER: builtins.int
    NLU_SESSION_NAME_FIELD_NUMBER: builtins.int
    account_name: typing.Text
    """Account name of the sip user. Usually something like <code>sip-user-1@mydomain.com</code> or
    <code>sip-user-1@192.168.123.123</code> which uses the default SIP port <code>5060</code>.
    Also a non-default SIP port can be specified via <code>sip-user-1@mydomain.com:5099</code> to connect
    to a SIP server running on port <code>5099</code>
    """

    @property
    def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Timestamp of the status"""
        pass
    status_type: global___SipStatus.StatusType.ValueType
    """Status type"""

    callee_id: typing.Text
    """SIP account name"""

    transfer_call_id: typing.Text
    """SIP account of the transfer"""

    @property
    def headers(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Headers to include when calling outbound or transfer"""
        pass
    description: typing.Text
    """More detailed description of the status"""

    exception_name: typing.Text
    """Name of the exception"""

    exception_traceback: typing.Text
    """Traceback of the exception"""

    nlu_session_name: typing.Text
    """session name of the NLU session"""

    def __init__(self,
        *,
        account_name: typing.Text = ...,
        timestamp: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        status_type: global___SipStatus.StatusType.ValueType = ...,
        callee_id: typing.Text = ...,
        transfer_call_id: typing.Text = ...,
        headers: typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        description: typing.Text = ...,
        exception_name: typing.Text = ...,
        exception_traceback: typing.Text = ...,
        nlu_session_name: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["timestamp",b"timestamp"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_name",b"account_name","callee_id",b"callee_id","description",b"description","exception_name",b"exception_name","exception_traceback",b"exception_traceback","headers",b"headers","nlu_session_name",b"nlu_session_name","status_type",b"status_type","timestamp",b"timestamp","transfer_call_id",b"transfer_call_id"]) -> None: ...
global___SipStatus = SipStatus

class SipStatusHistoryResponse(google.protobuf.message.Message):
    """History of SIP status"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STATUS_HISTORY_FIELD_NUMBER: builtins.int
    @property
    def status_history(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SipStatus]:
        """History of SIP status"""
        pass
    def __init__(self,
        *,
        status_history: typing.Optional[typing.Iterable[global___SipStatus]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["status_history",b"status_history"]) -> None: ...
global___SipStatusHistoryResponse = SipStatusHistoryResponse

class SipPlayWavFilesRequest(google.protobuf.message.Message):
    """Plays a list of wav files"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    WAV_FILES_FIELD_NUMBER: builtins.int
    @property
    def wav_files(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.bytes]:
        """Wav files as bytes in a list that will be played"""
        pass
    def __init__(self,
        *,
        wav_files: typing.Optional[typing.Iterable[builtins.bytes]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["wav_files",b"wav_files"]) -> None: ...
global___SipPlayWavFilesRequest = SipPlayWavFilesRequest
