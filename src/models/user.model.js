const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true
  },
  name: String,
  businessName: String,
  subscription: {
    plan: {
      type: String,
      enum: ['starter', 'a-plan', 'b-plan', 'luxury-leap'],
      default: 'starter'
    },
    status: {
      type: String,
      enum: ['active', 'inactive', 'cancelled'],
      default: 'active'
    },
    tokensUsed: {
      type: Number,
      default: 0
    },
    tokensLimit: {
      type: Number,
      default: 1000
    },
    startDate: Date,
    endDate: Date
  },
  language: {
    type: String,
    default: 'hu'
  },
  preferences: {
    industry: String,
    notifications: {
      email: { type: Boolean, default: true },
      sms: { type: Boolean, default: false }
    }
  }
}, {
  timestamps: true
});

// Hash password before saving
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

// Compare password method
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password);
};

module.exports = mongoose.model('User', userSchema);
