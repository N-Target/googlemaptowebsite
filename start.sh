#!/bin/bash
# Startup script for Hostinger deployment

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source ~/virtualenv/googlemaptowebsite/3.11/bin/activate

# Export environment variables
export APP_ENV=production

# Initialize database if needed
if [ ! -f googlemaptowebsite.db ]; then
    echo "Initializing database..."
    python init_db.py
fi

# Start the application
echo "Starting application..."
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1

# Note: This script is for manual testing.
# For production, Passenger should manage the application lifecycle.
