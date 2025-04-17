import requests
import ollama  # pip install ollama
from models.modelbase import ModelBase
from utils.printer import Printer

class ModelOllama(ModelBase):
    def __init__(self, model_name="llama3"):
        self.model_name = model_name
        super().__init__(model_name)

    def get_response(self, prompt: str) -> str:
        """
        Sends the prompt to a local LLM via Ollama and returns the response.
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content'].strip()

        except Exception as e:
            Printer.error(f"Error calling Ollama local model '{self.model_name}': {e}")
            return ""


# model = ModelOllama(model_name="llama3")
# response = model.get_response("Explain how a binary search tree works.")
# print(response)




# class ModelLocalOllamaClient:
#     def __init__(self, model_name="llama3"):
#         self.model_name = model_name
#         self.url = "http://localhost:11434/api/chat"

#     def get_response(self, prompt: str) -> str:
#         """
#         Sends a prompt to the locally running Ollama model and returns the response.
#         """
#         try:
#             payload = {
#                 "model": self.model_name,
#                 "messages": [
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 "temperature": 0.2,
#                 "stream": False
#             }

#             response = requests.post(self.url, json=payload)
#             response.raise_for_status()
#             data = response.json()

#             return data["message"]["content"].strip()

#         except Exception as e:
#             print(f"Error calling Ollama: {e}")
#             return None
