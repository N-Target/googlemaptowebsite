const axios = require('axios');

class GoogleMapsService {
  constructor() {
    this.apiKey = process.env.GOOGLE_MAPS_API_KEY;
    this.baseUrl = 'https://maps.googleapis.com/maps/api';
  }

  /**
   * Search for a business by name and location
   */
  async searchBusiness(businessName, location) {
    try {
      const response = await axios.get(`${this.baseUrl}/place/findplacefromtext/json`, {
        params: {
          input: `${businessName} ${location}`,
          inputtype: 'textquery',
          fields: 'place_id,name,formatted_address,rating,user_ratings_total',
          key: this.apiKey
        }
      });

      if (response.data.status === 'OK' && response.data.candidates.length > 0) {
        return response.data.candidates[0];
      }
      
      throw new Error('Business not found');
    } catch (error) {
      console.error('Google Maps Search Error:', error);
      throw error;
    }
  }

  /**
   * Get detailed information about a place
   */
  async getPlaceDetails(placeId) {
    try {
      const response = await axios.get(`${this.baseUrl}/place/details/json`, {
        params: {
          place_id: placeId,
          fields: 'name,formatted_address,formatted_phone_number,opening_hours,rating,user_ratings_total,photos,reviews,website,types',
          key: this.apiKey
        }
      });

      if (response.data.status === 'OK') {
        return this.formatPlaceData(response.data.result);
      }
      
      throw new Error('Place details not found');
    } catch (error) {
      console.error('Google Maps Details Error:', error);
      throw error;
    }
  }

  /**
   * Get place photos
   */
  async getPlacePhotos(photoReferences, maxPhotos = 5) {
    const photos = [];
    const refsToFetch = photoReferences.slice(0, maxPhotos);

    for (const photoRef of refsToFetch) {
      const photoUrl = `${this.baseUrl}/place/photo?maxwidth=800&photoreference=${photoRef.photo_reference}&key=${this.apiKey}`;
      photos.push(photoUrl);
    }

    return photos;
  }

  /**
   * Format place data for internal use
   */
  formatPlaceData(placeData) {
    return {
      placeId: placeData.place_id,
      name: placeData.name,
      address: placeData.formatted_address,
      phone: placeData.formatted_phone_number,
      website: placeData.website,
      rating: placeData.rating,
      reviewCount: placeData.user_ratings_total,
      businessTypes: placeData.types,
      hours: placeData.opening_hours,
      photos: placeData.photos ? placeData.photos.map(p => p.photo_reference) : [],
      reviews: placeData.reviews ? placeData.reviews.slice(0, 5) : []
    };
  }

  /**
   * Extract business category from types
   */
  extractBusinessCategory(types) {
    const categoryMap = {
      'hair_care': 'beauty',
      'beauty_salon': 'beauty',
      'spa': 'beauty',
      'car_repair': 'auto_repair',
      'car_dealer': 'auto_repair',
      'restaurant': 'restaurant',
      'cafe': 'restaurant',
      'store': 'retail'
    };

    for (const type of types) {
      if (categoryMap[type]) {
        return categoryMap[type];
      }
    }

    return 'other';
  }
}

module.exports = new GoogleMapsService();
