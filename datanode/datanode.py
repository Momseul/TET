import logging
import os
import sys
import threading
import time
import grpc
from protos import NameNodeService_pb2, NameNodeService_pb2_grpc


class DataNode:
    def __init__(self, namenode_address, datanode_address):
        self.namenode_address = namenode_address
        self.datanode_address = datanode_address
        self.channel = grpc.insecure_channel(namenode_address)
        self.stub = NameNodeService_pb2_grpc.NameNodeServiceStub(self.channel)

        logging.basicConfig(level=logging.INFO)

    def register_with_namenode(self):
        response = self.stub.RegisterDataNode(
            NameNodeService_pb2.RegisterDataNodeRequest(dataNodeAddress=self.datanode_address))
        if response.status.success:
            logging.info("Registration with NameNode successful")
        else:
            logging.error("Registration with NameNode failed: " +
                          response.status.message)

    def send_heartbeat(self):
        while True:
            try:
                response = self.stub.Heartbeat(NameNodeService_pb2.HeartbeatRequest(
                    dataNodeAddress=self.datanode_address, timestamp=int(time.time())))
                if not response.success:
                    logging.error("Heartbeat failed: " + response.message)
                time.sleep(3)
            except grpc.RpcError as e:
                logging.error(f"Heartbeat failed with error: {e}")

    def start(self):
        # registro inicial con el NameNode
        self.register_with_namenode()

        # Iniciar thread para heartbeats
        heartbeat_thread = threading.Thread(
            target=self.send_heartbeat, daemon=True)
        heartbeat_thread.start()


if __name__ == "__main__":
    # DataNode se ejecuta en localhost y escucha en el puerto 50052
    datanode = DataNode(namenode_address="localhost:50053",
                        datanode_address="localhost:50052")
    datanode.start()

    # DataNode corriendo
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("DataNode is shutting down.")
