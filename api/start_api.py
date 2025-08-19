#!/usr/bin/env python3
"""
Startup script for the Crop Disease Detection API
This script ensures proper module imports and starts the FastAPI server
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set environment variables if not already set
os.environ.setdefault("API_HOST", "0.0.0.0")
os.environ.setdefault("API_PORT", "8000")

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    print("🚀 Starting Crop Disease Detection API...")
    print(f"📍 Server will run on: {os.environ['API_HOST']}:{os.environ['API_PORT']}")
    print("🔧 API Documentation will be available at: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host=os.environ["API_HOST"],
        port=int(os.environ["API_PORT"]),
        reload=True,
        log_level="info"
    )
