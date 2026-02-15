# src/rag/document_loader.py

import json
from pathlib import Path

import yaml


class DocumentLoader:
    def __init__(self, base_path="src/rag/data"):
        self.base_path = Path(base_path)

    def load_yaml(self, filename):
        path = self.base_path / filename
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_json(self, filename):
        path = self.base_path / filename
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_all_documents(self):
        docs = []

        for file in self.base_path.glob("**/*"):
            if file.suffix in [".yaml", ".yml"]:
                content = yaml.safe_load(file.read_text())
                docs.append({"text": str(content), "source": str(file)})
            elif file.suffix == ".json":
                content = json.loads(file.read_text())
                docs.append({"text": str(content), "source": str(file)})

        return docs
