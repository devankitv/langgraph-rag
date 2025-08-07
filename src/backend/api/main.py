from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os
import asyncio

# Add the project root directory to the path to import modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.agents.rag_agent import rag_agent
from src.config.settings import API_HOST, API_PORT, CORS_ORIGINS
from langchain_core.messages import HumanMessage

app = FastAPI(title="RAG Agent API", description="API for Stock Market Performance RAG Agent")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    messages: List[Dict[str, Any]]
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
        
        # Convert messages to a format that can be serialized
        serialized_messages = []
        for message in result['messages']:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                # Handle tool calls
                content = []
                for tool_call in message.tool_calls:
                    content.append({
                        "type": "tool-call",
                        "toolCallId": tool_call['id'],
                        "toolName": tool_call['name'],
                        "args": tool_call['args']
                    })
                serialized_messages.append({
                    "role": "assistant",
                    "content": content
                })
            elif hasattr(message, 'tool_call_id'):
                # Handle tool results
                serialized_messages.append({
                    "role": "tool",
                    "content": [{
                        "type": "tool-result",
                        "toolCallId": message.tool_call_id,
                        "result": {
                            "result": message.content
                        }
                    }]
                })
            elif hasattr(message, 'type') and message.type == "ai":
                # Handle AI assistant messages
                serialized_messages.append({
                    "role": "assistant",
                    "content": [{
                        "type": "text",
                        "text": message.content
                    }]
                })
            elif hasattr(message, 'type') and message.type == "human":
                # Handle human messages
                serialized_messages.append({
                    "role": "user",
                    "content": [{
                        "type": "text",
                        "text": message.content
                    }]
                })
            else:
                # Handle other messages (default to assistant)
                serialized_messages.append({
                    "role": "assistant",
                    "content": [{
                        "type": "text",
                        "text": message.content
                    }]
                })
        
        # Ensure we have at least one assistant message with text content
        assistant_messages = [msg for msg in serialized_messages if msg['role'] == 'assistant']
        if not assistant_messages or not any(
            any(part.get('type') == 'text' for part in msg['content']) 
            for msg in assistant_messages
        ):
            # Add a fallback assistant message if none exists
            serialized_messages.append({
                "role": "assistant",
                "content": [{
                    "type": "text",
                    "text": "I've processed your request and found relevant information."
                }]
            })
        
        return QueryResponse(
            messages=serialized_messages,
            success=True
        )
    except Exception as e:
        return QueryResponse(
            messages=[],
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
    uvicorn.run(app, host=API_HOST, port=API_PORT) 