# Stock Market RAG Agent

A modern chat interface for querying Stock Market Performance data using LangGraph, FastAPI, and a simple HTML frontend.

## 🚀 Quick Start

### Option 1: Use the startup script (Recommended)
```bash
python3 start_app.py
```

### Option 2: Manual setup

1. **Start the FastAPI backend:**
   ```bash
   cd api
   python3 main.py
   ```

2. **Start the frontend server:**
   ```bash
   cd frontend
   python3 server.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🏗️ Architecture

### Backend (FastAPI + LangGraph)
- **RAG Agent**: LangGraph-based retrieval-augmented generation
- **Vector Store**: ChromaDB with OpenAI embeddings
- **Knowledge Base**: Stock Market Performance 2024 PDF
- **API**: FastAPI with CORS support

### Frontend (Simple HTML + JavaScript)
- **UI**: Clean HTML interface with JavaScript
- **Features**: Real-time streaming, message editing, copy functionality
- **Styling**: Modern CSS with responsive design

## 📁 Project Structure

```
langgraph/
├── ai_agents/
│   ├── rag_agent.py          # LangGraph RAG agent
│   └── Stock_Market_Performance_2024.pdf
├── api/
│   └── main.py               # FastAPI backend
├── frontend/
│   ├── index.html            # Main chat interface
│   └── server.py             # Simple HTTP server
├── vectorstore/              # ChromaDB vector store
├── start_app.py              # Startup script
└── README.md
```

## 🎯 Features

### Backend Features
- ✅ LangGraph-based RAG agent
- ✅ ChromaDB vector store
- ✅ OpenAI embeddings and GPT-4
- ✅ PDF document processing
- ✅ FastAPI REST API
- ✅ CORS support

### Frontend Features
- ✅ Clean and modern UI
- ✅ Real-time streaming responses
- ✅ Message editing and regeneration
- ✅ Copy message functionality
- ✅ Suggested questions
- ✅ Responsive design
- ✅ Markdown support

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```
OPENAI_API_KEY=your_openai_api_key
```

## 📚 Usage

1. **Ask Questions**: Type questions about stock market performance in 2024
2. **Streaming Responses**: Watch responses appear in real-time
3. **Edit Messages**: Click the edit icon to modify your questions
4. **Regenerate**: Use the regenerate button to get new responses
5. **Copy Responses**: Copy any assistant response to clipboard

## 🛠️ Development

### Backend Development
```bash
cd api
python3 main.py
```

### Frontend Development
```bash
cd frontend
python3 server.py
```

### Adding New Documents
1. Place PDF files in `ai_agents/`
2. Update the `pdf_path` in `rag_agent.py`
3. Restart the backend

## 🚀 Deployment

### Backend Deployment
- Deploy to any Python hosting platform (Railway, Heroku, etc.)
- Set environment variables
- Update CORS origins in `api/main.py`

### Frontend Deployment
- Deploy to any static hosting service
- Update API endpoint URLs in `frontend/index.html`

## 📖 API Documentation

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both backend and frontend
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [LangGraph](https://github.com/langchain-ai/langgraph) for the RAG agent framework
- [FastAPI](https://fastapi.tiangolo.com/) for the backend API 