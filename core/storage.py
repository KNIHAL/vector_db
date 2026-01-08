import json
import os

class Storage:
    def __init__(self, filepath):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump([], f)

    def read_all(self):
        with open(self.filepath, "r") as f:
            return json.load(f)

    def write_all(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)
