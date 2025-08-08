#!/usr/bin/env python3

import os
import sys

def verify_model_files():
    """Verify that model files are present and accessible"""
    print("🔍 Verifying model files...")
    
    # Check if models directory exists
    if not os.path.exists("models"):
        print("❌ models/ directory not found")
        return False
    
    print("✅ models/ directory found")
    
    # List all files in models directory
    model_files = os.listdir("models")
    print(f"📁 Files in models/: {model_files}")
    
    # Check for required files
    required_files = ["mobilenet.onnx", "class_map.json"]
    
    for file in required_files:
        file_path = os.path.join("models", file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file} found ({size} bytes)")
        else:
            print(f"❌ {file} not found")
            return False
    
    # Try to load the model
    try:
        import onnxruntime as ort
        model_path = os.path.join("models", "mobilenet.onnx")
        session = ort.InferenceSession(model_path)
        print("✅ Model loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False

if __name__ == "__main__":
    success = verify_model_files()
    if success:
        print("🎉 All model files verified successfully!")
        sys.exit(0)
    else:
        print("❌ Model verification failed!")
        sys.exit(1)
