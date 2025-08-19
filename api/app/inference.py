import os
import numpy as np
import onnxruntime as ort
from typing import Dict, Any, List
from .config import get_model_paths, get_class_map_paths, get_crop_map_paths

# Global model session - lazy loaded
_model_session = None

# Path to the ONNX model - use centralized config
def get_model_path():
    """Get the correct path to the model file"""
    # Use centralized config paths
    possible_paths = get_model_paths()
    
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

# Load class labels from disease_class_map.json
import json

def load_class_labels():
    """Load disease class labels from disease_class_map.json"""
    try:
        # First try to load the new disease class map
        disease_class_map_path = os.path.join(os.path.dirname(__file__), "..", "models", "disease_class_map.json")
        
        if os.path.exists(disease_class_map_path):
            with open(disease_class_map_path, "r") as f:
                class_map = json.load(f)
            # Convert to list, sorted by key
            labels = [class_map[str(i)] for i in range(len(class_map))]
            print(f"✅ Loaded disease class labels from: {disease_class_map_path}")
            return labels
        
        # Fallback to original class_map.json
        possible_paths = get_class_map_paths()
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    class_map = json.load(f)
                # Convert to list, sorted by key
                labels = [class_map[str(i)] for i in range(len(class_map))]
                print(f"✅ Loaded class labels from: {path}")
                return labels
        
        print("❌ No class map found, using fallback labels")
        # Fallback labels - update these based on your actual training classes
        return [
            "healthy_rice", "rice_bacterial_blight", "rice_brown_spot", "rice_leaf_smut",
            "healthy_wheat", "wheat_brown_rust", "wheat_yellow_rust", "wheat_septoria_leaf_blotch",
            "healthy_maize", "maize_gray_leaf_spot", "maize_common_rust", "maize_northern_leaf_blight",
            "healthy_potato", "potato_early_blight", "potato_late_blight",
            "healthy_tomato", "tomato_bacterial_spot", "tomato_early_blight", "tomato_late_blight"
        ]
    except Exception as e:
        print(f"Error loading class labels: {e}")
        # Fallback labels
        return [
            "healthy_rice", "rice_bacterial_blight", "rice_brown_spot", "rice_leaf_smut",
            "healthy_wheat", "wheat_brown_rust", "wheat_yellow_rust", "wheat_septoria_leaf_blotch",
            "healthy_maize", "maize_gray_leaf_spot", "maize_common_rust", "maize_northern_leaf_blight",
            "healthy_potato", "potato_early_blight", "potato_late_blight",
            "healthy_tomato", "tomato_bacterial_spot", "tomato_early_blight", "tomato_late_blight"
        ]

# Load crop labels - you'll need to create this based on your training
def load_crop_labels():
    """Load crop labels - update this based on your actual training crops"""
    try:
        # Use centralized config paths
        possible_paths = get_crop_map_paths()
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "r") as f:
                    crop_map = json.load(f)
                # Convert to list, sorted by key
                crops = [crop_map[str(i)] for i in range(len(crop_map))]
                print(f"✅ Loaded crop labels from: {path}")
                return crops
        
        print("❌ Crop map not found, using fallback crops")
        # Fallback crops - update these based on your actual training crops
        return ["rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate"]
    except Exception as e:
        print(f"Error loading crop labels: {e}")
        # Fallback crops
        return ["rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate"]

CLASS_LABELS = load_class_labels()
CROP_LABELS = load_crop_labels()

def get_crop_id(crop_name: str) -> int:
    """Get crop ID from crop name"""
    try:
        return CROP_LABELS.index(crop_name.lower())
    except ValueError:
        print(f"⚠️ Crop '{crop_name}' not found in crop labels, using default (0)")
        return 0

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


def run_inference(image_tensor, crop_name: str = None) -> Dict[str, Any]:
    """Run inference on the preprocessed image tensor with crop information
    
    Args:
        image_tensor: Preprocessed image tensor ready for model input
        crop_name: Name of the crop (optional, will use default if not provided)
        
    Returns:
        Dictionary containing prediction results
    """
    try:
        # Load the model (lazy loading - only loads on first request)
        session = load_model()
        
        # Get input names
        input_names = [input.name for input in session.get_inputs()]
        print(f"Model input names: {input_names}")
        
        # Convert tensor to numpy array if it's not already
        if hasattr(image_tensor, 'numpy'):
            image_np = image_tensor.numpy()
        else:
            image_np = image_tensor
            
        # Ensure the input has the right shape (add batch dimension if needed)
        if len(image_np.shape) == 3:
            image_np = np.expand_dims(image_np, axis=0)
        
        # Get crop ID
        crop_id = get_crop_id(crop_name) if crop_name else 0
        crop_id_np = np.array([crop_id], dtype=np.int64)
        
        # Prepare inputs for the model
        inputs = {}
        if 'image' in input_names and 'crop_id' in input_names:
            # New model with both image and crop_id inputs
            inputs = {
                'image': image_np,
                'crop_id': crop_id_np
            }
        elif 'input' in input_names:
            # Legacy model with single input
            inputs = {'input': image_np}
        else:
            # Fallback - try first input name
            inputs = {input_names[0]: image_np}
        
        # Run inference
        outputs = session.run(None, inputs)
        
        # Process the output
        scores = outputs[0][0]
        
        # Apply softmax to convert logits to probabilities
        exp_scores = np.exp(scores - np.max(scores))  # Subtract max for numerical stability
        probabilities = exp_scores / np.sum(exp_scores)
        
        # Get the index of the highest probability
        predicted_class_idx = np.argmax(probabilities)
        
        # Get the confidence score (probability is already between 0-1)
        confidence = float(probabilities[predicted_class_idx])
        
        # Ensure confidence is within valid range (0-1)
        confidence = max(0.0, min(1.0, confidence))
        
        # Get the class label
        label = CLASS_LABELS[predicted_class_idx]
        
        # Debug information
        print(f"🎯 Crop used: {crop_name or 'default'}")
        print(f"🎯 Raw scores: {scores[predicted_class_idx]:.4f}")
        print(f"🎯 Probability: {probabilities[predicted_class_idx]:.4f}")
        print(f"🎯 Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
        
        # Return the results
        return {
            "label": label,
            "confidence": confidence,
            "class_index": int(predicted_class_idx),
            "raw_scores": scores.tolist(),
            "probabilities": probabilities.tolist(),
            "crop_used": crop_name or "default"
        }
    
    except Exception as e:
        print(f"Error during inference: {e}")
        raise