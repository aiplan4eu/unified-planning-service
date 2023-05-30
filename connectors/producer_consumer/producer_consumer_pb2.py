# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: producer_consumer.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import unified_planning_pb2 as unified__planning__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='producer_consumer.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17producer_consumer.proto\x1a\x16unified_planning.proto\"\x07\n\x05\x45mpty2l\n\x1fUnifiedPlanningProducerConsumer\x12\x1f\n\x07produce\x12\x06.Empty\x1a\x0c.PlanRequest\x12(\n\x07\x63onsume\x12\x15.PlanGenerationResult\x1a\x06.Emptyb\x06proto3'
  ,
  dependencies=[unified__planning__pb2.DESCRIPTOR,])




_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='Empty',
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
  serialized_start=51,
  serialized_end=58,
)

DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), {
  'DESCRIPTOR' : _EMPTY,
  '__module__' : 'producer_consumer_pb2'
  # @@protoc_insertion_point(class_scope:Empty)
  })
_sym_db.RegisterMessage(Empty)



_UNIFIEDPLANNINGPRODUCERCONSUMER = _descriptor.ServiceDescriptor(
  name='UnifiedPlanningProducerConsumer',
  full_name='UnifiedPlanningProducerConsumer',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=60,
  serialized_end=168,
  methods=[
  _descriptor.MethodDescriptor(
    name='produce',
    full_name='UnifiedPlanningProducerConsumer.produce',
    index=0,
    containing_service=None,
    input_type=_EMPTY,
    output_type=unified__planning__pb2._PLANREQUEST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='consume',
    full_name='UnifiedPlanningProducerConsumer.consume',
    index=1,
    containing_service=None,
    input_type=unified__planning__pb2._PLANGENERATIONRESULT,
    output_type=_EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_UNIFIEDPLANNINGPRODUCERCONSUMER)

DESCRIPTOR.services_by_name['UnifiedPlanningProducerConsumer'] = _UNIFIEDPLANNINGPRODUCERCONSUMER

# @@protoc_insertion_point(module_scope)
