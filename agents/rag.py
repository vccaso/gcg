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


class RAGQueryAgent(BaseAgent):
    def __init__(self, collection_name: str, storage_path: str = "rag_dbs", model: str = "all-MiniLM-L6-v2", llm=None):
        self.collection_name = collection_name
        self.storage_path = storage_path
        self.llm = llm  # Your LLM (OpenAI, Ollama, etc.)

        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model)
        self.client = chromadb.PersistentClient(path=os.path.join(self.storage_path))
        self.collection = self.client.get_collection(name=self.collection_name, embedding_function=ef)

    def run(self, user_query: str) -> str:
        try:
            # Retrieve top 3 documents
            result = self.collection.query(query_texts=[user_query], n_results=3)
            docs = result["documents"][0]
            docs = result.get("documents", [[]])[0]
            if not docs:
                return "No relevant documents found."

            context = "\n---\n".join(docs)
            prompt = f"Using the following context, answer the user's question:\n{context}\n\nQuestion: {user_query}"

            if self.llm:
                answer = self.llm.get_response(prompt)
                return answer
            else:
                return f"[Context only — no LLM configured]\n\n{context}"

        except Exception as e:
            Printer.error(f"❌ Error during RAG query: {e}")
            return "[Error processing query]"


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

