import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from agents.base import BaseAgent
from utils.printer import Printer
from textwrap import wrap


class RAGAttachAgent(BaseAgent):
    def __init__(self, storage_path: str = "rag_dbs", model: str = "all-MiniLM-L6-v2"):
        self.storage_path = storage_path
        self.model = model

    def run(self, collection_name: str, alias: str) -> str:
        try:
            ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=self.model)
            client = chromadb.PersistentClient(path=os.path.join(self.storage_path))
            collection = client.get_collection(name=collection_name, embedding_function=ef)

            rag_registry[alias] = collection
            Printer.success(f"✅ Attached collection '{collection_name}' as alias '{alias}'")
            return f"Alias '{alias}' registered for collection '{collection_name}'"

        except Exception as e:
            Printer.error(f"❌ Failed to attach collection: {e}")
            return f"[Failed to attach collection]"

