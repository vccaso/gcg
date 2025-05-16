from agents.base import BaseAgent
from utils.printer import Printer

class OrchestratorBuilderAgent(BaseAgent):
    """
    Converts a structured YAML plan (from the planner) into a valid executable YAML workflow.
    """

    def __init__(self, llm, prompt_template):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, plan: str) -> dict:
        Printer.info("🏗️ Running OrchestratorBuilderAgent...")

        prompt = self.prompt_template.format(plan=plan)
        response = self.llm.get_response(prompt)

        return {
            "workflow": response.strip()
        }
