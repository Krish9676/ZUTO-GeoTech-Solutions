#!/usr/bin/env python3

import os
import sys
import argparse
import json
import torch
import torch.nn as nn
from torchvision import models
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

# Default paths
DEFAULT_INPUT_PATH = os.getenv("MODEL_PATH", "models/mobilenet_crop_pest_model.pth")
DEFAULT_OUTPUT_PATH = os.getenv("MODEL_PATH", "models/mobilenet.onnx")
DEFAULT_CLASS_MAP_PATH = "models/class_map.json"


def load_class_map(class_map_path):
    """Load class map from JSON file"""
    try:
        with open(class_map_path, 'r') as f:
            class_map = json.load(f)
        return class_map
    except Exception as e:
        print(f"Error loading class map: {e}", file=sys.stderr)
        return None


def create_model(num_classes):
    """Create a MobileNetV2 model with the specified number of classes"""
    # Create a MobileNetV2 model
    model = models.mobilenet_v2(pretrained=False)
    
    # Modify the classifier to match the number of classes
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    
    return model


def convert_to_onnx(input_path, output_path, class_map_path):
    """Convert PyTorch model to ONNX format"""
    try:
        # Load class map
        class_map = load_class_map(class_map_path)
        if not class_map:
            print("Error: Failed to load class map", file=sys.stderr)
            return False
        
        # Determine number of classes
        num_classes = len(class_map)
        print(f"Number of classes: {num_classes}")
        
        # Create model architecture
        model = create_model(num_classes)
        
        # Load model weights
        print(f"Loading model weights from {input_path}...")
        model.load_state_dict(torch.load(input_path, map_location=torch.device('cpu')))
        model.eval()
        
        # Create dummy input
        dummy_input = torch.randn(1, 3, 224, 224)
        
        # Export to ONNX
        print(f"Converting to ONNX format...")
        torch.onnx.export(
            model,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'},
                          'output': {0: 'batch_size'}}
        )
        
        print(f"Model successfully converted to ONNX format and saved to {output_path}")
        return True
    
    except Exception as e:
        print(f"Error converting model to ONNX: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Convert PyTorch model to ONNX format')
    parser.add_argument('--input', type=str, default=DEFAULT_INPUT_PATH,
                        help=f'Path to PyTorch model file (default: {DEFAULT_INPUT_PATH})')
    parser.add_argument('--output', type=str, default=DEFAULT_OUTPUT_PATH,
                        help=f'Path to save ONNX model (default: {DEFAULT_OUTPUT_PATH})')
    parser.add_argument('--class-map', type=str, default=DEFAULT_CLASS_MAP_PATH,
                        help=f'Path to class map JSON file (default: {DEFAULT_CLASS_MAP_PATH})')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Convert model
    success = convert_to_onnx(args.input, args.output, args.class_map)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()