import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from agents.base import BaseAgent
from utils.printer import Printer
from textwrap import wrap

class RAGDatabaseBuilderAgent(BaseAgent):
    
    def __init__(self, collection_name: str, storage_path: str = "rag_dbs", model: str = "all-MiniLM-L6-v2"):
        self.collection_name = collection_name
        self.storage_path = storage_path

        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
        self.client = chromadb.PersistentClient(path=os.path.join(self.storage_path))

        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.ef
        )

    def run(self, source_files: list[str]) -> str:
        """
        Create a vector database collection (ChromaDB) by embedding documents from local files.
        """
        try:
            documents = []
            ids = []

            for idx, file_path in enumerate(source_files):
                if not os.path.exists(file_path):
                    Printer.warn(f"File not found: {file_path}")
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    # documents.append(text)
                    # ids.append(f"doc-{idx}")
                    chunks = wrap(text, 200)  # 500-character chunks (adjust for tokens)
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        ids.append(f"{file_path}-chunk-{i}")

            if documents:
                self.collection.add(documents=documents, ids=ids)
                Printer.success(f"✅ Added {len(documents)} document(s) to collection '{self.collection_name}'")
            else:
                Printer.warn("⚠️ No documents were added.")

        except Exception as e:
            Printer.error(f"❌ Error while adding documents to collection: {e}")

        return f"Collection '{self.collection_name}' now contains {len(self.collection.get()['ids'])} items."

