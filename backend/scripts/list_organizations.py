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
            repos = org.get_repos()
            public_repos = org.public_repos
            private_repos = sum(1 for repo in repos if repo.private)
            forked_repos = sum(1 for repo in repos if repo.fork)
            total_repos = public_repos + private_repos

            # Get custom name from environment variable or use original name
            custom_name = os.getenv(f'CUSTOM_ORG_NAME_{org.login}', org.name)

            org_list.append({
                'id': org.id,
                'name': org.name,
                'login': org.login,
                'original_name': org.name,
                'custom_name': custom_name,
                'public_repos': public_repos,
                'private_repos': private_repos,
                'forked_repos': forked_repos,
                'total_repos': total_repos
            })
        return {"organizations": org_list}
    except Exception as e:
        logger.error(f"Error listing organizations: {str(e)}")
        raise

if __name__ == '__main__':
    print(json.dumps(list_all_organizations()))
