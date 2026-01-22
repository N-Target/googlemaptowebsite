"""
Website generator API routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os

from app.models.schemas import WebsiteGenerateRequest, WebsiteResponse
from app.models.models import GeneratedWebsite
from app.db.database import get_db
from app.services.google_maps_service import GoogleMapsService
from app.services.ai_generator import AIWebsiteGenerator

router = APIRouter()


@router.post("/generate", response_model=WebsiteResponse)
async def generate_website(
    request: WebsiteGenerateRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a website based on Google Maps business data
    
    This endpoint creates a complete website with AI-generated content,
    optimized for the specified language (default: Hungarian)
    """
    google_service = GoogleMapsService()
    ai_generator = AIWebsiteGenerator()
    
    # Search for business on Google Maps
    place_data = None
    if request.google_place_id:
        place_data = await google_service.get_place_details(request.google_place_id)
    elif request.business_name or request.address:
        query = request.business_name or request.address
        place = await google_service.search_place(query)
        if place:
            place_data = await google_service.get_place_details(place['place_id'])
    
    # Extract business information
    business_info = {}
    if place_data:
        business_info = {
            'name': place_data.get('name', request.business_name or 'Business'),
            'address': place_data.get('formatted_address', request.address or ''),
            'phone': place_data.get('formatted_phone_number', ''),
            'website': place_data.get('website', ''),
            'rating': place_data.get('rating'),
            'business_type': place_data.get('types', ['business'])[0] if place_data.get('types') else 'business',
            'place_id': place_data.get('place_id', request.google_place_id),
            'latitude': place_data.get('geometry', {}).get('location', {}).get('lat'),
            'longitude': place_data.get('geometry', {}).get('location', {}).get('lng')
        }
    else:
        business_info = {
            'name': request.business_name or 'Business',
            'address': request.address or '',
            'phone': '',
            'website': '',
            'rating': None,
            'business_type': 'business',
            'place_id': request.google_place_id
        }
    
    # Generate website content using AI
    generated_content = await ai_generator.generate_website_content(
        business_info,
        request.language
    )
    
    # Create database entry
    website = GeneratedWebsite(
        business_name=business_info['name'],
        google_place_id=business_info.get('place_id'),
        address=business_info['address'],
        latitude=business_info.get('latitude'),
        longitude=business_info.get('longitude'),
        phone=business_info['phone'],
        website_url=business_info['website'],
        rating=business_info.get('rating'),
        business_type=business_info['business_type'],
        generated_html=generated_content['html'],
        generated_css=generated_content['css'],
        seo_meta={
            'title': generated_content.get('seo_title', business_info['name']),
            'description': generated_content.get('seo_description', '')
        },
        language=request.language,
        status='draft'
    )
    
    db.add(website)
    db.commit()
    db.refresh(website)
    
    # Save generated files
    output_dir = f"static/generated/{website.id}"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(generated_content['html'])
    
    with open(f"{output_dir}/styles.css", 'w', encoding='utf-8') as f:
        f.write(generated_content['css'])
    
    website.published_url = f"/static/generated/{website.id}/index.html"
    website.status = 'published'
    db.commit()
    db.refresh(website)
    
    return website


@router.get("/websites", response_model=List[WebsiteResponse])
async def list_websites(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all generated websites"""
    websites = db.query(GeneratedWebsite).offset(skip).limit(limit).all()
    return websites


@router.get("/websites/{website_id}", response_model=WebsiteResponse)
async def get_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific generated website"""
    website = db.query(GeneratedWebsite).filter(GeneratedWebsite.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    return website


@router.delete("/websites/{website_id}")
async def delete_website(
    website_id: int,
    db: Session = Depends(get_db)
):
    """Delete a generated website"""
    website = db.query(GeneratedWebsite).filter(GeneratedWebsite.id == website_id).first()
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")
    
    db.delete(website)
    db.commit()
    
    return {"message": "Website deleted successfully"}
