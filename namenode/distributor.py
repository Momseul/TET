class BlockDistributor:
    def __init__(self, data_nodes):
        self.data_nodes = data_nodes
        self.current_index = 0

    def update_data_nodes(self, data_nodes):
        self.data_nodes = data_nodes

    def distribute_block(self, active_data_nodes):
        """" Return the address of the DataNodes to store a block"""
        if not active_data_nodes:
            print("No active DataNodes available")
            return None
        # round-robin simple block distribution
        selected_data_node_address = list(active_data_nodes)[
            self.current_index % len(active_data_nodes)]
        self.current_index += 1
        return selected_data_node_address
