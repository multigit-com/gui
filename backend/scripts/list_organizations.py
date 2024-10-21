import sys
import json
import os
import logging
import time
from github import Github
from github.GithubException import RateLimitExceededException
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def list_all_organizations(page=1, per_page=20, max_retries=3, delay=5):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    for attempt in range(max_retries):
        try:
            user = g.get_user()
            organizations = user.get_orgs().get_page(page - 1)
            org_list = []
            for org in organizations:
                repos = org.get_repos()
                public_repos = org.public_repos
                private_repos = sum(1 for repo in repos if repo.private)
                forked_repos = sum(1 for repo in repos if repo.fork)
                total_repos = public_repos + private_repos

                org_list.append({
                    'id': org.id,
                    'name': org.name,
                    'login': org.login,
                    'public_repos': public_repos,
                    'private_repos': private_repos,
                    'forked_repos': forked_repos,
                    'total_repos': total_repos
                })
            
            has_next_page = len(org_list) == per_page
            return {"organizations": org_list, "has_next_page": has_next_page, "page": page}
        except RateLimitExceededException as e:
            logger.warning(f"Rate limit exceeded. Waiting for {e.reset} seconds.")
            time.sleep(e.reset)
        except Exception as e:
            logger.error(f"Error listing organizations (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise

if __name__ == '__main__':
    print(json.dumps(list_all_organizations()))
