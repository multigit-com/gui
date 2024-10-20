import sys
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def list_repositories(org):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN is not set in the environment variables")

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
        raise Exception(f"Failed to fetch repositories. Status code: {response.status_code}, Response: {response.text}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python list_repositories.py <organization>")
    else:
        org = sys.argv[1]
        print(list_repositories(org))
