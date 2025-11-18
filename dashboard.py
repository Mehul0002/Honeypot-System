import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import subprocess
import threading
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from db import get_sessions, get_commands, get_login_attempts
from charts import create_ip_chart, create_login_attempts_chart
import csv

class HoneypotDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Honeypot Dashboard")
        self.root.geometry("1200x800")

        # Create tabs
        self.tab_control = ttk.Notebook(root)
        self.tab_dashboard = ttk.Frame(self.tab_control)
        self.tab_logs = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_dashboard, text='Dashboard')
        self.tab_control.add(self.tab_logs, text='Logs')
        self.tab_control.pack(expand=1, fill="both")

        # Dashboard tab
        self.create_dashboard_tab()

        # Logs tab
        self.create_logs_tab()

        # Start update thread
        self.update_thread = threading.Thread(target=self.update_data, daemon=True)
        self.update_thread.start()

    def create_dashboard_tab(self):
        # Buttons
        button_frame = ttk.Frame(self.tab_dashboard)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(button_frame, text="Start Honeypot", command=self.start_honeypot).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="Stop Honeypot", command=self.stop_honeypot).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="Parse Logs", command=self.parse_logs).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(button_frame, text="Export Logs", command=self.export_logs).pack(side=tk.LEFT, padx=5, pady=5)

        # Stats
        stats_frame = ttk.Frame(self.tab_dashboard)
        stats_frame.pack(side=tk.TOP, fill=tk.X)

        self.sessions_label = ttk.Label(stats_frame, text="Total Sessions: 0")
        self.sessions_label.pack(side=tk.LEFT, padx=10)

        self.attempts_label = ttk.Label(stats_frame, text="Login Attempts: 0")
        self.attempts_label.pack(side=tk.LEFT, padx=10)

        # Lists
        list_frame = ttk.Frame(self.tab_dashboard)
        list_frame.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(list_frame, text="Attacker IPs:").pack()
        self.ip_list = tk.Listbox(list_frame, height=10)
        self.ip_list.pack(fill=tk.BOTH, expand=True)

        ttk.Label(list_frame, text="Recent Commands:").pack()
        self.cmd_list = tk.Listbox(list_frame, height=10)
        self.cmd_list.pack(fill=tk.BOTH, expand=True)

        # Charts
        chart_frame = ttk.Frame(self.tab_dashboard)
        chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.ip_chart_frame = ttk.Frame(chart_frame)
        self.ip_chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        create_ip_chart(self.ip_chart_frame)

        self.attempts_chart_frame = ttk.Frame(chart_frame)
        self.attempts_chart_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        create_login_attempts_chart(self.attempts_chart_frame)

    def create_logs_tab(self):
        self.log_text = scrolledtext.ScrolledText(self.tab_logs)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self.tab_logs, text="Refresh Logs", command=self.refresh_logs).pack(side=tk.BOTTOM)

    def start_honeypot(self):
        subprocess.run(["docker-compose", "up", "-d"], cwd="..")

    def stop_honeypot(self):
        subprocess.run(["docker-compose", "down"], cwd="..")

    def parse_logs(self):
        subprocess.run(["python", "backend/parse_logs.py"], cwd="..")

    def export_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['IP', 'Timestamp', 'Username', 'Password', 'Success'])
                for attempt in get_login_attempts():
                    writer.writerow(attempt[1:])  # Skip id

    def update_data(self):
        while True:
            sessions = get_sessions()
            attempts = get_login_attempts()
            commands = get_commands()

            # Update labels
            self.sessions_label.config(text=f"Total Sessions: {len(sessions)}")
            self.attempts_label.config(text=f"Login Attempts: {len(attempts)}")

            # Update lists
            self.ip_list.delete(0, tk.END)
            ips = set(session[1] for session in sessions)
            for ip in ips:
                self.ip_list.insert(tk.END, ip)

            self.cmd_list.delete(0, tk.END)
            for cmd in commands[-10:]:  # Last 10 commands
                self.cmd_list.insert(tk.END, cmd[3])  # command text

            time.sleep(5)  # Update every 5 seconds

    def refresh_logs(self):
        self.log_text.delete(1.0, tk.END)
        try:
            with open("../logs/cowrie/cowrie.log", 'r') as f:
                self.log_text.insert(tk.END, f.read())
        except FileNotFoundError:
            self.log_text.insert(tk.END, "Log file not found.")
