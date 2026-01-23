# Contributing to Google Map to Website Generator

Köszönjük, hogy hozzá szeretnél járulni a projekthez! / Thank you for your interest in contributing!

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- pip (Python package manager)
- Virtual environment tool

### Quick Start

```bash
# Clone the repository
git clone https://github.com/N-Target/googlemaptowebsite.git
cd googlemaptowebsite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python init_db.py

# Run the application
python main.py

# Open in browser
# http://localhost:8000/admin
```

## Project Structure

```
googlemaptowebsite/
├── app/                    # Main application code
│   ├── api/               # API routes
│   │   └── routes/        # Route modules
│   ├── core/              # Core configuration
│   ├── db/                # Database setup
│   ├── models/            # Data models
│   └── services/          # Business logic
├── static/                # Static files (CSS, JS, HTML)
│   └── admin/             # Admin panel UI
├── .github/               # GitHub configuration
│   └── copilot-instructions.md  # Copilot AI assistant config
├── docs/                  # Documentation
├── tests/                 # Test files (future)
└── main.py               # Application entry point
```

## Coding Standards

### Python Code Style

- Follow PEP 8
- Use type hints for all functions
- Write docstrings for public functions and classes
- Use async/await for database operations
- Maximum line length: 100 characters

Example:
```python
async def create_website(
    business_data: dict,
    language: str = "hu",
    db: AsyncSession = None
) -> GeneratedWebsite:
    """
    Create a new website from business data.
    
    Args:
        business_data: Dictionary containing business information
        language: Language code (default: 'hu')
        db: Database session
        
    Returns:
        GeneratedWebsite: The created website object
        
    Raises:
        ValueError: If business_data is invalid
    """
    # Implementation here
    pass
```

### Database Operations

Always use async patterns:
```python
# Good ✅
async with get_db() as db:
    result = await db.execute(select(Model).where(Model.id == id))
    obj = result.scalar_one_or_none()

# Bad ❌
db = Session()
obj = db.query(Model).filter(Model.id == id).first()
```

### API Endpoints

- Use RESTful conventions
- Version APIs: `/api/v1/`
- Return appropriate HTTP status codes
- Use Pydantic for validation

```python
@router.post("/websites", response_model=WebsiteResponse, status_code=201)
async def create_website(
    request: WebsiteCreate,
    db: AsyncSession = Depends(get_db)
) -> WebsiteResponse:
    """Create a new website."""
    # Implementation
```

## Git Workflow

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Use conventional commits:

```
feat: Add new widget type for booking
fix: Resolve 503 error on Hostinger deployment
docs: Update API documentation
refactor: Simplify database query logic
chore: Update dependencies
```

### Pull Request Process

1. Create a feature branch
2. Make your changes
3. Test thoroughly (manual + automated)
4. Update documentation
5. Create pull request with description
6. Wait for code review
7. Address feedback
8. Merge after approval

## Testing

### Manual Testing

```bash
# Start the server
python main.py

# Test admin panel
open http://localhost:8000/admin

# Test API endpoints
open http://localhost:8000/docs
```

### API Testing

Use the built-in Swagger UI at `/docs` or curl:

```bash
# Health check
curl http://localhost:8000/health

# Create a website
curl -X POST http://localhost:8000/api/v1/generator/generate \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Test Business",
    "business_type": "Restaurant",
    "language": "hu"
  }'
```

## Adding New Features

### 1. New Database Model

Add to `app/models/models.py`:
```python
class NewModel(Base):
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

Add Pydantic schema to `app/models/schemas.py`:
```python
class NewModelBase(BaseModel):
    name: str

class NewModelCreate(NewModelBase):
    pass

class NewModelResponse(NewModelBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 2. New API Endpoint

Create or update router in `app/api/routes/`:
```python
from fastapi import APIRouter, Depends
from app.models.schemas import NewModelCreate, NewModelResponse

router = APIRouter(prefix="/api/v1/new", tags=["New Feature"])

@router.post("/", response_model=NewModelResponse)
async def create_new_model(
    request: NewModelCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new model."""
    # Implementation
```

Register in `main.py`:
```python
from app.api.routes import new_feature
app.include_router(new_feature.router)
```

### 3. New Service

Add to `app/services/`:
```python
class NewService:
    """Service for handling new feature logic."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def process_data(self, data: dict) -> dict:
        """Process data and return result."""
        # Implementation
        return result
```

### 4. New Admin UI Feature

Add to `static/admin/index.html` and `static/admin/admin.js`:

```javascript
// Add menu item
const menuItem = `
    <a href="#new-feature" class="menu-item">
        <i class="fas fa-icon"></i>
        <span>New Feature</span>
    </a>
`;

// Add page content
const pageContent = `
    <div id="new-feature-page" class="page-content">
        <h2>New Feature</h2>
        <!-- Content here -->
    </div>
`;

// Add navigation handler
function showNewFeature() {
    showPage('new-feature-page');
}
```

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use type hints
- Comment complex logic
- Keep comments up to date

### User Documentation

Update these files when adding features:
- `README.md` - Overview and quick start
- `ADMIN_PANEL_GUIDE.md` - Admin panel features
- `API_REFERENCE.md` - API endpoints (future)

## Common Issues

### Database Connection Error

```bash
# Reinitialize database
python init_db.py
```

### Missing Dependencies

```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

### Port Already in Use

```bash
# Change port in main.py or use environment variable
PORT=8001 python main.py
```

## Getting Help

- Check existing documentation in the repo
- Look at `.github/copilot-instructions.md` for detailed patterns
- Review similar code in the codebase
- Ask questions in pull requests
- Check FastAPI documentation: https://fastapi.tiangolo.com/

## Code Review Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All functions have type hints
- [ ] Documentation is updated
- [ ] Manual testing completed
- [ ] No hardcoded secrets or API keys
- [ ] Error handling implemented
- [ ] Database operations use async patterns
- [ ] API endpoints return appropriate status codes
- [ ] Changes don't break existing functionality

## Security

### Do NOT:
- Commit API keys or secrets
- Expose sensitive data in logs
- Use synchronous blocking operations
- Ignore error handling
- Store passwords in plaintext

### DO:
- Use environment variables for secrets
- Validate all user input
- Handle exceptions gracefully
- Use parameterized queries (SQLAlchemy ORM)
- Follow principle of least privilege

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

Contact the maintainers or open an issue for discussion.

---

Köszönjük a hozzájárulást! / Thank you for contributing!
