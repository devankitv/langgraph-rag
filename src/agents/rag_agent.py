from dotenv import load_dotenv
import os
import sys
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence, AsyncGenerator
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool
import asyncio

# Add the project root to Python path to handle imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0,
    streaming=True  # Enable streaming
) # minimize hallucination - temperature = 0 makes the model output more deterministic 

# Our Embedding Model - has to also be compatible with the LLM
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
)


from src.config.settings import PDF_PATH
pdf_path = str(PDF_PATH)


if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path) # This loads the PDF

# Checks if the PDF is there
try:
    pages = pdf_loader.load()
    print(f"PDF has been loaded and has {len(pages)} pages")
except Exception as e:
    print(f"Error loading PDF: {e}")
    raise

# Chunking Process
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)


pages_split = text_splitter.split_documents(pages) # We now apply this to our pages

from src.config.settings import VECTORSTORE_DIR
persist_directory = str(VECTORSTORE_DIR)
collection_name = "stock_market"

# If our collection does not exist in the directory, we create using the os command
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)


try:
    # Here, we actually create the chroma database using our embeddigns model
    vectorstore = Chroma.from_documents(
        documents=pages_split,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    print(f"Created ChromaDB vector store!")
    
except Exception as e:
    print(f"Error setting up ChromaDB: {str(e)}")
    raise


# Now we create our retriever 
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5} # K is the amount of chunks to return
)

@tool
def retriever_tool(query: str) -> str:
    """
    This tool searches and returns the information from the Stock Market Performance 2024 document.
    """

    docs = retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the Stock Market Performance 2024 document."
    
    results = []
    for i, doc in enumerate(docs):
        results.append(f"Document {i+1}:\n{doc.page_content}")
    
    return "\n\n".join(results)


tools = [retriever_tool]

llm = llm.bind_tools(tools)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState):
    """Check if the last message contains tool calls."""
    result = state['messages'][-1]
    return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0


system_prompt = """
You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.
Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
"""


tools_dict = {our_tool.name: our_tool for our_tool in tools} # Creating a dictionary of our tools

# LLM Agent
def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state."""
    messages = list(state['messages'])
    messages = [SystemMessage(content=system_prompt)] + messages
    message = llm.invoke(messages)
    return {'messages': [message]}


# Retriever Agent
def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""

    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        
        if not t['name'] in tools_dict: # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
            

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}


graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {True: "retriever_agent", False: END}
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


# Function to query the RAG agent (for API usage)
def query_rag_agent(question: str):
    """
    Query the RAG agent with a specific question.
    
    Args:
        question (str): The question to ask the RAG agent
        
    Returns:
        str: The agent's response
    """
    messages = [HumanMessage(content=question)]
    result = rag_agent.invoke({"messages": messages})
    return result['messages'][-1].content


# Advanced streaming function that handles the entire RAG process
async def stream_rag_agent_advanced(question: str) -> AsyncGenerator[dict, None]:
    """
    Advanced streaming function that streams the entire RAG process including tool calls.
    
    Args:
        question (str): The question to ask the RAG agent
        
    Yields:
        dict: Streamed events with type and content
    """
    messages = [HumanMessage(content=question)]
    
    # Create a streaming LLM for this specific call
    streaming_llm = ChatOpenAI(
        model="gpt-4o", 
        temperature=0,
        streaming=True
    ).bind_tools(tools)
    
    # First, let's try to stream the initial LLM response
    messages_with_system = [SystemMessage(content=system_prompt)] + messages
    
    try:
        # Try to stream the LLM response directly
        async for chunk in streaming_llm.astream(messages_with_system):
            if hasattr(chunk, 'content') and chunk.content:
                yield {
                    "type": "text",
                    "content": chunk.content
                }
            elif hasattr(chunk, 'tool_calls') and chunk.tool_calls:
                for tool_call in chunk.tool_calls:
                    yield {
                        "type": "tool_call",
                        "content": {
                            "id": tool_call['id'],
                            "name": tool_call['name'],
                            "args": tool_call['args']
                        }
                    }
    except Exception:
        # If direct streaming fails, fall back to the regular RAG agent
        result = rag_agent.invoke({"messages": messages})
        final_message = result['messages'][-1]
        
        # Stream the final response word by word
        words = final_message.content.split(' ')
        for word in words:
            yield {
                "type": "text",
                "content": f"{word} "
            }
            await asyncio.sleep(0.03)

# Keep the original streaming function for backward compatibility
async def stream_rag_agent(question: str) -> AsyncGenerator[str, None]:
    """
    Stream the RAG agent response with a specific question.
    
    Args:
        question (str): The question to ask the RAG agent
        
    Yields:
        str: Streamed chunks of the agent's response
    """
    messages = [HumanMessage(content=question)]
    
    # Run the full RAG agent to get the complete response
    result = rag_agent.invoke({"messages": messages})
    
    # Get the final response
    final_message = result['messages'][-1]
    
    # Check if there were tool calls
    tool_calls_present = any(
        hasattr(msg, 'tool_calls') and msg.tool_calls 
        for msg in result['messages']
    )
    
    if tool_calls_present:
        # If there were tool calls, indicate that tools were used
        yield "[Tool Call: retriever_tool] "
        # Add a small delay to simulate tool execution
        await asyncio.sleep(0.5)
    
    # Extract the text content from the final message
    if hasattr(final_message, 'content'):
        final_text = final_message.content
    else:
        # If it's a structured message, try to extract text
        final_text = str(final_message)
    
    # Stream the final response word by word
    words = final_text.split(' ')
    for word in words:
        yield f"{word} "
        await asyncio.sleep(0.03)  # 30ms delay between words

# Get the PNG data
png_data = rag_agent.get_graph().draw_mermaid_png()
# Save the graph image to root directory
import os
# Get the current filename without extension
current_filename = os.path.splitext(os.path.basename(__file__))[0]
# Save to root directory (workspace root)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
image_filename = os.path.join(root_dir, f"{current_filename}.png")
# Save the PNG data to file
with open(image_filename, 'wb') as f:
    f.write(png_data)
print(f"Graph image saved as: {image_filename}")


# Only run the interactive mode if this file is run directly
if __name__ == "__main__":
    def running_agent():
        print("\n=== RAG AGENT===")
        
        while True:
            user_input = input("\nWhat is your question: ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

            result = rag_agent.invoke({"messages": messages})
            
            print("\n=== ANSWER ===")
            print(result['messages'][-1].content)

    running_agent()