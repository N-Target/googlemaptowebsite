"""
WSGI entry point for Hostinger/Passenger deployment
This file is required for Passenger to serve the FastAPI application
"""
import sys
import os

# Add the application directory to Python path
INTERP = os.path.join(os.environ['HOME'], 'virtualenv', 'googlemaptowebsite', '3.11', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set working directory
sys.path.insert(0, os.getcwd())

# Import the FastAPI app
from main import app

# For Passenger
application = app
