#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend HTML file.
Run this to serve the frontend on http://localhost:3000
"""

import http.server
import socketserver
import os
import webbrowser
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config.settings import FRONTEND_HOST, FRONTEND_PORT

# Change to the templates directory
templates_dir = Path(__file__).parent / "templates"
os.chdir(templates_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    try:
        with socketserver.TCPServer((FRONTEND_HOST, FRONTEND_PORT), MyHTTPRequestHandler) as httpd:
            print(f"Frontend server running at http://localhost:{FRONTEND_PORT}")
            print("Press Ctrl+C to stop the server")
            
            # Open browser automatically
            webbrowser.open(f'http://localhost:{FRONTEND_PORT}')
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server...")
                httpd.shutdown()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Error: Port {FRONTEND_PORT} is already in use.")
            print("Please stop any existing server on this port and try again.")
        else:
            print(f"Error starting server: {e}") 