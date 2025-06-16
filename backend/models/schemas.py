from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, time
from decimal import Decimal


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
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    min_grade: Optional[int] = None
    max_grade: Optional[int] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_driving_distance_miles: Optional[float] = None

class CampSearchResult(BaseModel):
    camps: List[Camp]
    total_count: int
    filters_applied: CampSearchFilters
