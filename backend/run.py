#!/usr/bin/env python3
"""
Entry point for the Summer Camp Chatbot Backend
"""

import uvicorn
from app.main import app
from app.config import settings

if __name__ == "__main__":
    print(f"🚀 Starting {settings.app_name}")
    print(f"📍 Host: {settings.host}")
    print(f"🔌 Port: {settings.port}")
    print(f"🐛 Debug: {settings.debug}")
    print(f"🤖 LLM Provider: {settings.llm_provider}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    ) 