import sqlite3
import time
import os

DB_PATH = os.getenv('DB_PATH', 'github_cache.db')
ORGANIZATIONS_TABLE = os.getenv('ORGANIZATIONS_TABLE', 'organizations')
REPOSITORIES_TABLE = os.getenv('REPOSITORIES_TABLE', 'repositories')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {ORGANIZATIONS_TABLE}
                 (id INTEGER PRIMARY KEY, name TEXT, login TEXT,
                  public_repos INTEGER, private_repos INTEGER, forked_repos INTEGER, total_repos INTEGER,
                  last_updated INTEGER)''')
    c.execute(f'''CREATE TABLE IF NOT EXISTS {REPOSITORIES_TABLE}
                 (id INTEGER PRIMARY KEY, name TEXT, org TEXT, html_url TEXT, description TEXT, last_updated INTEGER)''')
    conn.commit()
    conn.close()

def cache_organizations(organizations):
    current_time = int(time.time())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(f'PRAGMA table_info({ORGANIZATIONS_TABLE})')
    columns = [column[1] for column in c.fetchall()]

    placeholders = ', '.join(['?' for _ in columns])
    sql = f'INSERT OR REPLACE INTO {ORGANIZATIONS_TABLE} ({", ".join(columns)}) VALUES ({placeholders})'

    data = []
    for org in organizations:
        row = [
            org.get('id'),
            org.get('name'),
            org.get('login'),
            org.get('public_repos'),
            org.get('private_repos'),
            org.get('forked_repos'),
            org.get('total_repos'),
            current_time  # last_updated
        ]
        data.append(tuple(row))

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
    c.execute(f'SELECT * FROM {ORGANIZATIONS_TABLE} ORDER BY login ASC')
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
    c.execute(f'SELECT * FROM {REPOSITORIES_TABLE} WHERE org = ? ORDER BY name ASC', (org,))
    repos = [{'id': row[0], 'name': row[1], 'org': row[2], 'html_url': row[3], 'description': row[4], 'last_updated': row[5]} for row in c.fetchall()]
    conn.close()
    return repos

def remove_repository_from_db(org, repo_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f'DELETE FROM {REPOSITORIES_TABLE} WHERE org = ? AND name = ?', (org, repo_name))
    conn.commit()
    conn.close()
