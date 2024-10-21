from github import Github
import os

def rename_organization_script(org_id, new_name):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        org = g.get_organization(org_id)
        org.edit(new_name)
        return {"success": True, "message": f"Organization renamed to {new_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python rename_organization.py <org_id> <new_name>")
    else:
        org_id = sys.argv[1]
        new_name = sys.argv[2]
        result = rename_organization_script(org_id, new_name)
        print(result)
