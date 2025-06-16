import os
from pydantic_settings import BaseSettings
from typing import Optional, List, Literal

class Settings(BaseSettings):

    app_name: str = "Summer Camp Chatbot API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    

    supabase_url: str
    supabase_key: str
    

    # LLM Configuration
    llm_provider: Literal["gemini", "openai"] = "gemini"  # Default to Gemini
    
    # Gemini Configuration
    google_api_key: str
    gemini_model: str = "gemini-pro"
    
    # Google Maps Configuration
    google_maps_api_key: str
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    

    langchain_tracing_v2: bool = False
    langchain_api_key: Optional[str] = None
    langchain_project: str = "summer-camp-chatbot"
    

    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:

        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
