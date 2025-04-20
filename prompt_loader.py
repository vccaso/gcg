import os

class PromptLoader:
    def __init__(self, base_path="prompts"):
        self.base_path = base_path

    def load_prompt(self, agent: str, name: str="default") -> str:
        path = os.path.join(self.base_path, agent, f"{name}.txt")
        with open(path, "r") as f:
            return f.read()
