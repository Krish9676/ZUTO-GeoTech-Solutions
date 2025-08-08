import os
import numpy as np
import onnxruntime as ort
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Path to the ONNX model
MODEL_PATH = os.getenv("MODEL_PATH", "models/mobilenet.onnx")

# Load class labels from class_map.json
import json

def load_class_labels():
    """Load class labels from class_map.json"""
    try:
        with open("models/class_map.json", "r") as f:
            class_map = json.load(f)
        # Convert to list, sorted by key
        labels = [class_map[str(i)] for i in range(len(class_map))]
        return labels
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
    """Load the ONNX model"""
    try:
        # Check if model file exists
        if not os.path.exists(MODEL_PATH):
            print(f"❌ Model file not found at: {MODEL_PATH}")
            print(f"📁 Current directory: {os.getcwd()}")
            print(f"📁 Available files in models/: {os.listdir('models') if os.path.exists('models') else 'models/ not found'}")
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        print(f"✅ Loading model from: {MODEL_PATH}")
        session = ort.InferenceSession(MODEL_PATH)
        print("✅ Model loaded successfully")
        return session
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        raise


def run_inference(image_tensor) -> Dict[str, Any]:
    """Run inference on the preprocessed image tensor
    
    Args:
        image_tensor: Preprocessed image tensor ready for model input
        
    Returns:
        Dictionary containing prediction results
    """
    try:
        # Load the model
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