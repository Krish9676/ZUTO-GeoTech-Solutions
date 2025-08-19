import os
import onnxruntime as ort
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import config here to avoid circular imports
from ..config import get_model_paths

# Get the resolved model path
MODEL_PATH = None

def get_model_path():
    """Get the correct path to the model file"""
    global MODEL_PATH
    
    if MODEL_PATH is None:
        # Use centralized config paths
        possible_paths = get_model_paths()
        
        for path in possible_paths:
            if path and os.path.exists(path):
                print(f"✅ Found model at: {path}")
                MODEL_PATH = path
                return MODEL_PATH
        
        # If no path found, show available paths for debugging
        print(f"❌ Model file not found. Searched in:")
        for path in possible_paths:
            if path:
                print(f"   - {path} (exists: {os.path.exists(path)})")
        
        raise FileNotFoundError("Model file not found in any expected location")
    
    return MODEL_PATH

# Singleton pattern for model session
_model_session = None


def get_model_session() -> ort.InferenceSession:
    """Get or create the ONNX model inference session
    
    Uses a singleton pattern to avoid loading the model multiple times.
    
    Returns:
        ONNX InferenceSession object
    """
    global _model_session
    
    if _model_session is None:
        try:
            # Check if model file exists
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            
            # Set execution providers - use CUDA if available, otherwise CPU
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            
            # Create session
            _model_session = ort.InferenceSession(MODEL_PATH, providers=providers)
            
            print(f"Model loaded successfully from {MODEL_PATH}")
            print(f"Using providers: {_model_session.get_providers()}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    return _model_session


def get_model_metadata() -> Dict[str, Any]:
    """Get metadata about the loaded model
    
    Returns:
        Dictionary containing model metadata
    """
    session = get_model_session()
    
    # Get input details
    inputs = session.get_inputs()
    input_details = []
    for input in inputs:
        input_details.append({
            "name": input.name,
            "shape": input.shape,
            "type": input.type
        })
    
    # Get output details
    outputs = session.get_outputs()
    output_details = []
    for output in outputs:
        output_details.append({
            "name": output.name,
            "shape": output.shape,
            "type": output.type
        })
    
    return {
        "model_path": MODEL_PATH,
        "providers": session.get_providers(),
        "inputs": input_details,
        "outputs": output_details
    }