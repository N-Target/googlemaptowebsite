#!/usr/bin/env python3
"""
Diagnostic script for troubleshooting Hostinger deployment issues
Run this script to check if the application can start properly
"""

import sys
import os
import subprocess

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
        if os.path.exists('static/admin'):
            print("   ✅ static/admin/ directory exists")
        else:
            print("   ⚠️  static/admin/ NOT FOUND")
        return True
    else:
        print("   ⚠️  static/ directory NOT FOUND, creating...")
        os.makedirs('static/generated', exist_ok=True)
        os.makedirs('static/admin', exist_ok=True)
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
        import traceback
        traceback.print_exc()
        return False

def check_passenger_wsgi():
    """Check passenger_wsgi.py configuration"""
    print("\n🔍 Checking passenger_wsgi.py...")
    if os.path.exists('passenger_wsgi.py'):
        print("   ✅ passenger_wsgi.py exists")
        with open('passenger_wsgi.py', 'r') as f:
            content = f.read()
            if 'username' in content.lower() and '/home/username' in content:
                print("   ❌ NEEDS CONFIGURATION: Contains placeholder 'username'")
                print("   Run: bash configure_hostinger.sh")
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
            if 'username' in content.lower() and '/home/username' in content:
                print("   ❌ NEEDS CONFIGURATION: Contains placeholder 'username'")
                print("   Run: bash configure_hostinger.sh")
                return False
            else:
                print("   ✅ .htaccess appears configured")
        return True
    else:
        print("   ❌ .htaccess NOT FOUND")
        return False

def check_virtualenv():
    """Check if virtual environment is properly set up"""
    print("\n🔍 Checking virtual environment...")
    home = os.path.expanduser("~")
    venv_path = os.path.join(home, 'virtualenv', 'googlemaptowebsite', '3.11')
    
    if os.path.exists(venv_path):
        print(f"   ✅ Virtual environment exists at {venv_path}")
        
        python_path = os.path.join(venv_path, 'bin', 'python')
        if os.path.exists(python_path):
            print(f"   ✅ Python executable found")
            
            # Check if it's the current Python
            if sys.executable == python_path or sys.executable.startswith(venv_path):
                print(f"   ✅ Currently using virtual environment")
            else:
                print(f"   ⚠️  Not using virtual environment")
                print(f"   Current: {sys.executable}")
                print(f"   Expected: {python_path}")
                print(f"   Activate: source {venv_path}/bin/activate")
        return True
    else:
        print(f"   ❌ Virtual environment NOT FOUND at {venv_path}")
        print(f"   Create: python3.11 -m venv {venv_path}")
        return False

def check_current_user():
    """Check current user and paths"""
    print("\n🔍 Checking user configuration...")
    import getpass
    username = getpass.getuser()
    current_dir = os.getcwd()
    home_dir = os.path.expanduser("~")
    
    print(f"   Username: {username}")
    print(f"   Home: {home_dir}")
    print(f"   Current dir: {current_dir}")
    
    # Check if we're in the expected location
    expected_patterns = [
        f'/home/{username}/public_html',
        f'/home/{username}/domains',
    ]
    
    in_expected = any(pattern in current_dir for pattern in expected_patterns)
    if in_expected:
        print(f"   ✅ In expected Hostinger directory")
    else:
        print(f"   ⚠️  Not in typical Hostinger directory")
        print(f"   Expected: /home/{username}/public_html/ or /home/{username}/domains/")
    
    return True

def main():
    """Run all diagnostic checks"""
    print("=" * 60)
    print("🏥 Hostinger Deployment Diagnostic Tool")
    print("=" * 60)
    
    checks = [
        ("User Configuration", check_current_user()),
        ("Python Version", check_python_version()),
        ("Virtual Environment", check_virtualenv()),
        ("Dependencies", check_dependencies()),
        (".env File", check_env_file()),
        ("Database", check_database()),
        ("Static Directory", check_static_directory()),
        ("passenger_wsgi.py", check_passenger_wsgi()),
        (".htaccess", check_htaccess()),
        ("Application Import", test_import_app()),
    ]
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\nPassed: {passed}/{total} checks")
    
    # Show failed checks
    failed_checks = [name for name, result in checks if not result]
    if failed_checks:
        print("\n❌ Failed checks:")
        for check_name in failed_checks:
            print(f"   - {check_name}")
    
    if passed == total:
        print("\n✅ All checks passed! Application should work.")
        print("\nNext steps:")
        print("1. Restart Passenger: mkdir -p tmp && touch tmp/restart.txt")
        print("2. Check your website: https://magyar-ai.com")
        print("3. View API docs: https://magyar-ai.com/docs")
        print("4. Access admin: https://magyar-ai.com/admin")
    else:
        print("\n⚠️  Some checks failed. Review the output above.")
        print("\n🔧 Quick fixes:")
        
        if not checks[7][1] or not checks[8][1]:  # passenger_wsgi or htaccess failed
            print("\n1. **CRITICAL**: Configuration files need update")
            print("   Run: bash configure_hostinger.sh")
        
        if not checks[3][1]:  # Dependencies failed
            print("\n2. Install dependencies:")
            print("   source ~/virtualenv/googlemaptowebsite/3.11/bin/activate")
            print("   pip install -r requirements.txt")
        
        if not checks[4][1]:  # .env failed
            print("\n3. Configure environment:")
            print("   cp .env.example .env")
            print("   nano .env  # Add your API keys")
        
        if not checks[5][1]:  # Database failed
            print("\n4. Initialize database:")
            print("   python init_db.py")
        
        print("\n5. Restart application:")
        print("   mkdir -p tmp && touch tmp/restart.txt")
        
        print("\n📖 For detailed help, see: FIX_503_ERROR.md")
    
    print("\n" + "=" * 60)
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
