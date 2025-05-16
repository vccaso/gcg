from agents.base import BaseAgent
import os
import sys
import git  # pip install GitPython
import requests
from utils.printer import Printer

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
            return {"status": "Success", "details":f"Pull Request created. {pr_data.get('html_url')}"}
        else:
            print(f"Failed to create Pull Request. Status Code: {response.status_code}")
            print(response.json())
            return {"status": "Fail", "details":f"Failed to create Pull Request {response.status_code}"}

