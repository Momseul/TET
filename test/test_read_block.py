import grpc
from protos import DataNodeService_pb2, DataNodeService_pb2_grpc

DATA_NODE_ADDRESS = 'localhost:50052'

def test_read_block(data_node_address, file_name, block_id):
    with grpc.insecure_channel(data_node_address) as channel:
        stub = DataNodeService_pb2_grpc.DataNodeServiceStub(channel)
        try:
            for response in stub.ReadBlock(DataNodeService_pb2.ReadBlockRequest(filename=file_name,blockId=block_id)):
                print("ReadBlock response for file:", file_name, "Block ID:", response.blockId, "Data:", response.data)
        except grpc.RpcError as e:
            print(f"GRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    test_read_block(DATA_NODE_ADDRESS, 'requirements','0')  # block_id STRING, no bytes

