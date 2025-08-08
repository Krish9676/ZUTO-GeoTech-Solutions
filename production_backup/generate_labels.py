#!/usr/bin/env python3

import os
import sys
import argparse
import json

# Sample class labels for different crops
SAMPLE_LABELS = {
    "maize": [
        "Healthy",
        "Fall Armyworm",
        "Corn Leaf Blight",
        "Common Rust",
        "Gray Leaf Spot",
        "Northern Leaf Blight"
    ],
    "rice": [
        "Healthy",
        "Brown Spot",
        "Leaf Blast",
        "Bacterial Leaf Blight",
        "Sheath Blight",
        "Stem Borer"
    ],
    "wheat": [
        "Healthy",
        "Leaf Rust",
        "Powdery Mildew",
        "Septoria Leaf Blotch",
        "Stripe Rust",
        "Fusarium Head Blight"
    ],
    "tomato": [
        "Healthy",
        "Early Blight",
        "Late Blight",
        "Leaf Mold",
        "Septoria Leaf Spot",
        "Spider Mites",
        "Target Spot",
        "Mosaic Virus",
        "Yellow Leaf Curl Virus"
    ],
    "potato": [
        "Healthy",
        "Early Blight",
        "Late Blight",
        "Black Scurf",
        "Common Scab",
        "Colorado Potato Beetle"
    ],
    "cotton": [
        "Healthy",
        "Bacterial Blight",
        "Fusarium Wilt",
        "Verticillium Wilt",
        "Cotton Bollworm",
        "Aphids"
    ],
    "general": [
        "Healthy",
        "Bacterial Infection",
        "Fungal Infection",
        "Viral Infection",
        "Pest Damage",
        "Nutrient Deficiency",
        "Environmental Stress"
    ]
}

def generate_labels(crop_type, output_file):
    """Generate class labels for the specified crop type"""
    if crop_type not in SAMPLE_LABELS:
        print(f"Error: Crop type '{crop_type}' not found", file=sys.stderr)
        print(f"Available crop types: {', '.join(SAMPLE_LABELS.keys())}")
        return False
    
    labels = SAMPLE_LABELS[crop_type]
    
    try:
        with open(output_file, 'w') as f:
            json.dump(labels, f, indent=2)
        return True
    except Exception as e:
        print(f"Error writing labels to file: {e}", file=sys.stderr)
        return False

def generate_all_labels(output_dir):
    """Generate class labels for all crop types"""
    os.makedirs(output_dir, exist_ok=True)
    
    success = True
    for crop_type in SAMPLE_LABELS:
        output_file = os.path.join(output_dir, f"{crop_type}_labels.json")
        if not generate_labels(crop_type, output_file):
            success = False
        else:
            print(f"Generated labels for {crop_type}: {output_file}")
    
    return success

def main():
    parser = argparse.ArgumentParser(description='Generate sample class labels for crop disease detection')
    parser.add_argument('--crop', type=str, default='maize',
                        help=f"Crop type (available: {', '.join(SAMPLE_LABELS.keys())})")
    parser.add_argument('--output', type=str, default='models/labels.json',
                        help='Output file path')
    parser.add_argument('--all', action='store_true',
                        help='Generate labels for all crop types')
    parser.add_argument('--output-dir', type=str, default='models',
                        help='Output directory for all labels (used with --all)')
    
    args = parser.parse_args()
    
    if args.all:
        print(f"Generating labels for all crop types in {args.output_dir}...")
        if generate_all_labels(args.output_dir):
            print("\n✅ All labels generated successfully!")
        else:
            print("\n❌ Error generating some labels")
            sys.exit(1)
    else:
        print(f"Generating labels for {args.crop} in {args.output}...")
        if generate_labels(args.crop, args.output):
            print(f"\n✅ Labels for {args.crop} generated successfully!")
            print(f"Output file: {args.output}")
        else:
            print("\n❌ Error generating labels")
            sys.exit(1)

if __name__ == '__main__':
    main()