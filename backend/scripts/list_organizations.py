import sys
import json
import requests
from dotenv import load_dotenv
import os
import logging
from github import Github

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def list_all_organizations():
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        user = g.get_user()
        organizations = user.get_orgs()
        org_list = []
        for org in organizations:
            org_list.append({
                'id': org.id,
                'name': org.name,
                'login': org.login,
                'public_repos': org.public_repos,
                'forks_count': org.get_repos().totalCount  # This is an approximation of forks across all repos
            })
        return {"organizations": org_list}
    except Exception as e:
        print(f"Error listing organizations: {str(e)}")
        raise

if __name__ == '__main__':
    print(list_all_organizations())
