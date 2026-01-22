"""
Lead management API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.schemas import LeadCreate, LeadResponse, LeadUpdate
from app.models.models import Lead, LeadActivity
from app.db.database import get_db

router = APIRouter()


@router.post("/", response_model=LeadResponse)
async def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new lead from website interaction
    
    Automatically tracks lead source (widget, form, etc.)
    """
    db_lead = Lead(
        website_id=lead.website_id,
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        message=lead.message,
        source=lead.source,
        status='new',
        tags=lead.tags,
        custom_fields=lead.custom_fields
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Track activity
    activity = LeadActivity(
        lead_id=db_lead.id,
        activity_type='lead_created',
        description=f'Lead created from {lead.source}',
        metadata={'source': lead.source}
    )
    db.add(activity)
    db.commit()
    
    return db_lead


@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    website_id: int = None,
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List leads with optional filtering
    
    Filter by website_id or status for targeted lead management
    """
    query = db.query(Lead)
    
    if website_id:
        query = query.filter(Lead.website_id == website_id)
    
    if status:
        query = query.filter(Lead.status == status)
    
    leads = query.offset(skip).limit(limit).all()
    return leads


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific lead"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: int,
    lead_update: LeadUpdate,
    db: Session = Depends(get_db)
):
    """
    Update lead information and status
    
    Tracks status changes for marketing automation
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if lead_update.status:
        old_status = lead.status
        lead.status = lead_update.status
        
        # Track status change
        activity = LeadActivity(
            lead_id=lead.id,
            activity_type='status_changed',
            description=f'Status changed from {old_status} to {lead_update.status}',
            metadata={'old_status': old_status, 'new_status': lead_update.status}
        )
        db.add(activity)
    
    if lead_update.tags is not None:
        lead.tags = lead_update.tags
    
    if lead_update.custom_fields is not None:
        lead.custom_fields = lead_update.custom_fields
    
    db.commit()
    db.refresh(lead)
    
    return lead


@router.delete("/{lead_id}")
async def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    """Delete a lead"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(lead)
    db.commit()
    
    return {"message": "Lead deleted successfully"}
