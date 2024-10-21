from github import Github
import os
import time
from github.GithubException import RateLimitExceededException
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = int(os.getenv('MAX_RETRIES', 5))
INITIAL_DELAY = int(os.getenv('INITIAL_DELAY', 1))
ORG_PAGINATION_SIZE = int(os.getenv('ORG_PAGINATION_SIZE', 20))

def update_all_organizations():
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    page = 1

    while True:
        for attempt in range(MAX_RETRIES):
            try:
                user = g.get_user()
                organizations = user.get_orgs().get_page(page - 1)
                org_list = []
                for org in organizations:
                    repos = org.get_repos()
                    public_repos = org.public_repos
                    private_repos = sum(1 for repo in repos if repo.private)
                    forked_repos = sum(1 for repo in repos if repo.fork)
                    total_repos = public_repos + private_repos

                    org_list.append({
                        'id': org.id,
                        'name': org.name,
                        'login': org.login,
                        'public_repos': public_repos,
                        'private_repos': private_repos,
                        'forked_repos': forked_repos,
                        'total_repos': total_repos
                    })
                
                yield org_list

                if len(org_list) < ORG_PAGINATION_SIZE:
                    return
                
                page += 1
                break
            except RateLimitExceededException as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                delay = INITIAL_DELAY * (2 ** attempt)
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
            except Exception as e:
                raise e

def list_repositories(org):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        organization = g.get_organization(org)
        repos = organization.get_repos()
        return [repo.raw_data for repo in repos]
    except Exception as e:
        raise e
