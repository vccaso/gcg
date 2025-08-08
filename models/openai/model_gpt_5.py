import os
from abc import ABC, abstractmethod
from openai import OpenAI  # pip install --upgrade openai
from models.modelbase import ModelBase
from utils.printer import Printer

class ModelGpt5(ModelBase):
    """
    Wrapper for OpenAI GPT-5 family using the modern Responses API,
    with a fallback to Chat Completions for older SDKs.
    """
    def __init__(self, temperature=0.2, model_name="gpt-5"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY env var")
        self.temperature = temperature
        self.model_name = model_name  # e.g., "gpt-5", "gpt-5-mini", "gpt-5-nano"
        self.client = OpenAI(api_key=api_key)
        super().__init__(api_key)

    def get_response(self, prompt: str) -> str:
        try:
            print(prompt)
            resp = self.client.responses.create(
                model=self.model_name,
                instructions="You are a helpful assistant.",
                input=prompt,
                max_output_tokens=4096,  # Responses API param
            )
            text = (getattr(resp, "output_text", None) or "").strip()
            if not text:
                # Fallback: inspect the structured output if helpers aren’t present
                parts = []
                print(resp)
                for item in getattr(resp, "output", []) or []:
                    for c in getattr(item, "content", []) or []:
                        if getattr(c, "type", None) in ("output_text", "output_message"):
                            parts.append(getattr(c, "text", "") or "")
                text = "\n".join(p for p in parts if p).strip()
            return text
        except Exception as e:
            Printer.error(f"Error calling OpenAI Responses API: {e}")
            return ""