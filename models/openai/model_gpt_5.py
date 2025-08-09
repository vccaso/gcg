import os
from abc import ABC, abstractmethod
from openai import OpenAI  # pip install --upgrade openai
from models.modelbase import ModelBase
from utils.printer import Printer

class ModelGpt5(ModelBase):
    """
    Wrapper for OpenAI GPT-5 family using the Responses API.
    Subclasses can override model_name / max_output_tokens / instructions.
    """
    def __init__(
        self,
        temperature: float = 0.2,
        model_name: str = "gpt-5",
        max_output_tokens: int = 4096,
        instructions: str = "You are a helpful assistant."
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY env var")

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature   # kept for API parity; not sent by default
        self.max_output_tokens = max_output_tokens
        self.instructions = instructions
        super().__init__(api_key)

    def get_response(self, prompt: str) -> str:
        try:
            resp = self.client.responses.create(
                model=self.model_name,
                instructions=self.instructions,
                input=prompt,
                max_output_tokens=self.max_output_tokens,
                # NOTE: Many GPT‑5 variants reject temperature; omit it.
            )
            text = (getattr(resp, "output_text", None) or "").strip()
            print(resp)
            if not text:
                # Fallback: stitch from structured output
                parts = []
                for item in getattr(resp, "output", []) or []:
                    for c in getattr(item, "content", []) or []:
                        if getattr(c, "type", None) in ("output_text", "output_message", "text"):
                            parts.append(getattr(c, "text", "") or "")
                text = "\n".join(p for p in parts if p).strip()
            return text
        except Exception as e:
            Printer.error(f"Error calling OpenAI Responses API: {e}")
            return ""


class ModelGpt5Mini(ModelGpt5):
    """
    Cheaper/faster GPT-5 variant. Defaults tuned for concise output.
    """
    def __init__(self, temperature: float = 0.2):
        super().__init__(
            temperature=temperature,
            model_name="gpt-5-mini",
            max_output_tokens=2048,
            instructions="You are a concise, helpful assistant. Prefer short, direct answers."
        )


class ModelGpt5Nano(ModelGpt5):
    """
    Lowest-cost GPT-5 variant. Extra concise by default.
    """
    def __init__(self, temperature: float = 0.2):
        super().__init__(
            temperature=temperature,
            model_name="gpt-5-nano",
            max_output_tokens=1024,
            instructions="You are a terse, helpful assistant. Answer in under 120 words unless asked otherwise."
        )