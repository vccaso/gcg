import os
import chromadb
from chromadb.utils import embedding_functions
from models.modelbase import ModelBase
from utils.printer import Printer
from config import debug


class RequirementAgent:
    def __init__(self, llm: ModelBase, prompt_template, embedding_model: str = "all-MiniLM-L6-v2"):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")

        self.llm = llm
        self.prompt_template = prompt_template
        self.embedding_model = embedding_model

    def _query_rag(self, storage_path: str, collection_name: str, query: str, top_k: int = 5) -> str:
        try:
            ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=self.embedding_model)
            client = chromadb.PersistentClient(path=storage_path)
            collection = client.get_collection(name=collection_name, embedding_function=ef)
            result = collection.query(query_texts=[query], n_results=top_k)
            if debug:
                Printer.info(result)
            docs = result.get("documents", [[]])[0]
            return "\n---\n".join(docs) if docs else ""
        except Exception as e:
            Printer.warn(f"⚠️ Failed RAG query: {e}")
            return ""

    def run(self, description: str, location: str, storage_path: str = "rag_dbs", collection_name: str = None, top_k: int = 5,
            save_to_file: bool = False, file_name: str = "requirements_output.txt") -> str:

        context = ""
        if collection_name:
            search_query = f"bathroom construction codes and requirements for {location}"
            context = self._query_rag(storage_path, collection_name, search_query, top_k=top_k)

        try:
            final_prompt = self.prompt_template.format(
                description=description,
                location=location,
                context=context
            )
        except KeyError as e:
            raise ValueError(f"Missing required placeholder in template: {e}")

        if debug:
            print(f"[🧠] Final Prompt:\n{final_prompt}\n")

        response = self.llm.get_response(final_prompt)

        if save_to_file:
            try:
                dir_path = os.path.dirname(file_name)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
                with open(file_name, "a", encoding="utf-8") as f:
                    if debug:
                        f.write(f"Prompt: {final_prompt}\n")
                        f.write(f"Response: {response}\n")
                        f.write("-" * 40 + "\n")
                    else:
                        f.write(f"{response}\n\n")
            except Exception as e:
                print(f"⚠️ Failed to save response to file '{file_name}': {e}")
                return {"status": "Fail", "details": f"Failed to save response to file '{file_name}': {e}"}

        return {"status": "Success", "details": response}
