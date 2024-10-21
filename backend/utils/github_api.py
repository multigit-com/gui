from github import Github
import os
import time

def update_all_organizations(max_retries=3, delay=5):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    page = 1
    ORG_PAGINATION_SIZE = int(os.getenv('ORG_PAGINATION_SIZE', 20))

    for attempt in range(max_retries):
        try:
            while True:
                user = g.get_user()
                organizations = user.get_orgs().get_page(page - 1)
                org_list = []
                for org in organizations:
                    repos = org.get_repos()
                    public_repos = org.public_repos
                    private_repos = sum(1 for repo in repos if repo.private)
                    forked_repos = sum(1 for repo in repos if repo.fork)
                    total_repos = public_repos + private_repos

                    custom_name = os.getenv(f'CUSTOM_ORG_NAME_{org.login}', org.name)

                    org_list.append({
                        'id': org.id,
                        'name': org.name,
                        'login': org.login,
                        'original_name': org.name,
                        'custom_name': custom_name,
                        'public_repos': public_repos,
                        'private_repos': private_repos,
                        'forked_repos': forked_repos,
                        'total_repos': total_repos
                    })
                
                yield org_list

                if len(org_list) < ORG_PAGINATION_SIZE:
                    break
                
                page += 1
                time.sleep(1)  # To avoid hitting rate limits
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
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
