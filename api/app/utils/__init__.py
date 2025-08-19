"""
Utility modules for the Crop Disease Detection API

This package contains utility functions for:
- Image processing and preprocessing
- Model loading and management
- Heatmap generation
- Supabase client operations
"""

__version__ = "1.0.0"

# Import utility functions for easy access
from .image_utils import preprocess_image, save_image_locally, resize_image, tensor_to_image
from .model_loader import get_model_session, get_model_metadata
from .heatmap import generate_heatmap
from .heatmap_simple import generate_heatmap_simple
from .supabase_client import get_supabase_client

__all__ = [
    "preprocess_image",
    "save_image_locally", 
    "resize_image",
    "tensor_to_image",
    "get_model_session",
    "get_model_metadata",
    "generate_heatmap",
    "generate_heatmap_simple",
    "get_supabase_client"
]
