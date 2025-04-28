import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from agents.base import BaseAgent
from utils.printer import Printer
from textwrap import wrap

class RAGDatabaseUpdaterAgent(BaseAgent):
    def __init__(self, collection_name: str, storage_path: str = "rag_dbs", model: str = "all-MiniLM-L6-v2"):
        self.collection_name = collection_name
        self.storage_path = storage_path

        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
        self.client = chromadb.PersistentClient(path=os.path.join(self.storage_path))
        self.collection = self.client.get_collection(name=self.collection_name, embedding_function=ef)

    def run(self, source_files: list[str]) -> str:
        try:
            documents = []
            ids = []
            start_index = len(self.collection.get()['ids'])

            for i, file_path in enumerate(source_files):
                if not os.path.exists(file_path):
                    Printer.warn(f"File not found: {file_path}")
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    chunks = wrap(text, 200)  # 500-character chunks (adjust for tokens)
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        ids.append(f"{file_path}-chunk-{i}")
                    # documents.append(text)
                    # ids.append(f"doc-{start_index + i}")

            if documents:
                self.collection.add(documents=documents, ids=ids)
                Printer.success(f"✅ Updated collection '{self.collection_name}' with {len(documents)} new document(s)")
            else:
                Printer.warn("⚠️ No new documents were added.")

        except Exception as e:
            Printer.error(f"❌ Error while updating collection: {e}")

        return f"Collection '{self.collection_name}' now contains {len(self.collection.get()['ids'])} items."

