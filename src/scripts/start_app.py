#!/usr/bin/env python3
"""
Startup script to run both the FastAPI backend and React+Vite frontend.
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
    """Run the React+Vite frontend development server"""
    print("Starting React+Vite frontend development server...")
    frontend_path = Path(__file__).parent.parent / "frontend"
    
    # Check if node_modules exists, if not run npm install
    node_modules_path = frontend_path / "node_modules"
    if not node_modules_path.exists():
        print("Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
    
    # Start the Vite development server
    subprocess.run(["npm", "run", "dev"], cwd=frontend_path)

def main():
    print("Starting Stock Market LangGraph RAG Agent Application")
    print("=" * 50)
    
    # Check if required files exist
    api_file = Path(__file__).parent.parent / "backend" / "api" / "main.py"
    frontend_package_json = Path(__file__).parent.parent / "frontend" / "package.json"
    frontend_vite_config = Path(__file__).parent.parent / "frontend" / "vite.config.ts"
    
    if not api_file.exists():
        print("Error: API file not found at src/backend/api/main.py")
        return
    
    if not frontend_package_json.exists():
        print("Error: Frontend package.json not found at src/frontend/package.json")
        return
    
    if not frontend_vite_config.exists():
        print("Error: Frontend vite.config.ts not found at src/frontend/vite.config.ts")
        return
    
    print("All required files found")
    print("\nInstructions:")
    print("1. The FastAPI backend will run on http://localhost:8000")
    print("2. The React+Vite frontend will run on http://localhost:5173")
    print("3. Open your browser to http://localhost:5173 to use the application")
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
        time.sleep(5)  # Give more time for npm install if needed
        
        print("\nBoth servers are running!")
        print("Frontend: http://localhost:5173")
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