"""
Configuration settings for the Crop Disease Detection API

This module centralizes all configuration settings including:
- Environment variables
- File paths
- Model settings
- API settings
"""

import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
APP_DIR = Path(__file__).parent

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "mobilenet.onnx"))
MODEL_INPUT_SIZE = int(os.getenv("MODEL_INPUT_SIZE", "160"))

# Class and crop map paths
CLASS_MAP_PATH = BASE_DIR / "models" / "class_map.json"
DISEASE_CLASS_MAP_PATH = BASE_DIR / "models" / "disease_class_map.json"
CROP_MAP_PATH = BASE_DIR / "models" / "crop_map.json"

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
STORAGE_BUCKET = os.getenv("STORAGE_BUCKET", "crop-images")

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Storage configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", str(BASE_DIR.parent / "temp"))

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# Validation functions
def validate_config() -> List[str]:
    """Validate configuration and return list of errors"""
    errors = []
    
    # Check required environment variables
    if not SUPABASE_URL:
        errors.append("SUPABASE_URL is required")
    if not SUPABASE_KEY:
        errors.append("SUPABASE_KEY is required")
    
    # Check if model file exists (try multiple locations)
    model_found = False
    for path in get_model_paths():
        if os.path.exists(path):
            model_found = True
            break
    
    if not model_found:
        errors.append("Model file not found in any expected location")
    
    # Check if class map exists (try multiple locations)
    class_map_found = False
    for path in get_class_map_paths():
        if os.path.exists(path):
            class_map_found = True
            break
    
    if not class_map_found:
        errors.append("Class map file not found in any expected location")
    
    return errors

def get_model_paths() -> List[str]:
    """Get all possible model paths for fallback"""
    return [
        MODEL_PATH,
        str(BASE_DIR / "models" / "mobilenet.onnx"),
        str(Path.cwd() / "models" / "mobilenet.onnx"),
        "models/mobilenet.onnx"
    ]

def get_class_map_paths() -> List[str]:
    """Get all possible class map paths for fallback"""
    return [
        str(DISEASE_CLASS_MAP_PATH),  # Try new disease class map first
        str(CLASS_MAP_PATH),
        str(BASE_DIR / "models" / "disease_class_map.json"),
        str(BASE_DIR / "models" / "class_map.json"),
        str(Path.cwd() / "models" / "disease_class_map.json"),
        str(Path.cwd() / "models" / "class_map.json"),
        "models/disease_class_map.json",
        "models/class_map.json"
    ]

def get_crop_map_paths() -> List[str]:
    """Get all possible crop map paths for fallback"""
    return [
        str(CROP_MAP_PATH),
        str(BASE_DIR / "models" / "crop_map.json"),
        str(Path.cwd() / "models" / "crop_map.json"),
        "models/crop_map.json"
    ]

def get_temp_dir() -> str:
    """Get the best available temp directory"""
    possible_dirs = [
        UPLOAD_DIR,
        str(BASE_DIR.parent / "temp"),
        str(BASE_DIR / "temp"),
        str(Path.cwd() / "temp"),
        "temp"
    ]
    
    for dir_path in possible_dirs:
        if os.path.exists(dir_path) or os.access(os.path.dirname(dir_path), os.W_OK):
            return dir_path
    
    return "temp"  # Fallback
