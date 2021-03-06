# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: shared_variable.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='shared_variable.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15shared_variable.proto\"\x12\n\x03\x41\x63k\x12\x0b\n\x03\x61\x63k\x18\x01 \x01(\x08\")\n\x07\x41\x64\x64ress\x12\x10\n\x08hostname\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"$\n\x07JoinReq\x12\x19\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x08.Address\"n\n\tJoinReply\x12\x16\n\x04next\x18\x01 \x01(\x0b\x32\x08.Address\x12\x16\n\x04prev\x18\x02 \x01(\x0b\x32\x08.Address\x12\x17\n\x05nnext\x18\x03 \x01(\x0b\x32\x08.Address\x12\x18\n\x06leader\x18\x04 \x01(\x0b\x32\x08.Address\"\'\n\rChangePrevMsg\x12\x16\n\x04prev\x18\x01 \x01(\x0b\x32\x08.Address\")\n\x0e\x43hangeNNextMsg\x12\x17\n\x05nnext\x18\x01 \x01(\x0b\x32\x08.Address\"+\n\x0eNodeMissingMsg\x12\x19\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x08.Address\"\x1d\n\rCheckNodesMsg\x12\x0c\n\x04stop\x18\x01 \x01(\x08\" \n\x0b\x45lectionMsg\x12\x11\n\ttimestamp\x18\x01 \x01(\x01\"9\n\nElectedMsg\x12\x18\n\x06leader\x18\x01 \x01(\x0b\x32\x08.Address\x12\x11\n\ttimestamp\x18\x02 \x01(\x01\"\x0c\n\nReadVarReq\"3\n\x0cReadVarReply\x12\x10\n\x08variable\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x01\"\x1f\n\x0bWriteVarReq\x12\x10\n\x08variable\x18\x01 \x01(\t\"\"\n\rWriteVarReply\x12\x11\n\ttimestamp\x18\x01 \x01(\x01\x32\xe7\x02\n\x0eSharedVariable\x12\x1e\n\x04Join\x12\x08.JoinReq\x1a\n.JoinReply\"\x00\x12(\n\nChangePrev\x12\x0e.ChangePrevMsg\x1a\x08.Address\"\x00\x12&\n\x0b\x43hangeNNext\x12\x0f.ChangeNNextMsg\x1a\x04.Ack\"\x00\x12&\n\x0bNodeMissing\x12\x0f.NodeMissingMsg\x1a\x04.Ack\"\x00\x12$\n\nCheckNodes\x12\x0e.CheckNodesMsg\x1a\x04.Ack\"\x00\x12 \n\x08\x45lection\x12\x0c.ElectionMsg\x1a\x04.Ack\"\x00\x12\x1e\n\x07\x45lected\x12\x0b.ElectedMsg\x1a\x04.Ack\"\x00\x12\'\n\x07ReadVar\x12\x0b.ReadVarReq\x1a\r.ReadVarReply\"\x00\x12*\n\x08WriteVar\x12\x0c.WriteVarReq\x1a\x0e.WriteVarReply\"\x00\x62\x06proto3'
)




_ACK = _descriptor.Descriptor(
  name='Ack',
  full_name='Ack',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ack', full_name='Ack.ack', index=0,
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
  serialized_start=25,
  serialized_end=43,
)


_ADDRESS = _descriptor.Descriptor(
  name='Address',
  full_name='Address',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='hostname', full_name='Address.hostname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='port', full_name='Address.port', index=1,
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
  serialized_start=45,
  serialized_end=86,
)


_JOINREQ = _descriptor.Descriptor(
  name='JoinReq',
  full_name='JoinReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='JoinReq.address', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=88,
  serialized_end=124,
)


_JOINREPLY = _descriptor.Descriptor(
  name='JoinReply',
  full_name='JoinReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='next', full_name='JoinReply.next', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='prev', full_name='JoinReply.prev', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='nnext', full_name='JoinReply.nnext', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='leader', full_name='JoinReply.leader', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=126,
  serialized_end=236,
)


_CHANGEPREVMSG = _descriptor.Descriptor(
  name='ChangePrevMsg',
  full_name='ChangePrevMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='prev', full_name='ChangePrevMsg.prev', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=238,
  serialized_end=277,
)


_CHANGENNEXTMSG = _descriptor.Descriptor(
  name='ChangeNNextMsg',
  full_name='ChangeNNextMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='nnext', full_name='ChangeNNextMsg.nnext', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=279,
  serialized_end=320,
)


_NODEMISSINGMSG = _descriptor.Descriptor(
  name='NodeMissingMsg',
  full_name='NodeMissingMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='address', full_name='NodeMissingMsg.address', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=322,
  serialized_end=365,
)


_CHECKNODESMSG = _descriptor.Descriptor(
  name='CheckNodesMsg',
  full_name='CheckNodesMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stop', full_name='CheckNodesMsg.stop', index=0,
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
  serialized_start=367,
  serialized_end=396,
)


_ELECTIONMSG = _descriptor.Descriptor(
  name='ElectionMsg',
  full_name='ElectionMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='ElectionMsg.timestamp', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=398,
  serialized_end=430,
)


_ELECTEDMSG = _descriptor.Descriptor(
  name='ElectedMsg',
  full_name='ElectedMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='leader', full_name='ElectedMsg.leader', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='ElectedMsg.timestamp', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=432,
  serialized_end=489,
)


_READVARREQ = _descriptor.Descriptor(
  name='ReadVarReq',
  full_name='ReadVarReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=491,
  serialized_end=503,
)


_READVARREPLY = _descriptor.Descriptor(
  name='ReadVarReply',
  full_name='ReadVarReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='variable', full_name='ReadVarReply.variable', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='ReadVarReply.timestamp', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=505,
  serialized_end=556,
)


_WRITEVARREQ = _descriptor.Descriptor(
  name='WriteVarReq',
  full_name='WriteVarReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='variable', full_name='WriteVarReq.variable', index=0,
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
  serialized_start=558,
  serialized_end=589,
)


_WRITEVARREPLY = _descriptor.Descriptor(
  name='WriteVarReply',
  full_name='WriteVarReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='WriteVarReply.timestamp', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=591,
  serialized_end=625,
)

_JOINREQ.fields_by_name['address'].message_type = _ADDRESS
_JOINREPLY.fields_by_name['next'].message_type = _ADDRESS
_JOINREPLY.fields_by_name['prev'].message_type = _ADDRESS
_JOINREPLY.fields_by_name['nnext'].message_type = _ADDRESS
_JOINREPLY.fields_by_name['leader'].message_type = _ADDRESS
_CHANGEPREVMSG.fields_by_name['prev'].message_type = _ADDRESS
_CHANGENNEXTMSG.fields_by_name['nnext'].message_type = _ADDRESS
_NODEMISSINGMSG.fields_by_name['address'].message_type = _ADDRESS
_ELECTEDMSG.fields_by_name['leader'].message_type = _ADDRESS
DESCRIPTOR.message_types_by_name['Ack'] = _ACK
DESCRIPTOR.message_types_by_name['Address'] = _ADDRESS
DESCRIPTOR.message_types_by_name['JoinReq'] = _JOINREQ
DESCRIPTOR.message_types_by_name['JoinReply'] = _JOINREPLY
DESCRIPTOR.message_types_by_name['ChangePrevMsg'] = _CHANGEPREVMSG
DESCRIPTOR.message_types_by_name['ChangeNNextMsg'] = _CHANGENNEXTMSG
DESCRIPTOR.message_types_by_name['NodeMissingMsg'] = _NODEMISSINGMSG
DESCRIPTOR.message_types_by_name['CheckNodesMsg'] = _CHECKNODESMSG
DESCRIPTOR.message_types_by_name['ElectionMsg'] = _ELECTIONMSG
DESCRIPTOR.message_types_by_name['ElectedMsg'] = _ELECTEDMSG
DESCRIPTOR.message_types_by_name['ReadVarReq'] = _READVARREQ
DESCRIPTOR.message_types_by_name['ReadVarReply'] = _READVARREPLY
DESCRIPTOR.message_types_by_name['WriteVarReq'] = _WRITEVARREQ
DESCRIPTOR.message_types_by_name['WriteVarReply'] = _WRITEVARREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Ack = _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), {
  'DESCRIPTOR' : _ACK,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:Ack)
  })
_sym_db.RegisterMessage(Ack)

Address = _reflection.GeneratedProtocolMessageType('Address', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESS,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:Address)
  })
_sym_db.RegisterMessage(Address)

JoinReq = _reflection.GeneratedProtocolMessageType('JoinReq', (_message.Message,), {
  'DESCRIPTOR' : _JOINREQ,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:JoinReq)
  })
_sym_db.RegisterMessage(JoinReq)

JoinReply = _reflection.GeneratedProtocolMessageType('JoinReply', (_message.Message,), {
  'DESCRIPTOR' : _JOINREPLY,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:JoinReply)
  })
_sym_db.RegisterMessage(JoinReply)

ChangePrevMsg = _reflection.GeneratedProtocolMessageType('ChangePrevMsg', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEPREVMSG,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:ChangePrevMsg)
  })
_sym_db.RegisterMessage(ChangePrevMsg)

ChangeNNextMsg = _reflection.GeneratedProtocolMessageType('ChangeNNextMsg', (_message.Message,), {
  'DESCRIPTOR' : _CHANGENNEXTMSG,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:ChangeNNextMsg)
  })
_sym_db.RegisterMessage(ChangeNNextMsg)

NodeMissingMsg = _reflection.GeneratedProtocolMessageType('NodeMissingMsg', (_message.Message,), {
  'DESCRIPTOR' : _NODEMISSINGMSG,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:NodeMissingMsg)
  })
_sym_db.RegisterMessage(NodeMissingMsg)

CheckNodesMsg = _reflection.GeneratedProtocolMessageType('CheckNodesMsg', (_message.Message,), {
  'DESCRIPTOR' : _CHECKNODESMSG,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:CheckNodesMsg)
  })
_sym_db.RegisterMessage(CheckNodesMsg)

ElectionMsg = _reflection.GeneratedProtocolMessageType('ElectionMsg', (_message.Message,), {
  'DESCRIPTOR' : _ELECTIONMSG,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:ElectionMsg)
  })
_sym_db.RegisterMessage(ElectionMsg)

ElectedMsg = _reflection.GeneratedProtocolMessageType('ElectedMsg', (_message.Message,), {
  'DESCRIPTOR' : _ELECTEDMSG,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:ElectedMsg)
  })
_sym_db.RegisterMessage(ElectedMsg)

ReadVarReq = _reflection.GeneratedProtocolMessageType('ReadVarReq', (_message.Message,), {
  'DESCRIPTOR' : _READVARREQ,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:ReadVarReq)
  })
_sym_db.RegisterMessage(ReadVarReq)

ReadVarReply = _reflection.GeneratedProtocolMessageType('ReadVarReply', (_message.Message,), {
  'DESCRIPTOR' : _READVARREPLY,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:ReadVarReply)
  })
_sym_db.RegisterMessage(ReadVarReply)

WriteVarReq = _reflection.GeneratedProtocolMessageType('WriteVarReq', (_message.Message,), {
  'DESCRIPTOR' : _WRITEVARREQ,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:WriteVarReq)
  })
_sym_db.RegisterMessage(WriteVarReq)

WriteVarReply = _reflection.GeneratedProtocolMessageType('WriteVarReply', (_message.Message,), {
  'DESCRIPTOR' : _WRITEVARREPLY,
  '__module__' : 'shared_variable_pb2'
  # @@protoc_insertion_point(class_scope:WriteVarReply)
  })
_sym_db.RegisterMessage(WriteVarReply)



_SHAREDVARIABLE = _descriptor.ServiceDescriptor(
  name='SharedVariable',
  full_name='SharedVariable',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=628,
  serialized_end=987,
  methods=[
  _descriptor.MethodDescriptor(
    name='Join',
    full_name='SharedVariable.Join',
    index=0,
    containing_service=None,
    input_type=_JOINREQ,
    output_type=_JOINREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ChangePrev',
    full_name='SharedVariable.ChangePrev',
    index=1,
    containing_service=None,
    input_type=_CHANGEPREVMSG,
    output_type=_ADDRESS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ChangeNNext',
    full_name='SharedVariable.ChangeNNext',
    index=2,
    containing_service=None,
    input_type=_CHANGENNEXTMSG,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='NodeMissing',
    full_name='SharedVariable.NodeMissing',
    index=3,
    containing_service=None,
    input_type=_NODEMISSINGMSG,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CheckNodes',
    full_name='SharedVariable.CheckNodes',
    index=4,
    containing_service=None,
    input_type=_CHECKNODESMSG,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Election',
    full_name='SharedVariable.Election',
    index=5,
    containing_service=None,
    input_type=_ELECTIONMSG,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Elected',
    full_name='SharedVariable.Elected',
    index=6,
    containing_service=None,
    input_type=_ELECTEDMSG,
    output_type=_ACK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ReadVar',
    full_name='SharedVariable.ReadVar',
    index=7,
    containing_service=None,
    input_type=_READVARREQ,
    output_type=_READVARREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='WriteVar',
    full_name='SharedVariable.WriteVar',
    index=8,
    containing_service=None,
    input_type=_WRITEVARREQ,
    output_type=_WRITEVARREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SHAREDVARIABLE)

DESCRIPTOR.services_by_name['SharedVariable'] = _SHAREDVARIABLE

# @@protoc_insertion_point(module_scope)
