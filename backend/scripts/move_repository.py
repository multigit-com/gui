import sys
import json
import requests
from dotenv import load_dotenv
import os
import time
import subprocess
from github import Github

load_dotenv()

def move_repository(repo_id, repo_name, source_org_id, target_org_id):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        source_org = g.get_organization(source_org_id)
        target_org = g.get_organization(target_org_id)
        repo = source_org.get_repo(repo_name)

        # Use the requests library to make the API call
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {github_token}"
        }
        data = {
            "new_owner": target_org.login
        }
        url = f"https://api.github.com/repos/{source_org.login}/{repo_name}/transfer"
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 202:  # 202 Accepted status code indicates success
            return {"success": True, "message": f"Repository {repo_name} moved from {source_org_id} to {target_org_id}"}
        else:
            return {"success": False, "error": f"Failed to move repository. Status code: {response.status_code}, Response: {response.text}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python move_repository.py <repo_id> <repo_name> <source_org_id> <target_org_id>")
    else:
        repo_id = sys.argv[1]
        repo_name = sys.argv[2]
        source_org_id = sys.argv[3]
        target_org_id = sys.argv[4]
        result = move_repository(repo_id, repo_name, source_org_id, target_org_id)
        print(json.dumps(result))
