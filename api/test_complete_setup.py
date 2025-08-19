#!/usr/bin/env python3
"""
Complete API Setup Test Script
This script tests all components of the API to ensure everything works correctly
"""

import os
import sys
import json
import numpy as np
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_1_model_files():
    """Test 1: Check if all required model files exist"""
    print("🧪 Test 1: Checking model files...")
    
    models_dir = Path("models")
    required_files = [
        "mobilenet.onnx",
        "class_map.json", 
        "crop_map.json"
    ]
    
    all_exist = True
    for file in required_files:
        file_path = models_dir / file
        if file_path.exists():
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
            all_exist = False
    
    return all_exist

def test_2_model_configuration():
    """Test 2: Check model configuration files"""
    print("\n🧪 Test 2: Checking model configuration...")
    
    try:
        # Load class map
        with open("models/class_map.json", "r") as f:
            class_map = json.load(f)
        num_classes = len(class_map)
        print(f"✅ Class map loaded: {num_classes} classes")
        
        # Load crop map
        with open("models/crop_map.json", "r") as f:
            crop_map = json.load(f)
        num_crops = len(crop_map)
        print(f"✅ Crop map loaded: {num_crops} crops")
        
        return True
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        return False

def test_3_onnx_model():
    """Test 3: Check ONNX model can be loaded"""
    print("\n🧪 Test 3: Testing ONNX model...")
    
    try:
        import onnxruntime as ort
        
        # Load the model
        model_path = "models/mobilenet.onnx"
        session = ort.InferenceSession(model_path)
        
        # Check inputs and outputs
        inputs = session.get_inputs()
        outputs = session.get_outputs()
        
        print(f"✅ ONNX model loaded successfully")
        print(f"   Inputs: {[input.name for input in inputs]}")
        print(f"   Outputs: {[output.name for output in outputs]}")
        
        # Test with dummy data
        if len(inputs) == 2 and 'image' in [input.name for input in inputs] and 'crop_id' in [input.name for input in inputs]:
            dummy_image = np.random.randn(1, 3, 160, 160).astype(np.float32)
            dummy_crop_id = np.array([0], dtype=np.int64)
            
            result = session.run(None, {
                'image': dummy_image,
                'crop_id': dummy_crop_id
            })
            
            print(f"✅ Model inference test passed")
            print(f"   Output shape: {result[0].shape}")
            return True
        else:
            print(f"⚠️ Model has unexpected input structure")
            return False
            
    except Exception as e:
        print(f"❌ Error testing ONNX model: {e}")
        return False

def test_4_api_imports():
    """Test 4: Check if API modules can be imported"""
    print("\n🧪 Test 4: Testing API imports...")
    
    try:
        # Test core imports
        from app.inference import run_inference
        from app.utils.image_utils import preprocess_image
        print("✅ Core API modules imported successfully")
        
        # Test API router
        from app.api import router
        print("✅ API router imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error importing API modules: {e}")
        return False

def test_5_fastapi_app():
    """Test 5: Check if FastAPI app can be created"""
    print("\n🧪 Test 5: Testing FastAPI app creation...")
    
    try:
        from app.main import app
        
        # Check if app has the expected structure
        if hasattr(app, 'routes') and hasattr(app, 'middleware'):
            print("✅ FastAPI app created successfully")
            print(f"   Routes: {len(app.routes)}")
            return True
        else:
            print("❌ FastAPI app missing expected attributes")
            return False
            
    except Exception as e:
        print(f"❌ Error creating FastAPI app: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Crop Disease Detection API - Complete Setup Test")
    print("=" * 60)
    
    tests = [
        test_1_model_files,
        test_2_model_configuration,
        test_3_onnx_model,
        test_4_api_imports,
        test_5_fastapi_app
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    for i, (test, result) in enumerate(zip(tests, results), 1):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"Test {i}: {test.__name__} - {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is ready to run.")
        print("\nTo start the API server, run:")
        print("   cd api")
        print("   python start_api.py")
    else:
        print("⚠️ Some tests failed. Please fix the issues before running the API.")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
