#!/usr/bin/env python3
"""
Test script to verify ONNX conversion and inference
"""

import os
import sys
import torch
import numpy as np
import onnxruntime as ort

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_onnx_model():
    """Test the converted ONNX model"""
    try:
        # Path to the ONNX model
        onnx_path = "api/models/mobilenet.onnx"
        
        if not os.path.exists(onnx_path):
            print(f"❌ ONNX model not found at: {onnx_path}")
            return False
        
        print(f"✅ Found ONNX model at: {onnx_path}")
        
        # Load the ONNX model
        session = ort.InferenceSession(onnx_path)
        
        # Get input and output details
        inputs = session.get_inputs()
        outputs = session.get_outputs()
        
        print(f"Model inputs: {[input.name for input in inputs]}")
        print(f"Model outputs: {[output.name for output in outputs]}")
        
        # Create dummy inputs
        dummy_image = np.random.randn(1, 3, 160, 160).astype(np.float32)
        dummy_crop_id = np.array([0], dtype=np.int64)
        
        # Run inference
        if len(inputs) == 2 and 'image' in [input.name for input in inputs] and 'crop_id' in [input.name for input in inputs]:
            # New model with both inputs
            result = session.run(None, {
                'image': dummy_image,
                'crop_id': dummy_crop_id
            })
            print("✅ Successfully ran inference with new model (image + crop_id)")
        else:
            # Legacy model
            result = session.run(None, {inputs[0].name: dummy_image})
            print("✅ Successfully ran inference with legacy model")
        
        print(f"Output shape: {result[0].shape}")
        print(f"Output sample: {result[0][0][:5]}")  # First 5 values
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing ONNX model: {e}")
        return False

def test_pytorch_model():
    """Test the original PyTorch model"""
    try:
        # Path to the PyTorch model
        pth_path = "api/models/mobilenet.pth"
        
        if not os.path.exists(pth_path):
            print(f"❌ PyTorch model not found at: {pth_path}")
            return False
        
        print(f"✅ Found PyTorch model at: {pth_path}")
        
        # Load the model
        checkpoint = torch.load(pth_path, map_location=torch.device('cpu'))
        
        print(f"Checkpoint keys: {list(checkpoint.keys()) if isinstance(checkpoint, dict) else 'Direct state dict'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing PyTorch model: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing model conversion and inference...")
    print()
    
    # Test PyTorch model
    print("1. Testing PyTorch model...")
    pytorch_ok = test_pytorch_model()
    print()
    
    # Test ONNX model
    print("2. Testing ONNX model...")
    onnx_ok = test_onnx_model()
    print()
    
    # Summary
    if pytorch_ok and onnx_ok:
        print("🎉 All tests passed! Models are working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)
