import os
import sys
import requests
from dotenv import load_dotenv
from log_utils import setup_logger

logger = setup_logger('copy_repository')

def copy_repository(source_url, target_url, env_path='../../.env'):
    logger.info(f"Starting repository move process from {source_url} to {target_url}")
    load_dotenv(env_path)

    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if not GITHUB_TOKEN:
        logger.error('GITHUB_TOKEN not found in the environment variables.')
        return {'success': False, 'message': 'GITHUB_TOKEN not found in the environment variables.'}

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Extract owner and repo name from the URLs
    _, _, _, source_owner, source_repo = source_url.rstrip('/').split('/')
    _, _, _, target_owner = target_url.rstrip('/').split('/')

    # Use the source repo name for the target
    target_repo = source_repo

    logger.info(f"Moving repository: {source_owner}/{source_repo} to {target_owner}/{target_repo}")

    # Get repository information
    get_repo_url = f'https://api.github.com/repos/{source_owner}/{source_repo}'
    logger.info(f"Fetching repository information from {get_repo_url}")
    response = requests.get(get_repo_url, headers=headers)
    if response.status_code != 200:
        logger.error(f"Failed to fetch repository information. Status code: {response.status_code}")
        return {'success': False, 'message': f'Failed to fetch repository information. Status code: {response.status_code}'}

    repo_info = response.json()

    # Create new repository
    create_url = f'https://api.github.com/orgs/{target_owner}/repos'
    create_data = {
        "name": target_repo,
        "description": repo_info.get('description', ''),
        "private": repo_info['private']
    }
    logger.info(f"Creating new repository: {target_owner}/{target_repo}")
    response = requests.post(create_url, headers=headers, json=create_data)
    if response.status_code != 201:
        logger.error(f"Failed to create new repository. Status code: {response.status_code}")
        return {'success': False, 'message': f'Failed to create new repository. Status code: {response.status_code}'}

    new_repo_info = response.json()

    # Clone and push repository
    clone_url = f'https://{GITHUB_TOKEN}@github.com/{source_owner}/{source_repo}.git'
    push_url = new_repo_info['clone_url'].replace('https://', f'https://{GITHUB_TOKEN}@')

    os.system(f'git clone --mirror {clone_url} temp_repo')
    os.chdir('temp_repo')
    os.system(f'git push --mirror {push_url}')
    os.chdir('..')
    os.system('rm -rf temp_repo')

    logger.info(f"Repository successfully moved from {source_url} to {new_repo_info['html_url']}")
    return {'success': True, 'message': f"Repository moved successfully. New URL: {new_repo_info['html_url']}"}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        logger.error("Incorrect number of arguments provided.")
        print("Usage: python copy_repository.py <source_url> <target_url>")
        sys.exit(1)

    source_url = sys.argv[1]
    target_url = sys.argv[2]

    logger.info(f"Script started with source_url: {source_url}, target_url: {target_url}")
    result = copy_repository(source_url, target_url)
    logger.info(f"Script finished with result: {result}")
    print(result)
