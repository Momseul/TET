import logging
import os
import threading
import time
import grpc
from concurrent import futures
from protos import NameNodeService_pb2, NameNodeService_pb2_grpc
from protos import DataNodeService_pb2, DataNodeService_pb2_grpc
from .storage import Storage

HEARTBEAT_INTERVAL = 3  # Time interval for checking DataNode liveness
HEARTBEAT_THRESHOLD = 10  # Max time of waitng for heartbeat before DataNode as dead


class DataNode(DataNodeService_pb2_grpc.DataNodeServiceServicer):
    def __init__(self, namenode_address, datanode_address):
        self.namenode_address = namenode_address
        self.datanode_address = datanode_address
        self.channel = grpc.insecure_channel(namenode_address)
        self.stub = NameNodeService_pb2_grpc.NameNodeServiceStub(self.channel)
        self.storage = Storage()

        logging.basicConfig(level=logging.INFO)

    def StoreBlock(self, request_iterator, context):
        """Store blocks from a file in the DataNode storage"""
        for request in request_iterator:
            block_id = request.blockData.blockId
            data = request.blockData.data
            file_name = request.filename
            if self.storage.store_block(file_name, block_id, data):
                logging.info(f"Stored block {block_id} successfully ")
            else:
                logging.error(f"Failed to store block {block_id}")
                return DataNodeService_pb2.StatusRes(success=False, message="Failed to store block")

        return DataNodeService_pb2.StatusRes(success=True, message=f"Blocks for file:{file_name} stored successfully.")

    def ReadBlock(self, request, context):
        block_id = request.blockId
        file_name = request.filename
        block_data = self.storage.read_block(file_name, block_id)
        if block_data is not None:
            logging.info(
                f"Block {block_id} read successfully from file {file_name}")
            yield DataNodeService_pb2.BlockData(blockId=block_id, data=block_data)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f'Block {block_id} not found.')
            return DataNodeService_pb2.StatusRes(success=False, message=f"Blocks for file:{file_name} not found.")

    def ReplicateBlock(self, request, context):
        # replication
        pass

    def register_with_namenode(self):
        try:
            response = self.stub.RegisterDataNode(
                NameNodeService_pb2.RegisterDataNodeRequest(dataNodeAddress=self.datanode_address))
            if response.status.success:
                logging.info(f"Registration with NameNode successful")
            else:
                logging.error("Registration with NameNode failed: " +
                              response.status.message)
        except grpc.RpcError as e:
            logging.error(f"Registration with NameNode failed: {e.details()}")

    def send_heartbeat(self):
        last_heartbeat_time = time.time()
        while True:
            try:
                current_time = time.time()
                if current_time - last_heartbeat_time > HEARTBEAT_INTERVAL * HEARTBEAT_THRESHOLD:
                    logging.error(
                        f"Heartbeat failed: {self.namenode_address} Exceeded maximum retry interval.")
                    # fin de heartbeat ?
                    break
                    # sys.exit(1) # exit the DataNode
                response = self.stub.Heartbeat(NameNodeService_pb2.HeartbeatRequest(
                    dataNodeAddress=self.datanode_address, timestamp=int(time.time())))
                if response.success:
                    # logging.info("Heartbeat to {self.namenode_address} sent successfully")
                    last_heartbeat_time = current_time
                else:
                    logging.error("Heartbeat failed: " + response.message)
                time.sleep(HEARTBEAT_INTERVAL)
            except grpc.RpcError as e:
                logging.error(f"Heartbeat failed with error: {e.details()}")
                time.sleep(HEARTBEAT_INTERVAL)

    def start_heartbeat(self):
        # registro inicial con el NameNode
        self.register_with_namenode()

        # Iniciar thread para heartbeats
        heartbeat_thread = threading.Thread(
            target=self.send_heartbeat, daemon=True)
        heartbeat_thread.start()
        logging.info(
            f"DataNode {self.datanode_address} started. Sending heartbeats to NameNode {self.namenode_address}")


def serve(data_node_service, datanode_address):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    DataNodeService_pb2_grpc.add_DataNodeServiceServicer_to_server(
        data_node_service, server)
    server.add_insecure_port(datanode_address)
    server.start()
    logging.info(f"DataNode serving at {datanode_address}")
    server.wait_for_termination()


def start_data_node_service(namenode_address, datanode_address):
    datanode = DataNode(namenode_address, datanode_address)
    datanode.start_heartbeat()
    serve(datanode, datanode_address)
    # DataNode corriendo
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("DataNode is shutting down.")
