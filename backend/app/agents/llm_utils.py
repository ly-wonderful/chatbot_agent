from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.config import settings
import logging

logger = logging.getLogger(__name__)

def get_llm():
    """
    Returns the appropriate LLM based on the configured provider
    """
    if settings.llm_provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0
        )
    elif settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key is required when using OpenAI as the LLM provider")
        return ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")

async def get_llm_response(prompt: str, model: str = None) -> str:
    """Get response from LLM based on configured provider"""
    try:
        if settings.llm_provider == "gemini":
            llm = ChatGoogleGenerativeAI(
                model=model or settings.gemini_model,
                google_api_key=settings.google_api_key,
                temperature=0.7
            )
        elif settings.llm_provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("OpenAI API key not configured")
            llm = ChatOpenAI(
                model=model or settings.openai_model,
                openai_api_key=settings.openai_api_key,
                temperature=0.7
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
        
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        logger.error(f"Error getting LLM response: {e}")
        return "I'm having trouble processing your request. Please try again." 