import sys
import os
import grpc
from protos import DataNodeService_pb2, DataNodeService_pb2_grpc
from protos import NameNodeService_pb2, NameNodeService_pb2_grpc
import logging


NAME_NODE_ADDRESS = 'localhost:50053'

logging.basicConfig(level=logging.INFO)


def create_file_namenode(file_name, namenode_address):
    channel = grpc.insecure_channel(namenode_address)
    stub = NameNodeService_pb2_grpc.NameNodeServiceStub(channel)
    try:
        response = stub.CreateFile(
            NameNodeService_pb2.CreateFileRequest(filename=file_name))
        if response.success:
            logging.info(
                f"File {file_name} registered on NameNode - MetaData: {response}")
            # y los metadatos de asignacion/d de bloques y distribucion datanodes ?
            return response
        else:
            logging.error(f"Failed to register file {file_name} in NameNode.")
            return None
    except (Exception, grpc.RpcError) as e:
        logging.error(f"Error creating file: {e}")
        return None


def put_file_to_datanode(ip_address, port, file_path):
    channel = grpc.insecure_channel(f"{ip_address}:{port}")
    datanode_service = DataNodeService_pb2_grpc.DataNodeServiceStub(channel)
    with open(file_path, 'rb') as file:
        block_id = 0
        for chunk in iter(lambda: file.read(4096), b''):
            request = DataNodeService_pb2.StoreBlockRequest(
                blockData=DataNodeService_pb2.BlockData(
                blockId=str(block_id),
                data=chunk),
                filename=file_path)
            response = datanode_service.StoreBlock(iter([request]))
            if not response.success:
                print("Failed to store block:", response.message)
                return
            block_id += 1
    print("File stored successfully on the DataNode.")

def get_file(ip_address, port, file_name):
    print("searching ...")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python main.py <ip address> <port> -p <file path>")
        sys.exit(1)

    ip_address = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]
    file_path = sys.argv[4]

    if command == "-p":
        create_file_namenode(file_path, NAME_NODE_ADDRESS)
        put_file_to_datanode(ip_address, port, file_path)
    elif command == "-g":
        file_name = os.path.basename(file_path)
        get_file(ip_address, port, file_name)
    else:
        print("Comando no reconocido")
