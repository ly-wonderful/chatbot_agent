from langgraph.graph import StateGraph, END
from langchain.schema import HumanMessage, SystemMessage
from langsmith import traceable
from app.models.schemas import CampChatState
from app.agents.llm_utils import get_llm_response
from app.database.supabase_client import supabase_client
from app.models.schemas import CampSearchFilters
from app.config import settings
from typing import Dict, Any, List, Optional
import logging
import json
import asyncio
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.schemas import UserProfile
from functools import partial
import time

logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def ensure_dict(state):
    if isinstance(state, CampChatState):
        return state.dict()
    return state

@traceable(name="collect_profile")
async def collect_profile_node(state: dict) -> dict:
    """Agent 1: Collect user profile information"""
    state = ensure_dict(state)
    try:
        chat_state = CampChatState(**state)
        last_message = chat_state.messages[-1].content if chat_state.messages else ""
        
        logger.info(f"🔍 PROFILE DEBUG - profile_step: {chat_state.profile_step}, profile exists: {chat_state.profile is not None}, last_message: '{last_message}'")

        # Initialize profile if not exists
        if not chat_state.profile:
            logger.info("🔍 PROFILE DEBUG - Initializing new profile")
            chat_state.profile = UserProfile(
                name="",
                child_name="",
                child_age=5,
                child_grade=0,
                interests=[],
                address="",
                max_distance_miles=25.0
            )
            chat_state.profile_step = "name"
            chat_state.final_response = """Welcome! I'm your personal camp search assistant. I'll help you find the perfect summer camp for your child.\n\nLet's start by getting to know you and your child better. What's your name?"""
            # Do NOT treat the first message as a profile answer
            logger.info("🔍 PROFILE DEBUG - Returning welcome message")
            return chat_state.dict()
        
        # Ensure profile is a UserProfile object (not a dict)
        if isinstance(chat_state.profile, dict):
            logger.info("🔍 PROFILE DEBUG - Converting profile dict to UserProfile object")
            chat_state.profile = UserProfile(**chat_state.profile)
        
        # Check if this message has already been processed for the current step
        # Use a simple hash of the message content and current step to detect duplicates
        message_hash = f"{chat_state.profile_step}:{last_message}"
        if hasattr(chat_state, 'last_processed_message') and chat_state.last_processed_message == message_hash:
            logger.info(f"🔍 PROFILE DEBUG - Message already processed, returning current state")
            return chat_state.dict()
        
        # Mark this message as processed
        chat_state.last_processed_message = message_hash

        # Only use the last message as an answer if profile_step is set and this is not the first prompt
        if chat_state.profile_step == "name":
            if chat_state.profile.name == "":  # Only set if not already set
                logger.info(f"🔍 PROFILE DEBUG - Setting name to: {last_message}")
                chat_state.profile.name = last_message
                chat_state.profile_step = "child_name"
                chat_state.final_response = f"Nice to meet you, {last_message}! What's your child's name?"
            else:
                chat_state.final_response = f"What's your name?"
        
        elif chat_state.profile_step == "child_name":
            logger.info(f"🔍 PROFILE DEBUG - Setting child_name to: {last_message}")
            chat_state.profile.child_name = last_message
            chat_state.profile_step = "child_age"
            chat_state.final_response = f"How old is {last_message}? (Please enter a number between 4 and 18)"
        
        elif chat_state.profile_step == "child_age":
            try:
                age = int(last_message)
                if 4 <= age <= 18:
                    logger.info(f"🔍 PROFILE DEBUG - Setting child_age to: {age}")
                    chat_state.profile.child_age = age
                    chat_state.profile_step = "child_grade"
                    chat_state.final_response = f"What grade is {chat_state.profile.child_name} in? (Please enter a number between 0 and 12)"
                else:
                    chat_state.final_response = "Please enter a valid age between 4 and 18."
            except ValueError:
                chat_state.final_response = "Please enter a valid number for the age."
        
        elif chat_state.profile_step == "child_grade":
            try:
                grade = int(last_message)
                if 0 <= grade <= 12:
                    logger.info(f"🔍 PROFILE DEBUG - Setting child_grade to: {grade}")
                    chat_state.profile.child_grade = grade
                    chat_state.profile_step = "interests"
                    chat_state.final_response = f"What are {chat_state.profile.child_name}'s interests? (Enter interests separated by commas, e.g., soccer, basketball, art)"
                else:
                    chat_state.final_response = "Please enter a valid grade between 0 and 12."
            except ValueError:
                chat_state.final_response = "Please enter a valid number for the grade."
        
        elif chat_state.profile_step == "interests":
            # Use the state dict to persist the interests_prompted flag
            interests_prompted = state.get('interests_prompted', False)
            logger.info(f"[DEBUG] interests_prompted={interests_prompted}, profile_step={chat_state.profile_step}, last_message='{last_message}'")
            
            if not interests_prompted:
                logger.info("[DEBUG] Showing categories prompt for interests step.")
                # Always show categories prompt the first time interests step is reached
                try:
                    categories = await supabase_client.get_unique_categories()
                    if categories:
                        category_list = "\n".join([f"{i+1}. {cat}" for i, cat in enumerate(categories)])
                        chat_state.final_response = f"""What are {chat_state.profile.child_name}'s interests? \n\nHere are some popular camp categories to choose from:\n{category_list}\n\nYou can:\n• Select numbers from the list above (e.g., '1, 3, 5')\n• Type your own interests separated by commas (e.g., 'soccer, art, science')\n• Or combine both (e.g., '1, 3, robotics, swimming')\n\nWhat interests {chat_state.profile.child_name}?"""
                    else:
                        chat_state.final_response = f"What are {chat_state.profile.child_name}'s interests? (Enter interests separated by commas, e.g., soccer, basketball, art)"
                except Exception as e:
                    logger.error(f"Error fetching categories: {e}")
                    chat_state.final_response = f"What are {chat_state.profile.child_name}'s interests? (Enter interests separated by commas, e.g., soccer, basketball, art)"
                state['interests_prompted'] = True
            elif interests_prompted and last_message and last_message.strip():
                logger.info("[DEBUG] Processing user input for interests step.")
                # Process the user's response
                logger.info(f"🔍 PROFILE DEBUG - Processing interests: {last_message}")
                interests_list = [interest.strip() for interest in last_message.split(',') if interest.strip()]
                try:
                    categories = await supabase_client.get_unique_categories()
                    if categories:
                        selected_categories = []
                        for interest in interests_list:
                            try:
                                num = int(interest)
                                if 1 <= num <= len(categories):
                                    selected_categories.append(categories[num-1])
                                else:
                                    selected_categories.append(interest)
                            except ValueError:
                                selected_categories.append(interest)
                        interests_list = selected_categories
                except Exception as e:
                    logger.error(f"Error processing category selections: {e}")
                chat_state.profile.interests = interests_list
                logger.info(f"🔍 PROFILE DEBUG - Added {len(interests_list)} interests: {interests_list}")
                chat_state.profile_step = "address"
                chat_state.final_response = f"Where are you located? Please enter your home address."
                state['interests_prompted'] = False  # Reset for next session
            else:
                logger.info("[DEBUG] Waiting for user to respond to interests prompt.")
                # Waiting for user to respond to interests prompt
                chat_state.final_response = None
        
        elif chat_state.profile_step == "address":
            logger.info(f"🔍 PROFILE DEBUG - Setting address to: {last_message}")
            chat_state.profile.address = last_message
            chat_state.profile_step = "distance"
            chat_state.final_response = "What's the maximum driving distance you're willing to travel for camps? (Enter a number in miles)"
        
        elif chat_state.profile_step == "distance":
            logger.info(f"🔍 PROFILE DEBUG - Processing distance step with message: '{last_message}'")
            try:
                distance = float(last_message)
                if distance > 0:
                    logger.info(f"🔍 PROFILE DEBUG - Setting max_distance_miles to: {distance}")
                    chat_state.profile.max_distance_miles = distance
                    # Profile collection complete
                    chat_state.profile_step = None
                    logger.info("🔍 PROFILE DEBUG - Profile collection complete!")
                    chat_state.final_response = f"""Thank you for providing your information! I'll use this to find the perfect camps for {chat_state.profile.child_name}.\n\nHere's what I know:\n- Parent/Guardian: {chat_state.profile.name}\n- Child: {chat_state.profile.child_name} (Age: {chat_state.profile.child_age}, Grade: {chat_state.profile.child_grade})\n- Interests: {', '.join(chat_state.profile.interests)}\n- Location: {chat_state.profile.address}\n- Maximum Distance: {chat_state.profile.max_distance_miles} miles\n\nNow I'll search for camps that match {chat_state.profile.child_name}'s profile..."""
                else:
                    logger.info(f"🔍 PROFILE DEBUG - Invalid distance: {distance}")
                    chat_state.final_response = "Please enter a valid distance greater than 0."
            except ValueError as e:
                logger.info(f"🔍 PROFILE DEBUG - ValueError in distance parsing: {e}")
                chat_state.final_response = "Please enter a valid number for the distance."
        
        logger.info(f"🔍 PROFILE DEBUG - Final profile_step: {chat_state.profile_step}")
        state['prev_profile_step'] = chat_state.profile_step
        return chat_state.dict()
        
    except Exception as e:
        logger.error(f"❌ PROFILE - Error: {e}")
        chat_state = CampChatState(**state)
        chat_state.final_response = "I'm having trouble collecting your profile information. Let's start over."
        return chat_state.dict()

@traceable(name="generate_sql_query")
async def generate_sql_query_node(state: dict) -> dict:
    """Agent 2: Convert profile to SQL query"""
    state = ensure_dict(state)
    try:
        chat_state = CampChatState(**state)
        
        if not chat_state.profile:
            chat_state.final_response = "No profile found. Please provide your profile information first."
            return chat_state.dict()
        
        # Create search filters based on profile
        filters = CampSearchFilters(
            min_grade=chat_state.profile.child_grade,
            max_grade=chat_state.profile.child_grade,
            address=chat_state.profile.address,
            max_driving_distance_miles=chat_state.profile.max_distance_miles,
            category=None  # We'll add category filtering later if needed
        )
        
        # Store filters for database query
        chat_state.search_filters = filters.dict()
        
        logger.info(f"🔍 SQL - Generated filters: {chat_state.search_filters}")
        
        # Set response message to inform user that search is being prepared
        chat_state.final_response = f"Perfect! I'm preparing a search for camps that match {chat_state.profile.child_name}'s profile. Searching for camps within {chat_state.profile.max_distance_miles} miles of {chat_state.profile.address}..."
        
        return chat_state.dict()
        
    except Exception as e:
        logger.error(f"❌ SQL - Error: {e}")
        chat_state = CampChatState(**state)
        chat_state.final_response = "I'm having trouble generating the search query. Please try again."
        return chat_state.dict()

@traceable(name="search_database")
async def search_database_node(state: dict) -> dict:
    """Agent 2: Execute database search"""
    state = ensure_dict(state)
    try:
        chat_state = CampChatState(**state)
        
        if not chat_state.search_filters:
            chat_state.final_response = "No search filters found. Please provide your profile information first."
            return chat_state.dict()
        
        # Convert filters back to CampSearchFilters object
        filters = CampSearchFilters(**chat_state.search_filters)
        
        # Search camps using profile-based filters
        results = await supabase_client.search_camps(filters)
        
        # Extract the camps list from the response
        if isinstance(results, dict) and 'camps' in results:
            camps_list = results['camps']
        else:
            camps_list = results if isinstance(results, list) else []
        
        chat_state.last_search_results = camps_list
        
        logger.info(f"✅ DATABASE - Found {len(camps_list)} camps")
        
        # Set response message to inform user about search results
        if camps_list:
            chat_state.final_response = f"Great! I found {len(camps_list)} camps that match {chat_state.profile.child_name}'s profile. Let me format the results for you..."
        else:
            chat_state.final_response = f"I searched for camps matching {chat_state.profile.child_name}'s profile, but I couldn't find any camps in the database. Would you like to try different search criteria?"
        
        return chat_state.dict()
        
    except Exception as e:
        logger.error(f"❌ DATABASE - Error: {e}")
        chat_state = CampChatState(**state)
        chat_state.last_search_results = []
        chat_state.final_response = "I'm having trouble searching the database. Please try again."
        return chat_state.dict()

@traceable(name="format_table")
async def format_table_node(state: dict) -> dict:
    """Agent 3: Format results as table"""
    state = ensure_dict(state)
    try:
        chat_state = CampChatState(**state)
        results = chat_state.last_search_results or []
        
        if not results:
            chat_state.final_response = f"I couldn't find any camps matching {chat_state.profile.child_name}'s profile. Would you like to try different search criteria?"
            return chat_state.dict()
        
        # Create table header
        table = "| Camp Name | Organization | Location | Grades | Price | Distance | Description |\n"
        table += "|-----------|--------------|----------|--------|-------|----------|-------------|\n"
        
        # Add rows
        for camp in results[:10]:  # Limit to top 10 results
            camp_name = camp.get('camp_name', 'Unknown')
            
            org = camp.get('organizations', {})
            org_name = org.get('name', 'Unknown') if org else 'Unknown'
            
            # Get location
            location = "Unknown"
            sessions = camp.get('camp_sessions', [])
            if sessions:
                session = sessions[0]
                loc = session.get('locations', {})
                if loc:
                    city = loc.get('city', '')
                    state = loc.get('state', '')
                    location = f"{city}, {state}".strip(', ')
            
            # Get grades
            min_grade = camp.get('min_grade', '')
            max_grade = camp.get('max_grade', '')
            grades = f"{min_grade}-{max_grade}" if min_grade and max_grade else "Unknown"
            
            # Get price
            price = camp.get('price', 'Unknown')
            if price and price != 'Unknown':
                price = f"${price}/week"
            
            # Get distance (if available)
            distance = camp.get('distance_miles', 'Unknown')
            if distance and distance != 'Unknown':
                distance = f"{distance} miles"
            
            # Get description
            description = camp.get('description', '')
            if description:
                description = description[:50] + "..." if len(description) > 50 else description
            
            table += f"| {camp_name} | {org_name} | {location} | {grades} | {price} | {distance} | {description} |\n"
        
        # Create final response
        chat_state.final_response = f"""I found {len(results)} camps that match {chat_state.profile.child_name}'s profile!\n\nHere are the top results:\n\n{table}\n\nWould you like me to:\n1. Show more details about any specific camp?\n2. Filter the results further?\n3. Search with different criteria?"""
        
        return chat_state.dict()
        
    except Exception as e:
        logger.error(f"❌ TABLE - Error: {e}")
        chat_state = CampChatState(**state)
        chat_state.final_response = "I'm having trouble formatting the results. Please try again."
        return chat_state.dict()

class CampAgent:
    def __init__(self):
        self.graph = self._create_graph()
    
    def _create_graph(self) -> StateGraph:
        """Create the workflow graph"""
        workflow = StateGraph(dict)  # Changed from CampChatState to dict
        
        # Add nodes
        workflow.add_node("process_request", self._process_request_node)
        
        # Define the workflow - single node that handles everything
        workflow.set_entry_point("process_request")
        workflow.add_edge("process_request", END)
        
        return workflow.compile()
    
    async def _process_request_node(self, state: dict) -> dict:
        """Single node that handles the entire workflow based on state"""
        state = ensure_dict(state)
        try:
            chat_state = CampChatState(**state)
            
            logger.info(f"🔍 WORKFLOW DEBUG - Profile complete: {self._is_profile_complete(chat_state)}")
            logger.info(f"🔍 WORKFLOW DEBUG - Search filters: {chat_state.search_filters}")
            logger.info(f"🔍 WORKFLOW DEBUG - Last search results: {len(chat_state.last_search_results) if chat_state.last_search_results else 0}")
            logger.info(f"🔍 WORKFLOW DEBUG - Final response: {chat_state.final_response}")
            
            # If profile is not complete, collect profile
            if not self._is_profile_complete(chat_state):
                logger.info("🔍 WORKFLOW DEBUG - Collecting profile")
                return await collect_profile_node(state)
            
            # If profile is complete but no search filters, generate SQL
            if not chat_state.search_filters:
                logger.info("🔍 WORKFLOW DEBUG - Generating SQL query")
                return await generate_sql_query_node(state)
            
            # If search filters exist but no results, search database
            if not chat_state.last_search_results:
                logger.info("🔍 WORKFLOW DEBUG - Searching database")
                return await search_database_node(state)
            
            # If results exist but no formatted response, format table
            if not chat_state.final_response or "I found" not in chat_state.final_response:
                logger.info("🔍 WORKFLOW DEBUG - Formatting table")
                return await format_table_node(state)
            
            # Everything is complete
            logger.info("🔍 WORKFLOW DEBUG - Workflow complete")
            return chat_state.dict()
            
        except Exception as e:
            logger.error(f"❌ PROCESS REQUEST - Error: {e}")
            chat_state = CampChatState(**state)
            chat_state.final_response = "I'm having trouble processing your request. Please try again."
            return chat_state.dict()
    
    def _is_profile_complete(self, chat_state: CampChatState) -> bool:
        """Check if profile collection is complete"""
        profile = chat_state.profile
        if not profile:
            return False
        
        # Profile is only complete if all fields are filled AND profile_step is None
        return (profile.name and 
                profile.child_name and 
                (profile.child_age is not None and 4 <= profile.child_age <= 18) and 
                (profile.child_grade is not None and 0 <= profile.child_grade <= 12) and 
                profile.interests and 
                profile.address and 
                (profile.max_distance_miles is not None and profile.max_distance_miles > 0) and
                chat_state.profile_step is None)  # Profile step must be None to be complete
    
    async def process_message(self, message: str, session_id: str, state: dict = None) -> dict:
        """Process a user message, maintaining state across turns"""
        try:
            if state is None:
                # Create initial state
                state = {
                    "session_id": session_id,
                    "messages": [],
                    "current_intent": None,
                    "last_search_results": None,
                    "search_filters": None,
                    "final_response": None,
                    "needs_profile": True,
                    "profile": None,
                    "profile_step": None,
                    "last_processed_message": None
                }
            
            # Ensure 'messages' is a list
            if "messages" not in state or not isinstance(state["messages"], list):
                state["messages"] = []
            
            # Add the new message
            state["messages"].append(HumanMessage(content=message))
            
            # Run the workflow with the current state
            result = await self.graph.ainvoke(state)
            
            # Ensure we return a complete state
            if not isinstance(result, dict):
                result = state.copy()
                result["final_response"] = "I'm having trouble processing your request. Please try again."
            
            return result
            
        except Exception as e:
            logger.error(f"❌ PROCESS - Error: {e}")
            # Always return a complete state, just update final_response
            if state is None:
                state = {
                    "session_id": session_id,
                    "messages": [],
                    "current_intent": None,
                    "last_search_results": None,
                    "search_filters": None,
                    "final_response": None,
                    "needs_profile": True,
                    "profile": None,
                    "profile_step": None,
                    "last_processed_message": None
                }
            state = dict(state)  # Make a copy
            state["final_response"] = "I'm having trouble processing your request. Please try again."
            return state

# Create global instance
camp_agent = CampAgent()
