# Stock Market LangGraph RAG Agent

A modern chat interface for querying Stock Market Performance data using LangGraph, FastAPI, and a simple HTML frontend.

Repository: https://github.com/devankitv/langgraph-rag.git

## Setup and Installation

### Step 1: Clone and Navigate
```bash
git clone https://github.com/devankitv/langgraph-rag.git
cd langgraph-rag
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the root directory:
```bash
# Create .env file
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Quick Start

### Option 1: Use the startup script (Recommended)
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Run the application
python3 main.py
```

### Option 2: Manual setup

1. **Start the FastAPI backend:**
   ```bash
   cd src/backend/api
   python3 main.py
   ```

2. **Start the frontend server:**
   ```bash
   cd src/frontend
   python3 server.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Architecture

### Backend (FastAPI + LangGraph)
- **RAG Agent**: LangGraph-based retrieval-augmented generation
- **Vector Store**: ChromaDB with OpenAI embeddings
- **Knowledge Base**: Stock Market Performance 2024 PDF
- **API**: FastAPI with CORS support

### Frontend (Simple HTML + JavaScript)
- **UI**: Clean HTML interface with JavaScript

## Project Structure

```
langgraph-rag/
├── src/
│   ├── backend/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── main.py          # FastAPI application
│   │   └── __init__.py
│   ├── frontend/
│   │   ├── templates/
│   │   │   └── index.html       # Main chat interface
│   │   ├── static/              # Static assets
│   │   ├── server.py            # HTTP server
│   │   └── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── rag_agent.py         # LangGraph RAG agent
│   ├── config/
│   │   └── settings.py          # Application configuration
│   ├── data/
│   │   └── Stock_Market_Performance_2024.pdf
│   ├── docs/
│   │   └── tutorials/           # Documentation and tutorials
│   ├── scripts/
│   │   └── start_app.py         # Startup script
│   └── __init__.py
├── vectorstore/                  # ChromaDB vector store
├── venv/                        # Virtual environment
├── main.py                      # Main entry point
├── requirements.txt              # Python dependencies
└── README.md
```

## Features

### Backend Features
- LangGraph-based RAG agent
- ChromaDB vector store
- OpenAI embeddings and GPT-4
- PDF document processing
- FastAPI REST API


### Adding New Documents
1. Place PDF files in `src/data/`
2. Update the `pdf_path` in `src/config/settings.py`
3. Restart the backend

### POST /query
Query the RAG agent with a question.

**Request:**
```json
{
  "question": "What were the top performing stocks in 2024?"
}
```

**Response:**
```json
{
  "answer": "Based on the Stock Market Performance 2024 data...",
  "success": true,
  "error": null
}
```