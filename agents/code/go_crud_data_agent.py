import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from utils.gocodeutil import GoCodeUtil
from config import debug
import openai
import requests


class GoCRUDDataAgent:
    def __init__(self, llm: ModelBase, prompt_template: str):
        self.llm = llm
        self.prompt_template = prompt_template

    def generate_prompt(self, **kwargs) -> str:
        model_name = kwargs.get("model")
        if model_name:
            kwargs.setdefault("Model", model_name[0].upper() + model_name[1:])
            kwargs.setdefault("model_lowercase", model_name.lower())

        return self.prompt_template.format(**kwargs)

    def run(self, **kwargs):
        final_prompt = self.generate_prompt(**kwargs)
        llm_response = self.llm.get_response(final_prompt).strip()
        # Write files
        written_files = self.write_data_file(llm_response)
        return "\n".join(written_files)

    def write_data_file(self, go_code: str) -> list:
        parts = re.split(r"==== (.+?)\/n", go_code)
        written = []
        for i in range(1, len(parts), 2):
            path = parts[i].strip()
            code = parts[i + 1].strip()
            go_code = GoCodeUtil.extract_go_code_block(code)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(go_code + "\n")
            written.append(path)
        return written

