#!/usr/bin/env python3
"""
Startup script to run both the FastAPI backend and frontend server.
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

def run_api():
    """Run the FastAPI backend server"""
    print("Starting FastAPI backend server...")
    api_path = Path(__file__).parent.parent / "backend" / "api" / "main.py"
    subprocess.run([sys.executable, str(api_path)], cwd=Path(__file__).parent.parent.parent)

def run_frontend():
    """Run the frontend HTTP server"""
    print("Starting frontend server...")
    frontend_path = Path(__file__).parent.parent / "frontend" / "server.py"
    subprocess.run([sys.executable, str(frontend_path)], cwd=Path(__file__).parent.parent.parent)

def main():
    print("Starting Stock Market LangGraph RAG Agent Application")
    print("=" * 50)
    
    # Check if required files exist
    api_file = Path(__file__).parent.parent / "backend" / "api" / "main.py"
    frontend_file = Path(__file__).parent.parent / "frontend" / "server.py"
    html_file = Path(__file__).parent.parent / "frontend" / "templates" / "index.html"
    
    if not api_file.exists():
        print("Error: API file not found at src/backend/api/main.py")
        return
    
    if not frontend_file.exists():
        print("Error: Frontend server file not found at src/frontend/server.py")
        return
    
    if not html_file.exists():
        print("Error: Frontend HTML file not found at src/frontend/templates/index.html")
        return
    
    print("All required files found")
    print("\nInstructions:")
    print("1. The FastAPI backend will run on http://localhost:8000")
    print("2. The frontend will run on http://localhost:3000")
    print("3. Open your browser to http://localhost:3000 to use the application")
    print("4. Press Ctrl+C to stop both servers")
    print("\n" + "=" * 50)
    
    # Start both servers in separate threads
    api_thread = threading.Thread(target=run_api, daemon=True)
    frontend_thread = threading.Thread(target=run_frontend, daemon=True)
    
    try:
        # Start the API server first
        api_thread.start()
        print("Waiting for API server to start...")
        time.sleep(3)
        
        # Start the frontend server
        frontend_thread.start()
        print("Waiting for frontend server to start...")
        time.sleep(2)
        
        print("\nBoth servers are running!")
        print("Frontend: http://localhost:3000")
        print("API: http://localhost:8000")
        print("API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop both servers...")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0)

if __name__ == "__main__":
    main() 