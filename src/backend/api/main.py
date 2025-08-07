from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import sys
import os
import asyncio
import json

# Add the project root directory to the path to import modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.agents.rag_agent import rag_agent, stream_rag_agent
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
async def stream_rag_agent_endpoint(request: QueryRequest):
    """Streaming endpoint for frontend integration"""
    try:
        async def generate_stream():
            async for chunk in stream_rag_agent(request.question):
                # Send each chunk as a Server-Sent Event
                yield f"data: {chunk}\n\n"
            # Send completion signal
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        async def error_stream():
            yield f"data: Error: {str(e)}\n\n"
        
        return StreamingResponse(
            error_stream(),
            media_type="text/event-stream",
            status_code=500,
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )

@app.post("/stream-with-tools")
async def stream_rag_agent_with_tools(request: QueryRequest):
    """Advanced streaming endpoint that includes tool calls and results"""
    try:
        async def generate_stream():
            # First, get the complete response to extract tool information
            messages = [HumanMessage(content=request.question)]
            result = rag_agent.invoke({"messages": messages})
            
            # Extract tool calls and results
            tool_calls = []
            tool_results = []
            
            for message in result['messages']:
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    for tool_call in message.tool_calls:
                        tool_calls.append({
                            "id": tool_call['id'],
                            "name": tool_call['name'],
                            "args": tool_call['args']
                        })
                elif hasattr(message, 'tool_call_id'):
                    tool_results.append({
                        "toolCallId": message.tool_call_id,
                        "result": message.content
                    })
            
            # Stream tool calls first
            for tool_call in tool_calls:
                yield f"data: {json.dumps({'type': 'tool_call', 'data': tool_call})}\n\n"
                await asyncio.sleep(0.1)
            
            # Stream tool results
            for tool_result in tool_results:
                # Simplify the result structure
                simplified_result = tool_result['result']
                if isinstance(simplified_result, dict) and 'result' in simplified_result:
                    simplified_result = simplified_result['result']
                
                yield f"data: {json.dumps({'type': 'tool_result', 'data': {'toolCallId': tool_result['toolCallId'], 'result': simplified_result}})}\n\n"
                await asyncio.sleep(0.1)
            
            # Stream the final response
            final_message = result['messages'][-1]
            final_text = final_message.content
            
            words = final_text.split(' ')
            for word in words:
                yield f"data: {json.dumps({'type': 'text', 'data': f'{word} '})}\n\n"
                await asyncio.sleep(0.03)
            
            # Send completion signal
            yield "data: [DONE]\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )
    except Exception as e:
        async def error_stream():
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"
        
        return StreamingResponse(
            error_stream(),
            media_type="text/event-stream",
            status_code=500,
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
            }
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT) 