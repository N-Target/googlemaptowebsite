"""
Initialize database - Run this script to create database tables
"""
from app.db.database import engine, Base
from app.models import models  # Import to register all models with SQLAlchemy

def init_database():
    """Initialize the database by creating all tables"""
    print("Initializing database...")
    print(f"Database URL: {engine.url}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # List created tables
    tables = list(Base.metadata.tables.keys())
    print(f"\n✓ Database initialized successfully!")
    print(f"Created tables: {', '.join(tables)}")
    print(f"Total tables: {len(tables)}")

if __name__ == "__main__":
    init_database()
