#!/usr/bin/env python3
"""
Test script to verify mobile app API integration
Tests the deployed API endpoints that the mobile app will use
"""

import requests
import json
from datetime import datetime

# API Configuration
BASE_URL = "https://crop-disease-detection-api-0spd.onrender.com"
API_ENDPOINTS = {
    "health": f"{BASE_URL}/",
    "upload": f"{BASE_URL}/api/upload",
    "history": f"{BASE_URL}/api/history",
    "detections": f"{BASE_URL}/api/detections"
}

def test_api_health():
    """Test if the API is accessible"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get(API_ENDPOINTS["health"], timeout=30)
        if response.status_code == 200:
            print("✅ API is healthy and accessible")
            print(f"   Response: {response.text[:100]}...")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check error: {e}")
        return False

def test_api_endpoints():
    """Test if all required API endpoints are accessible"""
    print("\n🔍 Testing API Endpoints...")
    
    for endpoint_name, url in API_ENDPOINTS.items():
        try:
            if endpoint_name == "upload":
                # Skip upload test for now as it requires a file
                print(f"⏭️  Skipping {endpoint_name} (requires file upload)")
                continue
                
            response = requests.get(url, timeout=30)
            print(f"✅ {endpoint_name}: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Data preview: {str(data)[:100]}...")
                except:
                    print(f"   Response: {response.text[:100]}...")
            elif response.status_code == 405:  # Method not allowed for GET on upload
                print(f"   Expected: Method not allowed for GET on upload endpoint")
            else:
                print(f"   Unexpected status: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint_name}: Error - {e}")

def test_mobile_app_integration():
    """Test the specific endpoints that the mobile app will use"""
    print("\n🔍 Testing Mobile App Integration Points...")
    
    # Test history endpoint (GET)
    try:
        response = requests.get(API_ENDPOINTS["history"], timeout=30)
        print(f"✅ History endpoint: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   History data: {len(data)} items")
                if data:
                    print(f"   Sample item: {json.dumps(data[0], indent=2)[:200]}...")
            except:
                print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ History endpoint error: {e}")
    
    # Test detections endpoint structure
    try:
        response = requests.get(f"{API_ENDPOINTS['detections']}/test", timeout=30)
        print(f"✅ Detections endpoint structure: {response.status_code}")
        if response.status_code == 404:  # Expected for non-existent ID
            print("   Expected: 404 for non-existent detection ID")
    except Exception as e:
        print(f"❌ Detections endpoint error: {e}")

def generate_mobile_app_config():
    """Generate the configuration needed for the mobile app"""
    print("\n📱 Mobile App Configuration...")
    
    config = {
        "api_base_url": BASE_URL,
        "endpoints": {
            "upload": "/api/upload",
            "history": "/api/history",
            "detections": "/api/detections"
        },
        "timeout_seconds": 30,
        "max_image_size": "5MB",
        "supported_image_formats": ["jpg", "jpeg", "png"],
        "test_timestamp": datetime.now().isoformat()
    }
    
    print("✅ Generated configuration:")
    print(json.dumps(config, indent=2))
    
    # Save to file
    with open("mobile_app_config.json", "w") as f:
        json.dump(config, f, indent=2)
    print("💾 Configuration saved to mobile_app_config.json")

def main():
    """Main test function"""
    print("🚀 Testing Mobile App API Integration")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not accessible. Please check your deployment.")
        return
    
    # Test endpoints
    test_api_endpoints()
    
    # Test mobile app specific integration
    test_mobile_app_integration()
    
    # Generate configuration
    generate_mobile_app_config()
    
    print("\n" + "=" * 50)
    print("✅ Mobile App API Integration Test Complete!")
    print("\n📋 Next Steps:")
    print("1. Update mobile app with the generated configuration")
    print("2. Test image upload functionality")
    print("3. Build and deploy the mobile app")
    print("4. Test on real devices")

if __name__ == "__main__":
    main()
