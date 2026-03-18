"""
Vercel serverless function entry point for FastAPI application
This file is specifically for Vercel deployment and should not affect other deployments.
"""
from main import app

# Vercel expects the ASGI application to be named 'app' or be the default export
# The main.py already defines 'app', so we just import and re-export it
__all__ = ["app"]
