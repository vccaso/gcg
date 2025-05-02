import requests
import ollama  # pip install ollama
from models.modelbase import ModelBase
from utils.printer import Printer

class ModelOllama(ModelBase):
    def __init__(self, temperature: float = 0.7):
        self.model_name = "llama3"
        super().__init__(self.model_name)

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
