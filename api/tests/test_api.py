#!/usr/bin/env python3

import requests
import json
import os
from PIL import Image
import numpy as np

# API Configuration
API_BASE_URL = "https://crop-disease-detection-api-0spd.onrender.com"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_api_docs():
    """Test if API documentation is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs")
        print(f"✅ API Docs: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API Docs Failed: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    # Create a 224x224 test image
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # Save test image
    test_image_path = "test_crop_image.jpg"
    img.save(test_image_path, "JPEG")
    return test_image_path

def test_image_upload(crop_name="tomato"):
    """Test image upload with crop name"""
    try:
        # Create test image
        test_image_path = create_test_image()
        
        # Prepare the upload
        url = f"{API_BASE_URL}/api/upload"
        
        with open(test_image_path, "rb") as f:
            files = {"file": ("test_image.jpg", f, "image/jpeg")}
            data = {"crop_name": crop_name}
            
            print(f"🔄 Uploading image with crop_name: {crop_name}")
            response = requests.post(url, files=files, data=data)
        
        # Clean up test image
        os.remove(test_image_path)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload Successful!")
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 'N/A')}%")
            print(f"Image URL: {result.get('image_url', 'N/A')}")
            print(f"Heatmap URL: {result.get('heatmap_url', 'N/A')}")
            print(f"Diagnosis: {result.get('diagnosis', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Upload Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload Test Failed: {e}")
        return False

def test_multiple_crops():
    """Test with different crop names"""
    test_crops = ["tomato", "potato", "rice", "wheat", "maize"]
    
    print("\n🌾 Testing Multiple Crops:")
    for crop in test_crops:
        print(f"\n--- Testing {crop.upper()} ---")
        success = test_image_upload(crop)
        if success:
            print(f"✅ {crop} test passed")
        else:
            print(f"❌ {crop} test failed")

def main():
    """Run all tests"""
    print("🚀 Testing Crop Disease Detection API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    health_ok = test_health_check()
    
    # Test 2: API Documentation
    print("\n2️⃣ Testing API Documentation...")
    docs_ok = test_api_docs()
    
    # Test 3: Single Image Upload
    print("\n3️⃣ Testing Image Upload with Crop Name...")
    upload_ok = test_image_upload("tomato")
    
    # Test 4: Multiple Crops
    print("\n4️⃣ Testing Multiple Crop Types...")
    test_multiple_crops()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"API Docs: {'✅ PASS' if docs_ok else '❌ FAIL'}")
    print(f"Image Upload: {'✅ PASS' if upload_ok else '❌ FAIL'}")
    
    if health_ok and docs_ok and upload_ok:
        print("\n🎉 ALL TESTS PASSED! Your API is working perfectly!")
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()
