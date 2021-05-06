# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/sip/sip.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='ondewo/sip/sip.proto',
  package='ondewo.sip',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x14ondewo/sip/sip.proto\x12\nondewo.sip\x1a\x1bgoogle/protobuf/empty.proto\"%\n\x0e\x45ndCallRequest\x12\x13\n\x0bhard_hangup\x18\x01 \x01(\x08\"%\n\x10StartCallRequest\x12\x11\n\tcallee_id\x18\x01 \x01(\t\"@\n\x16RegisterAccountRequest\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"I\n\x13StartSessionRequest\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\t\x12\x1c\n\x14\x61uto_answer_interval\x18\x02 \x01(\x05\"*\n\x13TransferCallRequest\x12\x13\n\x0btransfer_id\x18\x01 \x01(\t\"\x85\x04\n\tSipStatus\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x05\x12\x35\n\x0bstatus_type\x18\x03 \x01(\x0e\x32 .ondewo.sip.SipStatus.StatusType\x12\x11\n\tcallee_id\x18\x04 \x01(\t\x12\x18\n\x10transfer_call_id\x18\x05 \x01(\t\"\xea\x02\n\nStatusType\x12\x0e\n\nno_session\x10\x00\x12\x0e\n\nregistered\x10\x01\x12\t\n\x05ready\x10\x02\x12\x1b\n\x17incoming_call_initiated\x10\x03\x12\x1b\n\x17outgoing_call_initiated\x10\x04\x12\x1b\n\x17outgoing_call_connected\x10\x05\x12\x1b\n\x17incoming_call_connected\x10\x06\x12\x1b\n\x17transfer_call_initiated\x10\x07\x12\x19\n\x15soft_hangup_initiated\x10\x08\x12\x19\n\x15hard_hangup_initiated\x10\t\x12\x18\n\x14incoming_call_failed\x10\n\x12\x18\n\x14outgoing_call_failed\x10\x0b\x12\x1a\n\x16incoming_call_finished\x10\x0c\x12\x1a\n\x16outgoing_call_finished\x10\r\"I\n\x18SipStatusHistoryResponse\x12-\n\x0estatus_history\x18\x01 \x03(\x0b\x32\x15.ondewo.sip.SipStatus\"(\n\x13PlayWavFilesRequest\x12\x11\n\twav_files\x18\x01 \x03(\x0c\x32\x95\x05\n\x03Sip\x12I\n\x0cStartSession\x12\x1f.ondewo.sip.StartSessionRequest\x1a\x16.google.protobuf.Empty\"\x00\x12>\n\nEndSession\x12\x16.google.protobuf.Empty\x1a\x16.google.protobuf.Empty\"\x00\x12\x43\n\tStartCall\x12\x1c.ondewo.sip.StartCallRequest\x1a\x16.google.protobuf.Empty\"\x00\x12?\n\x07\x45ndCall\x12\x1a.ondewo.sip.EndCallRequest\x1a\x16.google.protobuf.Empty\"\x00\x12I\n\x0cTransferCall\x12\x1f.ondewo.sip.TransferCallRequest\x1a\x16.google.protobuf.Empty\"\x00\x12O\n\x0fRegisterAccount\x12\".ondewo.sip.RegisterAccountRequest\x1a\x16.google.protobuf.Empty\"\x00\x12?\n\x0cGetSipStatus\x12\x16.google.protobuf.Empty\x1a\x15.ondewo.sip.SipStatus\"\x00\x12U\n\x13GetSipStatusHistory\x12\x16.google.protobuf.Empty\x1a$.ondewo.sip.SipStatusHistoryResponse\"\x00\x12I\n\x0cPlayWavFiles\x12\x1f.ondewo.sip.PlayWavFilesRequest\x1a\x16.google.protobuf.Empty\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])



_SIPSTATUS_STATUSTYPE = _descriptor.EnumDescriptor(
  name='StatusType',
  full_name='ondewo.sip.SipStatus.StatusType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='no_session', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='registered', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='ready', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='incoming_call_initiated', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='outgoing_call_initiated', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='outgoing_call_connected', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='incoming_call_connected', index=6, number=6,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='transfer_call_initiated', index=7, number=7,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='soft_hangup_initiated', index=8, number=8,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='hard_hangup_initiated', index=9, number=9,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='incoming_call_failed', index=10, number=10,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='outgoing_call_failed', index=11, number=11,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='incoming_call_finished', index=12, number=12,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='outgoing_call_finished', index=13, number=13,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=484,
  serialized_end=846,
)
_sym_db.RegisterEnumDescriptor(_SIPSTATUS_STATUSTYPE)


_ENDCALLREQUEST = _descriptor.Descriptor(
  name='EndCallRequest',
  full_name='ondewo.sip.EndCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hard_hangup', full_name='ondewo.sip.EndCallRequest.hard_hangup', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=102,
)


_STARTCALLREQUEST = _descriptor.Descriptor(
  name='StartCallRequest',
  full_name='ondewo.sip.StartCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='callee_id', full_name='ondewo.sip.StartCallRequest.callee_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=104,
  serialized_end=141,
)


_REGISTERACCOUNTREQUEST = _descriptor.Descriptor(
  name='RegisterAccountRequest',
  full_name='ondewo.sip.RegisterAccountRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_name', full_name='ondewo.sip.RegisterAccountRequest.account_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='ondewo.sip.RegisterAccountRequest.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=207,
)


_STARTSESSIONREQUEST = _descriptor.Descriptor(
  name='StartSessionRequest',
  full_name='ondewo.sip.StartSessionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_name', full_name='ondewo.sip.StartSessionRequest.account_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='auto_answer_interval', full_name='ondewo.sip.StartSessionRequest.auto_answer_interval', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=209,
  serialized_end=282,
)


_TRANSFERCALLREQUEST = _descriptor.Descriptor(
  name='TransferCallRequest',
  full_name='ondewo.sip.TransferCallRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='transfer_id', full_name='ondewo.sip.TransferCallRequest.transfer_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=284,
  serialized_end=326,
)


_SIPSTATUS = _descriptor.Descriptor(
  name='SipStatus',
  full_name='ondewo.sip.SipStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_name', full_name='ondewo.sip.SipStatus.account_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='ondewo.sip.SipStatus.timestamp', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='status_type', full_name='ondewo.sip.SipStatus.status_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='callee_id', full_name='ondewo.sip.SipStatus.callee_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transfer_call_id', full_name='ondewo.sip.SipStatus.transfer_call_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SIPSTATUS_STATUSTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=329,
  serialized_end=846,
)


_SIPSTATUSHISTORYRESPONSE = _descriptor.Descriptor(
  name='SipStatusHistoryResponse',
  full_name='ondewo.sip.SipStatusHistoryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status_history', full_name='ondewo.sip.SipStatusHistoryResponse.status_history', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=848,
  serialized_end=921,
)


_PLAYWAVFILESREQUEST = _descriptor.Descriptor(
  name='PlayWavFilesRequest',
  full_name='ondewo.sip.PlayWavFilesRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='wav_files', full_name='ondewo.sip.PlayWavFilesRequest.wav_files', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=923,
  serialized_end=963,
)

_SIPSTATUS.fields_by_name['status_type'].enum_type = _SIPSTATUS_STATUSTYPE
_SIPSTATUS_STATUSTYPE.containing_type = _SIPSTATUS
_SIPSTATUSHISTORYRESPONSE.fields_by_name['status_history'].message_type = _SIPSTATUS
DESCRIPTOR.message_types_by_name['EndCallRequest'] = _ENDCALLREQUEST
DESCRIPTOR.message_types_by_name['StartCallRequest'] = _STARTCALLREQUEST
DESCRIPTOR.message_types_by_name['RegisterAccountRequest'] = _REGISTERACCOUNTREQUEST
DESCRIPTOR.message_types_by_name['StartSessionRequest'] = _STARTSESSIONREQUEST
DESCRIPTOR.message_types_by_name['TransferCallRequest'] = _TRANSFERCALLREQUEST
DESCRIPTOR.message_types_by_name['SipStatus'] = _SIPSTATUS
DESCRIPTOR.message_types_by_name['SipStatusHistoryResponse'] = _SIPSTATUSHISTORYRESPONSE
DESCRIPTOR.message_types_by_name['PlayWavFilesRequest'] = _PLAYWAVFILESREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EndCallRequest = _reflection.GeneratedProtocolMessageType('EndCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _ENDCALLREQUEST,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.EndCallRequest)
  })
_sym_db.RegisterMessage(EndCallRequest)

StartCallRequest = _reflection.GeneratedProtocolMessageType('StartCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTCALLREQUEST,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.StartCallRequest)
  })
_sym_db.RegisterMessage(StartCallRequest)

RegisterAccountRequest = _reflection.GeneratedProtocolMessageType('RegisterAccountRequest', (_message.Message,), {
  'DESCRIPTOR' : _REGISTERACCOUNTREQUEST,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.RegisterAccountRequest)
  })
_sym_db.RegisterMessage(RegisterAccountRequest)

StartSessionRequest = _reflection.GeneratedProtocolMessageType('StartSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTSESSIONREQUEST,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.StartSessionRequest)
  })
_sym_db.RegisterMessage(StartSessionRequest)

TransferCallRequest = _reflection.GeneratedProtocolMessageType('TransferCallRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFERCALLREQUEST,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.TransferCallRequest)
  })
_sym_db.RegisterMessage(TransferCallRequest)

SipStatus = _reflection.GeneratedProtocolMessageType('SipStatus', (_message.Message,), {
  'DESCRIPTOR' : _SIPSTATUS,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.SipStatus)
  })
_sym_db.RegisterMessage(SipStatus)

SipStatusHistoryResponse = _reflection.GeneratedProtocolMessageType('SipStatusHistoryResponse', (_message.Message,), {
  'DESCRIPTOR' : _SIPSTATUSHISTORYRESPONSE,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.SipStatusHistoryResponse)
  })
_sym_db.RegisterMessage(SipStatusHistoryResponse)

PlayWavFilesRequest = _reflection.GeneratedProtocolMessageType('PlayWavFilesRequest', (_message.Message,), {
  'DESCRIPTOR' : _PLAYWAVFILESREQUEST,
  '__module__' : 'ondewo.sip.sip_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.sip.PlayWavFilesRequest)
  })
_sym_db.RegisterMessage(PlayWavFilesRequest)



_SIP = _descriptor.ServiceDescriptor(
  name='Sip',
  full_name='ondewo.sip.Sip',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=966,
  serialized_end=1627,
  methods=[
  _descriptor.MethodDescriptor(
    name='StartSession',
    full_name='ondewo.sip.Sip.StartSession',
    index=0,
    containing_service=None,
    input_type=_STARTSESSIONREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='EndSession',
    full_name='ondewo.sip.Sip.EndSession',
    index=1,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='StartCall',
    full_name='ondewo.sip.Sip.StartCall',
    index=2,
    containing_service=None,
    input_type=_STARTCALLREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='EndCall',
    full_name='ondewo.sip.Sip.EndCall',
    index=3,
    containing_service=None,
    input_type=_ENDCALLREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='TransferCall',
    full_name='ondewo.sip.Sip.TransferCall',
    index=4,
    containing_service=None,
    input_type=_TRANSFERCALLREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RegisterAccount',
    full_name='ondewo.sip.Sip.RegisterAccount',
    index=5,
    containing_service=None,
    input_type=_REGISTERACCOUNTREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetSipStatus',
    full_name='ondewo.sip.Sip.GetSipStatus',
    index=6,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_SIPSTATUS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetSipStatusHistory',
    full_name='ondewo.sip.Sip.GetSipStatusHistory',
    index=7,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_SIPSTATUSHISTORYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='PlayWavFiles',
    full_name='ondewo.sip.Sip.PlayWavFiles',
    index=8,
    containing_service=None,
    input_type=_PLAYWAVFILESREQUEST,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SIP)

DESCRIPTOR.services_by_name['Sip'] = _SIP

# @@protoc_insertion_point(module_scope)
