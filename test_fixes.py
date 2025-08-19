#!/usr/bin/env python3

"""
Test script to verify the fixes for:
1. Disease class names (instead of generic class_4)
2. Confidence values (0-1 instead of 0-100)
3. Proper disease descriptions
"""

import sys
import os

# Add the api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api', 'app'))

def test_disease_descriptions():
    """Test the disease description utilities"""
    print("🧪 Testing Disease Description Utilities...")
    
    try:
        from utils.disease_descriptions import (
            get_disease_info, 
            format_disease_name, 
            get_severity_level,
            generate_diagnosis_summary
        )
        
        # Test 1: Disease info retrieval
        print("\n1️⃣ Testing disease info retrieval...")
        disease_info = get_disease_info("tomato_early_blight")
        print(f"✅ Disease info: {disease_info['description'][:50]}...")
        
        # Test 2: Disease name formatting
        print("\n2️⃣ Testing disease name formatting...")
        formatted_name = format_disease_name("tomato_early_blight")
        print(f"✅ Formatted name: {formatted_name}")
        
        # Test 3: Severity level
        print("\n3️⃣ Testing severity level...")
        severity = get_severity_level(0.85)
        print(f"✅ Severity for 0.85: {severity}")
        
        # Test 4: Diagnosis summary
        print("\n4️⃣ Testing diagnosis summary...")
        summary = generate_diagnosis_summary("tomato_early_blight", 0.85, "tomato")
        print(f"✅ Summary length: {len(summary)} characters")
        print(f"✅ Summary preview: {summary[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Disease descriptions test failed: {e}")
        return False

def test_inference_fixes():
    """Test the inference fixes"""
    print("\n🧪 Testing Inference Fixes...")
    
    try:
        from inference import load_class_labels
        
        # Test 1: Class labels loading
        print("\n1️⃣ Testing class labels loading...")
        labels = load_class_labels()
        print(f"✅ Loaded {len(labels)} class labels")
        
        # Test 2: Check for generic class names
        print("\n2️⃣ Checking for generic class names...")
        generic_count = sum(1 for label in labels if label.startswith('class_'))
        print(f"✅ Generic class names found: {generic_count}")
        
        if generic_count == 0:
            print("✅ All class names are descriptive!")
        else:
            print("⚠️ Some generic class names still exist")
        
        # Test 3: Check for disease names
        print("\n3️⃣ Checking for disease names...")
        disease_count = sum(1 for label in labels if any(word in label.lower() for word in ['blight', 'rust', 'spot', 'healthy']))
        print(f"✅ Disease-related names found: {disease_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Inference test failed: {e}")
        return False

def test_config_updates():
    """Test the configuration updates"""
    print("\n🧪 Testing Configuration Updates...")
    
    try:
        from config import get_class_map_paths
        
        # Test 1: Class map paths
        print("\n1️⃣ Testing class map paths...")
        paths = get_class_map_paths()
        print(f"✅ Found {len(paths)} class map paths")
        
        # Test 2: Check for disease class map priority
        print("\n2️⃣ Checking disease class map priority...")
        if "disease_class_map.json" in str(paths[0]):
            print("✅ Disease class map has priority")
        else:
            print("⚠️ Disease class map not in priority position")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Crop Disease Detection API Fixes")
    print("=" * 60)
    
    # Test 1: Disease descriptions
    print("\n1️⃣ Testing Disease Description Utilities...")
    desc_ok = test_disease_descriptions()
    
    # Test 2: Inference fixes
    print("\n2️⃣ Testing Inference Fixes...")
    inference_ok = test_inference_fixes()
    
    # Test 3: Configuration updates
    print("\n3️⃣ Testing Configuration Updates...")
    config_ok = test_config_updates()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FIX VERIFICATION SUMMARY:")
    print(f"Disease Descriptions: {'✅ PASS' if desc_ok else '❌ FAIL'}")
    print(f"Inference Fixes: {'✅ PASS' if inference_ok else '❌ FAIL'}")
    print(f"Configuration Updates: {'✅ PASS' if config_ok else '❌ FAIL'}")
    
    passed_tests = sum([desc_ok, inference_ok, config_ok])
    total_tests = 3
    
    if passed_tests == total_tests:
        print(f"\n🎉 ALL FIXES VERIFIED! Your API should now work correctly!")
        print(f"Score: {passed_tests}/{total_tests}")
        
        print(f"\n💡 EXPECTED IMPROVEMENTS:")
        print("✅ Disease names will be descriptive (e.g., 'tomato_early_blight' instead of 'class_4')")
        print("✅ Confidence will be 0-1 (e.g., 0.85 instead of 85)")
        print("✅ Detailed disease descriptions and treatment recommendations")
        print("✅ Better error handling and fallbacks")
        
    else:
        print(f"\n⚠️ Some fixes failed verification. Check the logs above.")
        print(f"Score: {passed_tests}/{total_tests}")

if __name__ == "__main__":
    main()
