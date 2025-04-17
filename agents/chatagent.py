from models.modelbase import ModelBase
from utils.printer import Printer

class ChatAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, prompt):
        """
        Uses the ChatGPT API to chat with local model.
        """
        response = self.llm.get_response(prompt)
        return response