#!/usr/bin/env python3
"""
Main entry point for the Crop Disease Detection API
This file serves as the entry point for deployment environments
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app
from api.app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=False
    )
