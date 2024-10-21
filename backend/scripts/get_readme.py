import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

def get_readme_content(repo):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN is not set in the environment variables")

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{repo}/readme'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        content = response.json()['content']
        return base64.b64decode(content).decode('utf-8')
    else:
        raise Exception(f"Failed to fetch README. Status code: {response.status_code}, Response: {response.text}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_readme.py <owner/repo>")
    else:
        repo = sys.argv[1]
        print(get_readme_content(repo))
