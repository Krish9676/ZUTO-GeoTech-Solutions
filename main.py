#!/usr/bin/env python3
"""
Main entry point for the Crop Disease Detection API
This file allows the API to be run from the root directory
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import and run the API
from api.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.app.main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=False
    )
