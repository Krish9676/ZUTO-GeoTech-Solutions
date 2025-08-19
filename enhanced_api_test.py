#!/usr/bin/env python3

import requests
import json
import os
import time
from PIL import Image
import numpy as np

# API Configuration
API_BASE_URL = "https://crop-disease-detection-api-0spd.onrender.com/"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=10)
        print(f"✅ Health Check: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            # Validate response structure
            if 'status' in data and 'message' in data:
                print(f"✅ Response structure is correct")
                return True
            else:
                print(f"⚠️ Response structure is unexpected")
                return False
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Health Check Timeout: API took too long to respond")
        return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Health Check Connection Error: Cannot connect to API")
        return False
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")
        return False

def test_api_docs():
    """Test if API documentation is accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=10)
        print(f"✅ API Docs: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ Swagger UI is accessible")
            return True
        else:
            print(f"❌ API Docs returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API Docs Failed: {e}")
        return False

def create_test_image():
    """Create a simple test image"""
    try:
        # Create a 224x224 test image (common ML model input size)
        img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)

        # Save test image
        test_image_path = "test_crop_image.jpg"
        img.save(test_image_path, "JPEG", quality=85)
        print(f"✅ Test image created: {test_image_path}")
        return test_image_path
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return None

def test_image_upload(crop_name="tomato", delay=2):
    """Test image upload with crop name"""
    try:
        # Create test image
        test_image_path = create_test_image()
        if not test_image_path:
            return False

        # Prepare the upload
        url = f"{API_BASE_URL}/api/upload"

        with open(test_image_path, "rb") as f:
            files = {"file": ("test_image.jpg", f, "image/jpeg")}
            data = {"crop_name": crop_name}

            print(f"🔄 Uploading image with crop_name: {crop_name}")
            response = requests.post(url, files=files, data=data, timeout=30)

        # Clean up test image
        os.remove(test_image_path)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload Successful!")
            
            # Validate response structure
            required_fields = ['id', 'prediction', 'confidence', 'image_url', 'diagnosis']
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                print(f"⚠️ Missing fields in response: {missing_fields}")
            else:
                print(f"✅ Response structure is complete")
            
            # Display results with proper formatting
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            
            # Display confidence (now properly formatted as 0-1)
            confidence = result.get('confidence', 0)
            if isinstance(confidence, (int, float)):
                confidence_pct = confidence * 100
                print(f"Confidence: {confidence_pct:.1f}% (raw: {confidence:.4f})")
            else:
                print(f"Confidence: {confidence} (raw value)")
            
            print(f"Image URL: {result.get('image_url', 'N/A')}")
            print(f"Heatmap URL: {result.get('heatmap_url', 'N/A')}")
            
            # Truncate long diagnosis text
            diagnosis = result.get('diagnosis', 'N/A')
            if len(diagnosis) > 100:
                print(f"Diagnosis: {diagnosis[:100]}...")
            else:
                print(f"Diagnosis: {diagnosis}")
                
            return True
            
        elif response.status_code == 400:
            print(f"❌ Bad Request (400): {response.text}")
            return False
        elif response.status_code == 500:
            print(f"❌ Internal Server Error (500): {response.text}")
            return False
        else:
            print(f"❌ Upload Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print(f"❌ Upload Timeout: Request took too long")
        return False
    except Exception as e:
        print(f"❌ Upload Test Failed: {e}")
        return False
    finally:
        # Add delay to avoid overwhelming the API
        if delay > 0:
            print(f"⏳ Waiting {delay} seconds before next request...")
            time.sleep(delay)

def test_history_endpoint():
    """Test the history endpoint"""
    try:
        print(f"🔄 Testing History Endpoint...")
        response = requests.get(f"{API_BASE_URL}/api/history", timeout=10)
        
        if response.status_code == 200:
            history = response.json()
            print(f"✅ History Retrieved Successfully!")
            print(f"Number of records: {len(history)}")
            
            if history:
                # Show first record as sample
                first_record = history[0]
                print(f"Sample record ID: {first_record.get('id', 'N/A')}")
                print(f"Sample prediction: {first_record.get('prediction', 'N/A')}")
            else:
                print(f"ℹ️ No history records found (this is normal for new API)")
            return True
        else:
            print(f"❌ History Failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ History Test Failed: {e}")
        return False

def test_multiple_crops():
    """Test with different crop names"""
    test_crops = ["tomato", "potato", "rice", "wheat", "maize"]
    
    print(f"\n🌾 Testing Multiple Crops:")
    successful_tests = 0
    
    for i, crop in enumerate(test_crops):
        print(f"\n--- Testing {crop.upper()} ({i+1}/{len(test_crops)}) ---")
        success = test_image_upload(crop, delay=3)  # Increased delay between requests
        
        if success:
            print(f"✅ {crop} test passed")
            successful_tests += 1
        else:
            print(f"❌ {crop} test failed")
    
    print(f"\n📊 Multiple Crop Test Results: {successful_tests}/{len(test_crops)} passed")
    return successful_tests == len(test_crops)

def test_error_handling():
    """Test error handling with invalid requests"""
    print(f"\n🧪 Testing Error Handling...")
    
    # Test 1: Invalid file type
    try:
        url = f"{API_BASE_URL}/api/upload"
        files = {"file": ("test.txt", b"this is not an image", "text/plain")}
        data = {"crop_name": "tomato"}
        
        response = requests.post(url, files=files, data=data, timeout=10)
        if response.status_code == 400:
            print(f"✅ Invalid file type correctly rejected (400)")
        else:
            print(f"⚠️ Unexpected response for invalid file: {response.status_code}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Test 2: Missing file
    try:
        url = f"{API_BASE_URL}/api/upload"
        data = {"crop_name": "tomato"}
        
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 422:  # FastAPI validation error
            print(f"✅ Missing file correctly rejected (422)")
        else:
            print(f"⚠️ Unexpected response for missing file: {response.status_code}")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing Crop Disease Detection API")
    print("=" * 60)

    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    health_ok = test_health_check()

    # Test 2: API Documentation
    print("\n2️⃣ Testing API Documentation...")
    docs_ok = test_api_docs()

    # Test 3: History Endpoint
    print("\n3️⃣ Testing History Endpoint...")
    history_ok = test_history_endpoint()

    # Test 4: Single Image Upload
    print("\n4️⃣ Testing Image Upload with Crop Name...")
    upload_ok = test_image_upload("tomato")

    # Test 5: Multiple Crops
    print("\n5️⃣ Testing Multiple Crop Types...")
    multiple_crops_ok = test_multiple_crops()

    # Test 6: Error Handling
    print("\n6️⃣ Testing Error Handling...")
    test_error_handling()

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"API Docs: {'✅ PASS' if docs_ok else '❌ FAIL'}")
    print(f"History Endpoint: {'✅ PASS' if history_ok else '❌ FAIL'}")
    print(f"Image Upload: {'✅ PASS' if upload_ok else '❌ FAIL'}")
    print(f"Multiple Crops: {'✅ PASS' if multiple_crops_ok else '❌ FAIL'}")

    passed_tests = sum([health_ok, docs_ok, history_ok, upload_ok, multiple_crops_ok])
    total_tests = 5

    if passed_tests == total_tests:
        print(f"\n🎉 ALL TESTS PASSED! Your API is working perfectly!")
        print(f"Score: {passed_tests}/{total_tests}")
    else:
        print(f"\n⚠️ Some tests failed. Check the logs above.")
        print(f"Score: {passed_tests}/{total_tests}")

    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if health_ok and docs_ok and upload_ok:
        print("✅ Your API is ready for production use!")
        print("✅ Consider adding rate limiting for production")
        print("✅ Monitor API performance and response times")
    else:
        print("⚠️ Fix the failing tests before deploying to production")
        print("⚠️ Check your API logs for detailed error information")

if __name__ == "__main__":
    main()
