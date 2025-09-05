# Crop-Aware Multicrop API Update Summary

## Overview
Successfully updated the API to work with the new crop-aware multicrop model that supports 21 crops with 15 disease classes each (315 total classes).

## Changes Made

### 1. Model Conversion
- **Updated conversion script** (`scripts/convert_multicrop_to_onnx.py`):
  - Created `ONNXMultiHeadCropDiseaseModel` class for ONNX export
  - Modified to export model with single image input and concatenated outputs
  - Handles 21 crops × 15 classes = 315 total output classes

### 2. Crop Mapping Updates
- **Updated `api/models/crop_map.json`**:
  - Replaced old crop list with new 21 crops:
    - `banana`, `brinjal`, `cabbage`, `cauliflower`, `chilli`, `cotton`, `grapes`, `maize`, `mango`, `mustard`, `onion`, `oranges`, `papaya`, `pomegranade`, `potato`, `rice`, `soyabean`, `sugarcane`, `tobacco`, `tomato`, `wheat`

### 3. Disease Class Mapping
- **Created new `api/models/disease_class_map.json`**:
  - 315 total classes (21 crops × 15 diseases each)
  - Each crop has: `healthy`, `bacterial_blight`, `anthracnose`, `leaf_spot`, `rust`, `verticillium_wilt`, `fusarium_wilt`, `leaf_curl`, `mosaic_virus`, `leaf_mold`, `early_blight`, `late_blight`, `root_rot`, `alternaria_blight`, `phomopsis_blight`

### 4. Inference Logic Updates
- **Updated `api/app/inference.py`**:
  - Modified `load_crop_to_global_classes()` to load from JSON file
  - Updated `load_preprocess_config()` to load from JSON file
  - Completely rewrote `run_inference()` function:
    - Handles single image input (no crop_id input needed)
    - Extracts crop-specific logits from concatenated output
    - Maps local class indices to global class indices correctly
    - Returns proper crop-specific disease predictions

### 5. Model Architecture
- **ONNX Model Structure**:
  - Input: `image` (1, 3, 160, 160)
  - Output: `logits` (1, 315) - concatenated outputs from all crop heads
  - Image size: 160×160 pixels
  - Normalization: ImageNet standard (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

### 6. Generated Files
- `api/models/mobilenet.onnx` - Updated ONNX model
- `api/models/crop_to_global_classes.json` - Crop to global class mapping
- `api/models/preprocess_config.json` - Preprocessing configuration
- `api/models/disease_class_map.json` - Disease class labels

## API Endpoints
All existing API endpoints remain unchanged:
- `GET /crops` - Returns list of 21 available crops
- `POST /upload` - Upload image with crop name for disease detection
- `GET /history` - Get detection history
- `GET /detections/{detection_id}` - Get specific detection

## Testing Results
✅ All 21 crops properly mapped and tested
✅ Inference working correctly for all crops
✅ Proper crop-specific disease predictions
✅ Confidence scores and class mappings working
✅ API endpoints functional

## Usage Example
```python
from api.app.inference import run_inference
import torch

# Create dummy image
image = torch.randn(3, 160, 160)

# Run inference for rice
result = run_inference(image, 'rice')
print(f"Prediction: {result['label']}")
print(f"Confidence: {result['confidence']:.4f}")
```

## Model Performance
- **Input**: 160×160 RGB images
- **Output**: Crop-specific disease predictions
- **Crops**: 21 different crop types
- **Diseases**: 15 disease classes per crop
- **Total Classes**: 315 (21 × 15)

The API is now fully updated and ready for production use with the new crop-aware multicrop model!
