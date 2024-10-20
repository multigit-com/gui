import os
import sys
import requests

def remove_repository_from_github_by_url_repo(repo_url):
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    
    # Extract owner and repo name from the URL
    _, _, _, owner, repo = repo_url.rstrip('/').split('/')
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    delete_url = f'https://api.github.com/repos/{owner}/{repo}'
    
    response = requests.delete(delete_url, headers=headers)
    
    if response.status_code == 204:
        return {'success': True, 'message': f'Repository {owner}/{repo} has been deleted.'}
    else:
        return {'success': False, 'message': f'Failed to delete repository. Status code: {response.status_code}'}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python remove_repository_from_github_by_url_repo.py <repo_url>")
        sys.exit(1)
    
    repo_url = sys.argv[1]
    result = remove_repository_from_github_by_url_repo(repo_url)
    print(result)
