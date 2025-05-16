from agents.base import BaseAgent
from utils.printer import Printer
import yaml


class OrchestratorFeedbackAgent(BaseAgent):
    """
    Given the original prompt and validator feedback, suggest an improved prompt.
    """

    def __init__(self, llm, prompt_template):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, original_prompt: str, validation_feedback: str) -> dict:
        Printer.info("🔁 Running OrchestratorFeedbackAgent...")

        prompt = self.prompt_template.format(original_prompt=original_prompt, validation_feedback=validation_feedback)
        response = self.llm.get_response(prompt)

        return {
            "new_prompt": response.strip()
        }