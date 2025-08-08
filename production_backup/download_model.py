#!/usr/bin/env python3

import os
import sys
import argparse
import requests
from tqdm import tqdm

# Default model URLs
MODEL_URLS = {
    "mobilenet": "https://github.com/onnx/models/raw/main/vision/classification/mobilenet/model/mobilenetv2-7.onnx",
    "resnet": "https://github.com/onnx/models/raw/main/vision/classification/resnet/model/resnet18-v1-7.onnx"
}

def download_file(url, destination):
    """Download a file from a URL to a destination with progress bar"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Get file size
    total_size = int(response.headers.get('content-length', 0))
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    # Download with progress bar
    with open(destination, 'wb') as f, tqdm(
        desc=os.path.basename(destination),
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            size = f.write(chunk)
            bar.update(size)

def main():
    parser = argparse.ArgumentParser(description='Download pre-trained ONNX models for crop disease detection')
    parser.add_argument('--model', choices=['mobilenet', 'resnet'], default='mobilenet',
                        help='Model to download (default: mobilenet)')
    parser.add_argument('--output', default=None,
                        help='Output file path (default: models/{model}.onnx)')
    parser.add_argument('--url', default=None,
                        help='Custom URL to download from (overrides --model)')
    
    args = parser.parse_args()
    
    # Determine URL and destination
    if args.url:
        url = args.url
        model_name = os.path.basename(url).split('.')[0]
    else:
        model_name = args.model
        url = MODEL_URLS[model_name]
    
    destination = args.output or os.path.join('models', f'{model_name}.onnx')
    
    print(f"Downloading {model_name} model from {url}")
    print(f"Saving to {destination}")
    
    try:
        download_file(url, destination)
        print(f"\nDownload complete! Model saved to {destination}")
    except Exception as e:
        print(f"Error downloading model: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()