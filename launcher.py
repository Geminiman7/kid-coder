import os
import sys
import threading
import time
import webview
import subprocess
import socket

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_server():
    """Start Django development server"""
    # Prevent multiple runs
    if not is_port_in_use(8000):
        subprocess.Popen([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"], shell=False)
    else:
        print("Server already running on port 8000")

def open_app():
    """Open the desktop app window"""
    time.sleep(4)  # Wait a bit for server startup
    webview.create_window(
        title="My Learning App",
        url="http://127.0.0.1:8000/",
        width=1200,
        height=800,
        resizable=True
    )
    webview.start()

if __name__ == "__main__":
    # Prevent recursive execution when frozen
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    # Run server in background thread only once
    threading.Thread(target=run_server, daemon=True).start()
    open_app()
