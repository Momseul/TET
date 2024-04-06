import grpc
from protos import DataNodeService_pb2, DataNodeService_pb2_grpc


DATA_NODE_ADDRESS = 'localhost:50052'

def test_store_block(data_node_address, block_id, block_data):
    with grpc.insecure_channel(data_node_address) as channel:
        stub = DataNodeService_pb2_grpc.DataNodeServiceStub(channel)
        response = stub.StoreBlock(iter([
            DataNodeService_pb2.StoreBlockRequest(
                blockData=DataNodeService_pb2.BlockData(blockId=block_id, data=block_data))
        ]))
        print(f"StoreBlock response: {response}")

if __name__ == "__main__":
    test_store_block(DATA_NODE_ADDRESS, 'test_block.txt', b'This is some block data.')
