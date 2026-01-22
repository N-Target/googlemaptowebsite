"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# Website Generator Schemas
class WebsiteGenerateRequest(BaseModel):
    """Request schema for generating a website"""
    business_name: Optional[str] = None
    google_place_id: Optional[str] = None
    address: Optional[str] = None
    language: str = Field(default="hu", description="Language code (hu, en, de, fr, es, it)")
    include_widgets: bool = Field(default=True, description="Include interactive widgets")
    
    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Kovács Étterem",
                "address": "Budapest, Andrássy út 1",
                "language": "hu",
                "include_widgets": True
            }
        }


class WebsiteResponse(BaseModel):
    """Response schema for generated website"""
    id: int
    business_name: str
    google_place_id: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    website_url: Optional[str]
    rating: Optional[float]
    business_type: Optional[str]
    language: str
    status: str
    published_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Lead Management Schemas
class LeadCreate(BaseModel):
    """Schema for creating a lead"""
    website_id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    message: Optional[str] = None
    source: str = "contact_form"
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None


class LeadResponse(BaseModel):
    """Response schema for lead"""
    id: int
    website_id: int
    name: str
    email: str
    phone: Optional[str]
    message: Optional[str]
    source: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class LeadUpdate(BaseModel):
    """Schema for updating lead status"""
    status: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None


# Widget Schemas
class WidgetCreate(BaseModel):
    """Schema for creating a widget"""
    website_id: int
    widget_type: str = Field(..., description="Type: contact_form, chatbot, booking, map, reviews")
    name: str
    configuration: Dict[str, Any] = Field(default_factory=dict)
    position: str = Field(default="bottom", description="Position: top, bottom, sidebar, popup")
    is_active: bool = True


class WidgetResponse(BaseModel):
    """Response schema for widget"""
    id: int
    website_id: int
    widget_type: str
    name: str
    configuration: Dict[str, Any]
    position: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Marketing Automation Schemas
class CampaignCreate(BaseModel):
    """Schema for creating marketing campaign"""
    name: str
    campaign_type: str = Field(..., description="Type: email, sms, notification")
    subject: Optional[str] = None
    content: str
    template: Optional[str] = None
    target_criteria: Dict[str, Any] = Field(default_factory=dict)
    scheduled_at: Optional[datetime] = None


class CampaignResponse(BaseModel):
    """Response schema for campaign"""
    id: int
    name: str
    campaign_type: str
    subject: Optional[str]
    status: str
    sent_count: int
    opened_count: int
    clicked_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Google Maps Integration Schemas
class GooglePlaceDetails(BaseModel):
    """Schema for Google Place details"""
    place_id: str
    name: str
    formatted_address: str
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    types: List[str] = []
    geometry: Dict[str, Any]
