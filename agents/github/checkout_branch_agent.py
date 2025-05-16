from agents.base import BaseAgent
import os
import sys
import git  # pip install GitPython
import requests
from utils.printer import Printer

class GitHubCheckoutBranchAgent(BaseAgent):
    def run(self, source_branch,local_repo_dir):
        """
        Check out the specified branch. If it does not exist locally, try to create it tracking origin.
        """
        try:
            self.repo = git.Repo(local_repo_dir)
            self.repo.git.checkout(source_branch)
        except git.exc.GitCommandError:
            Printer.error(f"Branch {source_branch} not found locally, creating tracking branch.")
            self.repo.git.checkout(f"origin/{source_branch}", b=source_branch)
            return {"status": "Fail", "details":f"Branch {source_branch} not found locally, creating tracking branch."}
        Printer.message(f"Checked out branch {source_branch}")
        return {"status": "Success", "details":f"Checked out branch {source_branch}"}
        

