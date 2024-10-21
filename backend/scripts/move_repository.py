import sys
import json
import requests
from dotenv import load_dotenv
import os
import time
import subprocess

load_dotenv()

def move_repository(repo_id, source_org, target_org):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get repository details
    repo_url = f'https://api.github.com/repositories/{repo_id}'
    repo_response = requests.get(repo_url, headers=headers)
    if repo_response.status_code != 200:
        return {'success': False, 'message': f'Failed to fetch repository details. Status: {repo_response.status_code}'}
    
    repo_data = repo_response.json()
    repo_name = repo_data['name']

    # Transfer repository
    transfer_url = f'https://api.github.com/repos/{source_org}/{repo_name}/transfer'
    transfer_data = {'new_owner': target_org}
    transfer_response = requests.post(transfer_url, headers=headers, json=transfer_data)
    
    if transfer_response.status_code == 202:
        # Wait for the transfer to complete
        for _ in range(10):  # Try up to 10 times
            time.sleep(2)  # Wait for 2 seconds before checking
            check_url = f'https://api.github.com/repos/{target_org}/{repo_name}'
            check_response = requests.get(check_url, headers=headers)
            if check_response.status_code == 200:
                # Log the successful move
                subprocess.run(['python', 'log_repository_move.py', repo_id, repo_name, source_org, target_org])
                return {'success': True, 'message': f'Repository {repo_name} moved successfully'}
        
        return {'success': False, 'message': 'Repository transfer initiated but not completed in time'}
    else:
        return {'success': False, 'message': f'Failed to move repository. Status: {transfer_response.status_code}, Response: {transfer_response.text}'}

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(json.dumps({'success': False, 'message': 'Required parameters: repo_id, source_org, target_org'}))
    else:
        repo_id, source_org, target_org = sys.argv[1], sys.argv[2], sys.argv[3]
        result = move_repository(repo_id, source_org, target_org)
        print(json.dumps(result))
