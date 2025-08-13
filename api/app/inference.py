import os
import numpy as np
import onnxruntime as ort
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Global model session - lazy loaded
_model_session = None

# Path to the ONNX model - use absolute path resolution
def get_model_path():
    """Get the correct path to the model file"""
    # Try multiple possible locations
    possible_paths = [
        # If MODEL_PATH environment variable is set
        os.getenv("MODEL_PATH"),
        # Relative to current file location
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "mobilenet.onnx"),
        # Relative to current working directory
        os.path.join(os.getcwd(), "models", "mobilenet.onnx"),
        # Relative to api directory
        os.path.join("models", "mobilenet.onnx"),
        # Absolute path from project root
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "api", "models", "mobilenet.onnx")
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            print(f"✅ Found model at: {path}")
            return path
    
    # If no path found, show available paths for debugging
    print(f"❌ Model file not found. Searched in:")
    for path in possible_paths:
        if path:
            print(f"   - {path} (exists: {os.path.exists(path)})")
    
    raise FileNotFoundError("Model file not found in any expected location")

# Load class labels from class_map.json
import json

def load_class_labels():
    """Load class labels from class_map.json"""
    try:
        # Try multiple possible locations for class_map.json
        possible_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "class_map.json"),
            os.path.join(os.getcwd(), "models", "class_map.json"),
            os.path.join("models", "class_map.json"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "api", "models", "class_map.json")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    class_map = json.load(f)
                # Convert to list, sorted by key
                labels = [class_map[str(i)] for i in range(len(class_map))]
                print(f"✅ Loaded class labels from: {path}")
                return labels
        
        print("❌ Class map not found, using fallback labels")
        # Fallback labels
        return [
            "banana", "brinjal", "cabbage", "cauliflower", "chilli", "cotton",
            "grapes", "maize", "mango", "mustard", "onion", "oranges",
            "papaya", "pomegranade", "potato", "rice", "soyabean", "sugarcane",
            "tobacco", "tomato", "wheat"
        ]
    except Exception as e:
        print(f"Error loading class labels: {e}")
        # Fallback labels
        return [
            "banana", "brinjal", "cabbage", "cauliflower", "chilli", "cotton",
            "grapes", "maize", "mango", "mustard", "onion", "oranges",
            "papaya", "pomegranade", "potato", "rice", "soyabean", "sugarcane",
            "tobacco", "tomato", "wheat"
        ]

CLASS_LABELS = load_class_labels()


def load_model():
    """Load the ONNX model (lazy loading)"""
    global _model_session
    
    if _model_session is None:
        try:
            # Get the correct model path
            model_path = get_model_path()
            
            print(f"✅ Loading model from: {model_path}")
            _model_session = ort.InferenceSession(model_path)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    return _model_session


def run_inference(image_tensor) -> Dict[str, Any]:
    """Run inference on the preprocessed image tensor
    
    Args:
        image_tensor: Preprocessed image tensor ready for model input
        
    Returns:
        Dictionary containing prediction results
    """
    try:
        # Load the model (lazy loading - only loads on first request)
        session = load_model()
        
        # Get input name
        input_name = session.get_inputs()[0].name
        
        # Convert tensor to numpy array if it's not already
        if hasattr(image_tensor, 'numpy'):
            image_np = image_tensor.numpy()
        else:
            image_np = image_tensor
            
        # Ensure the input has the right shape (add batch dimension if needed)
        if len(image_np.shape) == 3:
            image_np = np.expand_dims(image_np, axis=0)
        
        # Run inference
        outputs = session.run(None, {input_name: image_np})
        
        # Process the output
        scores = outputs[0][0]
        
        # Get the index of the highest score
        predicted_class_idx = np.argmax(scores)
        
        # Get the confidence score (convert to percentage)
        confidence = float(scores[predicted_class_idx] * 100)
        
        # Get the class label
        label = CLASS_LABELS[predicted_class_idx]
        
        # Return the results
        return {
            "label": label,
            "confidence": confidence,
            "class_index": int(predicted_class_idx),
            "raw_scores": scores.tolist(),
        }
    
    except Exception as e:
        print(f"Error during inference: {e}")
        raise