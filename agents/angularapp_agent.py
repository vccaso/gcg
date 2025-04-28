import os
from models.modelbase import ModelBase
from utils.printer import Printer
from config import debug

class AngularAppAgent:
    def __init__(self, llm: ModelBase, prompt_template: str):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM must be instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def generate_prompt(self, **kwargs):
        if "feature_description" not in kwargs:
            raise ValueError("Missing 'feature_description' in input")
        if "app_base_dir" not in kwargs:
            kwargs["app_base_dir"] = "src/app"

        return self.prompt_template.format(**kwargs)

    def run(self, **kwargs):
        final_prompt = self.generate_prompt(**kwargs)
        print(f"[🧠] Final Prompt:\n{final_prompt}\n")
        result = self.llm.get_response(final_prompt)

        if result.startswith("```"):
            result = result.split("```", 1)[-1].strip()
        return result
