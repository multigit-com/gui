import csv
import os
from datetime import datetime

LOG_FILE = 'repository_moves.csv'

def log_repository_move(repo_id, repo_name, source_org, target_org):
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'repo_id', 'repo_name', 'source_org', 'target_org']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'repo_id': repo_id,
            'repo_name': repo_name,
            'source_org': source_org,
            'target_org': target_org
        })

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 5:
        print("Usage: python log_repository_move.py <repo_id> <repo_name> <source_org> <target_org>")
    else:
        log_repository_move(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
