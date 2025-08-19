"""
Crop Disease Detection API Package

This package provides a FastAPI-based REST API for detecting crop diseases
from uploaded images using ONNX models and LLaMA integration.
"""

__version__ = "1.0.0"
__author__ = "Crop Disease Detection Team"

# Import the main FastAPI app
from .app.main import app

# Export the app for easy access
__all__ = ["app"]
