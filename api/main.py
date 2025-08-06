from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List
import sys
import os
import asyncio

# Add the parent directory to the path to import the rag_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agents.rag_agent import rag_agent
from langchain_core.messages import HumanMessage

app = FastAPI(title="RAG Agent API", description="API for Stock Market Performance RAG Agent")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    success: bool
    error: str = None

@app.get("/")
async def root():
    return {"message": "RAG Agent API is running"}

@app.post("/query", response_model=QueryResponse)
async def query_rag_agent(request: QueryRequest):
    try:
        # Create a human message with the user's question
        messages = [HumanMessage(content=request.question)]
        
        # Invoke the RAG agent
        result = rag_agent.invoke({"messages": messages})
        
        # Extract the answer from the last message
        answer = result['messages'][-1].content
        
        return QueryResponse(
            answer=answer,
            success=True
        )
    except Exception as e:
        return QueryResponse(
            answer="",
            success=False,
            error=str(e)
        )

@app.post("/stream")
async def stream_rag_agent(request: QueryRequest):
    """Streaming endpoint for frontend integration"""
    try:
        # Create a human message with the user's question
        messages = [HumanMessage(content=request.question)]
        
        # Invoke the RAG agent
        result = rag_agent.invoke({"messages": messages})
        
        # Extract the answer from the last message
        answer = result['messages'][-1].content
        
        async def generate_stream():
            words = answer.split(' ')
            for word in words:
                yield f"{word} "
                await asyncio.sleep(0.03)  # 30ms delay between words
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain"
        )
    except Exception as e:
        async def error_stream():
            yield f"Error: {str(e)}"
        
        return StreamingResponse(
            error_stream(),
            media_type="text/plain",
            status_code=500
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 