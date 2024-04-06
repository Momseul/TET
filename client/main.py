import sys
import grpc
from protos import DataNodeService_pb2, DataNodeService_pb2_grpc

def put_file_to_datanode(ip_address, port, file_path):
    channel = grpc.insecure_channel(f"{ip_address}:{port}")
    datanode_service = DataNodeService_pb2_grpc.DataNodeServiceStub(channel)
    with open(file_path, 'rb') as file:
        block_id = 0
        for chunk in iter(lambda: file.read(4096), b''):
            request = DataNodeService_pb2.StoreBlockRequest(blockData=DataNodeService_pb2.BlockData(blockId=block_id, data=chunk))
            response = datanode_service.StoreBlock(iter([request]))
            if not response.success:
                print("Failed to store block:", response.message)
                return
            block_id += 1
    print("File stored successfully on the DataNode.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python main.py <ip address> <port> -p <file path>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]
    file_path = sys.argv[4]

    if command == "-p":
        put_file_to_datanode(ip_address, port, file_path)
    else:
        print("Comando no reconocido")