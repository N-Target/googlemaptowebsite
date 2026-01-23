#!/bin/bash

################################################################################
# Teljes Hostinger Telepítő és Frissítő Script
# Complete Hostinger Deployment and Update Script
# 
# This script does EVERYTHING needed to deploy or update on Hostinger:
# 1. Health checks before deployment
# 2. Configuration
# 3. Dependencies installation
# 4. Database setup
# 5. Application restart
# 6. Post-deployment verification
################################################################################

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_BRANCH="${DEPLOY_BRANCH:-copilot/add-ai-web-generator}"
PYTHON_VERSION="3.11"
VENV_NAME="googlemaptowebsite"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo ""
    echo "=================================="
    echo -e "${BLUE}$1${NC}"
    echo "=================================="
    echo ""
}

print_step() {
    echo -e "${YELLOW}[$1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

################################################################################
# Health Check Functions
################################################################################

check_system_health() {
    print_header "Előzetes Rendszer Ellenőrzés / Pre-Deployment Health Check"
    
    local all_ok=true
    
    # Check 1: Internet connectivity
    print_step "1/6" "Internet kapcsolat ellenőrzése..."
    if ping -c 1 github.com &> /dev/null; then
        print_success "Internet kapcsolat rendben"
    else
        print_error "Nincs internet kapcsolat!"
        all_ok=false
    fi
    
    # Check 2: Git repository
    print_step "2/6" "Git repository ellenőrzése..."
    if [ -d ".git" ]; then
        print_success "Git repository rendben"
    else
        print_error "Nem Git repository! Kérlek futtasd a repo mappájában."
        all_ok=false
    fi
    
    # Check 3: Python availability
    print_step "3/6" "Python ellenőrzése..."
    if command -v python3.11 &> /dev/null; then
        print_success "Python 3.11 telepítve: $(python3.11 --version)"
    elif command -v python3 &> /dev/null; then
        print_warning "Python 3.11 nem található, használom: $(python3 --version)"
    else
        print_error "Python nem található!"
        all_ok=false
    fi
    
    # Check 4: Disk space
    print_step "4/6" "Lemezterület ellenőrzése..."
    local available_space=$(df -h . | tail -n 1 | awk '{print $4}')
    print_success "Elérhető lemezterület: $available_space"
    
    # Check 5: Required files
    print_step "5/6" "Szükséges fájlok ellenőrzése..."
    local required_files=("requirements.txt" "main.py" "passenger_wsgi.py" ".htaccess")
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        print_success "Minden szükséges fájl megtalálható"
    else
        print_error "Hiányzó fájlok: ${missing_files[*]}"
        all_ok=false
    fi
    
    # Check 6: Permissions
    print_step "6/6" "Engedélyek ellenőrzése..."
    if [ -w "." ]; then
        print_success "Írási jogosultság rendben"
    else
        print_error "Nincs írási jogosultság ebben a mappában!"
        all_ok=false
    fi
    
    echo ""
    if [ "$all_ok" = true ]; then
        print_success "Minden előzetes ellenőrzés sikeres! Folytatom..."
        return 0
    else
        print_error "Néhány ellenőrzés sikertelen. Javítsd a hibákat és futtasd újra."
        return 1
    fi
}

################################################################################
# Configuration Functions
################################################################################

configure_deployment() {
    print_header "Telepítési Konfiguráció / Deployment Configuration"
    
    # Detect environment
    USERNAME=$(whoami)
    HOME_DIR=$HOME
    CURRENT_DIR=$(pwd)
    
    print_success "Felhasználónév: $USERNAME"
    print_success "Home könyvtár: $HOME_DIR"
    print_success "Jelenlegi könyvtár: $CURRENT_DIR"
    echo ""
    
    # Configure .htaccess
    print_step "1/2" ".htaccess konfigurálása..."
    if [ -f ".htaccess" ]; then
        # Create backup with timestamp
        BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        cp .htaccess ".htaccess.backup.$BACKUP_TIMESTAMP" 2>/dev/null || true
        
        # Replace username placeholder
        sed -i "s|/home/username/|$HOME_DIR/|g" .htaccess
        
        print_success ".htaccess konfigurálva!"
    else
        print_warning ".htaccess nem található, átugorva"
    fi
    
    # Configure passenger_wsgi.py
    print_step "2/2" "passenger_wsgi.py konfigurálása..."
    if [ -f "passenger_wsgi.py" ]; then
        # Create backup with timestamp
        BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        cp passenger_wsgi.py "passenger_wsgi.py.backup.$BACKUP_TIMESTAMP" 2>/dev/null || true
        
        # Replace username placeholder
        sed -i "s|/home/username/|$HOME_DIR/|g" passenger_wsgi.py
        
        print_success "passenger_wsgi.py konfigurálva!"
    else
        print_warning "passenger_wsgi.py nem található, átugorva"
    fi
    
    echo ""
}

################################################################################
# Git Update Functions
################################################################################

update_from_git() {
    print_header "Git Frissítés / Git Update"
    
    print_step "1/3" "Git status ellenőrzése..."
    git status --short
    echo ""
    
    print_step "2/3" "Legújabb változások letöltése..."
    if git pull origin "$REPO_BRANCH"; then
        print_success "Git pull sikeres!"
    else
        print_error "Git pull sikertelen!"
        return 1
    fi
    echo ""
    
    print_step "3/3" "Jelenlegi commit információ..."
    git log -1 --oneline
    print_success "Git frissítés kész!"
    echo ""
}

################################################################################
# Virtual Environment Functions
################################################################################

setup_virtualenv() {
    print_header "Virtual Environment Beállítás"
    
    VENV_PATH="$HOME/virtualenv/$VENV_NAME/$PYTHON_VERSION"
    
    print_step "1/3" "Virtual environment keresése: $VENV_PATH"
    
    if [ -d "$VENV_PATH" ]; then
        print_success "Virtual environment megtalálva!"
        
        print_step "2/3" "Virtual environment aktiválása..."
        source "$VENV_PATH/bin/activate"
        print_success "Aktiválva! Python verzió: $(python --version)"
        
        print_step "3/3" "Függőségek frissítése..."
        pip install --upgrade pip -q
        pip install -r requirements.txt -q
        print_success "Függőségek telepítve!"
    else
        print_warning "Virtual environment nem található: $VENV_PATH"
        print_step "2/3" "Hostinger rendszer Python használata..."
        
        if command -v python3.11 &> /dev/null; then
            PYTHON_CMD="python3.11"
        elif command -v python3 &> /dev/null; then
            PYTHON_CMD="python3"
        else
            print_error "Python nem található!"
            return 1
        fi
        
        print_success "Python parancs: $PYTHON_CMD"
        
        print_step "3/3" "Függőségek telepítése (user mode)..."
        $PYTHON_CMD -m pip install --user -r requirements.txt -q
        print_success "Függőségek telepítve!"
    fi
    
    echo ""
}

################################################################################
# Database Functions
################################################################################

setup_database() {
    print_header "Adatbázis Beállítás / Database Setup"
    
    print_step "1/2" "Adatbázis ellenőrzése..."
    
    # Determine Python command
    if [ -n "$(type -t python)" ]; then
        PYTHON_CMD="python"
    elif command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        print_error "Python nem található!"
        return 1
    fi
    
    if [ -f "app.db" ]; then
        print_success "Adatbázis megtalálható (app.db)"
        
        # Get database size
        DB_SIZE=$(du -h app.db | cut -f1)
        print_success "Adatbázis méret: $DB_SIZE"
    else
        print_warning "Adatbázis nem található, létrehozom..."
        
        print_step "2/2" "Adatbázis inicializálása..."
        if $PYTHON_CMD init_db.py; then
            print_success "Adatbázis sikeresen inicializálva!"
        else
            print_error "Adatbázis inicializálás sikertelen!"
            return 1
        fi
    fi
    
    echo ""
}

################################################################################
# Configuration File Functions
################################################################################

check_configuration_files() {
    print_header "Konfigurációs Fájlok Ellenőrzése"
    
    print_step "1/1" ".env fájl ellenőrzése..."
    
    if [ -f ".env" ]; then
        print_success ".env fájl megtalálható"
        
        # Check if it has content
        if [ -s ".env" ]; then
            print_success ".env fájl nem üres"
        else
            print_warning ".env fájl üres! Konfiguráld az API kulcsokat."
        fi
    else
        print_warning ".env fájl nem található!"
        
        if [ -f ".env.example" ]; then
            echo ""
            echo "Létrehozom .env fájlt a példából..."
            cp .env.example .env
            print_warning ".env fájl létrehozva! FONTOS: Add meg az API kulcsokat!"
            echo ""
            echo "Szerkeszd a .env fájlt és add meg:"
            echo "  - OPENAI_API_KEY"
            echo "  - GOOGLE_MAPS_API_KEY"
            echo "  - GOOGLE_PLACES_API_KEY"
        fi
    fi
    
    echo ""
}

################################################################################
# Restart Functions
################################################################################

restart_application() {
    print_header "Alkalmazás Újraindítás / Application Restart"
    
    print_step "1/2" "Restart signal küldése Passenger-nek..."
    mkdir -p tmp
    touch tmp/restart.txt
    
    if [ $? -eq 0 ]; then
        print_success "Restart signal elküldve!"
    else
        print_error "Restart sikertelen!"
        return 1
    fi
    
    print_step "2/2" "Várakozás az alkalmazás indulására..."
    sleep 3
    print_success "Alkalmazás újraindul..."
    
    echo ""
}

################################################################################
# Verification Functions
################################################################################

verify_deployment() {
    print_header "Telepítés Ellenőrzése / Deployment Verification"
    
    local domain="magyar-ai.com"
    local all_ok=true
    
    print_step "1/4" "Fájlrendszer ellenőrzés..."
    if [ -f "main.py" ] && [ -f "app.db" ]; then
        print_success "Alapvető fájlok rendben"
    else
        print_error "Hiányzó fájlok!"
        all_ok=false
    fi
    
    print_step "2/4" "Konfiguráció ellenőrzés..."
    if [ -f ".env" ]; then
        print_success "Környezeti változók fájl rendben"
    else
        print_warning "Nincs .env fájl!"
        all_ok=false
    fi
    
    print_step "3/4" "Passenger konfiguráció ellenőrzés..."
    if [ -f "tmp/restart.txt" ]; then
        print_success "Restart jelző fájl rendben"
    else
        print_warning "Restart jelző hiányzik"
    fi
    
    print_step "4/4" "Weboldalunk ellenőrzése..."
    echo ""
    echo "Próbáld meg elérni:"
    echo "  🌐 https://$domain"
    echo "  🎨 https://$domain/admin"
    echo "  ❤️  https://$domain/health"
    echo ""
    
    if [ "$all_ok" = true ]; then
        print_success "Minden ellenőrzés sikeres!"
    else
        print_warning "Néhány ellenőrzés figyelmeztetést adott"
    fi
    
    echo ""
}

################################################################################
# Quick Restart Function (for subsequent updates)
################################################################################

quick_restart() {
    print_header "Gyors Újraindítás / Quick Restart"
    
    mkdir -p tmp
    touch tmp/restart.txt
    
    print_success "Újraindítás elküldve!"
    echo ""
    echo "Az alkalmazás 10-15 másodpercen belül újraindul."
    echo "Ellenőrizd: https://magyar-ai.com/admin"
    echo ""
}

################################################################################
# Main Installation Flow
################################################################################

full_deployment() {
    print_header "🚀 Teljes Hostinger Telepítés és Frissítés"
    echo "Magyar-AI.com Deployment Script"
    echo ""
    
    # Step 1: Health checks
    if ! check_system_health; then
        print_error "Egészség ellenőrzés sikertelen! Kilépés."
        exit 1
    fi
    
    # Step 2: Configuration
    configure_deployment
    
    # Step 3: Git update
    if ! update_from_git; then
        print_error "Git frissítés sikertelen!"
        exit 1
    fi
    
    # Step 4: Virtual environment setup
    if ! setup_virtualenv; then
        print_error "Virtual environment beállítás sikertelen!"
        exit 1
    fi
    
    # Step 5: Database setup
    if ! setup_database; then
        print_error "Adatbázis beállítás sikertelen!"
        exit 1
    fi
    
    # Step 6: Configuration files
    check_configuration_files
    
    # Step 7: Restart application
    if ! restart_application; then
        print_error "Újraindítás sikertelen!"
        exit 1
    fi
    
    # Step 8: Verification
    verify_deployment
    
    # Final success message
    print_header "✅ TELEPÍTÉS SIKERES / DEPLOYMENT SUCCESSFUL"
    
    echo "Az alkalmazásod most fut a magyar-ai.com-on!"
    echo ""
    echo "🌐 Weboldal: https://magyar-ai.com"
    echo "🎨 Admin Panel: https://magyar-ai.com/admin"
    echo "❤️  Health Check: https://magyar-ai.com/health"
    echo "📚 API Docs: https://magyar-ai.com/docs"
    echo ""
    echo "Ha 503 hibát látsz, várj 10-15 másodpercet a Passenger indulására."
    echo ""
    echo "📋 Logok megtekintése:"
    echo "   tail -f ~/logs/passenger.log"
    echo ""
    echo "🔄 Következő frissítéshez csak futtasd újra ezt a scriptet!"
    echo "   bash teljes_telepites.sh"
    echo ""
}

################################################################################
# Script Entry Point
################################################################################

# Parse command line arguments
case "${1:-full}" in
    full|install|deploy)
        full_deployment
        ;;
    restart|quick)
        quick_restart
        ;;
    health|check)
        check_system_health
        ;;
    *)
        echo "Használat / Usage:"
        echo "  bash teljes_telepites.sh [full|restart|health]"
        echo ""
        echo "  full    - Teljes telepítés vagy frissítés (alapértelmezett)"
        echo "  restart - Csak gyors újraindítás"
        echo "  health  - Csak rendszer ellenőrzés"
        echo ""
        exit 1
        ;;
esac
