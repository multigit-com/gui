import os
import sys
import json
from github import Github

def remove_organization(org_id):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        # Get the organization
        org = g.get_organization(org_id)

        # Delete all repositories in the organization
        for repo in org.get_repos():
            repo.delete()

        # Note: GitHub API doesn't provide a direct way to delete an organization
        # You might need to implement this part manually or through GitHub's web interface

        return {"success": True, "message": f"All repositories in organization {org_id} have been removed"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python remove_organization.py <org_id>")
    else:
        org_id = sys.argv[1]
        result = remove_organization(org_id)
        print(json.dumps(result))
