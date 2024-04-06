import grpc
from protos import NameNodeService_pb2, NameNodeService_pb2_grpc
from protos import DataNodeService_pb2, DataNodeService_pb2_grpc

def main():
    # conn server namenode
    name_node_address = "localhost:50053"
    # diferent node server
    data_node_address = "localhost:50052"
    
    
    name_node_stub = NameNodeService_pb2_grpc.NameNodeServiceStub(grpc.insecure_channel(name_node_address))
    data_node_stub = DataNodeService_pb2_grpc.DataNodeServiceStub(grpc.insecure_channel(data_node_address))

    def test_register_datanode(stub, address):
        print(f"Registering DataNode with address {address}")
        response = stub.RegisterDataNode(
            NameNodeService_pb2.RegisterDataNodeRequest(dataNodeAddress=address)
        )
        assert response.status.success, response.status.message
        print("Registration successful")

    test_register_datanode(name_node_stub, "datanode1:50054")

    def test_create_file(stub, filename):
        print(f"Creating file {filename}")
        try:
            response = stub.CreateFile(NameNodeService_pb2.CreateFileRequest(filename=filename))
            print("File created" if response.success else "File creation failed")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")

    def test_allocate_blocks(stub, filename, block_data):
        print(f"Allocating blocks for file {filename}")
        response = stub.AllocateBlocks(
            NameNodeService_pb2.AllocateBlocksRequest(filename=filename, blocksData=[block_data])
        )
        if response.status.success:
            print(f"Blocks allocated: {[b.blockId for b in response.blockAllocations]}")
        else:
            print("Block allocation failed:", response.status.message)

    # testing el archivo es solo texto, no tiene bloques ni datos
    test_create_file(name_node_stub, "fileTest.txt")
    test_allocate_blocks(name_node_stub, "fileTest.txt", b"some data for the block")


    def test_list_files(stub):
        print("Listing files")
        response = stub.ListFiles(NameNodeService_pb2.ListFilesRequest(path="/"))
        for filename in response.filenames:
            print(f"Found file: {filename}")

    test_list_files(name_node_stub)

    def test_get_block_locations(stub, filename):
        print(f"Getting block locations for file {filename}")
        try:
            responses = stub.GetBlockLocations(NameNodeService_pb2.GetBlockLocationsRequest(filename=filename))
            for response in responses:
                print(f"Block locations: {[(b.blockId, b.dataNodeAddresses) for b in response.blockLocations]}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.details()}")

    # testing el archivo es solo texto, no tiene bloques ni datos
    test_get_block_locations(name_node_stub, "fileTest.txt")

    def test_store_block(data_node_address, block_id, block_data):
        with grpc.insecure_channel(data_node_address) as channel:
            stub = DataNodeService_pb2_grpc.DataNodeServiceStub(channel)
            block_data_message = DataNodeService_pb2.BlockData(blockId=block_id, data=block_data)
            response = stub.StoreBlock(iter([DataNodeService_pb2.StoreBlockRequest(blockData=block_data_message)]))
            print("StoreBlock response:", response)

    test_store_block('localhost:50052', 'test_block', b'This is some block data.')
    
if __name__ == "__main__":
    main()
