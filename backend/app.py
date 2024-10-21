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
    repo = request.args.get('repo')
    app.logger.info(f"Received request for files of repo: {repo}")
    if not repo:
        app.logger.error("Repository parameter is missing")
        return jsonify({"error": "Repository parameter is required"}), 400
    
    try:
        app.logger.info(f"Fetching files for repo: {repo}")
        files = list_repository_files(repo)
        app.logger.info(f"Found {len(files)} files")
        return jsonify({"files": files})
    except Exception as e:
        app.logger.error(f"Error fetching repository files: {str(e)}")
        return jsonify({"error": "Failed to fetch repository files", "details": str(e)}), 500

@app.route('/api/readme', methods=['GET'])
def get_readme():
    repo = request.args.get('repo')
    app.logger.info(f"Received request for README of repo: {repo}")
    if not repo:
        app.logger.error("Repository parameter is missing")
        return jsonify({"error": "Repository parameter is required"}), 400
    
    try:
        app.logger.info(f"Fetching README for repo: {repo}")
        content = get_readme_content(repo)
        return jsonify({"content": content})
    except Exception as e:
        app.logger.error(f"Error fetching README: {str(e)}")
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
    source_org_id = data.get('sourceOrgId')
    target_org_id = data.get('targetOrgId')
    if not all([repo_id, source_org_id, target_org_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    result = move_repository(repo_id, source_org_id, target_org_id)
    return jsonify(result)

@app.route('/api/remove-repository', methods=['POST'])
def remove_repo():
    data = request.json
    repo_url = data.get('repoUrl')
    source_org_id = data.get('sourceOrgId')
    if not all([repo_url, source_org_id]):
        return jsonify({'error': 'Missing required parameters'}), 400
    result = remove_repository_from_github_by_url_repo(repo_url, source_org_id)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
