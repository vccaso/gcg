from models.modelbase import ModelBase
from utils.printer import Printer

class ChatAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, prompt: str, save_to_file: bool = False, file_name: str = "chat_output.txt") -> str:
        """
        Sends the prompt to the LLM and returns the response.
        If save_to_file is True, appends the response to the given file.
        """
        response = self.llm.get_response(prompt)

        if save_to_file:
            try:
                with open(file_name, "a", encoding="utf-8") as f:
                    f.write(f"Prompt: {prompt}\n")
                    f.write(f"Response: {response}\n")
                    f.write("-" * 40 + "\n")
            except Exception as e:
                print(f"⚠️ Failed to save response to file '{file_name}': {e}")

        return response