"""
Data models for website generation and lead management
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class GeneratedWebsite(Base):
    """Model for generated websites"""
    __tablename__ = "generated_websites"
    
    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(255), nullable=False)
    google_place_id = Column(String(255), unique=True, index=True)
    
    # Location data
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Business details
    phone = Column(String(50))
    website_url = Column(String(500))
    rating = Column(Float)
    business_type = Column(String(100))
    
    # Generated content
    generated_html = Column(Text)
    generated_css = Column(Text)
    seo_meta = Column(JSON)
    
    # Language and localization
    language = Column(String(5), default="hu")
    
    # Status
    status = Column(String(20), default="draft")  # draft, published, archived
    published_url = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    leads = relationship("Lead", back_populates="website")
    widgets = relationship("Widget", back_populates="website")


class Lead(Base):
    """Model for lead management"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("generated_websites.id"))
    
    # Contact information
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50))
    
    # Lead details
    message = Column(Text)
    source = Column(String(100))  # widget type, form, etc.
    status = Column(String(20), default="new")  # new, contacted, converted, lost
    
    # Marketing automation
    tags = Column(JSON)
    custom_fields = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    website = relationship("GeneratedWebsite", back_populates="leads")
    activities = relationship("LeadActivity", back_populates="lead")


class Widget(Base):
    """Model for interactive widgets"""
    __tablename__ = "widgets"
    
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("generated_websites.id"))
    
    # Widget configuration
    widget_type = Column(String(50), nullable=False)  # contact_form, chatbot, booking, etc.
    name = Column(String(255))
    configuration = Column(JSON)
    
    # Display settings
    position = Column(String(50))  # top, bottom, sidebar, popup
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    website = relationship("GeneratedWebsite", back_populates="widgets")


class LeadActivity(Base):
    """Model for tracking lead activities (marketing automation)"""
    __tablename__ = "lead_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    
    # Activity details
    activity_type = Column(String(50), nullable=False)  # email_sent, page_view, form_submit, etc.
    description = Column(Text)
    metadata = Column(JSON)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="activities")


class MarketingCampaign(Base):
    """Model for marketing automation campaigns"""
    __tablename__ = "marketing_campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Campaign details
    name = Column(String(255), nullable=False)
    campaign_type = Column(String(50))  # email, sms, notification
    
    # Content
    subject = Column(String(500))
    content = Column(Text)
    template = Column(String(100))
    
    # Targeting
    target_criteria = Column(JSON)
    
    # Schedule
    scheduled_at = Column(DateTime)
    status = Column(String(20), default="draft")  # draft, scheduled, sent, completed
    
    # Statistics
    sent_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
