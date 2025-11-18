import sqlite3
import os

DB_PATH = 'honeypot.db'

def create_db():
    """Create the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for sessions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            start_time TEXT,
            end_time TEXT,
            duration REAL,
            protocol TEXT
        )
    ''')

    # Table for commands
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY,
            session_id INTEGER,
            timestamp TEXT,
            command TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions (id)
        )
    ''')

    # Table for login attempts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY,
            ip TEXT,
            timestamp TEXT,
            username TEXT,
            password TEXT,
            success INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def insert_session(ip, start_time, end_time, duration, protocol):
    """Insert a new session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sessions (ip, start_time, end_time, duration, protocol)
        VALUES (?, ?, ?, ?, ?)
    ''', (ip, start_time, end_time, duration, protocol))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def insert_command(session_id, timestamp, command):
    """Insert a command for a session."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO commands (session_id, timestamp, command)
        VALUES (?, ?, ?)
    ''', (session_id, timestamp, command))
    conn.commit()
    conn.close()

def insert_login_attempt(ip, timestamp, username, password, success):
    """Insert a login attempt."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO login_attempts (ip, timestamp, username, password, success)
        VALUES (?, ?, ?, ?, ?)
    ''', (ip, timestamp, username, password, success))
    conn.commit()
    conn.close()

def get_sessions():
    """Get all sessions."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_commands():
    """Get all commands."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM commands')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_login_attempts():
    """Get all login attempts."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM login_attempts')
    rows = cursor.fetchall()
    conn.close()
    return rows
