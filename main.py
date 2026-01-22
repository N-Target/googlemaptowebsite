"""
Google Map to Website - AI-Based Website Generator and Lead Generation System
Main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.api.routes import website_generator, leads, widgets, marketing
from app.core.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup resources"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="Google Map to Website - AI Generator",
    description="AI-alapú automatizált weboldal-generáló és lead-szerző rendszer",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for EU deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(website_generator.router, prefix="/api/v1/generator", tags=["Website Generator"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Lead Management"])
app.include_router(widgets.router, prefix="/api/v1/widgets", tags=["Interactive Widgets"])
app.include_router(marketing.router, prefix="/api/v1/marketing", tags=["Marketing Automation"])

# Static files for generated websites
os.makedirs("static/generated", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Google Map to Website - AI Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "supported_languages": settings.SUPPORTED_LANGUAGES
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.APP_ENV == "development"
    )
