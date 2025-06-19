# agents/build/build_requirement_agent.py
from models.modelbase import ModelBase
from utils.printer import Printer
from config import debug
import os


class MaterialEstimatorAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, requirements: str, save_to_file: bool = False, file_name: str = "materials_output.txt") -> str:
        try:
            final_prompt = self.prompt_template.format(requirements=requirements)
        except KeyError as e:
            raise ValueError(f"Missing required placeholder in template: {e}")



        if debug:
            print(f"[🧠] Final Prompt:\n{final_prompt}\n")

        response = self.llm.get_response(final_prompt)

        if save_to_file:
            try:
                dir_path = os.path.dirname(file_name)
                if dir_path:
                    os.makedirs(dir_path, exist_ok=True)
                with open(file_name, "a", encoding="utf-8") as f:
                    if debug:
                        f.write(f"Prompt: {final_prompt}\n")
                        f.write(f"Response: {response}\n")
                        f.write("-" * 40 + "\n")
                    else:
                        f.write(f"{response}\n\n")
            except Exception as e:
                print(f"⚠️ Failed to save response to file '{file_name}': {e}")
                return {"status": "Fail", "details":f"Failed to save response to file '{file_name}': {e}"}
        return {"status": "Success", "details":f"{response}"}
    
    