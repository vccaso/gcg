import yaml
import os
from agents.agent_registry import AGENT_CATALOG
from models.model_registry import MODEL_CATALOG


class OrchestratorAgent:
    def __init__(self, llm, prompt_template: str = None):
        self.llm = llm
        self.prompt_template = prompt_template or "You are a workflow planner..."

    def generate_prompt(self, user_request: str, memory: dict = None) -> str:
        memory_context = ""
        if memory and "history" in memory and memory["history"]:
            memory_lines = ["### Previous User Requests:"]
            for i, item in enumerate(memory["history"][-3:], 1):
                memory_lines.append(f"{i}. {item['request']}")
            memory_context = "\n".join(memory_lines) + "\n---\n"

        base_prompt = self.prompt_template.format(
            request=user_request,
            agents_description=self.get_agent_description(),
            models_description=self.get_model_description()
        )

        return f"{memory_context}{base_prompt}"



    def get_agent_description(self) -> str:
        """
        Generate agent description for prompt building.
        """

        description_lines = []
        for agent_name, agent_info in AGENT_CATALOG.items():
            description_lines.append(f"- {agent_name}:")
            detailed_desc = agent_info.get("detailed_description")
            if detailed_desc:
                for line in detailed_desc:
                    description_lines.append(f"    - {line}")
            else:
                # fallback to short description if detailed missing
                description_lines.append(f"    - {agent_info['short_description']}")

        return "\n".join(description_lines)


    def get_model_description(self) -> str:
        """
        Generate model description dynamically for prompt building.
        """

        description_lines = []
        for model_name, model_info in MODEL_CATALOG.items():
            description_lines.append(f"- {model_name}:")
            detailed_desc = model_info.get("detailed_description")
            if detailed_desc:
                for line in detailed_desc:
                    description_lines.append(f"    - {line}")
            else:
                # fallback to short description
                description_lines.append(f"    - {model_info['short_description']}")

        return "\n".join(description_lines)
    

    def run(self, request: str, save_path: str = "workflows/wf_generated.yaml", memory: dict = None) -> dict:

        final_prompt = self.generate_prompt(request, memory)
        print(f"final prompt: {final_prompt}")
        workflow_yaml = self.llm.get_response(final_prompt).strip()

        # Clean markdown code block if present
        if workflow_yaml.startswith("```yaml"):
            workflow_yaml = workflow_yaml.replace("```yaml", "").strip()
        if workflow_yaml.endswith("```"):
            workflow_yaml = workflow_yaml[:-3].strip()

        # Save file
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(workflow_yaml)

        return {"path": save_path, "content": workflow_yaml}
