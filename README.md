# Stock Market LangGraph RAG Agent

A modern chat interface for querying Stock Market Performance data using LangGraph, FastAPI, and React + Vite frontend with real-time streaming capabilities.

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

### Client-Server Architecture

The application follows a modern client-server architecture with the following components:

**Frontend (Client):**
- React 19 with TypeScript and Vite
- Assistant UI framework for chat interface
- Real-time streaming with Server-Sent Events (SSE)
- Tailwind CSS for styling
- Responsive design with modern UI components

**Backend (Server):**
- FastAPI with async support
- LangGraph for RAG agent orchestration
- ChromaDB vector store with OpenAI embeddings
- Streaming responses with proper CORS handling
- PDF document processing and chunking

**Communication:**
- RESTful API endpoints for different use cases
- Server-Sent Events (SSE) for real-time streaming
- JSON-based message format
- CORS-enabled for cross-origin requests

### API Endpoints

The backend provides three main API endpoints:

#### 1. POST /query
Standard query endpoint that returns complete response with tool calls and results.

**Request:**
```json
{
  "question": "What were the top performing stocks in 2024?"
}
```

**Response:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": [{"type": "text", "text": "What were the top performing stocks in 2024?"}]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "tool-call",
          "toolCallId": "call_123",
          "toolName": "retriever_tool",
          "args": {"query": "top performing stocks 2024"}
        }
      ]
    },
    {
      "role": "tool",
      "content": [
        {
          "type": "tool-result",
          "toolCallId": "call_123",
          "result": {"result": "Document content..."}
        }
      ]
    },
    {
      "role": "assistant",
      "content": [{"type": "text", "text": "Based on the data..."}]
    }
  ],
  "success": true,
  "error": null
}
```

#### 2. POST /stream
Basic streaming endpoint for simple text streaming.

**Request:**
```json
{
  "question": "What were the top performing stocks in 2024?"
}
```

**Response:** Server-Sent Events stream
```
data: [Tool Call: retriever_tool] 
data: In 2024, the S&P 500 index delivered...
data: [DONE]
```

#### 3. POST /stream-with-tools
Advanced streaming endpoint with detailed tool call and result information.

**Request:**
```json
{
  "question": "What were the top performing stocks in 2024?"
}
```

**Response:** Server-Sent Events stream with structured data
```
data: {"type": "tool_call", "data": {"id": "call_123", "name": "retriever_tool", "args": {"query": "top performing stocks 2024"}}}
data: {"type": "tool_result", "data": {"toolCallId": "call_123", "result": "Document content..."}}
data: {"type": "text", "data": "In 2024, the S&P 500..."}
data: [DONE]
```

### Backend (FastAPI + LangGraph)
- **RAG Agent**: LangGraph-based retrieval-augmented generation with streaming support
- **Vector Store**: ChromaDB with OpenAI embeddings for document retrieval
- **Knowledge Base**: Stock Market Performance 2024 PDF with automatic chunking
- **API**: FastAPI with CORS support and multiple streaming endpoints
- **Tool Integration**: Built-in retriever tool for document search
- **Streaming**: Real-time response streaming with tool call visibility

### Frontend (React + Vite + TypeScript)
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite for fast development and building
- **UI Components**: Custom components with Tailwind CSS
- **Assistant UI**: @assistant-ui/react for modern chat interface
- **Streaming**: Real-time text streaming with tool call display
- **Styling**: Tailwind CSS with class-variance-authority
- **Icons**: Lucide React icons
- **Animations**: Framer Motion for smooth transitions

## Project Structure

```
langgraph-rag/
├── src/
│   ├── backend/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── main.py          # FastAPI application with streaming endpoints
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
│   │   │   └── MyRuntimeProvider.tsx # Streaming adapter
│   │   ├── public/              # Static assets
│   │   ├── package.json         # Frontend dependencies
│   │   ├── vite.config.ts       # Vite configuration
│   │   └── tsconfig.json        # TypeScript configuration
│   ├── agents/
│   │   ├── __init__.py
│   │   └── rag_agent.py         # LangGraph RAG agent with streaming
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
- LangGraph-based RAG agent with streaming capabilities
- ChromaDB vector store with OpenAI embeddings
- OpenAI GPT-4 integration with tool calling
- PDF document processing and automatic chunking
- FastAPI REST API with multiple endpoints
- Server-Sent Events (SSE) for real-time streaming
- Tool integration with retriever functionality
- CORS support for cross-origin requests

### Frontend Features
- Modern React 19 with TypeScript
- Vite for fast development and building
- Tailwind CSS for responsive styling
- Assistant UI components for modern chat interface
- Real-time streaming with word-by-word display
- Tool call visibility with expandable sections
- Markdown rendering for formatted responses
- Responsive design for all devices
- Smooth animations and transitions

### Streaming Capabilities
- Real-time text streaming with natural delays
- Tool call detection and display
- Tool result integration in UI
- Progressive message updates
- Server-Sent Events (SSE) implementation
- Proper error handling and fallbacks

### Adding New Documents
1. Place PDF files in `src/data/`
2. Update the `pdf_path` in `src/config/settings.py`
3. Restart the backend to rebuild the vector store

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

### Testing API Endpoints
```bash
# Test standard query endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What was Apple stock performance in 2024?"}'

# Test streaming endpoint
curl -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{"question": "What was Apple stock performance in 2024?"}' \
  --no-buffer

# Test advanced streaming endpoint
curl -X POST http://localhost:8000/stream-with-tools \
  -H "Content-Type: application/json" \
  -d '{"question": "What was Apple stock performance in 2024?"}' \
  --no-buffer
```