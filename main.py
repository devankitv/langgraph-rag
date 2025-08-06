#!/usr/bin/env python3
"""
Main entry point for the Stock Market RAG Agent application.
"""

import sys
from pathlib import Path

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.scripts.start_app import main

if __name__ == "__main__":
    main() 