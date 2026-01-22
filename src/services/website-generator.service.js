const Website = require('../models/website.model');
const aiService = require('./ai.service');
const googleMapsService = require('./googlemaps.service');
const User = require('../models/user.model');

class WebsiteGeneratorService {
  /**
   * Generate a complete website from Google Maps data
   */
  async generateWebsite(userId, businessData, options = {}) {
    try {
      // Check user's token quota
      await this.checkTokenQuota(userId);

      // Fetch Google Maps data
      let mapsData;
      if (businessData.placeId) {
        mapsData = await googleMapsService.getPlaceDetails(businessData.placeId);
      } else {
        const searchResult = await googleMapsService.searchBusiness(
          businessData.businessName,
          businessData.location
        );
        mapsData = await googleMapsService.getPlaceDetails(searchResult.place_id);
      }

      // Determine business category
      const businessType = businessData.businessType || 
        googleMapsService.extractBusinessCategory(mapsData.businessTypes);

      // Get photos
      const photos = mapsData.photos.length > 0 
        ? await googleMapsService.getPlacePhotos(mapsData.photos)
        : [];

      // Generate AI content
      const aiCopy = await aiService.generateWebsiteCopy({
        businessName: mapsData.name,
        businessType,
        address: mapsData.address,
        rating: mapsData.rating,
        services: this.extractServices(mapsData)
      }, options.language || 'hu');

      const copyContent = JSON.parse(aiCopy.content);

      // Create website document
      const website = new Website({
        userId,
        businessName: mapsData.name,
        businessType,
        googleMapsData: {
          placeId: mapsData.placeId,
          address: mapsData.address,
          phone: mapsData.phone,
          rating: mapsData.rating,
          reviews: mapsData.reviewCount,
          photos,
          hours: mapsData.hours
        },
        generatedContent: {
          headline: copyContent.headline,
          description: copyContent.description,
          features: copyContent.features,
          services: this.extractServices(mapsData),
          testimonials: this.formatReviews(mapsData.reviews)
        },
        design: {
          template: 'luxury',
          colors: this.selectColors(businessType),
          images: photos,
          layout: 'modern'
        },
        seo: {
          title: `${mapsData.name} - ${copyContent.headline}`,
          description: copyContent.description,
          keywords: this.generateKeywords(mapsData, businessType)
        },
        status: 'published',
        language: options.language || 'hu',
        url: this.generateUrl(mapsData.name),
        aiMetadata: aiCopy.metadata
      });

      await website.save();

      // Update user token usage
      await this.updateTokenUsage(userId, aiCopy.metadata.tokensUsed);

      return website;
    } catch (error) {
      console.error('Website Generation Error:', error);
      throw error;
    }
  }

  /**
   * Check if user has enough tokens
   */
  async checkTokenQuota(userId) {
    const user = await User.findById(userId);
    if (!user) throw new Error('User not found');

    const { plan, tokensUsed, tokensLimit } = user.subscription;
    
    if (plan !== 'b-plan' && plan !== 'luxury-leap') {
      if (tokensUsed >= tokensLimit) {
        throw new Error('Token quota exceeded. Please upgrade your plan.');
      }
    }

    return true;
  }

  /**
   * Update user token usage
   */
  async updateTokenUsage(userId, tokensUsed) {
    await User.findByIdAndUpdate(userId, {
      $inc: { 'subscription.tokensUsed': tokensUsed }
    });
  }

  /**
   * Extract services from business data
   */
  extractServices(mapsData) {
    const services = [];
    
    if (mapsData.businessTypes) {
      mapsData.businessTypes.forEach(type => {
        const formatted = type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        services.push(formatted);
      });
    }

    return services.slice(0, 5);
  }

  /**
   * Format reviews as testimonials
   */
  formatReviews(reviews) {
    return reviews.map(review => ({
      author: review.author_name,
      rating: review.rating,
      text: review.text,
      date: review.time
    }));
  }

  /**
   * Select colors based on business type
   */
  selectColors(businessType) {
    const colorSchemes = {
      beauty: {
        primary: '#E91E63',
        secondary: '#F8BBD0',
        accent: '#880E4F'
      },
      auto_repair: {
        primary: '#2196F3',
        secondary: '#BBDEFB',
        accent: '#0D47A1'
      },
      restaurant: {
        primary: '#FF5722',
        secondary: '#FFCCBC',
        accent: '#BF360C'
      },
      default: {
        primary: '#9C27B0',
        secondary: '#E1BEE7',
        accent: '#4A148C'
      }
    };

    return colorSchemes[businessType] || colorSchemes.default;
  }

  /**
   * Generate SEO keywords
   */
  generateKeywords(mapsData, businessType) {
    const keywords = [
      mapsData.name,
      businessType,
      mapsData.address ? mapsData.address.split(',')[1]?.trim() : '',
      'professional',
      'local'
    ].filter(Boolean);

    return keywords;
  }

  /**
   * Generate URL slug from business name
   */
  generateUrl(businessName) {
    return businessName
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }
}

module.exports = new WebsiteGeneratorService();
