const mongoose = require('mongoose');

const websiteSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  businessName: {
    type: String,
    required: true
  },
  businessType: {
    type: String,
    enum: ['beauty', 'auto_repair', 'restaurant', 'retail', 'other'],
    required: true
  },
  googleMapsData: {
    placeId: String,
    address: String,
    phone: String,
    rating: Number,
    reviews: Number,
    photos: [String],
    hours: Object
  },
  generatedContent: {
    headline: String,
    description: String,
    services: [String],
    features: [String],
    testimonials: [Object],
    pricing: Object
  },
  design: {
    template: {
      type: String,
      default: 'luxury'
    },
    colors: {
      primary: String,
      secondary: String,
      accent: String
    },
    images: [String],
    layout: String
  },
  seo: {
    title: String,
    description: String,
    keywords: [String]
  },
  status: {
    type: String,
    enum: ['draft', 'generating', 'published', 'archived'],
    default: 'draft'
  },
  language: {
    type: String,
    default: 'hu'
  },
  url: String,
  analytics: {
    views: { type: Number, default: 0 },
    leads: { type: Number, default: 0 },
    conversionRate: { type: Number, default: 0 }
  },
  aiMetadata: {
    model: String,
    tokensUsed: Number,
    generationTime: Number,
    complexity: String
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Website', websiteSchema);
