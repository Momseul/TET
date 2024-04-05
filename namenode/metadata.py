import json
import os
import threading
import uuid


class MetadataManager:
    def __init__(self, filepath="metadata.json"):
        self.lock = threading.Lock()
        self.filepath = filepath
        self.files_metadata = self.load_metadata()

    def load_metadata(self):
        """Loads metadata from a JSON file"""
        with self.lock:
            try:
                with open(self.filepath, 'r') as file:
                    self.files_metadata = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading metadata: {e}")
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

    def add_block(self, filename, data_node_address, block_data):
        if filename in self.files_metadata:
            # Genera un ID único para el bloque con UUIDs
            block_id = str(uuid.uuid4())
            self.files_metadata[filename]["blocks"].append({
                "id": block_id,
                "locations": [data_node_address],
            })
            self.save_metadata()
            return block_id
        else:
            return None

    def get_file_metadata(self, filename):
        return self.files_metadata.get(filename, None)

    def list_files(self):
        return list(self.files_metadata.keys())
