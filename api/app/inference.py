import os
import numpy as np
import onnxruntime as ort
import json
from typing import Dict, Any, List
from .config import get_model_paths, get_class_map_paths, get_crop_map_paths

# Global model session - lazy loaded
_model_session = None
_crop_to_global_classes = None
_preprocess_config = None

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

# Load crop to global classes mapping
def load_crop_to_global_classes():
    """Load the crop to global classes mapping from the trained model checkpoint"""
    global _crop_to_global_classes
    
    if _crop_to_global_classes is None:
        try:
            # First try to load from the JSON file created during conversion
            json_path = os.path.join(os.path.dirname(__file__), "..", "models", "crop_to_global_classes.json")
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    _crop_to_global_classes = json.load(f)
                print(f"✅ Loaded crop to global classes mapping from JSON: {json_path}")
            else:
                # Fallback to loading from the model checkpoint
                checkpoint_path = os.path.join(os.path.dirname(__file__), "..", "models", "cropaware_multicrop_model.pth")
                
                if os.path.exists(checkpoint_path):
                    import torch
                    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
                    _crop_to_global_classes = ckpt["crop_to_global_classes"]
                    
                    # Convert numpy types to Python types for JSON compatibility
                    def convert_numpy_types(obj):
                        if hasattr(obj, 'item'):
                            return obj.item()
                        elif isinstance(obj, list):
                            return [convert_numpy_types(item) for item in obj]
                        elif isinstance(obj, dict):
                            return {key: convert_numpy_types(value) for key, value in obj.items()}
                        return obj
                    
                    _crop_to_global_classes = convert_numpy_types(_crop_to_global_classes)
                    print(f"✅ Loaded crop to global classes mapping from model checkpoint: {checkpoint_path}")
                else:
                    print("❌ Neither JSON nor model checkpoint found, using fallback")
                    _crop_to_global_classes = {}
        except Exception as e:
            print(f"Error loading crop to global classes mapping: {e}")
            _crop_to_global_classes = {}
    
    return _crop_to_global_classes

# Load preprocessing config
def load_preprocess_config():
    """Load preprocessing configuration from the trained model checkpoint"""
    global _preprocess_config
    
    if _preprocess_config is None:
        try:
            # First try to load from the JSON file created during conversion
            json_path = os.path.join(os.path.dirname(__file__), "..", "models", "preprocess_config.json")
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    _preprocess_config = json.load(f)
                print(f"✅ Loaded preprocessing config from JSON: {json_path}")
            else:
                # Fallback to loading from the model checkpoint
                checkpoint_path = os.path.join(os.path.dirname(__file__), "..", "models", "cropaware_multicrop_model.pth")
                
                if os.path.exists(checkpoint_path):
                    import torch
                    ckpt = torch.load(checkpoint_path, map_location='cpu', weights_only=False)
                    _preprocess_config = {
                        "img_size": ckpt.get("img_size", 160),
                        "normalize_mean": ckpt.get("normalize_mean", [0.485, 0.456, 0.406]),
                        "normalize_std": ckpt.get("normalize_std", [0.229, 0.224, 0.225])
                    }
                    print(f"✅ Loaded preprocessing config from model checkpoint: {checkpoint_path}")
                else:
                    print("❌ Neither JSON nor model checkpoint found, using fallback")
                    # Fallback config
                    _preprocess_config = {
                        "img_size": 160,
                        "normalize_mean": [0.485, 0.456, 0.406],
                        "normalize_std": [0.229, 0.224, 0.225]
                    }
        except Exception as e:
            print(f"Error loading preprocessing config: {e}")
            _preprocess_config = {
                "img_size": 160,
                "normalize_mean": [0.485, 0.456, 0.406],
                "normalize_std": [0.229, 0.224, 0.225]
            }
    
    return _preprocess_config

# Load class labels from disease_class_map.json
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
        
        # Load crop to global classes mapping
        crop_to_global_classes = load_crop_to_global_classes()
        
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
        
        # Prepare inputs for the model
        inputs = {}
        if 'image' in input_names:
            # New model with image input only
            inputs = {'image': image_np}
        elif 'input' in input_names:
            # Legacy model with single input
            inputs = {'input': image_np}
        else:
            # Fallback - try first input name
            inputs = {input_names[0]: image_np}
        
        # Run inference
        outputs = session.run(None, inputs)
        
        # Process the output - now we get all concatenated logits
        all_logits = outputs[0][0]  # Shape: (total_classes,)
        
        # Extract crop-specific logits
        crop_id_str = str(crop_id)
        if crop_id_str in crop_to_global_classes:
            # Get the crop-specific class indices
            crop_class_indices = crop_to_global_classes[crop_id_str]
            
            # Calculate the start and end indices for this crop's logits
            # We need to find where this crop's logits start in the concatenated output
            start_idx = 0
            for cid in sorted(crop_to_global_classes.keys()):
                if cid == crop_id_str:
                    break
                start_idx += len(crop_to_global_classes[cid])
            
            end_idx = start_idx + len(crop_class_indices)
            scores = all_logits[start_idx:end_idx]
        else:
            # Fallback - use first few classes
            print(f"⚠️ Crop ID {crop_id} not found in mapping, using first classes")
            scores = all_logits[:15]  # Assume 15 classes per crop
        
        # Apply softmax to convert logits to probabilities
        exp_scores = np.exp(scores - np.max(scores))  # Subtract max for numerical stability
        probabilities = exp_scores / np.sum(exp_scores)
        
        # Get the index of the highest probability (local class index for this crop)
        local_class_idx = np.argmax(probabilities)
        
        # Get the confidence score (probability is already between 0-1)
        confidence = float(probabilities[local_class_idx])
        
        # Ensure confidence is within valid range (0-1)
        confidence = max(0.0, min(1.0, confidence))
        
        # Map local class index to global class index
        if crop_id_str in crop_to_global_classes:
            global_class_idx = crop_to_global_classes[crop_id_str][local_class_idx]
        else:
            # Fallback - use local index directly
            global_class_idx = local_class_idx
            print(f"⚠️ Crop ID {crop_id} not found in mapping, using local index")
        
        # Get the class label using global class index
        if global_class_idx < len(CLASS_LABELS):
            label = CLASS_LABELS[global_class_idx]
        else:
            # Fallback - use local index
            label = f"class_{local_class_idx}"
            print(f"⚠️ Global class index {global_class_idx} out of range, using fallback")
        
        # Debug information
        print(f"🎯 Crop used: {crop_name or 'default'} (ID: {crop_id})")
        print(f"🎯 Local class index: {local_class_idx}")
        print(f"🎯 Global class index: {global_class_idx}")
        print(f"🎯 Raw scores: {scores[local_class_idx]:.4f}")
        print(f"🎯 Probability: {probabilities[local_class_idx]:.4f}")
        print(f"🎯 Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
        
        # Return the results
        return {
            "label": label,
            "confidence": confidence,
            "class_index": int(global_class_idx),
            "local_class_index": int(local_class_idx),
            "raw_scores": scores.tolist(),
            "probabilities": probabilities.tolist(),
            "crop_used": crop_name or "default",
            "crop_id": int(crop_id)
        }
    
    except Exception as e:
        print(f"Error during inference: {e}")
        raise