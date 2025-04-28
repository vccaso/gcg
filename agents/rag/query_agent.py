import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from agents.base import BaseAgent
from utils.printer import Printer
from textwrap import wrap


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

