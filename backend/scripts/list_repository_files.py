from github import Github
import os
import json

def list_repository_files(org, repo):
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")

    g = Github(github_token)
    try:
        repository = g.get_repo(f"{org}/{repo}")
        contents = repository.get_contents("")
        files = []

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repository.get_contents(file_content.path))
            else:
                files.append({
                    "path": file_content.path,
                    "size": file_content.size,
                    "type": file_content.type
                })

        print(json.dumps(files))  # Print as JSON string
        return files
    except Exception as e:
        print(f"Error listing repository files: {str(e)}")
        raise

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python list_repository_files.py <org> <repo>")
    else:
        org = sys.argv[1]
        repo = sys.argv[2]
        list_repository_files(org, repo)
