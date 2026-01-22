#!/usr/bin/env python3
"""
Diagnostic script for troubleshooting Hostinger deployment issues
Run this script to check if the application can start properly
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("   ❌ Python 3.9+ required")
        return False
    print("   ✅ Python version OK")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    required = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'openai',
        'googlemaps'
    ]
    
    missing = []
    for module in required:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - NOT INSTALLED")
            missing.append(module)
    
    if missing:
        print(f"\n   Install missing: pip install {' '.join(missing)}")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    print("\n🔍 Checking .env file...")
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        
        # Check for required variables
        with open('.env', 'r') as f:
            content = f.read()
            required_vars = ['DATABASE_URL', 'APP_ENV']
            for var in required_vars:
                if var in content:
                    print(f"   ✅ {var} configured")
                else:
                    print(f"   ⚠️  {var} not found (optional)")
        return True
    else:
        print("   ❌ .env file NOT FOUND")
        print("   Run: cp .env.example .env")
        return False

def check_database():
    """Check if database exists"""
    print("\n🔍 Checking database...")
    if os.path.exists('googlemaptowebsite.db'):
        print("   ✅ Database file exists")
        return True
    else:
        print("   ⚠️  Database NOT initialized")
        print("   Run: python init_db.py")
        return False

def check_static_directory():
    """Check if static directory exists"""
    print("\n🔍 Checking static directory...")
    if os.path.exists('static') and os.path.isdir('static'):
        print("   ✅ static/ directory exists")
        if os.path.exists('static/generated'):
            print("   ✅ static/generated/ directory exists")
        else:
            print("   ⚠️  static/generated/ creating...")
            os.makedirs('static/generated', exist_ok=True)
        return True
    else:
        print("   ⚠️  static/ directory NOT FOUND, creating...")
        os.makedirs('static/generated', exist_ok=True)
        return True

def test_import_app():
    """Try to import the main app"""
    print("\n🔍 Testing application import...")
    try:
        from main import app
        print("   ✅ Application imports successfully")
        return True
    except Exception as e:
        print(f"   ❌ Application import FAILED: {e}")
        return False

def check_passenger_wsgi():
    """Check passenger_wsgi.py configuration"""
    print("\n🔍 Checking passenger_wsgi.py...")
    if os.path.exists('passenger_wsgi.py'):
        print("   ✅ passenger_wsgi.py exists")
        with open('passenger_wsgi.py', 'r') as f:
            content = f.read()
            if 'username' in content.lower() and 'home/username' in content:
                print("   ⚠️  NEEDS CONFIGURATION: Update 'username' in passenger_wsgi.py")
                return False
            else:
                print("   ✅ passenger_wsgi.py appears configured")
        return True
    else:
        print("   ❌ passenger_wsgi.py NOT FOUND")
        return False

def check_htaccess():
    """Check .htaccess configuration"""
    print("\n🔍 Checking .htaccess...")
    if os.path.exists('.htaccess'):
        print("   ✅ .htaccess exists")
        with open('.htaccess', 'r') as f:
            content = f.read()
            if 'username' in content.lower() and 'home/username' in content:
                print("   ⚠️  NEEDS CONFIGURATION: Update 'username' in .htaccess")
                return False
            else:
                print("   ✅ .htaccess appears configured")
        return True
    else:
        print("   ❌ .htaccess NOT FOUND")
        return False

def main():
    """Run all diagnostic checks"""
    print("=" * 60)
    print("🏥 Hostinger Deployment Diagnostic Tool")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_env_file(),
        check_database(),
        check_static_directory(),
        check_passenger_wsgi(),
        check_htaccess(),
        test_import_app(),
    ]
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if passed == total:
        print("\n✅ All checks passed! Application should work.")
        print("\nNext steps:")
        print("1. Restart Passenger: mkdir -p tmp && touch tmp/restart.txt")
        print("2. Check your website: https://magyar-ai.com")
        print("3. View API docs: https://magyar-ai.com/docs")
    else:
        print("\n⚠️  Some checks failed. Review the output above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env: cp .env.example .env && nano .env")
        print("3. Initialize database: python init_db.py")
        print("4. Update passenger_wsgi.py with your username")
        print("5. Update .htaccess with your username")
        print("6. Restart: mkdir -p tmp && touch tmp/restart.txt")
    
    print("\n" + "=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
