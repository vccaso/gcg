# models/model_qwen3_8b.py
import ollama
from models.modelbase import ModelBase
from utils.printer import Printer

class ModelQwen3_8b(ModelBase):
    def __init__(self, temperature: float = 0.7):
        self.model_name = "qwen3:8b"
        self.temperature = temperature
        super().__init__(self.model_name)

    def get_response(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                options={"temperature": self.temperature}
            )
            return response['message']['content'].strip()
        except Exception as e:
            Printer.error(f"Error calling Ollama model '{self.model_name}': {e}")
            return ""
