"""
Crop Disease Detection API Application

This module contains the main FastAPI application and related components
for the crop disease detection service.
"""

__version__ = "1.0.0"

# Import the main FastAPI app
from .main import app

# Export the app for easy access
__all__ = ["app"]
