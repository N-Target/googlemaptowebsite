"""
Google Maps and Places API integration service
"""
import googlemaps
from typing import Optional, Dict, Any
from app.core.config import settings
from app.core.settings_helper import get_api_key


class GoogleMapsService:
    """Service for interacting with Google Maps and Places API"""
    
    def __init__(self):
        self.client = None
        # Try to get API key from database first, fallback to env
        api_key = get_api_key('GOOGLE_MAPS_API_KEY') or settings.GOOGLE_MAPS_API_KEY
        if api_key:
            self.client = googlemaps.Client(key=api_key)
    
    async def search_place(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for a place using text query
        
        Args:
            query: Business name or address
            
        Returns:
            Place details or None
        """
        if not self.client:
            return None
            
        try:
            # Search for place
            result = self.client.places(query=query)
            
            if result and result.get('results'):
                place = result['results'][0]
                return place
                
        except Exception as e:
            print(f"Error searching place: {e}")
            
        return None
    
    async def get_place_details(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place
        
        Args:
            place_id: Google Place ID
            
        Returns:
            Detailed place information
        """
        if not self.client:
            return None
            
        try:
            result = self.client.place(
                place_id=place_id,
                fields=['name', 'formatted_address', 'formatted_phone_number',
                       'website', 'rating', 'types', 'geometry', 'photos',
                       'opening_hours', 'reviews']
            )
            
            if result and result.get('result'):
                return result['result']
                
        except Exception as e:
            print(f"Error getting place details: {e}")
            
        return None
    
    async def geocode_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Geocode an address to get coordinates
        
        Args:
            address: Address string
            
        Returns:
            Geocoding result with coordinates
        """
        if not self.client:
            return None
            
        try:
            result = self.client.geocode(address)
            
            if result:
                return result[0]
                
        except Exception as e:
            print(f"Error geocoding address: {e}")
            
        return None
