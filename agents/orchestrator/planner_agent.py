from agents.base import BaseAgent
from utils.printer import Printer

class OrchestratorPlannerAgent(BaseAgent):
    """
    This agent converts a natural language request into a structured YAML plan
    that includes workflow vars and step descriptions.
    """

    def __init__(self, llm, prompt_template):
        self.llm = llm
        self.prompt_template = prompt_template

    def run(self, request: str, agents_description: str, models_description: str) -> dict:
        Printer.info("🧠 Running OrchestratorPlannerAgent...")

        prompt = self.prompt_template.format(
            request=request,
            agents_description=agents_description,
            models_description=models_description
        )

        response = self.llm.get_response(prompt)

        return {
            "yaml_plan": response.strip()
        }