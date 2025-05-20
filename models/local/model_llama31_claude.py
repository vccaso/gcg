# models/model_llama31_claude.py
import ollama
from models.modelbase import ModelBase
from utils.printer import Printer

class ModelLlama31Claude(ModelBase):
    def __init__(self, temperature: float = 0.7):
        self.model_name = "incept5/llama3.1-claude"
        self.temperature = temperature
        super().__init__(self.model_name)

    def get_response(self, prompt: str) -> str:
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are an assistant called Claude."},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": self.temperature,
                    "stop": ["<|start_header_id|>", "<|end_header_id|>", "<|eot_id|>"]
                }
            )
            return response['message']['content'].strip()
        except Exception as e:
            Printer.error(f"Error calling Ollama model '{self.model_name}': {e}")
            return ""
