import logging
from github import Github
import os
import base64

def get_readme_content(org, repo):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        logging.error("GITHUB_TOKEN environment variable is not set")
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        logging.info(f"Attempting to fetch repo: {org}/{repo}")
        repository = g.get_repo(f"{org}/{repo}")
        logging.info(f"Fetching README for repo: {repository.full_name}")
        readme = repository.get_readme()
        content = base64.b64decode(readme.content).decode('utf-8')
        logging.info(f"README fetched successfully. Length: {len(content)}")
        return content
    except Exception as e:
        logging.error(f"Error fetching README: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python get_readme.py <owner> <repo>")
    else:
        org = sys.argv[1]
        repo = sys.argv[2]
        print(get_readme_content(org, repo))
