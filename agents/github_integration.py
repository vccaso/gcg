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

class GitHubPRAgent(BaseAgent):
    def run(self, repo_name, pr_title, new_branch, source_branch, pr_body):
        owner = "vccaso"  # update with repository owner
        repo_name = "avila-easychat-goals"  # update with repository name
        pr_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
        
        github_token = os.getenv("GITHUB_TOKEN")

        if github_token is None:
            Printer.error("Error: GITHUB_TOKEN environment variable is not set.")
            sys.exit(1)

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        payload = {
            "title": pr_title,
            "head": new_branch,
            "base": source_branch,
            "body": pr_body,
        }
        
        response = requests.post(pr_url, json=payload, headers=headers)
        if response.status_code == 201:
            pr_data = response.json()
            print(f"Pull Request created: {pr_data.get('html_url')}")
        else:
            print(f"Failed to create Pull Request. Status Code: {response.status_code}")
            print(response.json())

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
        Printer.message(f"Checked out branch {source_branch}")


class GitHubCloneOrUpdateRepoAgent():
     def run(self, repo_url, local_repo_dir):

        github_token = os.getenv("GITHUB_TOKEN")

        if github_token is None:
            Printer.error("Error: GITHUB_TOKEN environment variable is not set.")
            sys.exit(1)
        
        # Insert token into URL for HTTPS authentication.
        auth_repo_url = repo_url.replace("https://", f"https://{github_token}@")
        if os.path.exists(local_repo_dir):
            self.repo = git.Repo(local_repo_dir)
            Printer.error("Repository exists locally. Fetching updates...")
            self.repo.remotes.origin.fetch()
        else:
            Printer.message("Cloning repository...")
            self.repo = git.Repo.clone_from(auth_repo_url, local_repo_dir)
        return self.repo