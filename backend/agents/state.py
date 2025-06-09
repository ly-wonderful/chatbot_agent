from typing import Dict, List, Any, Optional
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class CampChatState(BaseModel):

    

    messages: List[BaseMessage] = Field(default_factory=list)
    

    session_id: Optional[str] = None
    

    current_intent: Optional[str] = None
    search_filters: Optional[Dict[str, Any]] = None
    last_search_results: Optional[List[Dict[str, Any]]] = None
    

    final_response: Optional[str] = None
    
    class Config:
        arbitrary_types_allowed = True
