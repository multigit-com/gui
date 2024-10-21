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

        # Transfer the repository
        repo.transfer(target_org.login)

        return {"success": True, "message": f"Repository {repo_name} moved from {source_org_id} to {target_org_id}"}
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
        print(result)
