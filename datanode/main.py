import argparse

from .datanode import start_data_node_service

# Default addresses
NAME_NODE_ADDRESS = 'localhost:50053'
DATA_NODE_ADDRESS = 'localhost:50052'

def parse_args():
    parser = argparse.ArgumentParser(description="DataNode for Distributed File System")
    parser.add_argument('--namenode_address', type=str, default=NAME_NODE_ADDRESS,
                        help='The address of the NameNode to connect to')
    parser.add_argument('--datanode_address', type=str, default=DATA_NODE_ADDRESS,
                        help='The address that this DataNode should bind to')
    return parser.parse_args()

if __name__ == "__main__":
    # Utiliza los argumentos proporcionados para configurar las direcciones y correr el DataNode
    args = parse_args()
    start_data_node_service(args.namenode_address, args.datanode_address)
