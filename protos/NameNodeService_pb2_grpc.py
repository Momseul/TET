# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

#import NameNodeService_pb2 as NameNodeService__pb2
from . import NameNodeService_pb2 as NameNodeService__pb2


class NameNodeServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterDataNode = channel.unary_unary(
                '/protos.NameNodeService/RegisterDataNode',
                request_serializer=NameNodeService__pb2.RegisterDataNodeRequest.SerializeToString,
                response_deserializer=NameNodeService__pb2.RegisterDataNodeResponse.FromString,
                )
        self.Heartbeat = channel.unary_unary(
                '/protos.NameNodeService/Heartbeat',
                request_serializer=NameNodeService__pb2.HeartbeatRequest.SerializeToString,
                response_deserializer=NameNodeService__pb2.StatusResponse.FromString,
                )
        self.GetBlockLocations = channel.unary_stream(
                '/protos.NameNodeService/GetBlockLocations',
                request_serializer=NameNodeService__pb2.GetBlockLocationsRequest.SerializeToString,
                response_deserializer=NameNodeService__pb2.GetBlockLocationsResponse.FromString,
                )
        self.CreateFile = channel.unary_unary(
                '/protos.NameNodeService/CreateFile',
                request_serializer=NameNodeService__pb2.CreateFileRequest.SerializeToString,
                response_deserializer=NameNodeService__pb2.CreateFileResponse.FromString,
                )
        self.AllocateBlocks = channel.unary_unary(
                '/protos.NameNodeService/AllocateBlocks',
                request_serializer=NameNodeService__pb2.AllocateBlocksRequest.SerializeToString,
                response_deserializer=NameNodeService__pb2.AllocateBlocksResponse.FromString,
                )
        self.ListFiles = channel.unary_unary(
                '/protos.NameNodeService/ListFiles',
                request_serializer=NameNodeService__pb2.ListFilesRequest.SerializeToString,
                response_deserializer=NameNodeService__pb2.ListFilesResponse.FromString,
                )


class NameNodeServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterDataNode(self, request, context):
        """Registers a DataNode with the NameNode.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Heartbeat(self, request, context):
        """Receives heartbeats from DataNodes to keep them marked as active.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetBlockLocations(self, request, context):
        """Retrieves the locations of blocks for reading a file, streaming response to handle large number of blocks.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateFile(self, request, context):
        """Requests creation of a new file, returns initial DataNodes for block placement.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AllocateBlocks(self, request, context):
        """Adds a new block to the filesystem, returning the DataNodes it should be placed on.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiles(self, request, context):
        """Lists files/directories within a specific path.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NameNodeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterDataNode': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterDataNode,
                    request_deserializer=NameNodeService__pb2.RegisterDataNodeRequest.FromString,
                    response_serializer=NameNodeService__pb2.RegisterDataNodeResponse.SerializeToString,
            ),
            'Heartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.Heartbeat,
                    request_deserializer=NameNodeService__pb2.HeartbeatRequest.FromString,
                    response_serializer=NameNodeService__pb2.StatusResponse.SerializeToString,
            ),
            'GetBlockLocations': grpc.unary_stream_rpc_method_handler(
                    servicer.GetBlockLocations,
                    request_deserializer=NameNodeService__pb2.GetBlockLocationsRequest.FromString,
                    response_serializer=NameNodeService__pb2.GetBlockLocationsResponse.SerializeToString,
            ),
            'CreateFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFile,
                    request_deserializer=NameNodeService__pb2.CreateFileRequest.FromString,
                    response_serializer=NameNodeService__pb2.CreateFileResponse.SerializeToString,
            ),
            'AllocateBlocks': grpc.unary_unary_rpc_method_handler(
                    servicer.AllocateBlocks,
                    request_deserializer=NameNodeService__pb2.AllocateBlocksRequest.FromString,
                    response_serializer=NameNodeService__pb2.AllocateBlocksResponse.SerializeToString,
            ),
            'ListFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFiles,
                    request_deserializer=NameNodeService__pb2.ListFilesRequest.FromString,
                    response_serializer=NameNodeService__pb2.ListFilesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'protos.NameNodeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NameNodeService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterDataNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.NameNodeService/RegisterDataNode',
            NameNodeService__pb2.RegisterDataNodeRequest.SerializeToString,
            NameNodeService__pb2.RegisterDataNodeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Heartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.NameNodeService/Heartbeat',
            NameNodeService__pb2.HeartbeatRequest.SerializeToString,
            NameNodeService__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetBlockLocations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/protos.NameNodeService/GetBlockLocations',
            NameNodeService__pb2.GetBlockLocationsRequest.SerializeToString,
            NameNodeService__pb2.GetBlockLocationsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.NameNodeService/CreateFile',
            NameNodeService__pb2.CreateFileRequest.SerializeToString,
            NameNodeService__pb2.CreateFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AllocateBlocks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.NameNodeService/AllocateBlocks',
            NameNodeService__pb2.AllocateBlocksRequest.SerializeToString,
            NameNodeService__pb2.AllocateBlocksResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/protos.NameNodeService/ListFiles',
            NameNodeService__pb2.ListFilesRequest.SerializeToString,
            NameNodeService__pb2.ListFilesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
