import csv
import os
from datetime import datetime

LOG_FILE = 'repository_removals.csv'

def log_repository_remove(repo_url, source_org):
    file_exists = os.path.isfile(LOG_FILE)
    
    with open(LOG_FILE, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'repo_url', 'source_org']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'timestamp': datetime.now().isoformat(),
            'repo_url': repo_url,
            'source_org': source_org
        })

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: python log_repository_remove.py <repo_url> <source_org>")
    else:
        log_repository_remove(sys.argv[1], sys.argv[2])
