# models/model_deepseek.py

from models.modelbase import ModelBase
import requests
import os

class ModelDeepSeek(ModelBase):
    def __init__(self, base_url=None):
        # Local DeepSeek endpoint, e.g., http://localhost:11434
        self.base_url = base_url or os.getenv("DEEPSEEK_URL", "http://localhost:11434")
        self.model = "deepseek-coder"  # or "deepseek-chat"
        super().__init__(self.base_url)

    def get_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "temperature": temperature,
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
