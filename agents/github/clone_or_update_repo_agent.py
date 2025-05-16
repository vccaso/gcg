from agents.base import BaseAgent
import os
import sys
import git  # pip install GitPython
import requests
from utils.printer import Printer



class GitHubCloneOrUpdateRepoAgent():
     def run(self, repo_url, local_repo_dir, update_if_exists=False):

        github_token = os.getenv("GITHUB_TOKEN")

        if github_token is None:
            Printer.error("Error: GITHUB_TOKEN environment variable is not set.")
            sys.exit(1)
        
        # Insert token into URL for HTTPS authentication.
        auth_repo_url = repo_url.replace("https://", f"https://{github_token}@")
        if os.path.exists(local_repo_dir):
            if update_if_exists:
                Printer.message("Repository exists. Fetching updates...")
                self.repo = git.Repo(local_repo_dir)
                self.repo.remotes.origin.fetch()
                return {"status": "updated", "repo_path": local_repo_dir}
            else:
                Printer.info("Repo exists and update_if_exists=False. Skipping.")
                return {"status": "skipped", "repo_path": local_repo_dir}
        else:
            Printer.message("Cloning repository...")
            self.repo = git.Repo.clone_from(auth_repo_url, local_repo_dir)
        return {"status": "Success", "details": f"repo_path {local_repo_dir}"}