import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from db import get_sessions, get_login_attempts

def create_ip_chart(canvas_frame):
    """Create a bar chart of attacker IPs."""
    sessions = get_sessions()
    ip_counts = {}
    for session in sessions:
        ip = session[1]  # ip is second column
        ip_counts[ip] = ip_counts.get(ip, 0) + 1

    fig, ax = plt.subplots()
    ax.bar(ip_counts.keys(), ip_counts.values())
    ax.set_xlabel('IP Address')
    ax.set_ylabel('Number of Sessions')
    ax.set_title('Attacker IP Distribution')

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def create_login_attempts_chart(canvas_frame):
    """Create a line chart of login attempts over time."""
    attempts = get_login_attempts()
    if not attempts:
        # No data, show empty chart
        fig, ax = plt.subplots()
        ax.set_title('No Login Attempts Data')
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        return

    from datetime import datetime
    timestamps = [datetime.fromisoformat(att[2]) for att in attempts]  # timestamp is third column
    # For simplicity, count per day
    from collections import Counter
    dates = [ts.date() for ts in timestamps]
    date_counts = Counter(dates)

    fig, ax = plt.subplots()
    ax.plot(list(date_counts.keys()), list(date_counts.values()))
    ax.set_xlabel('Date')
    ax.set_ylabel('Login Attempts')
    ax.set_title('Login Attempts Over Time')

    canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
