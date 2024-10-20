import os
import sys
import requests
from dotenv import load_dotenv
from log_utils import setup_logger

logger = setup_logger('create_repository')

def create_repository_on_github(repo_name, description="", env_path='../../.env'):
    logger.info(f"Starting repository creation process for {repo_name}")
    # Load environment variables from the specified .env file
    load_dotenv(env_path)
    
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    if not GITHUB_TOKEN:
        logger.error('GITHUB_TOKEN not found in the environment variables.')
        return {'success': False, 'message': 'GITHUB_TOKEN not found in the environment variables.'}

    logger.info(f"Using token: {GITHUB_TOKEN[:4]}...{GITHUB_TOKEN[-4:]}")

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        "name": repo_name,
        "description": description,
        "private": False
    }
    
    create_url = 'https://api.github.com/user/repos'
    
    logger.info(f"Sending POST request to {create_url}")
    response = requests.post(create_url, headers=headers, json=data)
    
    if response.status_code == 201:
        logger.info(f"Repository {repo_name} has been successfully created.")
        return {'success': True, 'message': f'Repository {repo_name} has been created.', 'url': response.json()['html_url']}
    else:
        logger.error(f"Failed to create repository. Status code: {response.status_code}, Response: {response.text}")
        return {'success': False, 'message': f'Failed to create repository. Status code: {response.status_code}, Response: {response.text}'}

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        logger.error("Incorrect number of arguments provided.")
        print("Usage: python create_repository_on_github.py <repo_name> [description] [env_file_path]")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    env_path = sys.argv[3] if len(sys.argv) == 4 else '../../.env'
    
    logger.info(f"Script started with repo_name: {repo_name}, description: {description}, env_path: {env_path}")
    result = create_repository_on_github(repo_name, description, env_path)
    logger.info(f"Script finished with result: {result}")
    print(result)
