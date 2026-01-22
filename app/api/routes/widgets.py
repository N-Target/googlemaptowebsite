"""
Interactive widgets API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.schemas import WidgetCreate, WidgetResponse
from app.models.models import Widget
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=WidgetResponse)
async def create_widget(
    widget: WidgetCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new interactive widget for a website
    
    Widget types:
    - contact_form: Contact form with email integration
    - chatbot: AI-powered chatbot
    - booking: Appointment booking widget
    - map: Interactive Google Maps widget
    - reviews: Google Reviews display widget
    """
    db_widget = Widget(
        website_id=widget.website_id,
        widget_type=widget.widget_type,
        name=widget.name,
        configuration=widget.configuration,
        position=widget.position,
        is_active=widget.is_active
    )
    
    db.add(db_widget)
    db.commit()
    db.refresh(db_widget)
    
    return db_widget


@router.get("/website/{website_id}", response_model=List[WidgetResponse])
async def list_website_widgets(
    website_id: int,
    db: Session = Depends(get_db)
):
    """List all widgets for a specific website"""
    widgets = db.query(Widget).filter(
        Widget.website_id == website_id,
        Widget.is_active == True
    ).all()
    return widgets


@router.get("/{widget_id}", response_model=WidgetResponse)
async def get_widget(
    widget_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific widget"""
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    return widget


@router.patch("/{widget_id}", response_model=WidgetResponse)
async def update_widget(
    widget_id: int,
    widget_update: dict,
    db: Session = Depends(get_db)
):
    """Update widget configuration or status"""
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    
    if 'configuration' in widget_update:
        widget.configuration = widget_update['configuration']
    
    if 'is_active' in widget_update:
        widget.is_active = widget_update['is_active']
    
    if 'position' in widget_update:
        widget.position = widget_update['position']
    
    db.commit()
    db.refresh(widget)
    
    return widget


@router.delete("/{widget_id}")
async def delete_widget(
    widget_id: int,
    db: Session = Depends(get_db)
):
    """Delete a widget"""
    widget = db.query(Widget).filter(Widget.id == widget_id).first()
    if not widget:
        raise HTTPException(status_code=404, detail="Widget not found")
    
    db.delete(widget)
    db.commit()
    
    return {"message": "Widget deleted successfully"}


@router.get("/types/available")
async def get_available_widget_types():
    """
    Get list of available widget types with descriptions
    """
    return {
        "widget_types": [
            {
                "type": "contact_form",
                "name": "Kapcsolati Űrlap",
                "description": "Email-integráció kapcsolati űrlappal",
                "configuration": {
                    "fields": ["name", "email", "phone", "message"],
                    "email_notification": True
                }
            },
            {
                "type": "chatbot",
                "name": "AI Chatbot",
                "description": "Mesterséges intelligenciával működő chatbot",
                "configuration": {
                    "greeting": "Szia! Miben segíthetek?",
                    "ai_enabled": True
                }
            },
            {
                "type": "booking",
                "name": "Időpontfoglalás",
                "description": "Időpontfoglalás widget",
                "configuration": {
                    "time_slots": ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"],
                    "duration": 60
                }
            },
            {
                "type": "map",
                "name": "Térkép",
                "description": "Interaktív Google Maps térkép",
                "configuration": {
                    "show_directions": True,
                    "show_street_view": True
                }
            },
            {
                "type": "reviews",
                "name": "Értékelések",
                "description": "Google értékelések megjelenítése",
                "configuration": {
                    "max_reviews": 5,
                    "show_rating": True
                }
            }
        ]
    }
