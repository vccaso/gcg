from models.modelbase import ModelBase
from utils.printer import Printer

class GoCRUDAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, final_prompt):
        """
        Uses the ChatGPT API to generate complete CRUD code for a given model.
        The final_prompt should be the prompt with any necessary placeholders (e.g. {model})
        already substituted. Returns the generated code output.
        """
        crud_code = self.llm.get_response(final_prompt)

        # Optionally remove markdown formatting.
        if crud_code.startswith("```go"):
            crud_code = crud_code.replace("```go", "").strip()
        if crud_code.endswith("```"):
            crud_code = crud_code[:-3].strip()

        return crud_code