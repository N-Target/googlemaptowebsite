# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                   (Future Implementation)                    │
│           React / Next.js with Voice Interface              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTPS / REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    API Gateway / Express                     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Auth       │  │   Website    │  │    Lead      │     │
│  │   Routes     │  │   Routes     │  │   Routes     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
┌───────▼────────┐ ┌───▼────────┐ ┌───▼────────────┐
│   Controllers  │ │ Middleware │ │    Services    │
│                │ │            │ │                │
│ • Auth         │ │ • Auth     │ │ • AI Service   │
│ • Website      │ │ • Error    │ │ • Google Maps  │
│ • Lead         │ │ • Rate     │ │ • Generator    │
│ • Subscription │ │   Limit    │ │                │
└────────────────┘ └────────────┘ └────────┬───────┘
                                           │
                    ┌──────────────────────┼──────────────┐
                    │                      │              │
            ┌───────▼────────┐    ┌───────▼────────┐   ┌▼──────────┐
            │  AI Services   │    │  External APIs │   │  Database │
            │                │    │                │   │           │
            │ • Gemini Flash │    │ • Google Maps  │   │ MongoDB   │
            │ • GPT-4o       │    │ • OpenAI       │   │           │
            │ • Smart Crop   │    │ • Gemini       │   │ • Users   │
            │ • Voice-to-JSON│    │                │   │ • Websites│
            │ • Trend Analyzer│   │                │   │ • Leads   │
            └────────────────┘    └────────────────┘   └───────────┘
```

## Data Flow

### Website Generation Flow

```
1. User Request
   └─> POST /api/websites/generate
       {businessName, location, businessType, language}

2. Authentication
   └─> JWT Verification
       └─> Check User Subscription & Tokens

3. Google Maps Integration
   └─> Search Business
       └─> Get Place Details
           └─> Fetch Photos & Reviews

4. AI Content Generation
   ├─> Task Analysis (complexity check)
   ├─> Model Selection
   │   ├─> Simple → Gemini Flash
   │   └─> Complex → GPT-4o
   └─> Generate Content
       ├─> Headline
       ├─> Description
       ├─> Features
       └─> CTA

5. Website Assembly
   ├─> Select Template (luxury, modern, minimal)
   ├─> Apply Color Scheme (industry-based)
   ├─> Process Images (Smart Crop)
   └─> Generate SEO Tags

6. Database Storage
   └─> Save Website Document
       └─> Update User Token Usage

7. Response
   └─> Return Website Data + Metadata
```

### Lead Capture Flow

```
1. Public Form Submission
   └─> POST /api/leads
       {websiteId, name, email, phone, message}

2. Validation
   └─> Verify Website Exists
       └─> Validate Contact Data

3. Lead Scoring (Future)
   └─> Analyze Lead Quality
       ├─> Contact Completeness
       ├─> Message Intent
       └─> Source Quality

4. Storage & Analytics
   ├─> Save Lead
   └─> Update Website Stats
       └─> Increment Lead Count

5. Notification (Future)
   ├─> Email to Business Owner
   └─> SMS Alert (if enabled)

6. Response
   └─> Confirm Receipt
```

## AI Model Selection Logic

```javascript
Decision Tree:

                     ┌─────────────┐
                     │ Task Request│
                     └──────┬──────┘
                            │
                    ┌───────▼────────┐
                    │ Analyze Task   │
                    │ • Type         │
                    │ • Token Count  │
                    └───────┬────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
       ┌──────▼──────┐            ┌──────▼──────┐
       │  Complex?   │            │   Simple?   │
       │             │            │             │
       │ • Copywrite │            │ • Format    │
       │ • Analysis  │            │ • Translate │
       │ • >1000 tok │            │ • Extract   │
       └──────┬──────┘            └──────┬──────┘
              │                          │
       ┌──────▼──────┐            ┌──────▼──────┐
       │  GPT-4o     │            │ Gemini Flash│
       │             │            │             │
       │ High Quality│            │ Fast & Cheap│
       │ $0.01/1k    │            │ $0.001/1k   │
       └─────────────┘            └─────────────┘
```

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique, indexed),
  password: String (hashed),
  name: String,
  businessName: String,
  subscription: {
    plan: String, // starter, a-plan, b-plan, luxury-leap
    status: String, // active, inactive, cancelled
    tokensUsed: Number,
    tokensLimit: Number, // -1 for unlimited
    startDate: Date,
    endDate: Date
  },
  language: String,
  createdAt: Date,
  updatedAt: Date
}
```

### Websites Collection
```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref: User, indexed),
  businessName: String,
  businessType: String,
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
    testimonials: [Object]
  },
  design: {
    template: String,
    colors: Object,
    images: [String],
    layout: String
  },
  seo: {
    title: String,
    description: String,
    keywords: [String]
  },
  status: String, // draft, generating, published, archived
  language: String,
  url: String (indexed),
  analytics: {
    views: Number,
    leads: Number,
    conversionRate: Number
  },
  aiMetadata: {
    model: String,
    tokensUsed: Number,
    generationTime: Number,
    complexity: String
  },
  createdAt: Date,
  updatedAt: Date
}
```

### Leads Collection
```javascript
{
  _id: ObjectId,
  websiteId: ObjectId (ref: Website, indexed),
  name: String,
  email: String,
  phone: String,
  message: String,
  source: String, // contact_form, chat_widget, voice_input
  status: String, // new, contacted, qualified, converted, lost
  score: Number, // 0-100
  metadata: {
    userAgent: String,
    ip: String,
    referrer: String,
    language: String
  },
  createdAt: Date,
  updatedAt: Date
}
```

## API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/leads` - Create lead (from website forms)
- `GET /api/subscriptions/plans` - View pricing plans

### Protected Endpoints (JWT Required)

#### Authentication
- `GET /api/auth/me` - Get current user

#### Websites
- `POST /api/websites/generate` - Generate new website
- `GET /api/websites` - List user's websites
- `GET /api/websites/:id` - Get website details
- `PUT /api/websites/:id` - Update website
- `DELETE /api/websites/:id` - Delete website
- `GET /api/websites/:id/analytics` - Get analytics

#### Leads
- `GET /api/leads` - Get all user's leads
- `GET /api/leads/website/:websiteId` - Get website leads
- `PATCH /api/leads/:id` - Update lead status

#### Subscriptions
- `GET /api/subscriptions/current` - Current subscription
- `POST /api/subscriptions/upgrade` - Upgrade plan
- `POST /api/subscriptions/cancel` - Cancel subscription

## Security Layers

```
┌─────────────────────────────────────────┐
│         Request from Client             │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼───────┐
         │  HTTPS/TLS    │  Layer 1: Transport Security
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │  CORS Policy  │  Layer 2: Cross-Origin Control
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │ Rate Limiting │  Layer 3: DDoS Protection
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │ JWT Auth      │  Layer 4: Authentication
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │ Input Valid.  │  Layer 5: Data Validation
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │ Authorization │  Layer 6: Access Control
         └───────┬───────┘
                 │
         ┌───────▼───────┐
         │ Business Logic│  Layer 7: Application
         └───────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- **Stateless API**: JWT-based auth allows multiple instances
- **PM2 Cluster Mode**: Utilize all CPU cores
- **Load Balancer**: Nginx distributes traffic
- **Database Replication**: MongoDB replica set

### Caching Strategy
- **Redis**: Cache frequently accessed data
  - User sessions
  - Generated content
  - Google Maps results
- **CDN**: Static assets and images
- **HTTP Caching**: ETags and Cache-Control headers

### Performance Optimization
- **Database Indexes**: userId, websiteId, email, url
- **Connection Pooling**: MongoDB connection pool
- **Async Processing**: Background jobs for heavy tasks
- **Image Optimization**: Smart Crop + CDN

## Monitoring & Logging

### Application Metrics
- Request count & response times
- Error rates & types
- Token usage per user
- AI model selection distribution

### Infrastructure Metrics
- CPU & Memory usage
- Database connections
- Response times
- Network throughput

### Logging Strategy
```javascript
{
  timestamp: ISO8601,
  level: 'info|warn|error',
  service: 'api|ai|worker',
  userId: String,
  action: String,
  duration: Number,
  metadata: Object
}
```

## Future Architecture Enhancements

### Phase 2
- [ ] WebSocket for real-time updates
- [ ] Message Queue (RabbitMQ/Redis)
- [ ] Microservices separation
- [ ] GraphQL API

### Phase 3
- [ ] Kubernetes orchestration
- [ ] Multi-region deployment
- [ ] Edge computing (Cloudflare Workers)
- [ ] Real-time collaboration

### Phase 4
- [ ] AI model fine-tuning
- [ ] Custom ML models
- [ ] Blockchain integration (future consideration)
- [ ] Advanced analytics with ML
