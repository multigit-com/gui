import os
import sys
import requests
from dotenv import load_dotenv
import json
import subprocess

load_dotenv()

def remove_repository_from_github_by_url_repo(repo_url, source_org):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Extract owner and repo name from the URL
    _, _, _, owner, repo = repo_url.rstrip('/').split('/')

    delete_url = f'https://api.github.com/repos/{owner}/{repo}'
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 204:
        # Log the successful removal
        subprocess.run(['python', 'log_repository_remove.py', repo_url, source_org])
        return {'success': True, 'message': f'Repository {owner}/{repo} has been deleted.'}
    else:
        return {'success': False, 'message': f'Failed to delete repository. Status code: {response.status_code}'}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(json.dumps({'success': False, 'message': 'Repository URL and source organization are required'}))
    else:
        repo_url = sys.argv[1]
        source_org = sys.argv[2]
        result = remove_repository_from_github_by_url_repo(repo_url, source_org)
        print(json.dumps(result))
