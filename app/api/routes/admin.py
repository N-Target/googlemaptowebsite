"""
Admin API routes for settings and configuration management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.models.models import AppSettings, AIPromptTemplate
from app.db.database import get_db

router = APIRouter()


# Pydantic schemas
class SettingCreate(BaseModel):
    key: str
    value: str
    category: str = "general"
    description: Optional[str] = None
    is_secret: bool = False


class SettingResponse(BaseModel):
    id: int
    key: str
    value: Optional[str] = None  # Hidden if is_secret
    category: str
    description: Optional[str]
    is_secret: bool
    
    class Config:
        from_attributes = True


class PromptTemplateCreate(BaseModel):
    name: str
    language: str = "hu"
    prompt_type: str = "generation"
    prompt_text: str
    variables: Optional[dict] = None
    is_active: bool = True
    is_default: bool = False


class PromptTemplateResponse(BaseModel):
    id: int
    name: str
    language: str
    prompt_type: str
    prompt_text: str
    variables: Optional[dict]
    is_active: bool
    is_default: bool
    
    class Config:
        from_attributes = True


# Settings endpoints
@router.get("/settings", response_model=List[SettingResponse])
async def list_settings(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all application settings"""
    query = db.query(AppSettings)
    
    if category:
        query = query.filter(AppSettings.category == category)
    
    settings = query.all()
    
    # Hide secret values in response
    result = []
    for setting in settings:
        setting_dict = {
            "id": setting.id,
            "key": setting.key,
            "value": "***" if setting.is_secret else setting.value,
            "category": setting.category,
            "description": setting.description,
            "is_secret": setting.is_secret
        }
        result.append(SettingResponse(**setting_dict))
    
    return result


@router.post("/settings", response_model=SettingResponse)
async def create_or_update_setting(
    setting: SettingCreate,
    db: Session = Depends(get_db)
):
    """Create or update a setting"""
    # Check if setting exists
    existing = db.query(AppSettings).filter(AppSettings.key == setting.key).first()
    
    if existing:
        # Update existing
        existing.value = setting.value
        existing.category = setting.category
        existing.description = setting.description
        existing.is_secret = setting.is_secret
        db.commit()
        db.refresh(existing)
        
        return SettingResponse(
            id=existing.id,
            key=existing.key,
            value="***" if existing.is_secret else existing.value,
            category=existing.category,
            description=existing.description,
            is_secret=existing.is_secret
        )
    else:
        # Create new
        db_setting = AppSettings(
            key=setting.key,
            value=setting.value,
            category=setting.category,
            description=setting.description,
            is_secret=setting.is_secret
        )
        db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        
        return SettingResponse(
            id=db_setting.id,
            key=db_setting.key,
            value="***" if db_setting.is_secret else db_setting.value,
            category=db_setting.category,
            description=db_setting.description,
            is_secret=db_setting.is_secret
        )


@router.get("/settings/{key}")
async def get_setting(
    key: str,
    db: Session = Depends(get_db)
):
    """Get a specific setting by key"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    return {
        "id": setting.id,
        "key": setting.key,
        "value": "***" if setting.is_secret else setting.value,
        "category": setting.category,
        "description": setting.description,
        "is_secret": setting.is_secret
    }


@router.delete("/settings/{key}")
async def delete_setting(
    key: str,
    db: Session = Depends(get_db)
):
    """Delete a setting"""
    setting = db.query(AppSettings).filter(AppSettings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    db.delete(setting)
    db.commit()
    
    return {"message": "Setting deleted successfully"}


# Prompt template endpoints
@router.get("/prompts", response_model=List[PromptTemplateResponse])
async def list_prompts(
    language: Optional[str] = None,
    prompt_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """List all AI prompt templates"""
    query = db.query(AIPromptTemplate)
    
    if language:
        query = query.filter(AIPromptTemplate.language == language)
    if prompt_type:
        query = query.filter(AIPromptTemplate.prompt_type == prompt_type)
    if is_active is not None:
        query = query.filter(AIPromptTemplate.is_active == is_active)
    
    prompts = query.all()
    return prompts


@router.post("/prompts", response_model=PromptTemplateResponse)
async def create_prompt(
    prompt: PromptTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new prompt template"""
    # If this is set as default, unset other defaults for this language and type
    if prompt.is_default:
        db.query(AIPromptTemplate).filter(
            AIPromptTemplate.language == prompt.language,
            AIPromptTemplate.prompt_type == prompt.prompt_type
        ).update({"is_default": False})
    
    db_prompt = AIPromptTemplate(
        name=prompt.name,
        language=prompt.language,
        prompt_type=prompt.prompt_type,
        prompt_text=prompt.prompt_text,
        variables=prompt.variables,
        is_active=prompt.is_active,
        is_default=prompt.is_default
    )
    
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    
    return db_prompt


@router.get("/prompts/{prompt_id}", response_model=PromptTemplateResponse)
async def get_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific prompt template"""
    prompt = db.query(AIPromptTemplate).filter(AIPromptTemplate.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt template not found")
    
    return prompt


@router.put("/prompts/{prompt_id}", response_model=PromptTemplateResponse)
async def update_prompt(
    prompt_id: int,
    prompt_update: PromptTemplateCreate,
    db: Session = Depends(get_db)
):
    """Update a prompt template"""
    prompt = db.query(AIPromptTemplate).filter(AIPromptTemplate.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt template not found")
    
    # If this is set as default, unset other defaults for this language and type
    if prompt_update.is_default:
        db.query(AIPromptTemplate).filter(
            AIPromptTemplate.language == prompt_update.language,
            AIPromptTemplate.prompt_type == prompt_update.prompt_type,
            AIPromptTemplate.id != prompt_id
        ).update({"is_default": False})
    
    prompt.name = prompt_update.name
    prompt.language = prompt_update.language
    prompt.prompt_type = prompt_update.prompt_type
    prompt.prompt_text = prompt_update.prompt_text
    prompt.variables = prompt_update.variables
    prompt.is_active = prompt_update.is_active
    prompt.is_default = prompt_update.is_default
    
    db.commit()
    db.refresh(prompt)
    
    return prompt


@router.delete("/prompts/{prompt_id}")
async def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):
    """Delete a prompt template"""
    prompt = db.query(AIPromptTemplate).filter(AIPromptTemplate.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt template not found")
    
    db.delete(prompt)
    db.commit()
    
    return {"message": "Prompt template deleted successfully"}


@router.get("/dashboard/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    from app.models.models import GeneratedWebsite, Lead, Widget, MarketingCampaign
    
    total_websites = db.query(GeneratedWebsite).count()
    total_leads = db.query(Lead).count()
    total_widgets = db.query(Widget).count()
    total_campaigns = db.query(MarketingCampaign).count()
    
    # Recent activity
    recent_websites = db.query(GeneratedWebsite).order_by(
        GeneratedWebsite.created_at.desc()
    ).limit(5).all()
    
    recent_leads = db.query(Lead).order_by(
        Lead.created_at.desc()
    ).limit(5).all()
    
    return {
        "stats": {
            "total_websites": total_websites,
            "total_leads": total_leads,
            "total_widgets": total_widgets,
            "total_campaigns": total_campaigns
        },
        "recent_websites": [
            {
                "id": w.id,
                "business_name": w.business_name,
                "language": w.language,
                "status": w.status,
                "created_at": w.created_at.isoformat()
            } for w in recent_websites
        ],
        "recent_leads": [
            {
                "id": l.id,
                "name": l.name,
                "email": l.email,
                "status": l.status,
                "created_at": l.created_at.isoformat()
            } for l in recent_leads
        ]
    }
