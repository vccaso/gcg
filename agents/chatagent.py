from models.modelbase import ModelBase
from utils.printer import Printer

class ChatAgent:
    def __init__(self, llm: ModelBase, prompt_template):
        if not isinstance(llm, ModelBase):
            raise ValueError("LLM model must be an instance of ModelBase")
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, question: str, save_to_file: bool = False, file_name: str = "chat_output.txt") -> str:
        """
        Formats the user input using the prompt template, sends it to the LLM, and returns the response.
        Example template: "You are a helpful assistant in Germany. Answer this in German: {question}"
        """
        try:
            final_prompt = self.prompt_template.format(question=question)
        except KeyError as e:
            raise ValueError(f"Missing required placeholder in template: {e}")

        print(f"[🧠] Final Prompt:\n{final_prompt}\n")

        response = self.llm.get_response(final_prompt)

        if save_to_file:
            try:
                with open(file_name, "a", encoding="utf-8") as f:
                    f.write(f"Prompt: {final_prompt}\n")
                    f.write(f"Response: {response}\n")
                    f.write("-" * 40 + "\n")
            except Exception as e:
                print(f"⚠️ Failed to save response to file '{file_name}': {e}")

        return response
    