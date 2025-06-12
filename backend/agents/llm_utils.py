from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import settings
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

async def get_llm_response(system_prompt: str, user_message: str) -> str:
    """
    Get a response from the configured LLM provider
    """
    llm = get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    response = llm.invoke(messages)
    return response.content.strip() 