const express = require('express');
const router = express.Router();
const subscriptionController = require('../controllers/subscription.controller');
const { authenticate } = require('../middleware/auth.middleware');

// Public route to view plans
router.get('/plans', subscriptionController.getPlans);

// Protected routes
router.use(authenticate);

// Get current subscription
router.get('/current', subscriptionController.getCurrentSubscription);

// Upgrade subscription
router.post('/upgrade', subscriptionController.upgradeSubscription);

// Cancel subscription
router.post('/cancel', subscriptionController.cancelSubscription);

module.exports = router;
