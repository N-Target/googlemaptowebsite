# GitHub Copilot Instructions for googlemaptowebsite

## Project Overview

This is an AI-powered website generator and lead generation system that creates websites from Google Maps business data. The system is designed for rapid deployment in EU markets with Hungarian as the primary language.

## Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.11+) with async/await patterns
- **Database**: SQLAlchemy ORM with SQLite (dev) / PostgreSQL (prod)
- **AI**: OpenAI GPT-4 for content generation
- **External APIs**: Google Maps API, Google Places API
- **Frontend**: Vanilla JavaScript with Tailwind CSS
- **Deployment**: Docker Compose, Hostinger Passenger/Apache

### Project Structure
```
app/
├── api/routes/          # API endpoints organized by domain
│   ├── admin.py         # Admin dashboard routes
│   ├── leads.py         # Lead management
│   ├── marketing.py     # Marketing automation
│   ├── website_generator.py  # Website generation
│   └── widgets.py       # Interactive widgets
├── core/                # Core configuration
│   ├── config.py        # Settings and environment config
│   └── settings_helper.py  # Database settings helper
├── db/                  # Database setup
│   └── database.py      # SQLAlchemy session management
├── models/              # Data models
│   ├── models.py        # SQLAlchemy ORM models
│   └── schemas.py       # Pydantic validation schemas
└── services/            # Business logic
    ├── ai_generator.py  # AI content generation
    └── google_maps_service.py  # Google Maps integration

static/admin/            # Admin UI (HTML/JS/CSS)
```

## Database Models

### Core Tables
1. **generated_websites** - Stores generated websites with HTML/CSS
2. **widgets** - Interactive widgets (contact_form, chatbot, booking, map, reviews)
3. **leads** - Captured leads with status workflow (new → contacted → converted/lost)
4. **lead_activities** - Activity tracking for leads
5. **marketing_campaigns** - Marketing automation campaigns
6. **app_settings** - Application configuration (API keys, settings)
7. **ai_prompt_templates** - Customizable AI prompts for different languages

### Relationships
- generated_websites → widgets (1:N)
- generated_websites → leads (1:N)
- leads → lead_activities (1:N)
- All models have created_at and updated_at timestamps

## Coding Standards

### Python Style
- Use async/await for all database operations
- Type hints required for all function parameters and return values
- Follow PEP 8 style guide
- Use Pydantic models for request/response validation
- Use SQLAlchemy 2.0 style (not legacy 1.x)

### API Design
- RESTful endpoints with clear resource naming
- Version all APIs under `/api/v1/`
- Use HTTP status codes properly (200, 201, 400, 404, 500)
- Return consistent error responses with detail messages
- Use dependency injection for database sessions

### Database Operations
- Always use async sessions: `async with get_db() as db:`
- Use `db.execute()` with `select()` for queries
- Commit transactions explicitly: `await db.commit()`
- Refresh objects after creation: `await db.refresh(obj)`
- Handle exceptions with try/except blocks

### Configuration Priority
1. Database (app_settings table)
2. Environment variables (.env file)
3. Default values in config.py

## Key Features to Remember

### 1. Admin Dashboard
- Located at `/admin` route
- No authentication (dev mode by design)
- Manages: API keys, AI prompts, websites, leads
- Uses Tailwind CSS for styling
- JavaScript in `static/admin/admin.js`

### 2. AI Website Generation
- Uses OpenAI GPT-4 with fallback to templates
- Customizable prompts stored in database
- Multi-language support (hu, en, de, fr, es, it)
- Variable substitution: `{business_name}`, `{address}`, `{phone}`, `{business_type}`
- Returns: HTML, CSS, SEO metadata

### 3. Settings Management
- Use `settings_helper.py` functions:
  - `get_setting(key, default)` - Get any setting
  - `get_api_key(service)` - Get API keys with fallback
  - `get_active_prompt(language, prompt_type)` - Get AI prompts
- Never hardcode API keys in code
- Store secrets in database or environment variables

### 4. Lead Management
- Status workflow: new → contacted → qualified → converted/lost
- Activity tracking for all interactions
- Custom fields stored as JSON
- Tags for segmentation

### 5. Multi-Language Support
- Default language: Hungarian (hu)
- Supported: en, de, fr, es, it
- Language codes follow ISO 639-1
- All user-facing text should be localizable

## Common Patterns

### Creating a New API Endpoint
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.schemas import ResponseSchema

router = APIRouter()

@router.get("/endpoint", response_model=ResponseSchema)
async def get_resource(
    resource_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a resource by ID."""
    try:
        result = await db.execute(
            select(Model).where(Model.id == resource_id)
        )
        resource = result.scalar_one_or_none()
        
        if not resource:
            raise HTTPException(status_code=404, detail="Not found")
        
        return resource
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Database Query Pattern
```python
from sqlalchemy import select
from app.models.models import GeneratedWebsite

# Single record
result = await db.execute(
    select(GeneratedWebsite).where(GeneratedWebsite.id == website_id)
)
website = result.scalar_one_or_none()

# Multiple records
result = await db.execute(
    select(GeneratedWebsite).order_by(GeneratedWebsite.created_at.desc())
)
websites = result.scalars().all()
```

### Creating Database Records
```python
new_record = Model(field1="value1", field2="value2")
db.add(new_record)
await db.commit()
await db.refresh(new_record)
return new_record
```

### Using Settings Helper
```python
from app.core.settings_helper import get_api_key, get_active_prompt

# Get API key (DB first, then env, then None)
openai_key = await get_api_key(db, "openai_api_key")

# Get AI prompt template
prompt = await get_active_prompt(db, language="hu", prompt_type="website_generation")
```

## Environment Variables

Required in `.env` file (with fallback to database):
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Google APIs
GOOGLE_MAPS_API_KEY=AIza...
GOOGLE_PLACES_API_KEY=AIza...

# Database
DATABASE_URL=sqlite+aiosqlite:///./app.db  # Dev
# DATABASE_URL=postgresql+asyncpg://user:pass@host/db  # Prod

# App Config
APP_NAME="Magyar AI Website Generator"
APP_VERSION=1.0.0
DEBUG=True
```

## Testing Guidelines

### Manual Testing
- Use the admin panel at `/admin` for UI testing
- Use `/docs` for API documentation and testing
- Use `/health` endpoint to check system status

### API Testing with curl
```bash
# Health check
curl http://localhost:8000/health

# Generate website
curl -X POST http://localhost:8000/api/v1/generator/generate \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Business",
    "business_type": "Restaurant",
    "address": "123 Main St",
    "phone": "+36 1 234 5678",
    "language": "hu"
  }'
```

## Deployment Notes

### Hostinger Deployment
- Use `configure_hostinger.sh` for automatic setup
- Passenger WSGI configured in `passenger_wsgi.py`
- Apache config in `.htaccess`
- Python 3.11 required
- Virtual environment required

### Docker Deployment
- Use `docker-compose up` for full stack
- PostgreSQL and Redis included
- Environment variables in `.env` file

## Security Considerations

### Current Status (Dev Mode)
- ⚠️ No authentication on admin panel
- ⚠️ No rate limiting
- ⚠️ CORS wide open
- ⚠️ API keys visible in admin UI

### Future (V2)
- JWT authentication
- Role-based access control
- Rate limiting with Redis
- API key encryption
- Audit logging

## Hungarian Translation Notes

Common Hungarian terms in the codebase:
- **weboldal** = website
- **lead** = lead (same in Hungarian)
- **kampány** = campaign
- **widget** = widget (same)
- **beállítások** = settings
- **prompt** = prompt (same)
- **generálás** = generation

## Troubleshooting

### 503 Error on Hostinger
- Run `bash configure_hostinger.sh` to auto-configure
- Check `diagnose.py` for diagnostics
- See `FIX_503_ERROR.md` for detailed guide

### Database Issues
- Run `python init_db.py` to initialize
- Check database connection in config
- Verify SQLAlchemy version compatibility

### API Key Issues
- Check admin panel settings
- Verify `.env` file exists
- Use `settings_helper.py` functions

## When Adding New Features

1. **New Model**: Add to `app/models/models.py` and `schemas.py`
2. **New Endpoint**: Add to appropriate router in `app/api/routes/`
3. **New Service**: Add to `app/services/`
4. **New UI**: Add to `static/admin/` with JavaScript
5. **New Setting**: Add to `app_settings` table via admin panel

## Important: Do NOT

- ❌ Hardcode API keys in code
- ❌ Use synchronous database calls
- ❌ Break existing API endpoints
- ❌ Remove authentication placeholders (V2 needs them)
- ❌ Change database schema without migration
- ❌ Store passwords in plaintext
- ❌ Expose sensitive data in logs

## Documentation

Always update when making changes:
- API docs (auto-generated from FastAPI)
- README.md for user-facing changes
- Code comments for complex logic
- Admin panel guide for new admin features

## Questions?

Check these files first:
- `README.md` - General overview
- `ADMIN_PANEL_GUIDE.md` - Admin panel documentation
- `HOSTINGER_DEPLOYMENT.md` - Deployment guide
- `SECURITY_SUMMARY.md` - Security notes
- `/docs` endpoint - Interactive API docs
