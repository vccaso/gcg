import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from utils.gocodeutil import GoCodeUtil
from config import debug
import openai
import requests


class GoSwaggerAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template


    def get_go_files(self, local_repo_dir):
        """
        Walk through LOCAL_REPO_DIR and return a list of paths for .go files.
        """
        go_files = []
        for root, dirs, files in os.walk(local_repo_dir):
            for file in files:
                if file.endswith(".go"):
                    go_files.append(os.path.join(root, file))
        return go_files


    def run(self, local_repo_dir):

        go_files = self.get_go_files(local_repo_dir)
        if not go_files:
            print("No Go files found in the repository.")
        else:
            for file_path in go_files:
                print(f"Processing file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as f:
                    original_code = f.read()

                # prepare the promt
                final_prompt = self.prompt_template.format(original_code=original_code)
                # call the model
                response = self.llm.get_response(final_prompt)

                # Optionally remove markdown formatting.
                if response.startswith("```go"):
                    response = response.replace("```go", "").strip()
                if response.endswith("```"):
                    response = response[:-3].strip()

                # Write back the updated code.
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(response)
                Printer.success(f"Processed and updated {file_path}")
