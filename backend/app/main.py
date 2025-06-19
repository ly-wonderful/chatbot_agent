from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chat import router as chat_router
from app.config import settings
import logging
import os


print(f"DEBUG: LANGCHAIN_TRACING_V2 = {settings.langchain_tracing_v2}")
print(f"DEBUG: LANGCHAIN_API_KEY = {settings.langchain_api_key[:20] if settings.langchain_api_key else None}...")
print(f"DEBUG: LANGCHAIN_PROJECT = {settings.langchain_project}")

if settings.langchain_tracing_v2 and settings.langchain_api_key:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
    print(f"🔍 LangSmith tracing enabled for project: {settings.langchain_project}")
else:
    print("📋 LangSmith tracing disabled")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():

    return {"message": "Summer Camp Chatbot API", "status": "running"}

@app.get("/health")
async def health_check():

    return {"status": "healthy", "app": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
