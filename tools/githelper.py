import os
import sys
import git  # pip install GitPython
import requests
from utils.printer import Printer

class GitHelper:
    def __init__(self, github_token,repo_name, repo_url, local_repo_dir, source_branch, pr_title, pr_body):
        self.github_token = github_token
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.local_repo_dir = local_repo_dir
        self.source_branch = source_branch
        self.pr_title = pr_title
        self.pr_body = pr_body
        self.repo = None

    def clone_or_update_repo(self):
        """
        Clone the repository if not already cloned; otherwise, pull the latest changes.
        """
        if self.github_token is None:
            Printer.error("Error: GITHUB_TOKEN environment variable is not set.")
            sys.exit(1)
        
        # Insert token into URL for HTTPS authentication.
        auth_repo_url = self.repo_url.replace("https://", f"https://{self.github_token}@")
        if os.path.exists(self.local_repo_dir):
            self.repo = git.Repo(self.local_repo_dir)
            Printer.error("Repository exists locally. Fetching updates...")
            self.repo.remotes.origin.fetch()
        else:
            Printer.message("Cloning repository...")
            self.repo = git.Repo.clone_from(auth_repo_url, self.local_repo_dir)
        return self.repo

    def checkout_branch(self, branch_name):
        """
        Check out the specified branch. If it does not exist locally, try to create it tracking origin.
        """
        try:
            self.repo.git.checkout(branch_name)
        except git.exc.GitCommandError:
            Printer.error(f"Branch {branch_name} not found locally, creating tracking branch.")
            self.repo.git.checkout(f"origin/{branch_name}", b=branch_name)
        Printer.message(f"Checked out branch {branch_name}")

    def create_new_branch(self, new_branch):
        """
        Create a new branch from the current branch.
        """
        self.repo.git.checkout("-b", new_branch)
        Printer.message(f"Created and switched to new branch {new_branch}")

    def get_go_files(self):
        """
        Walk through LOCAL_REPO_DIR and return a list of paths for .go files.
        """
        go_files = []
        for root, dirs, files in os.walk(self.local_repo_dir):
            for file in files:
                if file.endswith(".go"):
                    go_files.append(os.path.join(root, file))
        return go_files

    def stage_commit_push(self, new_branch,commit_message="GCG: message added from git tool"):
        """
        Stage all changes, commit them, and push the branch to GitHub.
        """
        self.repo.git.add(A=True)  # stage all changes
        try:
            self.repo.git.commit("-m", commit_message)
            Printer.message("Committed changes.")
        except git.exc.GitCommandError as e:
            Printer.error("No changes to commit or commit failed:", e)
            return

        origin = self.repo.remotes.origin
        try:
            origin.push(new_branch)
            Printer.message(f"Pushed branch {new_branch} to GitHub.")
        except Exception as e:
            Printer.error("Error during push:", e)

    def create_pull_request(self, new_branch):
        """
        Create a pull request from the new branch to the source branch using GitHub API.
        """
        # Update these values to match your repository owner and name, if necessary.
        owner = "vccaso"
        repo_name = self.repo_name
        pr_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
        
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        
        payload = {
            "title": self.pr_title,
            "head": new_branch,
            "base": self.source_branch,
            "body": self.pr_body,
        }
        
        response = requests.post(pr_url, json=payload, headers=headers)
        if response.status_code == 201:
            pr_data = response.json()
            Printer.message(f"Pull Request created: {pr_data.get('html_url')}")
        else:
            Printer.error(f"Failed to create Pull Request. Status Code: {response.status_code}")
            print(response.json())
