import json
import logging
import os
import threading


class MetadataManager:
    def __init__(self, filepath="metadata.json"):
        self.lock = threading.Lock()
        self.filepath = filepath
        self.files_metadata = self.load_metadata()

    def load_metadata(self):
        """Loads metadata from a JSON file"""
        with self.lock:
            if not os.path.isfile(self.filepath):
                self.files_metadata = {}
                return self.files_metadata
            try:
                with open(self.filepath, 'r') as file:
                    self.files_metadata = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logging.error(f"Error loading metadata: {e}")
                self.files_metadata = {}
            return self.files_metadata

    def save_metadata(self):
        """Saves the current metadata to a JSON file."""
        with self.lock:
            with open(self.filepath, 'w') as file:
                json.dump(self.files_metadata, file, indent=4)

    def create_file(self, filename):
        if filename not in self.files_metadata and self.get_file_metadata(filename) is None:
            self.files_metadata[filename] = {"blocks": []}
            self.save_metadata()
            return True
        else:
            return False

    def add_block(self, filename, block_id, data_node_addresses):
            if filename not in self.files_metadata:
                self.create_file(filename)
                logging.error(
                    f"File {filename} not found in metadata. Ensure the file is created first.")
                return False

            blocks = self.files_metadata[filename]["blocks"]
            # Verificar si el bloque ya existe
            if any(block["id"] == block_id for block in blocks):
                logging.error(
                    f"Block {block_id} already exists for file {filename}.")
                return False

            # Agregar el nuevo bloque y ubicaciones a la lista de bloques
            blocks.append({
                "id": block_id,
                "locations": [data_node_addresses]
            })
            self.files_metadata[filename]["blocks"] = blocks
            # Guardar los metadatos actualizados
            self.save_metadata()
            logging.info(
                f"Block {block_id} added for file {filename} with locations {data_node_addresses}.")
            return True

    def get_file_metadata(self, filename):
        return self.files_metadata.get(filename, None)

    def list_files(self):
        return list(self.files_metadata.keys())
