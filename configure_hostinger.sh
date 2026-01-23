#!/bin/bash
# Automatic Hostinger deployment configuration script
# This script will detect your username and configure all deployment files

echo "🚀 Hostinger Deployment Konfiguráló"
echo "===================================="
echo ""

# Detect username
USERNAME=$(whoami)
HOME_DIR=$HOME
CURRENT_DIR=$(pwd)

echo "✓ Felhasználónév: $USERNAME"
echo "✓ Home könyvtár: $HOME_DIR"
echo "✓ Jelenlegi könyvtár: $CURRENT_DIR"
echo ""

# Update .htaccess
echo "📝 .htaccess frissítése..."
if [ -f ".htaccess" ]; then
    # Create backup
    cp .htaccess .htaccess.backup
    
    # Replace username placeholder
    sed -i "s|/home/username/|$HOME_DIR/|g" .htaccess
    
    echo "✓ .htaccess frissítve!"
else
    echo "❌ .htaccess nem található!"
    exit 1
fi

# Update passenger_wsgi.py
echo "📝 passenger_wsgi.py frissítése..."
if [ -f "passenger_wsgi.py" ]; then
    # Create backup
    cp passenger_wsgi.py passenger_wsgi.py.backup
    
    # Replace HOME environment variable usage with actual path
    cat > passenger_wsgi.py << EOF
"""
WSGI entry point for Hostinger/Passenger deployment
This file is required for Passenger to serve the FastAPI application
Auto-configured for user: $USERNAME
"""
import sys
import os

# Add the application directory to Python path
INTERP = '$HOME_DIR/virtualenv/googlemaptowebsite/3.11/bin/python'
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set working directory to the application root
sys.path.insert(0, '$CURRENT_DIR')
os.chdir('$CURRENT_DIR')

# Import the FastAPI app
from main import app

# For Passenger
application = app
EOF
    
    echo "✓ passenger_wsgi.py frissítve!"
else
    echo "❌ passenger_wsgi.py nem található!"
    exit 1
fi

# Check if virtual environment exists
echo ""
echo "🔍 Virtual environment ellenőrzése..."
if [ -d "$HOME_DIR/virtualenv/googlemaptowebsite/3.11" ]; then
    echo "✓ Virtual environment létezik"
else
    echo "⚠️  Virtual environment nem található!"
    echo "   Létrehozás: python3.11 -m venv $HOME_DIR/virtualenv/googlemaptowebsite/3.11"
fi

# Check if dependencies are installed
echo ""
echo "🔍 Függőségek ellenőrzése..."
if [ -f "requirements.txt" ]; then
    echo "✓ requirements.txt megtalálva"
    echo "   Telepítés: source $HOME_DIR/virtualenv/googlemaptowebsite/3.11/bin/activate && pip install -r requirements.txt"
else
    echo "❌ requirements.txt nem található!"
fi

# Check if .env exists
echo ""
echo "🔍 Környezeti változók ellenőrzése..."
if [ -f ".env" ]; then
    echo "✓ .env fájl létezik"
else
    echo "⚠️  .env fájl nem található!"
    if [ -f ".env.example" ]; then
        echo "   Másolás: cp .env.example .env"
        echo "   Majd szerkeszd a .env fájlt az API kulcsokkal"
    fi
fi

# Check if database is initialized
echo ""
echo "🔍 Adatbázis ellenőrzése..."
if [ -f "googlemaptowebsite.db" ]; then
    echo "✓ Adatbázis létezik"
else
    echo "⚠️  Adatbázis nincs inicializálva!"
    echo "   Inicializálás: python init_db.py"
fi

# Create tmp directory for Passenger restarts
echo ""
echo "📁 tmp könyvtár létrehozása..."
mkdir -p tmp
echo "✓ tmp könyvtár kész"

# Show summary
echo ""
echo "════════════════════════════════════"
echo "✅ KONFIGURÁCIÓ KÉSZ!"
echo "════════════════════════════════════"
echo ""
echo "📋 Következő lépések:"
echo ""
echo "1. Telepítsd a függőségeket:"
echo "   source $HOME_DIR/virtualenv/googlemaptowebsite/3.11/bin/activate"
echo "   pip install -r requirements.txt"
echo ""
echo "2. Állítsd be a környezeti változókat:"
echo "   cp .env.example .env"
echo "   nano .env  # Add meg az API kulcsokat"
echo ""
echo "3. Inicializáld az adatbázist:"
echo "   python init_db.py"
echo ""
echo "4. Indítsd újra az alkalmazást:"
echo "   touch tmp/restart.txt"
echo ""
echo "5. Ellenőrizd a weboldalt:"
echo "   https://magyar-ai.com"
echo ""
echo "🔧 Ha még mindig 503 hibát kapsz:"
echo "   python diagnose.py"
echo ""

# Create a quick restart script
cat > restart.sh << 'EOF'
#!/bin/bash
# Quick restart script
mkdir -p tmp
touch tmp/restart.txt
echo "✓ Alkalmazás újraindítva!"
echo "Ellenőrizd: https://magyar-ai.com"
EOF
chmod +x restart.sh

echo "✓ restart.sh létrehozva (gyors újraindításhoz: ./restart.sh)"
echo ""
