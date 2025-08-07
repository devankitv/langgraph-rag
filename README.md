# Stock Market LangGraph RAG Agent

A modern chat interface for querying Stock Market Performance data using LangGraph, FastAPI, and React + Vite frontend.

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
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd src/frontend
npm install
cd ../..
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

2. **Start the React frontend:**
   ```bash
   cd src/frontend
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173 (Vite dev server)
   - Backend API: http://localhost:8000

## Architecture

### Backend (FastAPI + LangGraph)
- **RAG Agent**: LangGraph-based retrieval-augmented generation
- **Vector Store**: ChromaDB with OpenAI embeddings
- **Knowledge Base**: Stock Market Performance 2024 PDF
- **API**: FastAPI with CORS support

### Frontend (React + Vite + TypeScript)
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite for fast development and building
- **UI Components**: Custom components with Tailwind CSS
- **Assistant UI**: @assistant-ui/react for chat interface
- **Styling**: Tailwind CSS with class-variance-authority
- **Icons**: Lucide React icons
- **Animations**: Framer Motion

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
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── assistant-ui/ # Chat interface components
│   │   │   │   │   ├── thread.tsx
│   │   │   │   │   ├── retriever-tool-ui.tsx
│   │   │   │   │   ├── markdown-text.tsx
│   │   │   │   │   └── tool-fallback.tsx
│   │   │   │   └── ui/          # Reusable UI components
│   │   │   ├── App.tsx          # Main React component
│   │   │   ├── main.tsx         # React entry point
│   │   │   └── MyRuntimeProvider.tsx
│   │   ├── public/              # Static assets
│   │   ├── package.json         # Frontend dependencies
│   │   ├── vite.config.ts       # Vite configuration
│   │   └── tsconfig.json        # TypeScript configuration
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

### Frontend Features
- Modern React 19 with TypeScript
- Vite for fast development and building
- Tailwind CSS for styling
- Assistant UI components for chat interface
- Responsive design
- Real-time chat interface
- Markdown rendering for responses
- Tool integration UI

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

## Development

### Frontend Development
```bash
cd src/frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Backend Development
```bash
# Activate virtual environment
source venv/bin/activate

# Run backend
cd src/backend/api
python3 main.py
```