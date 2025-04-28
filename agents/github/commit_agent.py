from agents.base import BaseAgent
import os
import sys
import git  # pip install GitPython
import requests
from utils.printer import Printer


class GitHubCommitAgent(BaseAgent):
    def run(self, new_branch,local_repo_dir,commit_message):
        self.repo = git.Repo(local_repo_dir)
        self.repo.git.add(A=True)  # stage all changes
        try:
            self.repo.git.commit("-m", commit_message)
            Printer.message("Committed changes.")
        except git.exc.GitCommandError as e:
            Printer.error(f"No changes to commit or commit failed: {e}")
            return

        origin = self.repo.remotes.origin
        try:
            origin.push(new_branch)
            Printer.message(f"Pushed branch {new_branch} to GitHub.")
        except Exception as e:
            Printer.error("Error during push:", e)
