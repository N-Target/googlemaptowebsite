const User = require('../models/user.model');
const jwt = require('jsonwebtoken');

class AuthController {
  /**
   * Register a new user
   */
  async register(req, res, next) {
    try {
      const { email, password, name, businessName, language } = req.body;

      // Check if user exists
      const existingUser = await User.findOne({ email });
      if (existingUser) {
        return res.status(400).json({ error: 'User already exists' });
      }

      // Create new user with starter plan
      const user = new User({
        email,
        password,
        name,
        businessName,
        language: language || 'hu',
        subscription: {
          plan: 'starter',
          status: 'active',
          tokensUsed: 0,
          tokensLimit: 1000,
          startDate: new Date()
        }
      });

      await user.save();

      // Generate token
      const token = this.generateToken(user);

      res.status(201).json({
        success: true,
        message: 'User registered successfully',
        data: {
          user: this.sanitizeUser(user),
          token
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Login user
   */
  async login(req, res, next) {
    try {
      const { email, password } = req.body;

      // Find user
      const user = await User.findOne({ email });
      if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }

      // Check password
      const isMatch = await user.comparePassword(password);
      if (!isMatch) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }

      // Generate token
      const token = this.generateToken(user);

      res.json({
        success: true,
        data: {
          user: this.sanitizeUser(user),
          token
        }
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get current user
   */
  async getCurrentUser(req, res, next) {
    try {
      const user = await User.findById(req.user.id);
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }

      res.json({
        success: true,
        data: this.sanitizeUser(user)
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Generate JWT token
   */
  generateToken(user) {
    return jwt.sign(
      { id: user._id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '7d' }
    );
  }

  /**
   * Remove sensitive data from user object
   */
  sanitizeUser(user) {
    const userObj = user.toObject();
    delete userObj.password;
    return userObj;
  }
}

module.exports = new AuthController();
