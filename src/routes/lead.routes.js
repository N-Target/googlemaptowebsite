const express = require('express');
const router = express.Router();
const leadController = require('../controllers/lead.controller');
const { authenticate } = require('../middleware/auth.middleware');

// Public route for creating leads (from website contact forms)
router.post('/', leadController.createLead);

// Protected routes
router.use(authenticate);

// Get all user's leads
router.get('/', leadController.getUserLeads);

// Get leads for a specific website
router.get('/website/:websiteId', leadController.getWebsiteLeads);

// Update lead status
router.patch('/:id', leadController.updateLeadStatus);

module.exports = router;
