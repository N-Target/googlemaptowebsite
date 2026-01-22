"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    GOOGLE_MAPS_API_KEY: str = ""
    GOOGLE_PLACES_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "sqlite:///./googlemaptowebsite.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Application
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-this-in-production"
    API_VERSION: str = "v1"
    
    # Localization - Hungary and EU focus
    DEFAULT_LANGUAGE: str = "hu"
    SUPPORTED_LANGUAGES: List[str] = ["hu", "en", "de", "fr", "es", "it"]
    
    # AI Configuration
    AI_MODEL: str = "gpt-4"
    AI_TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 2000
    
    # Marketing
    EMAIL_SENDER: str = "noreply@yourdomain.com"
    EMAIL_SMTP_HOST: str = "smtp.gmail.com"
    EMAIL_SMTP_PORT: int = 587
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
