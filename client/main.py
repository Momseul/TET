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
    block_id = 0
    DATA_DOWNLOAD_DIR = "downloads"

    download_directory = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), DATA_DOWNLOAD_DIR)
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    file_name_parsed = os.path.splitext(file_name)[0]
    downloaded_file = os.path.join(download_directory, file_name_parsed)
    if not os.path.exists(downloaded_file):
        os.makedirs(downloaded_file)

    channel = grpc.insecure_channel(f"{ip_address}:{port}")
    datanode_service = DataNodeService_pb2_grpc.DataNodeServiceStub(channel)

    #len([name for name in os.listdir(fil) if os.path.isfile(name)])

    while True:
        try:
            request = DataNodeService_pb2.ReadBlockRequest(
                filename=file_name_parsed,
                blockId=str(block_id))
            for block in  datanode_service.ReadBlock(request):
                
                block_path = os.path.join(download_directory, file_name_parsed, str(block_id))
            
                with open(block_path, "wb") as block_file:
                        block_file.write(block.data)
                        logging.info(
                        f"Stored block {block_id} for file {file_name_parsed} successfully.")
            block_id+=1

        except AttributeError as atte:
            logging.error(f"no more files"+ {atte} )
            break
        except grpc.RpcError as e:
            logging.error("error %s", e )
            break
            
    destiny = downloaded_file+"/"+file_name
    merge_chunks(downloaded_file,destiny)

def merge_chunks(input_directory, output_file):
    try:
        with open(output_file, 'wb') as output:
            chunk_number = 0
            while True:
                chunk_file = f"{input_directory}/{chunk_number}"
                try:
                    with open(chunk_file, 'rb') as chunk:
                        output.write(chunk.read())
                        print(f"Fragmento {chunk_number} agregado al archivo")
                        chunk_number += 1
                except FileNotFoundError:
                    break  # No hay más fragmentos
    except Exception as e:
        print(f"Error al reensamblar los fragmentos: {e}")
    


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
        print(file_path)
        file_name = os.path.basename(file_path)
        print(file_name)
        get_file(ip_address, port, file_name)
    else:
        print("Comando no reconocido")
