"""
Marketing automation API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models.schemas import CampaignCreate, CampaignResponse
from app.models.models import MarketingCampaign, Lead, LeadActivity
from app.db.database import get_db

router = APIRouter()


@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new marketing campaign
    
    Campaign types: email, sms, notification
    Supports automated lead targeting with criteria
    """
    db_campaign = MarketingCampaign(
        name=campaign.name,
        campaign_type=campaign.campaign_type,
        subject=campaign.subject,
        content=campaign.content,
        template=campaign.template,
        target_criteria=campaign.target_criteria,
        scheduled_at=campaign.scheduled_at,
        status='draft' if campaign.scheduled_at else 'draft'
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign


@router.get("/campaigns", response_model=List[CampaignResponse])
async def list_campaigns(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List marketing campaigns"""
    query = db.query(MarketingCampaign)
    
    if status:
        query = query.filter(MarketingCampaign.status == status)
    
    campaigns = query.offset(skip).limit(limit).all()
    return campaigns


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific campaign"""
    campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/campaigns/{campaign_id}/send")
async def send_campaign(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """
    Send/execute a marketing campaign
    
    Targets leads based on campaign criteria
    Tracks opens and clicks for optimization
    """
    campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get target leads based on criteria
    query = db.query(Lead)
    
    # Apply targeting criteria
    if campaign.target_criteria:
        if 'status' in campaign.target_criteria:
            query = query.filter(Lead.status == campaign.target_criteria['status'])
        
        if 'website_id' in campaign.target_criteria:
            query = query.filter(Lead.website_id == campaign.target_criteria['website_id'])
    
    target_leads = query.all()
    
    # Simulate sending (in production, integrate with email service)
    sent_count = 0
    for lead in target_leads:
        # Track activity
        activity = LeadActivity(
            lead_id=lead.id,
            activity_type=f'campaign_{campaign.campaign_type}',
            description=f'Received campaign: {campaign.name}',
            metadata={
                'campaign_id': campaign.id,
                'campaign_name': campaign.name,
                'campaign_type': campaign.campaign_type
            }
        )
        db.add(activity)
        sent_count += 1
    
    # Update campaign statistics
    campaign.sent_count = sent_count
    campaign.status = 'sent'
    
    db.commit()
    
    return {
        "message": f"Campaign sent to {sent_count} leads",
        "campaign_id": campaign_id,
        "sent_count": sent_count
    }


@router.get("/analytics/overview")
async def get_analytics_overview(
    db: Session = Depends(get_db)
):
    """
    Get marketing analytics overview
    
    Returns key metrics for short cycle optimization
    """
    total_leads = db.query(Lead).count()
    new_leads = db.query(Lead).filter(Lead.status == 'new').count()
    converted_leads = db.query(Lead).filter(Lead.status == 'converted').count()
    
    total_campaigns = db.query(MarketingCampaign).count()
    active_campaigns = db.query(MarketingCampaign).filter(
        MarketingCampaign.status.in_(['scheduled', 'sent'])
    ).count()
    
    # Calculate conversion rate
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    return {
        "leads": {
            "total": total_leads,
            "new": new_leads,
            "converted": converted_leads,
            "conversion_rate": round(conversion_rate, 2)
        },
        "campaigns": {
            "total": total_campaigns,
            "active": active_campaigns
        }
    }


@router.post("/webhooks/email-open/{campaign_id}/{lead_id}")
async def track_email_open(
    campaign_id: int,
    lead_id: int,
    db: Session = Depends(get_db)
):
    """Track email open event"""
    campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
    if campaign:
        campaign.opened_count += 1
        
        # Track lead activity
        activity = LeadActivity(
            lead_id=lead_id,
            activity_type='email_opened',
            description=f'Opened email from campaign: {campaign.name}',
            metadata={'campaign_id': campaign_id}
        )
        db.add(activity)
        db.commit()
    
    return {"status": "tracked"}


@router.post("/webhooks/email-click/{campaign_id}/{lead_id}")
async def track_email_click(
    campaign_id: int,
    lead_id: int,
    db: Session = Depends(get_db)
):
    """Track email click event"""
    campaign = db.query(MarketingCampaign).filter(MarketingCampaign.id == campaign_id).first()
    if campaign:
        campaign.clicked_count += 1
        
        # Track lead activity
        activity = LeadActivity(
            lead_id=lead_id,
            activity_type='email_clicked',
            description=f'Clicked link in campaign: {campaign.name}',
            metadata={'campaign_id': campaign_id}
        )
        db.add(activity)
        db.commit()
    
    return {"status": "tracked"}
