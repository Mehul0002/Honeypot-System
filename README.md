# Honeypot System

A complete honeypot system using Cowrie, Docker, Python backend, and Tkinter GUI.

## Features

- Cowrie-based SSH/Telnet honeypot in Docker
- Log parsing and storage in SQLite database
- GUI dashboard with real-time updates, charts, and controls
- Export logs to CSV

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- matplotlib (install via pip)

## Installation

1. Clone or download the project.
2. Navigate to the `honeypot-system` directory.
3. Install Python dependencies: `pip install -r backend/requirements.txt`

## Running the Honeypot

1. Start the honeypot: In the GUI, click "Start Honeypot" or run `docker-compose up -d`
2. The honeypot will listen on ports 2222 (SSH) and 23 (Telnet).

## Using the GUI

1. Run `python gui/main.py`
2. Dashboard shows stats, attacker IPs, recent commands, and charts.
3. Use buttons to start/stop honeypot, parse logs, view logs, export to CSV.

## Log Parsing

- Logs are stored in `logs/cowrie/`
- Run parse_logs.py to process logs into the database.

## Attacker Profiling

- View IPs, commands, and login attempts in the GUI.
- Charts show IP distribution and attempts over time.

## Notes

- Ensure Docker is running before starting the honeypot.
- Logs are mounted from container to host for easy access.
