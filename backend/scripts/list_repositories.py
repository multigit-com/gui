import sys
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def list_repositories(org):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f'https://api.github.com/orgs/{org}/repos'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        return [{'id': repo['id'], 'name': repo['name'], 'html_url': repo['html_url']} for repo in repos]
    else:
        return []

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'Organization parameter is required'}))
    else:
        org = sys.argv[1]
        repositories = list_repositories(org)
        print(json.dumps(repositories))
