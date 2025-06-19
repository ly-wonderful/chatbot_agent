from langchain.tools import tool
from database.supabase_client import supabase_client
from models.schemas import CampSearchFilters
from typing import Dict, List, Any, Optional
import json
import asyncio



@tool
def search_camps_tool(
    location: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    category: Optional[str] = None,
    min_grade: Optional[int] = None,
    max_grade: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> str:
"""
    Search for summer camps based on various criteria.
    This is a tool definition for LangGraph. Actual implementation is in search node.
    """
    filters = CampSearchFilters(
        location=location,
        city=city,
        state=state,
        category=category,
        min_grade=min_grade,
        max_grade=max_grade,
        min_price=min_price,
        max_price=max_price
    )
    

    return json.dumps({
        "filters": filters.dict(exclude_none=True),
        "note": "Search executed in graph node"
    })

@tool
def get_camp_details_tool(camp_id: int) -> str:
"""
    Get detailed information about a specific camp.
    """
    try:

        camp_details = {}
        
        return json.dumps(camp_details, default=str)
    
    except Exception as e:
        return json.dumps({"error": str(e), "camp": None})

@tool
def get_categories_tool() -> str:
"""
    Get all available camp categories.
    """
    try:
        categories = []
        return json.dumps({"categories": categories})
    
    except Exception as e:
        return json.dumps({"error": str(e), "categories": []})

@tool
def get_locations_tool() -> str:
"""
    Get all available camp locations.
    """
    try:
        locations = []
        return json.dumps({"locations": locations})
    
    except Exception as e:
        return json.dumps({"error": str(e), "locations": []})


CAMP_TOOLS = [
    search_camps_tool,
    get_camp_details_tool,
    get_categories_tool,
    get_locations_tool
]
