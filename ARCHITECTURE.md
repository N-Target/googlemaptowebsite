# Architecture Documentation

## System Overview

The Google Map to Website Generator is an AI-powered system that automatically creates professional websites from Google Maps business data. It includes lead capture, marketing automation, and a comprehensive admin dashboard.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Admin Panel  │  │ Generated    │  │  API Docs    │     │
│  │  (Tailwind)  │  │  Websites    │  │  (Swagger)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
┌──────────────────────────┴──────────────────────────────────┐
│                    FastAPI Application                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │              API Routes Layer                       │    │
│  │  • /admin  • /api/v1/generator  • /api/v1/leads    │    │
│  │  • /api/v1/widgets  • /api/v1/marketing            │    │
│  └─────────────────────┬──────────────────────────────┘    │
│                        │                                     │
│  ┌─────────────────────┴──────────────────────────────┐    │
│  │            Business Logic Services                  │    │
│  │  • AI Generator  • Google Maps  • Settings Helper  │    │
│  └─────────────────────┬──────────────────────────────┘    │
│                        │                                     │
│  ┌─────────────────────┴──────────────────────────────┐    │
│  │              Data Access Layer                      │    │
│  │  • SQLAlchemy ORM  • Pydantic Schemas              │    │
│  └─────────────────────┬──────────────────────────────┘    │
└────────────────────────┴─────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
┌───────┴────┐  ┌────────┴─────┐  ┌──────┴─────┐
│  Database  │  │   OpenAI     │  │   Google   │
│  SQLite/   │  │   GPT-4 API  │  │  Maps API  │
│  Postgres  │  │              │  │            │
└────────────┘  └──────────────┘  └────────────┘
```

## Component Details

### 1. Frontend Layer

#### Admin Panel (`static/admin/`)
- **Technology**: Vanilla JavaScript + Tailwind CSS
- **Components**:
  - Dashboard with live statistics
  - API settings manager
  - AI prompt editor
  - Website preview and testing
  - Lead management table
  - Widget configuration

#### Generated Websites
- Server-rendered HTML/CSS
- Responsive design
- Embedded widgets
- SEO optimized

### 2. API Layer (`app/api/routes/`)

#### Admin Routes (`admin.py`)
```python
GET  /admin                    # Admin UI
GET  /api/v1/admin/settings    # List settings
POST /api/v1/admin/settings    # Create/update setting
GET  /api/v1/admin/prompts     # List prompts
POST /api/v1/admin/prompts     # Create prompt
GET  /api/v1/admin/dashboard/stats  # Dashboard statistics
```

#### Website Generator Routes (`website_generator.py`)
```python
POST /api/v1/generator/generate           # Generate website
GET  /api/v1/generator/websites           # List websites
GET  /api/v1/generator/websites/{id}      # Get website
PUT  /api/v1/generator/websites/{id}      # Update website
DELETE /api/v1/generator/websites/{id}    # Delete website
```

#### Lead Routes (`leads.py`)
```python
POST /api/v1/leads                    # Create lead
GET  /api/v1/leads                    # List leads
GET  /api/v1/leads/{id}               # Get lead
PUT  /api/v1/leads/{id}               # Update lead
DELETE /api/v1/leads/{id}             # Delete lead
POST /api/v1/leads/{id}/activities    # Add activity
```

#### Widget Routes (`widgets.py`)
```python
POST /api/v1/widgets                  # Create widget
GET  /api/v1/widgets                  # List widgets
GET  /api/v1/widgets/{id}             # Get widget
PUT  /api/v1/widgets/{id}             # Update widget
DELETE /api/v1/widgets/{id}           # Delete widget
```

#### Marketing Routes (`marketing.py`)
```python
POST /api/v1/marketing/campaigns          # Create campaign
GET  /api/v1/marketing/campaigns          # List campaigns
GET  /api/v1/marketing/campaigns/{id}     # Get campaign
POST /api/v1/marketing/campaigns/{id}/send  # Send campaign
GET  /api/v1/marketing/analytics          # Get analytics
```

### 3. Business Logic Layer (`app/services/`)

#### AI Generator Service (`ai_generator.py`)
- **Purpose**: Generate website content using AI
- **Dependencies**: OpenAI API, prompt templates
- **Key Methods**:
  ```python
  async def generate_website_content(
      business_data: dict,
      language: str
  ) -> dict
  ```
- **Features**:
  - Multi-language support
  - Variable substitution
  - Template fallback
  - Customizable prompts

#### Google Maps Service (`google_maps_service.py`)
- **Purpose**: Fetch business data from Google
- **Dependencies**: Google Maps API, Google Places API
- **Key Methods**:
  ```python
  async def get_business_info(
      place_id: str
  ) -> dict
  
  async def search_business(
      query: str,
      location: str
  ) -> list
  ```

#### Settings Helper (`settings_helper.py`)
- **Purpose**: Centralized configuration management
- **Priority**: Database → Environment → Defaults
- **Key Functions**:
  ```python
  async def get_setting(db, key, default) -> str
  async def get_api_key(db, service) -> str
  async def get_active_prompt(db, language, type) -> str
  ```

### 4. Data Layer (`app/models/`)

#### ORM Models (`models.py`)

##### GeneratedWebsite
```python
id: int (PK)
business_name: str
business_type: str
address: str
phone: str
website_url: str
html_content: text
css_content: text
seo_metadata: JSON
language: str
status: str (draft/published/archived)
created_at: datetime
updated_at: datetime

# Relationships
widgets: List[Widget]
leads: List[Lead]
```

##### Widget
```python
id: int (PK)
website_id: int (FK)
widget_type: str (contact_form/chatbot/booking/map/reviews)
position: str (header/sidebar/footer/inline)
configuration: JSON
is_active: bool
created_at: datetime

# Relationship
website: GeneratedWebsite
```

##### Lead
```python
id: int (PK)
website_id: int (FK)
name: str
email: str
phone: str
message: text
status: str (new/contacted/qualified/converted/lost)
source: str
custom_fields: JSON
tags: str[]
created_at: datetime
updated_at: datetime

# Relationships
website: GeneratedWebsite
activities: List[LeadActivity]
```

##### LeadActivity
```python
id: int (PK)
lead_id: int (FK)
activity_type: str (email/call/meeting/note)
description: text
activity_metadata: JSON
created_at: datetime

# Relationship
lead: Lead
```

##### MarketingCampaign
```python
id: int (PK)
name: str
campaign_type: str (email/sms/notification)
target_criteria: JSON
content: text
status: str (draft/scheduled/active/completed)
sent_count: int
opened_count: int
clicked_count: int
scheduled_at: datetime
created_at: datetime
```

##### AppSettings
```python
id: int (PK)
key: str (unique)
value: text
is_secret: bool
description: text
created_at: datetime
updated_at: datetime
```

##### AIPromptTemplate
```python
id: int (PK)
name: str
prompt_type: str (website_generation/email/sms)
language: str
prompt_text: text
variables: str[]
is_active: bool
is_default: bool
created_at: datetime
updated_at: datetime
```

#### Pydantic Schemas (`schemas.py`)
- Request validation models
- Response serialization models
- Follows ORM model structure
- Includes nested relationships

### 5. Database Layer (`app/db/`)

#### Database Configuration (`database.py`)
```python
# SQLAlchemy 2.0 async engine
engine = create_async_engine(DATABASE_URL)

# Async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency injection
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

#### Supported Databases
- **Development**: SQLite with aiosqlite
- **Production**: PostgreSQL with asyncpg

### 6. Configuration Layer (`app/core/`)

#### Config (`config.py`)
```python
class Settings(BaseSettings):
    # Application
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    
    # Database
    DATABASE_URL: str
    
    # APIs (fallback values)
    OPENAI_API_KEY: str
    GOOGLE_MAPS_API_KEY: str
    GOOGLE_PLACES_API_KEY: str
    
    class Config:
        env_file = ".env"
```

## Data Flow Examples

### 1. Website Generation Flow

```
Client → POST /api/v1/generator/generate
    ↓
API Route validates request (Pydantic)
    ↓
Settings Helper gets API keys from DB/env
    ↓
Google Maps Service fetches business data
    ↓
AI Generator creates HTML/CSS content
    - Loads prompt template from DB
    - Substitutes variables
    - Calls OpenAI API
    - Falls back to template if needed
    ↓
Database saves GeneratedWebsite
    ↓
Response returned with website data
    ↓
Client shows preview and download options
```

### 2. Lead Capture Flow

```
Widget embedded in website
    ↓
User submits form
    ↓
POST /api/v1/leads
    ↓
API Route validates data
    ↓
Database creates Lead record
    ↓
Database creates LeadActivity (initial)
    ↓
Response confirms capture
    ↓
Admin dashboard shows new lead
```

### 3. Settings Management Flow

```
Admin panel → Update API key
    ↓
POST /api/v1/admin/settings
    ↓
Database upserts AppSettings
    ↓
Settings Helper cache invalidated
    ↓
Next API call uses new key
```

## Deployment Architecture

### Docker Deployment

```
┌──────────────────────────────────────┐
│         Docker Compose               │
│  ┌────────────┐  ┌────────────┐     │
│  │  FastAPI   │  │ PostgreSQL │     │
│  │  Container │→→│  Container │     │
│  │  Port 8000 │  │  Port 5432 │     │
│  └────────────┘  └────────────┘     │
│  ┌────────────┐                      │
│  │   Redis    │                      │
│  │  Container │ (future)             │
│  │  Port 6379 │                      │
│  └────────────┘                      │
└──────────────────────────────────────┘
```

### Hostinger Deployment

```
┌──────────────────────────────────────┐
│      Apache with Passenger           │
│  ┌────────────────────────────┐     │
│  │  .htaccess config          │     │
│  │  → PassengerPython path    │     │
│  │  → Document root           │     │
│  └────────────────────────────┘     │
│           ↓                          │
│  ┌────────────────────────────┐     │
│  │  passenger_wsgi.py         │     │
│  │  → Imports FastAPI app     │     │
│  │  → WSGI adapter            │     │
│  └────────────────────────────┘     │
│           ↓                          │
│  ┌────────────────────────────┐     │
│  │  Virtual Environment       │     │
│  │  Python 3.11 + packages    │     │
│  └────────────────────────────┘     │
│           ↓                          │
│  ┌────────────────────────────┐     │
│  │  FastAPI Application       │     │
│  │  SQLite database           │     │
│  └────────────────────────────┘     │
└──────────────────────────────────────┘
```

## Security Architecture

### Current (Dev Mode)
- No authentication (intentional)
- Wide CORS policy
- API keys stored in DB (readable)
- Admin panel open access

### Planned (V2)
- JWT authentication
- Role-based access control
- API key encryption
- Rate limiting
- Audit logging
- CORS restrictions
- Input sanitization

## Performance Considerations

### Current Optimizations
- Async database operations
- Connection pooling
- Lazy loading relationships
- Indexed database columns

### Future Optimizations
- Redis caching
- CDN for static assets
- Database query optimization
- Background job processing (Celery)
- API response compression

## Monitoring & Logging

### Health Checks
- `/health` endpoint
- Database connectivity check
- API availability check

### Logging
- Python logging module
- Log levels: DEBUG, INFO, WARNING, ERROR
- Structured logging format

### Future Monitoring
- Prometheus metrics
- Grafana dashboards
- Error tracking (Sentry)
- Performance monitoring (New Relic)

## Scalability

### Current Capacity
- Single server deployment
- SQLite (dev) / PostgreSQL (prod)
- Synchronous AI generation

### Scaling Strategy
- Horizontal scaling with load balancer
- Database replication
- Async task queue (Celery + Redis)
- Microservices architecture (if needed)
- CDN for static content

## Testing Strategy

### Current
- Manual testing via admin panel
- API testing via `/docs` (Swagger)
- Diagnostic tools (`diagnose.py`)

### Planned
- Unit tests (pytest)
- Integration tests
- API endpoint tests
- Database migration tests
- Load testing

## Documentation

- **Code**: Inline comments and docstrings
- **API**: Auto-generated Swagger docs at `/docs`
- **User**: Markdown files in repository
- **Developer**: This architecture document
- **Deployment**: Hostinger and Docker guides

## Future Enhancements

1. **Authentication & Authorization**
   - User management
   - JWT tokens
   - Role-based access

2. **Background Processing**
   - Celery task queue
   - Scheduled jobs
   - Batch operations

3. **Advanced Features**
   - Multi-tenant support
   - Custom domains
   - Email integration
   - SMS notifications
   - Payment processing

4. **Analytics**
   - Visitor tracking
   - Conversion analytics
   - A/B testing
   - Performance metrics

5. **Internationalization**
   - Additional languages
   - Regional customization
   - Currency support

---

Last updated: 2026-01-23
