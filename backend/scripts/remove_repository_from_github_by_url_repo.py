import os
import sys
import requests
from dotenv import load_dotenv
from log_utils import setup_logger

logger = setup_logger('remove_repository')

def remove_repository_from_github_by_url_repo(repo_url, env_path='../../.env'):
    logger.info(f"Starting repository removal process for {repo_url}")
    # Load environment variables from the specified .env file
    load_dotenv(env_path)
    
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if not GITHUB_TOKEN:
        logger.error('GITHUB_TOKEN not found in the environment variables.')
        return {'success': False, 'message': 'GITHUB_TOKEN not found in the environment variables.'}

    # Extract owner and repo name from the URL
    _, _, _, owner, repo = repo_url.rstrip('/').split('/')

    logger.info(f"Using token: {GITHUB_TOKEN[:4]}...{GITHUB_TOKEN[-4:]}")
    logger.info(f"Owner: {owner}, Repo: {repo}")

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    delete_url = f'https://api.github.com/repos/{owner}/{repo}'

    logger.info(f"Sending DELETE request to {delete_url}")
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        logger.info(f"Repository {owner}/{repo} has been successfully deleted.")
        return {'success': True, 'message': f'Repository {owner}/{repo} has been deleted.'}
    else:
        logger.error(f"Failed to delete repository. Status code: {response.status_code}, Response: {response.text}")
        return {'success': False, 'message': f'Failed to delete repository. Status code: {response.status_code}, Response: {response.text}'}

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        logger.error("Incorrect number of arguments provided.")
        print("Usage: python remove_repository_from_github_by_url_repo.py <repo_url> [env_file_path]")
        sys.exit(1)

    repo_url = sys.argv[1]
    env_path = sys.argv[2] if len(sys.argv) == 3 else '../../.env'
    
    logger.info(f"Script started with repo_url: {repo_url}, env_path: {env_path}")
    result = remove_repository_from_github_by_url_repo(repo_url, env_path)
    logger.info(f"Script finished with result: {result}")
    print(result)
