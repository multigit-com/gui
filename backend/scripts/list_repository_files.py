import os
import requests
from dotenv import load_dotenv

load_dotenv()

def list_repository_files(repo):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN is not set in the environment variables")

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Assuming the repo parameter is in the format "owner/repo"
    url = f'https://api.github.com/repos/{repo}/contents'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        contents = response.json()
        return [{'name': item['name'], 'size': item['size']} for item in contents if item['type'] == 'file']
    else:
        raise Exception(f"Failed to fetch repository contents. Status code: {response.status_code}, Response: {response.text}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python list_repository_files.py <owner/repo>")
    else:
        repo = sys.argv[1]
        print(list_repository_files(repo))
