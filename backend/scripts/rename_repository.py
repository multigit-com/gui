from github import Github
import os

def rename_repository_script(org_name, old_name, new_name):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        org = g.get_organization(org_name)
        repo = org.get_repo(old_name)
        repo.edit(name=new_name)
        return {"success": True, "message": f"Repository renamed from {old_name} to {new_name}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        print("Usage: python rename_repository.py <org_name> <old_name> <new_name>")
    else:
        org_name = sys.argv[1]
        old_name = sys.argv[2]
        new_name = sys.argv[3]
        result = rename_repository_script(org_name, old_name, new_name)
        print(result)
