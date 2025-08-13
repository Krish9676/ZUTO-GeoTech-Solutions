#!/usr/bin/env python3
"""
Test script to verify model loading works correctly
"""

import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from inference import load_model, load_class_labels
    
    print("🔍 Testing model loading...")
    print(f"📁 Current working directory: {os.getcwd()}")
    print(f"📁 Current file location: {os.path.dirname(__file__)}")
    
    # Test class labels loading
    print("\n📚 Testing class labels loading...")
    labels = load_class_labels()
    print(f"✅ Loaded {len(labels)} class labels")
    print(f"📋 Labels: {labels[:5]}...")  # Show first 5 labels
    
    # Test model loading
    print("\n🤖 Testing model loading...")
    model = load_model()
    print("✅ Model loaded successfully!")
    
    # Test inference
    print("\n🧪 Testing inference...")
    import numpy as np
    
    # Create a dummy input tensor (1, 3, 224, 224) - typical MobileNet input
    dummy_input = np.random.randn(1, 3, 224, 224).astype(np.float32)
    
    # Get input name
    input_name = model.get_inputs()[0].name
    print(f"📥 Input name: {input_name}")
    print(f"📥 Input shape: {model.get_inputs()[0].shape}")
    
    # Run inference
    outputs = model.run(None, {input_name: dummy_input})
    print(f"📤 Output shape: {outputs[0].shape}")
    
    # Get prediction
    scores = outputs[0][0]
    predicted_class_idx = np.argmax(scores)
    confidence = float(scores[predicted_class_idx] * 100)
    label = labels[predicted_class_idx]
    
    print(f"🎯 Prediction: {label} (confidence: {confidence:.2f}%)")
    print("✅ Inference test passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
