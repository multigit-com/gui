import sys
import json
import requests
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def list_all_organizations():
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        logger.error("GITHUB_TOKEN not found in environment variables")
        return {'organizations': [], 'error': 'GitHub token not found'}

    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = 'https://api.github.com/user/orgs'
    all_orgs = []
    page = 1

    while True:
        try:
            response = requests.get(f'{url}?page={page}&per_page=100', headers=headers)
            response.raise_for_status()
            orgs = response.json()
            if not orgs:
                break

            all_orgs.extend(orgs)
            page += 1
        except requests.RequestException as e:
            logger.error(f"Error fetching organizations: {e}")
            return {'organizations': [], 'error': str(e)}

    if not all_orgs:
        logger.warning("No organizations found for the user")

    sorted_orgs = sorted([{'id': org['login'], 'name': org['login']} for org in all_orgs], key=lambda x: x['name'].lower())
    return {'organizations': sorted_orgs}

if __name__ == '__main__':
    result = list_all_organizations()
    print(json.dumps(result))
