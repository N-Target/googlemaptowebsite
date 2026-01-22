const websiteGeneratorService = require('../services/website-generator.service');
const Website = require('../models/website.model');

class WebsiteController {
  /**
   * Generate a new website
   */
  async generateWebsite(req, res, next) {
    try {
      const userId = req.user.id;
      const { businessName, location, placeId, businessType, language } = req.body;

      if (!businessName && !placeId) {
        return res.status(400).json({ 
          error: 'Either businessName with location or placeId is required' 
        });
      }

      const website = await websiteGeneratorService.generateWebsite(userId, {
        businessName,
        location,
        placeId,
        businessType
      }, { language });

      res.status(201).json({
        success: true,
        message: 'Website generated successfully',
        data: website
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get user's websites
   */
  async getUserWebsites(req, res, next) {
    try {
      const userId = req.user.id;
      const { page = 1, limit = 10, status } = req.query;

      const query = { userId };
      if (status) query.status = status;

      const websites = await Website.find(query)
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(parseInt(limit));

      const total = await Website.countDocuments(query);

      res.json({
        success: true,
        data: websites,
        pagination: {
          page: parseInt(page),
          limit: parseInt(limit),
          total,
          pages: Math.ceil(total / limit)
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get single website
   */
  async getWebsite(req, res, next) {
    try {
      const { id } = req.params;
      const website = await Website.findById(id);

      if (!website) {
        return res.status(404).json({ error: 'Website not found' });
      }

      // Check ownership
      if (website.userId.toString() !== req.user.id) {
        return res.status(403).json({ error: 'Access denied' });
      }

      res.json({
        success: true,
        data: website
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Update website
   */
  async updateWebsite(req, res, next) {
    try {
      const { id } = req.params;
      const updates = req.body;

      const website = await Website.findById(id);
      if (!website) {
        return res.status(404).json({ error: 'Website not found' });
      }

      if (website.userId.toString() !== req.user.id) {
        return res.status(403).json({ error: 'Access denied' });
      }

      Object.assign(website, updates);
      await website.save();

      res.json({
        success: true,
        message: 'Website updated successfully',
        data: website
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete website
   */
  async deleteWebsite(req, res, next) {
    try {
      const { id } = req.params;
      const website = await Website.findById(id);

      if (!website) {
        return res.status(404).json({ error: 'Website not found' });
      }

      if (website.userId.toString() !== req.user.id) {
        return res.status(403).json({ error: 'Access denied' });
      }

      await website.deleteOne();

      res.json({
        success: true,
        message: 'Website deleted successfully'
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get website analytics
   */
  async getAnalytics(req, res, next) {
    try {
      const { id } = req.params;
      const website = await Website.findById(id);

      if (!website) {
        return res.status(404).json({ error: 'Website not found' });
      }

      if (website.userId.toString() !== req.user.id) {
        return res.status(403).json({ error: 'Access denied' });
      }

      res.json({
        success: true,
        data: {
          views: website.analytics.views,
          leads: website.analytics.leads,
          conversionRate: website.analytics.conversionRate,
          aiCost: website.aiMetadata.tokensUsed
        }
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new WebsiteController();
