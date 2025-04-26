# models/model_deepseek.py

from models.modelbase import ModelBase
import requests
import os

class ModelDeepSeekCoder67(ModelBase):
    def __init__(self, temperature: float = 0.7):
        # Local DeepSeek endpoint, e.g., http://localhost:11434
        self.base_url = os.getenv("DEEPSEEK_URL", "http://localhost:11434")
        self.temperature = temperature
        self.model = "deepseek-coder:6.7b"  # or "deepseek-chat"
        super().__init__(self.base_url)

    def get_response(self, prompt: str, max_tokens: int = 1024) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": self.temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"❌ DeepSeek error: {e}")
            return f"Error: {e}"
