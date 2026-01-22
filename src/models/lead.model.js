const mongoose = require('mongoose');

const leadSchema = new mongoose.Schema({
  websiteId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Website',
    required: true
  },
  name: {
    type: String,
    required: true
  },
  email: {
    type: String,
    required: true
  },
  phone: String,
  message: String,
  source: {
    type: String,
    enum: ['contact_form', 'chat_widget', 'phone', 'voice_input'],
    default: 'contact_form'
  },
  status: {
    type: String,
    enum: ['new', 'contacted', 'qualified', 'converted', 'lost'],
    default: 'new'
  },
  score: {
    type: Number,
    min: 0,
    max: 100
  },
  metadata: {
    userAgent: String,
    ip: String,
    referrer: String,
    language: String
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Lead', leadSchema);
