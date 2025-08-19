# Model Conversion and API Update Guide

This guide explains how to convert your trained PyTorch model to ONNX format and update the API to match your training process.

## Overview

Your training process uses a custom `CropAwareDiseaseModel` that:
- Takes both image and crop information as input
- Uses MobileNetV3-Small as the backbone
- Combines image features with crop embeddings
- Outputs disease predictions for crop-pest combinations

## Step 1: Convert PyTorch Model to ONNX

### Prerequisites
- Your trained model at `api/models/mobilenet.pth`
- PyTorch and ONNX installed
- The updated conversion script

### Run Conversion
```bash
cd scripts
python convert_to_onnx.py --input ../api/models/mobilenet.pth --output ../api/models/mobilenet.onnx
```

### What the Script Does
1. Loads your trained model checkpoint
2. Recreates the `CropAwareDiseaseModel` architecture
3. Exports to ONNX with two inputs: `image` and `crop_id`
4. Handles both checkpoint formats (with/without `model_state_dict`)

## Step 2: Verify the Conversion

Run the test script to verify everything works:
```bash
python test_onnx_conversion.py
```

This will:
- Check if both PyTorch and ONNX models exist
- Verify the ONNX model can run inference
- Confirm input/output shapes are correct

## Step 3: API Updates Made

### 1. Inference Module (`api/app/inference.py`)
- Updated to handle both `image` and `crop_id` inputs
- Added crop label loading from `crop_map.json`
- Maintains backward compatibility with legacy models
- Passes crop information through the entire inference pipeline

### 2. Image Utils (`api/app/utils/image_utils.py`)
- Changed preprocessing from 224x224 to 160x160 (matching training)
- Removed center crop to maintain aspect ratio

### 3. API Endpoint (`api/app/api.py`)
- Updated to pass `crop_name` parameter to inference
- Maintains the same API interface for mobile apps

### 4. Configuration Files
- `class_map.json`: Updated with actual training classes (crop_pest format)
- `crop_map.json`: Created with crop labels used in training

## Step 4: Model Architecture Details

### Input Format
- **Image**: 3x160x160 tensor (RGB, 160x160 resolution)
- **Crop ID**: Integer representing the crop type (0-21)

### Model Structure
```
MobileNetV3-Small Features → 576 channels
Crop Embedding (22 crops × 64) → 64 channels
Concatenated → 640 channels → Linear → 67 classes
```

### Output
- 67 classes representing crop-disease combinations
- Confidence scores for each class

## Step 5: Testing the Updated API

### Test with Crop Information
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@test_image.jpg" \
  -F "crop_name=rice"
```

### Expected Response
```json
{
  "id": "uuid",
  "prediction": "rice_bacterial_leaf_blight",
  "confidence": 95.2,
  "image_url": "...",
  "heatmap_url": "...",
  "diagnosis": "...",
  "crop_used": "rice"
}
```

## Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Check if ONNX file exists at `api/models/mobilenet.onnx`
   - Verify the model architecture matches your training

2. **Input Shape Mismatch**
   - Ensure images are preprocessed to 160x160
   - Check that crop_id is provided as integer

3. **Class Map Issues**
   - Verify `class_map.json` has the correct number of classes
   - Ensure class indices match your training data

### Debug Information
The API provides detailed logging:
- Model loading status
- Input preprocessing steps
- Inference results with crop information
- Error details if something fails

## Next Steps

1. **Test the conversion** with your actual model
2. **Verify inference accuracy** matches PyTorch results
3. **Update mobile app** if needed to handle crop selection
4. **Deploy the updated API** with the new ONNX model

## Files Modified

- `scripts/convert_to_onnx.py` - ONNX conversion script
- `api/app/inference.py` - Inference logic with crop support
- `api/app/utils/image_utils.py` - Image preprocessing (160x160)
- `api/app/api.py` - API endpoint updates
- `api/models/class_map.json` - Updated class labels
- `api/models/crop_map.json` - New crop labels file
- `test_onnx_conversion.py` - Testing script

## Notes

- The API maintains backward compatibility
- Crop information is optional (defaults to crop 0)
- Image resolution changed from 224x224 to 160x160
- Model expects both image and crop inputs for optimal performance
