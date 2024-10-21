from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import sqlite3
import time
from dotenv import load_dotenv
from scripts.list_repository_files import list_repository_files
from scripts.move_repository import move_repository
from scripts.remove_repository_from_github_by_url_repo import remove_repository_from_github_by_url_repo
from scripts.list_organizations import list_all_organizations
from scripts.list_repositories import list_repositories
from scripts.get_readme import get_readme_content
from scripts.rename_organization import rename_organization_script
from scripts.rename_repository import rename_repository_script

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# SQLite setup
DB_PATH = os.getenv('DB_PATH', 'github_cache.db')
ORGANIZATIONS_TABLE = os.getenv('ORGANIZATIONS_TABLE', 'organizations')
REPOSITORIES_TABLE = os.getenv('REPOSITORIES_TABLE', 'repositories')
CACHE_DURATION = int(os.getenv('CACHE_DURATION', 300))

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {ORGANIZATIONS_TABLE}
                 (id INTEGER PRIMARY KEY, name TEXT, login TEXT, original_name TEXT, custom_name TEXT,
                  public_repos INTEGER, private_repos INTEGER, forked_repos INTEGER, total_repos INTEGER,
                  last_updated INTEGER)''')
    c.execute(f'''CREATE TABLE IF NOT EXISTS {REPOSITORIES_TABLE}
                 (id INTEGER PRIMARY KEY, name TEXT, org TEXT, html_url TEXT, description TEXT, last_updated INTEGER)''')
    conn.commit()
    conn.close()

init_db()

def cache_organizations(organizations):
    current_time = int(time.time())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Get the current table structure
    c.execute(f'PRAGMA table_info({ORGANIZATIONS_TABLE})')
    columns = [column[1] for column in c.fetchall()]
    
    # Prepare the SQL query
    placeholders = ', '.join(['?' for _ in columns])
    sql = f'INSERT OR REPLACE INTO {ORGANIZATIONS_TABLE} ({", ".join(columns)}) VALUES ({placeholders})'
    
    # Prepare the data
    data = []
    for org in organizations:
        row = [org.get(column, None) for column in columns]
        data.append(tuple(row))
    
    # Execute the query
    c.executemany(sql, data)
    conn.commit()
    conn.close()

def cache_repositories(org, repositories):
    current_time = int(time.time())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executemany(f'INSERT OR REPLACE INTO {REPOSITORIES_TABLE} VALUES (?, ?, ?, ?, ?, ?)',
                  [(repo['id'], repo['name'], org, repo['html_url'], repo.get('description', ''), current_time) for repo in repositories])
    conn.commit()
    conn.close()

def get_cached_organizations():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {ORGANIZATIONS_TABLE}')
    columns = [column[0] for column in c.description]
    orgs = []
    for row in c.fetchall():
        org = {}
        for i, column in enumerate(columns):
            org[column] = row[i]
        orgs.append(org)
    conn.close()
    return orgs

def get_cached_repositories(org):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'SELECT * FROM {REPOSITORIES_TABLE} WHERE org = ?', (org,))
    repos = [{'id': row[0], 'name': row[1], 'org': row[2], 'html_url': row[3], 'description': row[4], 'last_updated': row[5]} for row in c.fetchall()]
    conn.close()
    return repos

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
        cached_orgs = get_cached_organizations()
        current_time = int(time.time())
        if cached_orgs and (current_time - cached_orgs[0]['last_updated'] < CACHE_DURATION):
            return jsonify({"organizations": cached_orgs})
        
        organizations = list_all_organizations()
        app.logger.info(f"Fetched organizations: {organizations}")
        cache_organizations(organizations['organizations'])
        return jsonify(organizations)
    except Exception as e:
        app.logger.error(f"Error fetching organizations: {str(e)}", exc_info=True)
        cached_orgs = get_cached_organizations()
        if cached_orgs:
            return jsonify({"organizations": cached_orgs})
        return jsonify({"error": "Failed to fetch organizations", "details": str(e)}), 500

@app.route('/api/repositories', methods=['GET'])
def get_repositories():
    org = request.args.get('org')
    app.logger.info(f"Received request for repositories of org: {org}")
    if not org:
        app.logger.error("Organization parameter is missing")
        return jsonify({"error": "Organization parameter is required"}), 400
    
    try:
        cached_repos = get_cached_repositories(org)
        current_time = int(time.time())
        if cached_repos and (current_time - cached_repos[0]['last_updated'] < CACHE_DURATION):
            return jsonify(cached_repos)
        
        app.logger.info(f"Fetching repositories for org: {org}")
        repos = list_repositories(org)
        cache_repositories(org, repos)
        app.logger.info(f"Found {len(repos)} repositories")
        return jsonify(repos)
    except Exception as e:
        app.logger.error(f"Error fetching repositories: {str(e)}")
        cached_repos = get_cached_repositories(org)
        if cached_repos:
            return jsonify(cached_repos)
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
        if result.get('success'):
            # Update the cache for the organization
            org_data = list_all_organizations()
            cache_organizations(org_data['organizations'])
            
            # Update the cache for the repositories of this organization
            repos = list_repositories(source_org_id)
            cache_repositories(source_org_id, repos)
        
        return jsonify(result)
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

@app.route('/api/rename-organization', methods=['POST'])
def rename_organization():
    data = request.json
    org_id = data.get('orgId')
    new_name = data.get('newName')
    if not org_id or not new_name:
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        result = rename_organization_script(org_id, new_name)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error renaming organization: {str(e)}")
        return jsonify({"error": "Failed to rename organization", "details": str(e)}), 500

@app.route('/api/rename-repository', methods=['POST'])
def rename_repository():
    data = request.json
    org_name = data.get('orgName')
    old_name = data.get('oldName')
    new_name = data.get('newName')
    if not org_name or not old_name or not new_name:
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        result = rename_repository_script(org_name, old_name, new_name)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error renaming repository: {str(e)}")
        return jsonify({"error": "Failed to rename repository", "details": str(e)}), 500

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

# Add a new route to remove an organization
@app.route('/api/remove-organization', methods=['POST'])
def remove_org():
    data = request.json
    org_id = data.get('orgId')
    if not org_id:
        return jsonify({'error': 'Missing required parameter: orgId'}), 400
    try:
        # Implement the remove_organization function in a new script
        result = remove_organization(org_id)
        if result.get('success'):
            # Update the cache for all organizations
            org_data = list_all_organizations()
            cache_organizations(org_data['organizations'])
        
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error removing organization: {str(e)}")
        return jsonify({"error": "Failed to remove organization", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
