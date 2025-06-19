from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatMessage, ChatResponse
from app.agents.camp_agent_dynamic import camp_agent
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Simple in-memory state store (in production, use Redis or database)
session_states = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):

    try:

        session_id = message.session_id or str(uuid.uuid4())
        
        logger.info(f"Processing message: {message.message} for session: {session_id}")

        # Get existing state for this session
        existing_state = session_states.get(session_id)

        response = await camp_agent.process_message(
            message=message.message,
            session_id=session_id,
            state=existing_state
        )
        
        # Store the updated state
        session_states[session_id] = response
        logger.info(f"Session state for {session_id}: {session_states[session_id]}")
        
        logger.info(f"Agent response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")
        logger.info(f"Agent response: {response}")
        
        # Extract the final_response from the agent response
        final_response = response.get("final_response", "Sorry, I encountered an error.")
        
        return ChatResponse(
            response=final_response,
            session_id=session_id,
            context=response.get("context")
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/chat/health")
async def chat_health():

    return {"status": "healthy", "service": "chat"}
