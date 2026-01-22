# API Testing Guide

## Using cURL

### Register User
```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123",
    "name": "Test User",
    "businessName": "My Salon"
  }'
```

### Login
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123"
  }'
```

Save the token from the response for subsequent requests.

### Generate Website
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

### Get User Websites
```bash
curl -X GET http://localhost:3000/api/websites \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Subscription Plans
```bash
curl -X GET http://localhost:3000/api/subscriptions/plans
```

### Upgrade Subscription
```bash
curl -X POST http://localhost:3000/api/subscriptions/upgrade \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "plan": "b-plan"
  }'
```

### Create Lead (Public)
```bash
curl -X POST http://localhost:3000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "websiteId": "WEBSITE_ID_HERE",
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "+36301234567",
    "message": "I would like to book an appointment"
  }'
```

### Get Leads for Website
```bash
curl -X GET http://localhost:3000/api/leads/website/WEBSITE_ID_HERE \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Using Postman

1. Import the Postman collection from `postman_collection.json` (if available)
2. Set environment variables:
   - `base_url`: http://localhost:3000
   - `token`: Your JWT token after login

## Integration Testing

### Test Website Generation Flow

```bash
# 1. Register
TOKEN=$(curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }' | jq -r '.data.token')

# 2. Generate Website
WEBSITE_ID=$(curl -X POST http://localhost:3000/api/websites/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "businessName": "Test Salon",
    "location": "Budapest",
    "businessType": "beauty"
  }' | jq -r '.data._id')

# 3. View Website
curl -X GET http://localhost:3000/api/websites/$WEBSITE_ID \
  -H "Authorization: Bearer $TOKEN"

# 4. Create Lead
curl -X POST http://localhost:3000/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "websiteId": "'$WEBSITE_ID'",
    "name": "Test Customer",
    "email": "customer@example.com",
    "message": "Test message"
  }'

# 5. View Leads
curl -X GET http://localhost:3000/api/leads/website/$WEBSITE_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Expected Responses

### Success Response Format
```json
{
  "success": true,
  "message": "Operation successful",
  "data": {
    // Response data
  }
}
```

### Error Response Format
```json
{
  "error": "Error message",
  "stack": "Stack trace (development only)"
}
```

## Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

Currently no rate limiting is implemented. In production, implement rate limiting:

```javascript
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use('/api/', limiter);
```
