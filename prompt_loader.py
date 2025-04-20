import os

class PromptLoader:
    def __init__(self, base_path="prompts"):
        self.base_path = base_path

    def load_prompt(self, agent: str, name: str = "default") -> str:
        """
        Load a prompt template file by agent and template name.
        """
        file_path = os.path.join(self.base_path, agent, f"{name}.txt")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt '{name}.txt' not found for agent '{agent}'")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()


    def list_prompts(self) -> dict:
        """
        Scan all agents and list available prompt names.
        Returns a dict like { "AgentName": ["default", "foo", "bar"] }
        """
        prompts = {}
        for agent in os.listdir(self.base_path):
            agent_path = os.path.join(self.base_path, agent)
            if not os.path.isdir(agent_path):
                continue
            prompt_files = [
                f[:-4] for f in os.listdir(agent_path)
                if f.endswith(".txt")
            ]
            prompts[agent] = sorted(prompt_files)
        return prompts