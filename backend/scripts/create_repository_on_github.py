import os
import sys
import requests

def create_repository_on_github(repo_name, description=""):
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
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
    
    response = requests.post(create_url, headers=headers, json=data)
    
    if response.status_code == 201:
        return {'success': True, 'message': f'Repository {repo_name} has been created.', 'url': response.json()['html_url']}
    else:
        return {'success': False, 'message': f'Failed to create repository. Status code: {response.status_code}'}

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python create_repository_on_github.py <repo_name> [description]")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) == 3 else ""
    result = create_repository_on_github(repo_name, description)
    print(result)
