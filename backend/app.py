from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from scripts.list_repository_files import list_repository_files
from scripts.move_repository import move_repository
from scripts.remove_repository_from_github_by_url_repo import remove_repository_from_github_by_url_repo
from scripts.list_organizations import list_all_organizations
from scripts.list_repositories import list_repositories  # Make sure you have this script
from scripts.get_readme import get_readme_content

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route('/api/repository-files', methods=['GET'])
def get_repository_files():
    org = request.args.get('org')
    repo = request.args.get('repo')
    app.logger.info(f"Received request for files of org: {org}, repo: {repo}")
    if not org or not repo:
        app.logger.error("Organization or Repository parameter is missing")
        return jsonify({"error": "Both Organization and Repository parameters are required"}), 400
    
    try:
        app.logger.info(f"Fetching files for org: {org}, repo: {repo}")
        files = list_repository_files(org, repo)
        # Add 'name' property to each file dictionary
        files_with_names = [
            {**file, 'name': file['path'].split('/')[-1]}
            for file in files
        ]
        app.logger.info(f"Found {len(files_with_names)} files")
        return jsonify({"files": files_with_names})
    except Exception as e:
        app.logger.error(f"Error fetching repository files: {str(e)}")
        return jsonify({"error": "Failed to fetch repository files", "details": str(e)}), 500

@app.route('/api/readme', methods=['GET'])
def get_readme():
    org = request.args.get('org')
    repo = request.args.get('repo')
    app.logger.info(f"Received request for README of org: {org}, repo: {repo}")
    if not org or not repo:
        app.logger.error("Organization or Repository parameter is missing")
        return jsonify({"error": "Both Organization and Repository parameters are required"}), 400
    
    try:
        app.logger.info(f"Fetching README for org: {org}, repo: {repo}")
        content = get_readme_content(org, repo)
        app.logger.info(f"README content fetched successfully. Length: {len(content)}")
        return jsonify({"content": content})
    except Exception as e:
        app.logger.error(f"Error fetching README: {str(e)}", exc_info=True)
        return jsonify({"error": "Failed to fetch README", "details": str(e)}), 500

@app.route('/api/organizations', methods=['GET'])
def get_organizations():
    try:
        organizations = list_all_organizations()
        return jsonify(organizations)
    except Exception as e:
        print(f"Error fetching organizations: {str(e)}")
        return jsonify({"error": "Failed to fetch organizations"}), 500

@app.route('/api/repositories', methods=['GET'])
def get_repositories():
    org = request.args.get('org')
    app.logger.info(f"Received request for repositories of org: {org}")
    if not org:
        app.logger.error("Organization parameter is missing")
        return jsonify({"error": "Organization parameter is required"}), 400
    
    try:
        app.logger.info(f"Fetching repositories for org: {org}")
        repos = list_repositories(org)
        app.logger.info(f"Found {len(repos)} repositories")
        return jsonify(repos)
    except Exception as e:
        app.logger.error(f"Error fetching repositories: {str(e)}")
        return jsonify({"error": "Failed to fetch repositories", "details": str(e)}), 500

@app.route('/api/move-repository', methods=['POST'])
def move_repo():
    data = request.json
    repo_id = data.get('repoId')
    repo_name = data.get('repoName')
    source_org_id = data.get('sourceOrgId')
    target_org_id = data.get('targetOrgId')
    if not all([repo_id, repo_name, source_org_id, target_org_id]):
        return jsonify({'error': 'Missing required parameters', 'received': data}), 400
    try:
        result = move_repository(repo_id, repo_name, source_org_id, target_org_id)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error moving repository: {str(e)}")
        return jsonify({"error": "Failed to move repository", "details": str(e)}), 500

@app.route('/api/remove-repository', methods=['POST'])
def remove_repo():
    data = request.json
    repo_url = data.get('repoUrl')
    source_org_id = data.get('sourceOrgId')
    if not all([repo_url, source_org_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    try:
        result = remove_repository_from_github_by_url_repo(repo_url, source_org_id)
        return jsonify(result)
    except FileNotFoundError as e:
        app.logger.error(f"File not found error: {str(e)}")
        return jsonify({"error": "Failed to remove repository", "details": "Required script not found"}), 500
    except Exception as e:
        app.logger.error(f"Error removing repository: {str(e)}")
        return jsonify({"error": "Failed to remove repository", "details": str(e)}), 500

@app.route('/api/repo', methods=['POST'])
def set_repo():
    data = request.json
    org = data.get('org')
    repo = data.get('repo')
    if not org or not repo:
        return jsonify({"error": "Both 'org' and 'repo' are required"}), 400
    
    # Update the environment variables
    os.environ['GITHUB_ORG'] = org
    os.environ['GITHUB_REPO'] = repo
    
    # Update the .env file
    update_env_file('GITHUB_ORG', org)
    update_env_file('GITHUB_REPO', repo)
    
    return jsonify({"message": "Repository information updated successfully"})

@app.route('/api/repo', methods=['GET'])
def get_repo():
    org = os.getenv('GITHUB_ORG', '')
    repo = os.getenv('GITHUB_REPO', '')
    return jsonify({"org": org, "repo": repo})

def update_env_file(key, value):
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    with open(env_path, 'r') as file:
        lines = file.readlines()
    
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break
    
    if not updated:
        lines.append(f"{key}={value}\n")
    
    with open(env_path, 'w') as file:
        file.writelines(lines)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
