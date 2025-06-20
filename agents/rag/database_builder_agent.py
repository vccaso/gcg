import os
import json
import hashlib
import yaml
from textwrap import wrap
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from agents.base import BaseAgent
from utils.printer import Printer


class RAGDatabaseBuilderAgent(BaseAgent):
    def __init__(self, collection_name: str, storage_path: str = "rag_dbs", model: str = "all-MiniLM-L6-v2", chunk_size: int = 400):
        self.collection_name = collection_name
        self.storage_path = storage_path
        self.chunk_size = chunk_size
        self.registry_path = os.path.join(self.storage_path, collection_name, ".registry.json")

        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
        self.client = chromadb.PersistentClient(path=self.storage_path)

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.ef
        )

        self.registry = self._load_registry()

    def _load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_registry(self):
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2)

    def _file_key(self, file_path):
        stat = os.stat(file_path)
        return f"{file_path}:{stat.st_mtime}"

    def chunk_text(self, text: str) -> list:
        return wrap(text, width=self.chunk_size)

    def generate_chunk_id(self, file_path: str, chunk_text: str, index: int) -> str:
        raw = f"{file_path}-{index}-{chunk_text}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def run(self, source_files: list[str]) -> str:
        documents, ids, metadatas = [], [], []

        for file_path in source_files:
            if not os.path.exists(file_path):
                Printer.error(f"File not found: {file_path}")
                continue

            file_key = self._file_key(file_path)
            if file_path in self.registry and self.registry[file_path] == file_key:
                Printer.info(f"✅ Skipping already indexed file: {file_path}")
                continue

            ext = os.path.splitext(file_path)[-1].lower()
            try:
                if ext in [".yaml", ".yml"]:
                    with open(file_path, "r", encoding="utf-8") as f:
                        entries = yaml.safe_load(f)
                    for entry in entries:
                        text = entry["text"]
                        chunk_id = self.generate_chunk_id(file_path, text, 0)
                        documents.append(text)
                        ids.append(chunk_id)
                        metadatas.append({
                            "tags": ", ".join(entry.get("tags", [])),
                            "source": entry.get("source", ""),
                            "context": entry.get("context", "")
                        })

                elif ext == ".jsonl":
                    with open(file_path, "r", encoding="utf-8") as f:
                        for i, line in enumerate(f):
                            entry = json.loads(line)
                            text = entry["text"]
                            chunk_id = self.generate_chunk_id(file_path, text, i)
                            documents.append(text)
                            ids.append(chunk_id)
                            metadatas.append({
                                "tags": ", ".join(entry.get("tags", [])),
                                "source": entry.get("source", ""),
                                "context": entry.get("context", "")
                            })

                else:  # treat as plain text
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    chunks = self.chunk_text(text)
                    for i, chunk in enumerate(chunks):
                        chunk_id = self.generate_chunk_id(file_path, chunk, i)
                        documents.append(chunk)
                        ids.append(chunk_id)
                        metadatas.append({})

                # Mark file as indexed
                self.registry[file_path] = file_key

            except Exception as e:
                Printer.error(f"❌ Failed to process file {file_path}: {e}")

        if documents:
            self.collection.add(documents=documents, ids=ids, metadatas=metadatas)
            Printer.success(f"✅ Added {len(documents)} document(s) to collection '{self.collection_name}'")
        else:
            Printer.error("⚠️ No new documents were added.")

        self._save_registry()

        return f"Collection '{self.collection_name}' now contains {len(self.collection.get()['ids'])} items."
