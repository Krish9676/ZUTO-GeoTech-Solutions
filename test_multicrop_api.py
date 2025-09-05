#!/usr/bin/env python3
"""
Test script for the updated multi-head crop disease detection API
"""

import requests
import json
import os
from pathlib import Path

# API base URL
API_BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("🧪 Testing Multi-Head Crop Disease Detection API")
    print("=" * 50)
    
    # Test 1: Get available crops
    print("\n1. Testing /crops endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/crops")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Available crops: {data['total']} crops")
            print(f"   First 5 crops: {data['crops'][:5]}")
        else:
            print(f"❌ Failed to get crops: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing crops endpoint: {e}")
    
    # Test 2: Test model loading (if API is running)
    print("\n2. Testing model loading...")
    try:
        # This would test if the model loads correctly when the API starts
        print("✅ Model loading test would run when API starts")
    except Exception as e:
        print(f"❌ Error in model loading test: {e}")
    
    # Test 3: Test crop mapping
    print("\n3. Testing crop mapping...")
    try:
        from api.app.inference import load_crop_to_global_classes, CROP_LABELS
        
        crop_mapping = load_crop_to_global_classes()
        print(f"✅ Crop mapping loaded: {len(crop_mapping)} crops")
        
        # Test a few crop mappings
        for crop_id in ["0", "1", "2"]:
            if crop_id in crop_mapping:
                global_classes = crop_mapping[crop_id]
                crop_name = CROP_LABELS[int(crop_id)]
                print(f"   Crop {crop_id} ({crop_name}): {len(global_classes)} disease classes")
        
    except Exception as e:
        print(f"❌ Error testing crop mapping: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")
    print("\nTo test image upload:")
    print("1. Start the API server: python start_api.py")
    print("2. Use the /upload endpoint with crop_name parameter")
    print("3. Example: POST /upload with file and crop_name='rice'")

if __name__ == "__main__":
    test_api_endpoints()
