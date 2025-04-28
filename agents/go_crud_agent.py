import os
import re
from models.modelbase import ModelBase
from utils.printer import Printer
from utils.gocodeutil import GoCodeUtil
from config import debug
import openai
import requests

class GoCRUDAgent:
    def __init__(self, llm: ModelBase, prompt_template: str):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def write_files_from_output(self, output: str) -> list:
        """
        Parses code output marked with:
        ==== ./some/path/to/file.go/n
        Writes or updates files:
        - Overwrites model/ and data/
        - Updates http/api/ and http/server.go if file exists
        Returns a list of written/updated file paths.
        """
        written_files = []
        parts = re.split(r"==== (.+?)\/n", output)

        for i in range(1, len(parts), 2):
            file_path = parts[i].strip()
            new_content = parts[i + 1].strip()

            go_code = GoCodeUtil.extract_go_code_block(new_content)
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Detect mode: overwrite or update
            if "http/api/" in file_path or file_path.endswith("server.go"):
                # Update logic: append to existing file
                if os.path.exists(file_path):
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write("\n\n// === AI-generated addition ===\n")
                        f.write(go_code + "\n")
                    action = "updated"
                else:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(go_code + "\n")
                    action = "created"
            else:
                # Default: overwrite
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content + "\n")
                action = "written"

            written_files.append(f"{file_path} ({action})")

        return written_files

    def generate_prompt(self, **kwargs) -> str:
        """
        Fills in the prompt template using keyword arguments.
        Example:
            prompt_template = "Generate CRUD for model {model} with fields {fields}"
            kwargs = { "model": "Product", "fields": "ID, Name, Price" }
        """
        try:
            return self.prompt_template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing placeholder in template: {e}")

    def run(self, **kwargs) -> str:
        """
        Generates CRUD Go code and updates files intelligently where needed.
        """

        local_repo_dir = kwargs.get("local_repo_dir", ".")

        # Load existing API file content if exists
        api_path = os.path.join(local_repo_dir, "http/api", f"{kwargs['model']}.go")
        if os.path.exists(api_path):
            with open(api_path, "r", encoding="utf-8") as f:
                kwargs["existing_api"] = f.read()
        else:
            kwargs["existing_api"] = ""

        # Load existing server.go if exists
        server_path = os.path.join(local_repo_dir, "http", "server.go")
        if os.path.exists(server_path):
            with open(server_path, "r", encoding="utf-8") as f:
                kwargs["existing_routes"] = f.read()
        else:
            kwargs["existing_routes"] = ""

        final_prompt = self.generate_prompt(**kwargs)
        crud_code = self.llm.get_response(final_prompt)
        crud_code = GoCodeUtil.strip_markdown_formatting(crud_code)

        written_files = self.write_files_from_output(crud_code)

        if debug:
            print(f"[📁] Files written:\n- " + "\n- ".join(written_files))

        return crud_code
