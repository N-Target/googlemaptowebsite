const express = require('express');
const router = express.Router();
const websiteController = require('../controllers/website.controller');
const { authenticate } = require('../middleware/auth.middleware');

// All routes require authentication
router.use(authenticate);

// Generate new website
router.post('/generate', websiteController.generateWebsite);

// Get user's websites
router.get('/', websiteController.getUserWebsites);

// Get single website
router.get('/:id', websiteController.getWebsite);

// Update website
router.put('/:id', websiteController.updateWebsite);

// Delete website
router.delete('/:id', websiteController.deleteWebsite);

// Get website analytics
router.get('/:id/analytics', websiteController.getAnalytics);

module.exports = router;
