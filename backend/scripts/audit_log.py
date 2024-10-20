import os
import sys
import json
from datetime import datetime
from log_utils import setup_logger

logger = setup_logger('audit_log')

AUDIT_LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'audit_log.json')

def log_action(action, details):
    logger.info(f"Logging action: {action}, details: {details}")
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'details': details
    }
    
    try:
        with open(AUDIT_LOG_FILE, 'r+') as f:
            try:
                log = json.load(f)
            except json.JSONDecodeError:
                logger.warning("Existing audit log is empty or invalid JSON. Starting a new log.")
                log = []
            log.append(log_entry)
            f.seek(0)
            json.dump(log, f, indent=2)
        logger.info("Action logged successfully")
    except FileNotFoundError:
        logger.warning(f"Audit log file not found. Creating a new file at {AUDIT_LOG_FILE}")
        with open(AUDIT_LOG_FILE, 'w') as f:
            json.dump([log_entry], f, indent=2)
        logger.info("Action logged successfully in new file")

def get_audit_log():
    logger.info("Retrieving audit log")
    try:
        with open(AUDIT_LOG_FILE, 'r') as f:
            log = json.load(f)
        logger.info(f"Retrieved {len(log)} log entries")
        return log
    except FileNotFoundError:
        logger.warning(f"Audit log file not found at {AUDIT_LOG_FILE}")
        return []

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logger.info("No arguments provided. Retrieving full audit log.")
        print(json.dumps(get_audit_log(), indent=2))
    else:
        action = sys.argv[1]
        details = ' '.join(sys.argv[2:])
        logger.info(f"Logging action: {action}, details: {details}")
        log_action(action, details)
        print(f"Action '{action}' logged successfully.")
