#!/bin/bash

################################################################################
# Automatic Update Script for Hostinger Deployment
# This script pulls latest changes from GitHub and restarts the application
################################################################################

set -e  # Exit on error

echo "=================================="
echo "Magyar-AI.com Automatic Update"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Pull latest changes from GitHub
echo -e "${YELLOW}[1/5]${NC} Pulling latest changes from GitHub..."
git pull origin copilot/add-ai-web-generator

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Git pull successful"
else
    echo -e "${RED}✗${NC} Git pull failed"
    exit 1
fi
echo ""

# Step 2: Activate virtual environment and update dependencies
echo -e "${YELLOW}[2/5]${NC} Checking virtual environment..."
VENV_PATH="$HOME/virtualenv/googlemaptowebsite/3.11"

if [ -d "$VENV_PATH" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH/bin/activate"
    echo -e "${GREEN}✓${NC} Virtual environment activated"
    
    echo "Updating dependencies..."
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓${NC} Dependencies updated"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found at $VENV_PATH"
    echo "Attempting to use system Python..."
fi
echo ""

# Step 3: Run database migrations if needed
echo -e "${YELLOW}[3/5]${NC} Checking database..."
if [ -f "init_db.py" ]; then
    # Check if database exists
    if [ ! -f "app.db" ]; then
        echo "Database not found. Initializing..."
        python init_db.py
        echo -e "${GREEN}✓${NC} Database initialized"
    else
        echo -e "${GREEN}✓${NC} Database exists"
    fi
else
    echo -e "${YELLOW}⚠${NC} init_db.py not found, skipping database check"
fi
echo ""

# Step 4: Check configuration
echo -e "${YELLOW}[4/5]${NC} Checking configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
else
    echo -e "${YELLOW}⚠${NC} .env file not found"
    echo "Please create .env file with your API keys"
    echo "Copy from .env.example: cp .env.example .env"
fi
echo ""

# Step 5: Restart application
echo -e "${YELLOW}[5/5]${NC} Restarting application..."
mkdir -p tmp
touch tmp/restart.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Restart signal sent to Passenger"
else
    echo -e "${RED}✗${NC} Restart failed"
    exit 1
fi
echo ""

# Final status
echo "=================================="
echo -e "${GREEN}Update Complete!${NC}"
echo "=================================="
echo ""
echo "Your application should be live at:"
echo "  → https://magyar-ai.com"
echo "  → https://magyar-ai.com/admin"
echo ""
echo "Check status:"
echo "  → https://magyar-ai.com/health"
echo ""
echo "If you see 503 error, wait 10-15 seconds for Passenger to restart"
echo ""
echo "View logs: tail -f ~/logs/passenger.log"
echo ""
