"""
Application settings and configuration.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent.parent

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
API_DEBUG = True

# Frontend Settings
FRONTEND_HOST = ""  # Empty string to bind to all interfaces
FRONTEND_PORT = 3000

# OpenAI Settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector Store Settings
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# Data Settings
DATA_DIR = BASE_DIR / "src" / "data"
PDF_PATH = DATA_DIR / "Stock_Market_Performance_2024.pdf"

# CORS Settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
] 