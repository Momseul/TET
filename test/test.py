import grpc
from protos import NameNodeService_pb2, NameNodeService_pb2_grpc

def main():
    # conn server namenode
    channel = grpc.insecure_channel('localhost:50053')
    name_node_stub = NameNodeService_pb2_grpc.NameNodeServiceStub(channel)

    def test_register_datanode(stub, address):
        print(f"Registering DataNode with address {address}")
        response = stub.RegisterDataNode(
            NameNodeService_pb2.RegisterDataNodeRequest(dataNodeAddress=address)
        )
        assert response.status.success, response.status.message
        print("Registration successful")

    test_register_datanode(name_node_stub, "datanode1:50052")

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

if __name__ == "__main__":
    main()
