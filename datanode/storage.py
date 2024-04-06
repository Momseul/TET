import os
import logging


class Storage:
    DATA_STORAGE_DIR = "storage"
    storage_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_STORAGE_DIR)

    def __init__(self):
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

    def store_block(self, block_id, data):
        try:
            block_path = os.path.join(self.storage_directory, block_id)
            with open(block_path, "wb") as block_file:
                block_file.write(data)
            return True
        except Exception as e:
            logging.error(f"Error storing block {block_id}: {e}")
            return False

    def read_block(self, block_id):
        block_path = os.path.join(self.storage_directory, block_id)
        # print(f"Esta es la ruta del bloque READ: {block_path}")
        try:
            with open(block_path, "rb") as block_file:
                return block_file.read()
        except FileNotFoundError:
            logging.error(f"Block {block_id} not found.")
        except Exception as e:
            logging.error(f"Error reading block {block_id}: {e}")
            return None
