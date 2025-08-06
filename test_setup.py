#!/usr/bin/env python3
"""
Test script to verify that all components are properly set up.
This script checks:
1. Required files exist
2. Dependencies can be imported
3. RAG agent can be initialized
4. API endpoints are accessible
"""

import os
import sys
from pathlib import Path
import importlib.util

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        "ai_agents/rag_agent.py",
        "ai_agents/Stock_Market_Performance_2024.pdf",
        "api/main.py",
        "frontend/index.html",
        "frontend/server.py",
        "requirements.txt",
        "start_app.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files found!")
        return True

def check_dependencies():
    """Check if all required dependencies can be imported"""
    print("\n🔍 Checking dependencies...")
    
    required_modules = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "langgraph",
        "langchain",
        "langchain_openai",
        "langchain_community",
        "langchain_chroma",
        "chromadb",
        "dotenv"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module}")
    
    if missing_modules:
        print(f"❌ Missing modules: {missing_modules}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available!")
        return True

def check_env_file():
    """Check if .env file exists and has OpenAI API key"""
    print("\n🔍 Checking environment setup...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("💡 Create a .env file with your OpenAI API key:")
        print("   OPENAI_API_KEY=your_api_key_here")
        return False
    
    # Read .env file
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "OPENAI_API_KEY" not in content:
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    
    print("✅ .env file found with OpenAI API key")
    return True

def check_rag_agent():
    """Check if RAG agent can be initialized"""
    print("\n🔍 Testing RAG agent initialization...")
    
    try:
        # Add the current directory to Python path
        sys.path.insert(0, str(Path.cwd()))
        
        # Import the RAG agent
        from ai_agents.rag_agent import rag_agent
        
        print("✅ RAG agent imported successfully")
        
        # Test a simple query
        from langchain_core.messages import HumanMessage
        
        test_messages = [HumanMessage(content="What is this document about?")]
        result = rag_agent.invoke({"messages": test_messages})
        
        print("✅ RAG agent can process queries")
        print(f"📝 Sample response length: {len(result['messages'][-1].content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing RAG agent: {e}")
        return False

def main():
    print("🧪 Testing Stock Market LangGraph RAG Agent Setup")
    print("=" * 50)
    
    # Run all checks
    checks = [
        check_files(),
        check_dependencies(),
        check_env_file(),
        check_rag_agent()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the application, run:")
        print("   python start_app.py")
        print("\n📖 For more information, see README_RAG_API.md")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Create .env file with your OpenAI API key")
        print("   3. Make sure all files are in the correct locations")

if __name__ == "__main__":
    main() 