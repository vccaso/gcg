from agents.base import BaseAgent
import os, re

class RequirementsExtractorAgent(BaseAgent):

    def run(self, repo_path):
        print(f"[extract] Scanning repo at {repo_path}")
        packages = set()

        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(".py"):
                    
                    with open(os.path.join(root, file), "r") as f:
                        for line in f:
                            match = re.match(r"^import (\w+)|^from (\w+)", line)
                            if match:
                                pkg = match.group(1) or match.group(2)
                                if pkg:
                                    packages.add(pkg)

        return {"requirements": sorted(packages)}
