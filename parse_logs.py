import json
import os
from datetime import datetime
from db import create_db, insert_session, insert_command, insert_login_attempt

LOG_DIR = '../logs/cowrie'

def parse_json_log(file_path):
    """Parse Cowrie JSON log file."""
    if not os.path.exists(file_path):
        print(f"Log file {file_path} does not exist.")
        return

    with open(file_path, 'r') as f:
        for line in f:
            try:
                log_entry = json.loads(line.strip())
                process_log_entry(log_entry)
            except json.JSONDecodeError:
                continue

def process_log_entry(entry):
    """Process a single log entry."""
    event_type = entry.get('eventid')

    if event_type == 'cowrie.session.connect':
        # New session
        ip = entry.get('src_ip')
        start_time = entry.get('timestamp')
        protocol = entry.get('protocol', 'ssh')
        session_id = insert_session(ip, start_time, None, None, protocol)
        # Store session_id for later use, perhaps in a dict

    elif event_type == 'cowrie.session.closed':
        # Session closed
        # Update session with end_time and duration
        # For simplicity, assume we have session_id from connect
        pass  # Need to track sessions properly

    elif event_type == 'cowrie.command.input':
        # Command input
        session_id = entry.get('session')  # Assuming session ID is available
        timestamp = entry.get('timestamp')
        command = entry.get('input')
        insert_command(session_id, timestamp, command)

    elif event_type == 'cowrie.login.success' or event_type == 'cowrie.login.failed':
        # Login attempt
        ip = entry.get('src_ip')
        timestamp = entry.get('timestamp')
        username = entry.get('username')
        password = entry.get('password')
        success = 1 if event_type == 'cowrie.login.success' else 0
        insert_login_attempt(ip, timestamp, username, password, success)

def main():
    create_db()
    json_log_path = os.path.join(LOG_DIR, 'cowrie.json')
    parse_json_log(json_log_path)
    print("Logs parsed and stored in database.")

if __name__ == '__main__':
    main()
