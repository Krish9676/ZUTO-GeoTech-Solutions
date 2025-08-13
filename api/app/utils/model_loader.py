import os
import onnxruntime as ort
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to the ONNX model
MODEL_PATH = os.getenv("MODEL_PATH", "models/mobilenet.onnx")

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