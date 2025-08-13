#!/usr/bin/env python3
"""
WSGI entry point for the Crop Disease Detection API
This file serves as an alternative entry point for deployment environments
"""

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the FastAPI app
from api.app.main import app

# For WSGI compatibility
application = app
