#!/usr/bin/env python3

import os
from PIL import Image, ImageDraw
import numpy as np

def create_test_image():
    """Create a simple test image for model testing"""
    # Create a 224x224 RGB image
    image = Image.new('RGB', (224, 224), color='green')
    draw = ImageDraw.Draw(image)
    
    # Draw some simple shapes to simulate a crop leaf
    draw.ellipse([50, 50, 174, 174], fill='lightgreen', outline='darkgreen')
    draw.rectangle([80, 80, 144, 144], fill='yellow', outline='orange')
    
    # Create temp directory if it doesn't exist
    os.makedirs('temp', exist_ok=True)
    
    # Save the test image
    test_image_path = 'temp/test_crop_image.jpg'
    image.save(test_image_path)
    
    print(f"Test image created: {test_image_path}")
    return test_image_path

if __name__ == '__main__':
    create_test_image()