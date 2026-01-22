const Lead = require('../models/lead.model');
const Website = require('../models/website.model');

class LeadController {
  /**
   * Create a new lead
   */
  async createLead(req, res, next) {
    try {
      const { websiteId, name, email, phone, message, source } = req.body;

      // Verify website exists
      const website = await Website.findById(websiteId);
      if (!website) {
        return res.status(404).json({ error: 'Website not found' });
      }

      const lead = new Lead({
        websiteId,
        name,
        email,
        phone,
        message,
        source: source || 'contact_form',
        metadata: {
          userAgent: req.headers['user-agent'],
          ip: req.ip,
          referrer: req.headers.referer,
          language: req.headers['accept-language']
        }
      });

      await lead.save();

      // Update website analytics
      await Website.findByIdAndUpdate(websiteId, {
        $inc: { 'analytics.leads': 1 }
      });

      res.status(201).json({
        success: true,
        message: 'Lead created successfully',
        data: lead
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get leads for a website
   */
  async getWebsiteLeads(req, res, next) {
    try {
      const { websiteId } = req.params;
      const { page = 1, limit = 20, status } = req.query;

      // Verify website ownership
      const website = await Website.findById(websiteId);
      if (!website) {
        return res.status(404).json({ error: 'Website not found' });
      }

      if (website.userId.toString() !== req.user.id) {
        return res.status(403).json({ error: 'Access denied' });
      }

      const query = { websiteId };
      if (status) query.status = status;

      const leads = await Lead.find(query)
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(parseInt(limit));

      const total = await Lead.countDocuments(query);

      res.json({
        success: true,
        data: leads,
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
   * Update lead status
   */
  async updateLeadStatus(req, res, next) {
    try {
      const { id } = req.params;
      const { status, score } = req.body;

      const lead = await Lead.findById(id).populate('websiteId');
      if (!lead) {
        return res.status(404).json({ error: 'Lead not found' });
      }

      if (lead.websiteId.userId.toString() !== req.user.id) {
        return res.status(403).json({ error: 'Access denied' });
      }

      if (status) lead.status = status;
      if (score !== undefined) lead.score = score;

      await lead.save();

      res.json({
        success: true,
        message: 'Lead updated successfully',
        data: lead
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get all leads for user
   */
  async getUserLeads(req, res, next) {
    try {
      const userId = req.user.id;
      const { page = 1, limit = 20 } = req.query;

      // Get all user's websites
      const websites = await Website.find({ userId }).select('_id');
      const websiteIds = websites.map(w => w._id);

      const leads = await Lead.find({ websiteId: { $in: websiteIds } })
        .populate('websiteId', 'businessName url')
        .sort({ createdAt: -1 })
        .skip((page - 1) * limit)
        .limit(parseInt(limit));

      const total = await Lead.countDocuments({ websiteId: { $in: websiteIds } });

      res.json({
        success: true,
        data: leads,
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
}

module.exports = new LeadController();
