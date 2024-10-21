import logging
from github import Github
import os
import base64
import time
from requests.exceptions import RequestException

def get_readme_content(org, repo, max_retries=3, delay=5):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        logging.error("GITHUB_TOKEN environment variable is not set")
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    for attempt in range(max_retries):
        try:
            logging.info(f"Attempting to fetch repo: {org}/{repo} (Attempt {attempt + 1}/{max_retries})")
            repository = g.get_repo(f"{org}/{repo}")
            logging.info(f"Fetching README for repo: {repository.full_name}")
            readme = repository.get_readme()
            content = base64.b64decode(readme.content).decode('utf-8')
            logging.info(f"README fetched successfully. Length: {len(content)}")
            return content
        except (RequestException, ConnectionError) as e:
            logging.warning(f"Connection error on attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"Failed to fetch README after {max_retries} attempts")
                raise
        except Exception as e:
            logging.error(f"Unexpected error fetching README: {str(e)}", exc_info=True)
            raise

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python get_readme.py <owner> <repo>")
    else:
        org = sys.argv[1]
        repo = sys.argv[2]
        try:
            print(get_readme_content(org, repo))
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
