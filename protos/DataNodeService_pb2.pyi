from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusRes(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class BlockData(_message.Message):
    __slots__ = ("blockId", "data")
    BLOCKID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    blockId: str
    data: bytes
    def __init__(self, blockId: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ReadBlockRequest(_message.Message):
    __slots__ = ("blockId",)
    BLOCKID_FIELD_NUMBER: _ClassVar[int]
    blockId: str
    def __init__(self, blockId: _Optional[str] = ...) -> None: ...

class StoreBlockRequest(_message.Message):
    __slots__ = ("blockData",)
    BLOCKDATA_FIELD_NUMBER: _ClassVar[int]
    blockData: BlockData
    def __init__(self, blockData: _Optional[_Union[BlockData, _Mapping]] = ...) -> None: ...

class ReplicateBlockRequest(_message.Message):
    __slots__ = ("blockData", "dataNodeAddress")
    BLOCKDATA_FIELD_NUMBER: _ClassVar[int]
    DATANODEADDRESS_FIELD_NUMBER: _ClassVar[int]
    blockData: BlockData
    dataNodeAddress: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, blockData: _Optional[_Union[BlockData, _Mapping]] = ..., dataNodeAddress: _Optional[_Iterable[str]] = ...) -> None: ...
