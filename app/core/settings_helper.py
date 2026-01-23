"""
Helper functions for accessing settings from database
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import AppSettings, AIPromptTemplate
from app.db.database import SessionLocal


def get_setting(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get a setting value from database"""
    db = SessionLocal()
    try:
        setting = db.query(AppSettings).filter(AppSettings.key == key).first()
        if setting:
            return setting.value
        return default
    finally:
        db.close()


def get_api_key(key_name: str) -> Optional[str]:
    """Get an API key from database with fallback to env"""
    from app.core.config import settings as env_settings
    
    # Try database first
    db_value = get_setting(key_name)
    if db_value:
        return db_value
    
    # Fallback to environment variable
    return getattr(env_settings, key_name, None)


def get_active_prompt(language: str = "hu", prompt_type: str = "generation") -> Optional[str]:
    """Get the active/default prompt for a language"""
    db = SessionLocal()
    try:
        # Try to get default prompt
        prompt = db.query(AIPromptTemplate).filter(
            AIPromptTemplate.language == language,
            AIPromptTemplate.prompt_type == prompt_type,
            AIPromptTemplate.is_default == True,
            AIPromptTemplate.is_active == True
        ).first()
        
        if prompt:
            return prompt.prompt_text
        
        # Fallback to any active prompt
        prompt = db.query(AIPromptTemplate).filter(
            AIPromptTemplate.language == language,
            AIPromptTemplate.prompt_type == prompt_type,
            AIPromptTemplate.is_active == True
        ).first()
        
        if prompt:
            return prompt.prompt_text
        
        return None
    finally:
        db.close()
