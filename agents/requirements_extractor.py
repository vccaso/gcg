from agents.base import BaseAgent

class RequirementsExtractorAgent(BaseAgent):
    def run(self, repo_path):
        print(f"[extract] Scanning repo at {repo_path}")
        return {"requirements": ["flask", "sqlalchemy"]}
