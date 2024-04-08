import os
import logging


class Storage:
    DATA_STORAGE_DIR = "storage"

    def __init__(self):
        self.storage_directory = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), self.DATA_STORAGE_DIR)
        if not os.path.exists(self.storage_directory):
            os.makedirs(self.storage_directory)

    def store_block(self, file_name, block_id, data):
        try:
            # archivo sin su extension para la creacion del directory
            file_name = os.path.splitext(file_name)[0]
            file_directory = os.path.join(self.storage_directory, file_name)
            if not os.path.exists(file_directory):
                os.makedirs(file_directory)

            block_path = os.path.join(
                self.storage_directory, file_name, block_id)
            with open(block_path, "wb") as block_file:
                block_file.write(data)
            logging.info(
                f"Stored block {block_id} for file {file_name} successfully.")
            return True
        except Exception as e:
            logging.error(
                f"Error storing block {block_id} in {file_name}: {e}")
            return False

    def read_block(self, file_name, block_id):
        file_name = os.path.splitext(file_name)[0]
        block_path = os.path.join(self.storage_directory, file_name, block_id)
        try:
            if not os.path.exists(block_path):
                logging.error(
                    f"Block {block_id} for file {file_name} not found.")
                return None
            with open(block_path, "rb") as block_file:
                logging.info(
                    f"Read block {block_id} for file {file_name} successfully.")
                return block_file.read()
            
        except FileNotFoundError:
            logging.error(f"Block {block_id} not found.")
        except Exception as e:
            logging.error(f"Error reading block {block_id}: {e}")
            return None
