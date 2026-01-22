const User = require('../models/user.model');

class SubscriptionController {
  /**
   * Get subscription plans
   */
  async getPlans(req, res, next) {
    try {
      const plans = {
        starter: {
          name: 'Starter',
          price: 0,
          currency: 'HUF',
          tokens: 1000,
          features: [
            'Ingyenes demo',
            '1 weboldal',
            'Alapvető AI funkciók',
            'Email támogatás'
          ],
          type: 'free'
        },
        'a-plan': {
          name: 'A-Plan',
          price: 49900,
          currency: 'HUF',
          tokens: 50000,
          features: [
            'Egyszeri díj',
            '5 weboldal',
            'Teljes AI funkciók',
            'Google Maps integráció',
            'Email és telefon támogatás'
          ],
          type: 'one-time'
        },
        'b-plan': {
          name: 'B-Plan',
          price: 29900,
          currency: 'HUF',
          tokens: 'unlimited',
          features: [
            'Havi előfizetés',
            'Korlátlan weboldalak',
            'Korlátlan AI tokenek',
            'Trend analízis',
            'Prémium sablonok',
            'Prioritás támogatás'
          ],
          type: 'monthly'
        },
        'luxury-leap': {
          name: 'Luxury Leap',
          price: 99900,
          currency: 'HUF',
          tokens: 'unlimited',
          features: [
            'Havi előfizetés',
            'Minden B-Plan funkció',
            'Dedikált account manager',
            'Egyedi fejlesztések',
            'White-label opció',
            '24/7 támogatás'
          ],
          type: 'monthly'
        }
      };

      res.json({
        success: true,
        data: plans
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Upgrade subscription
   */
  async upgradeSubscription(req, res, next) {
    try {
      const userId = req.user.id;
      const { plan } = req.body;

      const validPlans = ['starter', 'a-plan', 'b-plan', 'luxury-leap'];
      if (!validPlans.includes(plan)) {
        return res.status(400).json({ error: 'Invalid plan' });
      }

      const user = await User.findById(userId);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      // Set token limits based on plan
      const tokenLimits = {
        'starter': 1000,
        'a-plan': 50000,
        'b-plan': -1, // unlimited
        'luxury-leap': -1 // unlimited
      };

      user.subscription.plan = plan;
      user.subscription.tokensLimit = tokenLimits[plan];
      user.subscription.startDate = new Date();
      
      if (plan === 'b-plan' || plan === 'luxury-leap') {
        user.subscription.endDate = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000); // 30 days
      } else if (plan === 'a-plan') {
        user.subscription.endDate = null; // lifetime
      }

      await user.save();

      res.json({
        success: true,
        message: 'Subscription upgraded successfully',
        data: {
          plan: user.subscription.plan,
          tokensLimit: user.subscription.tokensLimit,
          endDate: user.subscription.endDate
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get current subscription
   */
  async getCurrentSubscription(req, res, next) {
    try {
      const user = await User.findById(req.user.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({
        success: true,
        data: {
          plan: user.subscription.plan,
          status: user.subscription.status,
          tokensUsed: user.subscription.tokensUsed,
          tokensLimit: user.subscription.tokensLimit,
          startDate: user.subscription.startDate,
          endDate: user.subscription.endDate
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Cancel subscription
   */
  async cancelSubscription(req, res, next) {
    try {
      const user = await User.findById(req.user.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      user.subscription.status = 'cancelled';
      await user.save();

      res.json({
        success: true,
        message: 'Subscription cancelled successfully'
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new SubscriptionController();
