#!/usr/bin/env python3

import os
import sys
import argparse
import time
import json
import numpy as np
from PIL import Image
import onnxruntime as ort
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import app modules
try:
    from app.utils.image_utils import preprocess_image, resize_image
    from app.utils.model_loader import get_model_session, get_model_metadata
    from app.utils.heatmap import generate_heatmap
except ImportError as e:
    print(f"Error importing app modules: {e}", file=sys.stderr)
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH", "models/mobilenet.onnx")

# Class labels (example - replace with your actual labels)
CLASS_LABELS = [
    "Healthy",
    "Fall Armyworm",
    "Corn Leaf Blight",
    "Common Rust",
    "Gray Leaf Spot",
    "Northern Leaf Blight"
]

def load_model(model_path):
    """Load ONNX model"""
    try:
        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}", file=sys.stderr)
            print("\nYou can download a model using the scripts/download_model.py script:")
            print("  python scripts/download_model.py --model mobilenet")
            sys.exit(1)
        
        # Create inference session
        session = ort.InferenceSession(model_path)
        return session
    except Exception as e:
        print(f"Error loading model: {e}", file=sys.stderr)
        sys.exit(1)

def load_image(image_path):
    """Load and preprocess image for inference"""
    try:
        if not os.path.exists(image_path):
            print(f"Error: Image file not found at {image_path}", file=sys.stderr)
            sys.exit(1)
        
        # Open image
        image = Image.open(image_path).convert("RGB")
        
        # Preprocess image
        input_tensor = preprocess_image(image)
        
        return image, input_tensor
    except Exception as e:
        print(f"Error loading image: {e}", file=sys.stderr)
        sys.exit(1)

def run_inference(session, input_tensor):
    """Run inference on input tensor"""
    try:
        # Get input name
        input_name = session.get_inputs()[0].name
        
        # Run inference
        start_time = time.time()
        outputs = session.run(None, {input_name: input_tensor.numpy()})
        end_time = time.time()
        
        # Get output
        output = outputs[0]
        
        # Get prediction
        scores = output[0]
        predicted_class_idx = np.argmax(scores)
        confidence = float(scores[predicted_class_idx]) * 100
        
        # Get class label
        if predicted_class_idx < len(CLASS_LABELS):
            predicted_class = CLASS_LABELS[predicted_class_idx]
        else:
            predicted_class = f"Class {predicted_class_idx}"
        
        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "class_idx": int(predicted_class_idx),
            "scores": scores.tolist(),
            "time_taken": end_time - start_time
        }
    except Exception as e:
        print(f"Error running inference: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Test ONNX model inference')
    parser.add_argument('--image', type=str, required=True,
                        help='Path to image file')
    parser.add_argument('--model', type=str, default=MODEL_PATH,
                        help=f'Path to ONNX model file (default: {MODEL_PATH})')
    parser.add_argument('--labels', type=str, default=None,
                        help='Path to JSON file with class labels')
    parser.add_argument('--heatmap', action='store_true',
                        help='Generate heatmap visualization')
    parser.add_argument('--output', type=str, default=None,
                        help='Path to save output JSON')
    
    args = parser.parse_args()
    
    # Load class labels if provided
    global CLASS_LABELS
    if args.labels:
        try:
            with open(args.labels, 'r') as f:
                CLASS_LABELS = json.load(f)
        except Exception as e:
            print(f"Error loading class labels: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Load model
    print(f"Loading model from {args.model}...")
    session = load_model(args.model)
    
    # Get model metadata
    model_metadata = get_model_metadata()
    print(f"Model loaded successfully!")
    print(f"Input details: {model_metadata['inputs']}")
    print(f"Output details: {model_metadata['outputs']}")
    print(f"Providers: {model_metadata['providers']}")
    
    # Load image
    print(f"\nLoading image from {args.image}...")
    image, input_tensor = load_image(args.image)
    print(f"Image loaded successfully!")
    print(f"Image size: {image.size}")
    print(f"Input tensor shape: {input_tensor.shape}")
    
    # Run inference
    print("\nRunning inference...")
    result = run_inference(session, input_tensor)
    
    # Print results
    print(f"\nPrediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2f}%")
    print(f"Class index: {result['class_idx']}")
    print(f"Time taken: {result['time_taken']:.4f} seconds")
    
    # Print top 3 predictions
    print("\nTop 3 predictions:")
    scores = np.array(result['scores'])
    top_indices = np.argsort(scores)[::-1][:3]
    for i, idx in enumerate(top_indices):
        if idx < len(CLASS_LABELS):
            class_name = CLASS_LABELS[idx]
        else:
            class_name = f"Class {idx}"
        print(f"{i+1}. {class_name}: {scores[idx]*100:.2f}%")
    
    # Generate heatmap if requested
    if args.heatmap:
        print("\nGenerating heatmap...")
        try:
            heatmap_path = os.path.splitext(args.image)[0] + "_heatmap.jpg"
            generate_heatmap(image, input_tensor, result['class_idx'], heatmap_path)
            print(f"Heatmap saved to {heatmap_path}")
        except Exception as e:
            print(f"Error generating heatmap: {e}", file=sys.stderr)
    
    # Save output if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nOutput saved to {args.output}")
        except Exception as e:
            print(f"Error saving output: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()