from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatusResponse(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class RegisterDataNodeRequest(_message.Message):
    __slots__ = ("dataNodeAddress",)
    DATANODEADDRESS_FIELD_NUMBER: _ClassVar[int]
    dataNodeAddress: str
    def __init__(self, dataNodeAddress: _Optional[str] = ...) -> None: ...

class RegisterDataNodeResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: StatusResponse
    def __init__(self, status: _Optional[_Union[StatusResponse, _Mapping]] = ...) -> None: ...

class HeartbeatRequest(_message.Message):
    __slots__ = ("dataNodeAddress", "timestamp")
    DATANODEADDRESS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    dataNodeAddress: str
    timestamp: int
    def __init__(self, dataNodeAddress: _Optional[str] = ..., timestamp: _Optional[int] = ...) -> None: ...

class GetBlockLocationsRequest(_message.Message):
    __slots__ = ("filename",)
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class GetBlockLocationsResponse(_message.Message):
    __slots__ = ("blockLocations",)
    class BlockLocation(_message.Message):
        __slots__ = ("blockId", "dataNodeAddresses")
        BLOCKID_FIELD_NUMBER: _ClassVar[int]
        DATANODEADDRESSES_FIELD_NUMBER: _ClassVar[int]
        blockId: str
        dataNodeAddresses: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, blockId: _Optional[str] = ..., dataNodeAddresses: _Optional[_Iterable[str]] = ...) -> None: ...
    BLOCKLOCATIONS_FIELD_NUMBER: _ClassVar[int]
    blockLocations: _containers.RepeatedCompositeFieldContainer[GetBlockLocationsResponse.BlockLocation]
    def __init__(self, blockLocations: _Optional[_Iterable[_Union[GetBlockLocationsResponse.BlockLocation, _Mapping]]] = ...) -> None: ...

class CreateFileRequest(_message.Message):
    __slots__ = ("filename",)
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    filename: str
    def __init__(self, filename: _Optional[str] = ...) -> None: ...

class CreateFileResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class AllocateBlocksRequest(_message.Message):
    __slots__ = ("filename", "blocksData")
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    BLOCKSDATA_FIELD_NUMBER: _ClassVar[int]
    filename: str
    blocksData: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, filename: _Optional[str] = ..., blocksData: _Optional[_Iterable[bytes]] = ...) -> None: ...

class AllocateBlocksResponse(_message.Message):
    __slots__ = ("status", "blockAllocations")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BLOCKALLOCATIONS_FIELD_NUMBER: _ClassVar[int]
    status: StatusResponse
    blockAllocations: _containers.RepeatedCompositeFieldContainer[BlockAllocation]
    def __init__(self, status: _Optional[_Union[StatusResponse, _Mapping]] = ..., blockAllocations: _Optional[_Iterable[_Union[BlockAllocation, _Mapping]]] = ...) -> None: ...

class BlockAllocation(_message.Message):
    __slots__ = ("blockId", "dataNodeAddresses")
    BLOCKID_FIELD_NUMBER: _ClassVar[int]
    DATANODEADDRESSES_FIELD_NUMBER: _ClassVar[int]
    blockId: str
    dataNodeAddresses: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, blockId: _Optional[str] = ..., dataNodeAddresses: _Optional[_Iterable[str]] = ...) -> None: ...

class ListFilesRequest(_message.Message):
    __slots__ = ("path",)
    PATH_FIELD_NUMBER: _ClassVar[int]
    path: str
    def __init__(self, path: _Optional[str] = ...) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ("filenames",)
    FILENAMES_FIELD_NUMBER: _ClassVar[int]
    filenames: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, filenames: _Optional[_Iterable[str]] = ...) -> None: ...
