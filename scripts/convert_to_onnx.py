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
DEFAULT_INPUT_PATH = os.getenv("MODEL_PATH", "../api/models/mobilenet.pth")
DEFAULT_OUTPUT_PATH = os.getenv("MODEL_PATH", "../api/models/mobilenet.onnx")
DEFAULT_CLASS_MAP_PATH = "../api/models/class_map.json"


def load_class_map(class_map_path):
    """Load class map from JSON file"""
    try:
        with open(class_map_path, 'r') as f:
            class_map = json.load(f)
        return class_map
    except Exception as e:
        print(f"Error loading class map: {e}", file=sys.stderr)
        return None


class CropAwareDiseaseModel(nn.Module):
    """Custom model architecture matching the training process"""
    def __init__(self, num_classes, num_crops):
        super().__init__()
        self.cnn = models.mobilenet_v3_small(weights=None).features
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.crop_embed = nn.Embedding(num_crops, 64)
        self.fc = nn.Linear(576 + 64, num_classes)  # 576 channels in mobilenet_v3_small

    def forward(self, images, crop_ids):
        x_img = self.cnn(images)
        x_img = self.avgpool(x_img)
        x_img = torch.flatten(x_img, 1)
        x_crop = self.crop_embed(crop_ids)
        x = torch.cat((x_img, x_crop), dim=1)
        return self.fc(x)


def convert_to_onnx(input_path, output_path, class_map_path):
    """Convert PyTorch model to ONNX format"""
    try:
        # Load class map
        class_map = load_class_map(class_map_path)
        if not class_map:
            print("Error: Failed to load class map", file=sys.stderr)
            return False
        
        # Determine number of classes and crops from the checkpoint
        # We'll load the checkpoint first to get the actual dimensions
        try:
            from torch.serialization import safe_globals
            import sklearn.preprocessing._label
            import numpy._core.multiarray
            import numpy.dtypes
            with safe_globals([
                sklearn.preprocessing._label.LabelEncoder,
                numpy._core.multiarray._reconstruct,
                numpy._core.multiarray.ndarray,
                numpy.dtype,
                numpy.dtypes.StrDType,
                numpy.dtypes.Int64DType,
                numpy.dtypes.Float64DType,
                numpy.dtypes.BoolDType
            ]):
                checkpoint = torch.load(input_path, map_location=torch.device('cpu'))
        except ImportError:
            # Fallback for older PyTorch versions
            checkpoint = torch.load(input_path, map_location=torch.device('cpu'), weights_only=False)
        
        # Extract actual dimensions from checkpoint
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
        elif 'state_dict' in checkpoint:
            state_dict = checkpoint['state_dict']
        else:
            state_dict = checkpoint
        
        # Get actual dimensions from the checkpoint
        num_crops = state_dict['crop_embed.weight'].shape[0]
        num_classes = state_dict['fc.weight'].shape[0]
        
        print(f"Actual model dimensions from checkpoint:")
        print(f"  - Number of crops: {num_crops}")
        print(f"  - Number of classes: {num_classes}")
        
        # Create model architecture matching the actual checkpoint
        model = CropAwareDiseaseModel(num_classes=num_classes, num_crops=num_crops)
        
        # Load model weights
        print(f"Loading model weights from checkpoint...")
        model.load_state_dict(state_dict)
        print("✅ Model weights loaded successfully")
        
        model.eval()
        
        # Create dummy inputs for both image and crop_id
        dummy_image = torch.randn(1, 3, 160, 160)  # 160x160 as per your training
        dummy_crop_id = torch.tensor([0], dtype=torch.long)
        
        # Export to ONNX with two inputs
        print(f"Converting to ONNX format...")
        torch.onnx.export(
            model,
            (dummy_image, dummy_crop_id),
            output_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['image', 'crop_id'],
            output_names=['output'],
            dynamic_axes={
                'image': {0: 'batch_size'},
                'crop_id': {0: 'batch_size'},
                'output': {0: 'batch_size'}
            }
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