from fastapi import APIRouter, HTTPException
from models.schemas import ChatMessage, ChatResponse
from agents.camp_agent_dynamic import camp_agent
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):

    try:

        session_id = message.session_id or str(uuid.uuid4())
        

        response = await camp_agent.process_message(
            message=message.message,
            session_id=session_id
        )
        
        return ChatResponse(
            response=response["response"],
            session_id=session_id,
            context=response.get("context")
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/chat/health")
async def chat_health():

    return {"status": "healthy", "service": "chat"}
