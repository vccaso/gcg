from agents.base import BaseAgent
import os
import sys
import git  # pip install GitPython
import requests
from utils.printer import Printer

class GitHubCreateBranchAgent(BaseAgent):
    def run(self, branch_name,local_repo_dir):
        """
        Check out the specified branch. If it does not exist locally, try to create it tracking origin.
        """
        try:
            self.repo = git.Repo(local_repo_dir)
            self.repo.git.checkout("-b", branch_name)
            Printer.message(f"Created and switched to new branch {branch_name}")
        except git.exc.GitCommandError:
            Printer.error(f"Branch {branch_name} not found locally, creating tracking branch.")
