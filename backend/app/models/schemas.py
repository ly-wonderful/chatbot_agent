from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from decimal import Decimal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class ChatMessage(BaseModel):
    message: str = Field(..., description="User message")
    session_id: Optional[str] = Field(None, description="Chat session ID")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Bot response")
    session_id: str = Field(..., description="Chat session ID")
    context: Optional[dict] = Field(None, description="Additional context data")


class Organization(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    contact: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Location(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    formatted_address: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Camp(BaseModel):
    id: int
    organization_id: int
    camp_name: str
    description: Optional[str] = None
    price: Optional[Decimal] = None
    min_grade: Optional[int] = None
    max_grade: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    

    organization: Optional[Organization] = None
    categories: Optional[List[str]] = None

class CampSession(BaseModel):
    id: int
    camp_id: int
    location_id: int
    start_date: date
    end_date: date
    days: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    created_at: datetime
    updated_at: datetime
    

    camp: Optional[Camp] = None
    location: Optional[Location] = None

class Category(BaseModel):
    id: int
    name: str
    created_at: datetime

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CampSearchFilters(BaseModel):
    category: Optional[str] = None
    min_grade: Optional[int] = None
    max_grade: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    # Location-based search fields
    address: Optional[str] = None
    max_driving_distance_miles: Optional[float] = None

class CampSearchResult(BaseModel):
    camps: List[Camp]
    total_count: int
    filters_applied: CampSearchFilters

class UserProfile(BaseModel):
    name: str = Field(..., description="Parent/Guardian's name")
    child_name: str = Field(..., description="Child's name")
    child_age: int = Field(..., description="Child's age", ge=4, le=18)
    child_grade: int = Field(..., description="Child's grade level", ge=0, le=12)
    interests: List[str] = Field(default_factory=list, description="Child's interests and activities")
    address: str = Field(..., description="Home address for distance-based search")
    max_distance_miles: float = Field(..., description="Maximum driving distance in miles", gt=0)
    special_needs: Optional[str] = Field(None, description="Any special needs or accommodations required")
    preferred_categories: Optional[List[str]] = Field(None, description="Preferred camp categories")

class CampChatState(BaseModel):
    messages: List[HumanMessage] = Field(default_factory=list)
    session_id: str
    current_intent: Optional[str] = None
    search_filters: Optional[Dict[str, Any]] = None
    last_search_results: Optional[List[Dict[str, Any]]] = None
    final_response: Optional[str] = None
    needs_profile: bool = False
    profile: Optional[UserProfile] = None
    profile_step: Optional[str] = None  # Current step in profile collection
    last_processed_message: Optional[str] = None  # Track last processed message to prevent duplicates

    @validator('profile', pre=True, always=True)
    def ensure_profile_object(cls, v):
        if v is None:
            return v
        if isinstance(v, UserProfile):
            return v
        if isinstance(v, dict):
            return UserProfile(**v)
        return v
