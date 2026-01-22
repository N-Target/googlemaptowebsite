# Quick Start Guide

Get your AI-powered website generator up and running in 5 minutes!

## Prerequisites

Before you begin, ensure you have:
- ✅ Node.js 18+ installed
- ✅ Python 3.9+ installed  
- ✅ MongoDB running locally or accessible
- ✅ API Keys ready:
  - OpenAI API key
  - Google Gemini API key
  - Google Maps API key

## Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/N-Target/googlemaptowebsite.git
cd googlemaptowebsite

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

## Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env
```

Required configuration:
```env
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
GOOGLE_MAPS_API_KEY=your-google-maps-key-here
MONGODB_URI=mongodb://localhost:27017/googlemaptowebsite
JWT_SECRET=your-secure-random-string-here
```

## Step 3: Start MongoDB

```bash
# On Linux/Mac
sudo systemctl start mongod

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:6.0
```

## Step 4: Start the Application

```bash
# Development mode (with auto-reload)
npm run dev

# Or production mode
npm start
```

You should see:
```
🚀 Server running on port 3000
📍 Environment: development
✅ Connected to MongoDB
```

## Step 5: Test the API

### Register a User

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User",
    "businessName": "My Salon"
  }'
```

Save the `token` from the response.

### Generate Your First Website

```bash
curl -X POST http://localhost:3000/api/websites/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "businessName": "Beautiful Hair Salon",
    "location": "Budapest, Hungary",
    "businessType": "beauty",
    "language": "hu"
  }'
```

🎉 **Congratulations!** Your first AI-generated website is ready!

## What's Next?

### Explore the API
- Check out [API_TESTING.md](./API_TESTING.md) for more examples
- Import [postman_collection.json](./postman_collection.json) into Postman
- Read the [FEATURES.md](./FEATURES.md) to learn about all features

### Deploy to Production
- Follow [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup
- Use Docker: `docker-compose up -d`
- Or deploy to your favorite cloud provider

### Customize
- Edit templates in `public/templates/`
- Modify AI prompts in `src/services/ai.service.js`
- Add new industries in `src/services/website-generator.service.js`

## Common Issues

### MongoDB Connection Error
```
Error: Failed to connect to MongoDB
```
**Solution:** Ensure MongoDB is running:
```bash
sudo systemctl status mongod
# or
docker ps | grep mongodb
```

### API Key Error
```
Error: OpenAI API key not configured
```
**Solution:** Check your `.env` file has valid API keys.

### Port Already in Use
```
Error: listen EADDRINUSE: address already in use :::3000
```
**Solution:** Change the port in `.env`:
```env
PORT=3001
```

## Need Help?

- 📖 Read the full [README.md](./README.md)
- 📧 Email: support@n-target.com
- 🐛 Report issues on GitHub

## Quick Reference

### Essential Commands
```bash
# Start development server
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Start with PM2 (production)
pm2 start ecosystem.config.js

# View PM2 logs
pm2 logs
```

### Important Endpoints
- Health Check: `GET /health`
- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`
- Generate Website: `POST /api/websites/generate`
- Get Plans: `GET /api/subscriptions/plans`

### Directory Structure
```
googlemaptowebsite/
├── src/               # Node.js application
│   ├── config/        # Configuration
│   ├── controllers/   # Request handlers
│   ├── models/        # Database models
│   ├── routes/        # API routes
│   └── services/      # Business logic
├── ai_services/       # Python AI services
├── public/            # Static files & templates
└── tests/             # Test files
```

## Performance Tips

1. **Use Gemini Flash** for simple tasks to save costs
2. **Enable caching** for repeated requests
3. **Optimize images** before uploading
4. **Monitor token usage** in user dashboard
5. **Scale with PM2** cluster mode for high traffic

## Security Checklist

- [ ] Change default JWT_SECRET
- [ ] Use strong passwords
- [ ] Enable HTTPS in production
- [ ] Set up rate limiting
- [ ] Enable MongoDB authentication
- [ ] Keep API keys secure
- [ ] Regular backups

---

**Ready to build amazing websites with AI? Let's go! 🚀**
