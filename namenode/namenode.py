from protos import NameNodeService_pb2_grpc, NameNodeService_pb2
import grpc
from concurrent import futures
import time
import logging
from .metadata import MetadataManager
from .distributor import BlockDistributor
import threading


HEARTBEAT_INTERVAL = 3  # Time interval for checking DataNode liveness
HEARTBEAT_THRESHOLD = 10  # Max time of waitng for heartbeat before DataNode as dead

NAME_NODE_ADDRESS = 'localhost:50053'


class NameNode(NameNodeService_pb2_grpc.NameNodeServiceServicer):

    def __init__(self):
        self.data_nodes = {}  # registro de los datanodes
        self.metadata_manager = MetadataManager()  # metadata de los archivos
        self.block_distribudor = BlockDistributor(
            self.data_nodes)  # Distribuidor de bloques
        self.heartbeat_lock = threading.Lock()  # Lock para manejar los heartbeats

        logging.basicConfig(level=logging.INFO)

    # Registro de DataNodes en el NameNode.
    def RegisterDataNode(self, request, context):
        address = request.dataNodeAddress
        with self.heartbeat_lock:
            # Registrar la direccion del DataNode y marcarlo como activo
            self.data_nodes[address] = {
                "active": True, "last_seen": time.time()}
        logging.info(f"DataNode {address} registered successfully.")
        return NameNodeService_pb2.RegisterDataNodeResponse(
            status=NameNodeService_pb2.StatusResponse(
                success=True, message=f"Registered {address} successfully.")
        )

    # Recepcion de heartbeats de DataNodes para mantenerlos activos.
    def Heartbeat(self, request, context):
        with self.heartbeat_lock:
            address = request.dataNodeAddress
            data_node_info = self.data_nodes.get(address)

            if data_node_info is not None:
                data_node_info["active"] = True
                data_node_info["last_seen"] = time.time()
                logging.info(f"Heartbeat received from DataNode {address}.")
                return NameNodeService_pb2.StatusResponse(success=True)
            else:
                logging.info(
                    f"Heartbeat received from an unknown DataNode {address}.")
                return NameNodeService_pb2.StatusResponse(success=False, message="Unknown DataNode")

    def GetBlockLocations(self, request, context):
        """ Recupera la ubicación de los bloques para leer un archivo."""
        filename = request.filename
        file_metadata = self.metadata_manager.get_file_metadata(filename)

        if file_metadata:
            for block in file_metadata["blocks"]:
                yield NameNodeService_pb2.GetBlockLocationsResponse(
                    blockLocations=[
                        NameNodeService_pb2.GetBlockLocationsResponse.BlockLocation(
                            blockId=block["id"],
                            dataNodeAddresses=block["locations"]
                        )
                    ]
                )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('File not found.')

    # Creación de un nuevo archivo en el sistema de archivos.
    def CreateFile(self, request, context):
        try:
            filename = request.filename
            if self.metadata_manager.get_file_metadata(filename) is None:
                if self.metadata_manager.create_file(filename):
                    logging.info(f"File {filename} created successfully.")
                    context.set_details(f'File created {filename}')
                    return NameNodeService_pb2.CreateFileResponse(success=True)
            else:
                logging.error(f"File {filename} already exists.")
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details('File already exists.')
                return NameNodeService_pb2.CreateFileResponse(success=False)
        except (grpc.RpcError, Exception) as e:
            logging.error(f"Error creating file: {filename} not found: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_code(grpc.StatusCode.INTERNAL)

    # AllocateBlocks es el metodo que se encarga de saber q bloques de datos a los DataNodes
    def AllocateBlocks(self, request, context):
        filename = request.filename
        blocks_ids = request.blockIds
        block_allocations = []  # Lista de bloques asignados

        # Se obtienen los DataNodes activos
        active_data_nodes = [address for address, data_node_info in self.data_nodes.items(
        ) if data_node_info["active"]]
        # Si no hay DataNodes activos, no se pueden asignar bloques
        if not active_data_nodes:
            context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
            context.set_details("No active DataNodes available.")
            return NameNodeService_pb2.AllocateBlocksResponse(status=NameNodeService_pb2.StatusResponse(success=False, message="No active DataNodes available."))

        for block_id in blocks_ids:
            logging.info(f"Allocating block {block_id} for file {filename}")
            # lista de datanodes activos para distribuir los bloques entre ellos
            data_nodes_to_storage = self.block_distribudor.distribute_block(
                active_data_nodes)

            if not data_nodes_to_storage:
                context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
                context.set_details(
                    "Failed to distribute block due to lack of active DataNodes.")
                return NameNodeService_pb2.AllocateBlocksResponse(status=NameNodeService_pb2.StatusResponse(success=False, message="Failed to distribute block."))

            block_data = self.metadata_manager.add_block(
                filename, block_id, data_nodes_to_storage)

            if block_data:
                block_allocations.append(NameNodeService_pb2.BlockAllocation
                                         (blockId=block_id,
                                          dataNodeAddresses=[data_nodes_to_storage]))
                logging.info(
                    f"Block {block_id} allocated to DataNode {data_nodes_to_storage}")
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Error adding block to metadata.")
                logging.error("Error adding block to metadata.")
                return NameNodeService_pb2.AllocateBlocksResponse(status=NameNodeService_pb2.StatusResponse(success=False, message="Error adding block to metadata."))

        return NameNodeService_pb2.AllocateBlocksResponse(status=NameNodeService_pb2.StatusResponse(success=True, message="Blocks allocated successfully."), blockAllocations=block_allocations)

    # Listado de archivos/directorios
    def ListFiles(self, request, context):
        filenames = list(self.metadata_manager.list_files())
        return NameNodeService_pb2.ListFilesResponse(filenames=filenames)

    def check_data_node_liveness(self):
        """Runs in a separate thread to check DataNode states"""
        while True:
            with self.heartbeat_lock:
                current_time = time.time()
                for address, data_node_info in list(self.data_nodes.items()):
                    if current_time - data_node_info["last_seen"] > HEARTBEAT_THRESHOLD and data_node_info["active"]:
                        # marca DataNode como inactivo si el heartbeat no se ha recibido en el tiempo esperado.
                        data_node_info["active"] = False
                        logging.info(
                            f"DataNode {address} marked as inactive due to timeout.")
            time.sleep(HEARTBEAT_INTERVAL)


def serve():
    name_node = NameNode()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    NameNodeService_pb2_grpc.add_NameNodeServiceServicer_to_server(
        name_node, server)
    server.add_insecure_port(NAME_NODE_ADDRESS)

    liveness_thread = threading.Thread(
        target=name_node.check_data_node_liveness, daemon=True)
    liveness_thread.start()

    server.start()
    logging.info(
        f"NameNode gRPC server started, listening on {NAME_NODE_ADDRESS}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        logging.info("NameNode is shutting down.")


if __name__ == '__main__':
    serve()
