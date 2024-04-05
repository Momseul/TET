class BlockDistributor:
    def __init__(self, data_nodes):
        self.data_nodes = data_nodes
        self.current_index = 0

    def update_data_nodes(self, data_nodes):
        self.data_nodes = data_nodes

    def distribute_block(self):
        """" Return the address of the DataNode to store a block"""
        # round-robin simple block distribution
        if not self.data_nodes:
            return None, "No DataNodes available"
        data_node_addresses = list(self.data_nodes.keys())
        selected_data_node_address = data_node_addresses[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.data_nodes)
        return selected_data_node_address, None
