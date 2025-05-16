from agents.base import BaseAgent
from utils.printer import Printer
import yaml

class OrchestratorValidatorAgent(BaseAgent):
    """
    Validates a generated YAML workflow, assigns a quality score, and provides feedback.
    """

    def __init__(self, llm, prompt_template):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, workflow: str) -> dict:
        Printer.info("✅ Running OrchestratorValidatorAgent...")

        prompt = self.prompt_template.format(workflow=workflow)
        response_raw = self.llm.get_response(prompt)
        try:
            response = yaml.safe_load(response_raw)
        except yaml.YAMLError:
            response = {"status": "fail", "score": 0, "feedback": "Invalid YAML returned from model."}
        return {
            "score": response.get("score", 0),
            "status": response.get("status", "fail"),
            "feedback": response.get("feedback", "No feedback returned.")
        }

