import os
import sys
import json
from github import Github

def remove_repository_from_github_by_url_repo(repo_url, source_org_id):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        # Extract repo name from URL
        repo_name = repo_url.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        # Get the repository
        repo = g.get_repo(f"{source_org_id}/{repo_name}")

        # Delete the repository
        repo.delete()

        # Log the removal (without using an external script)
        log_message = f"Repository {repo_url} removed from {source_org_id}"
        print(log_message)  # Print to console
        # You can add more logging here if needed

        return {"success": True, "message": log_message}
    except Exception as e:
        error_message = f"Error removing repository: {str(e)}"
        print(error_message)  # Print to console
        return {"success": False, "error": error_message}

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python remove_repository_from_github_by_url_repo.py <repo_url> <source_org_id>")
    else:
        repo_url = sys.argv[1]
        source_org_id = sys.argv[2]
        result = remove_repository_from_github_by_url_repo(repo_url, source_org_id)
        print(json.dumps(result))
