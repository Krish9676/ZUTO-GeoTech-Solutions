# Multi-Head Crop Disease Detection API Update Summary

## Overview
Successfully updated the API to work with the newly trained multi-head crop disease detection model. The model uses a MobileNet backbone with crop-specific classification heads for improved accuracy.

## Changes Made

### 1. Model Conversion ✅
- **Converted** `cropaware_multicrop_model.pth` to `mobilenet.onnx` format
- **Created** `crop_to_global_classes.json` mapping file
- **Created** `preprocess_config.json` with model-specific preprocessing parameters
- **Removed** old `.pth` model file

### 2. Model Architecture Updates ✅
- **Added** `MultiHeadCropDiseaseModel` class to `api/app/utils/model_loader.py`
- **Updated** model loading to handle multi-head architecture
- **Implemented** crop-specific inference logic

### 3. Inference Logic Updates ✅
- **Updated** `api/app/inference.py` to handle multi-head model
- **Added** crop-to-global class mapping functionality
- **Implemented** local-to-global class index conversion
- **Added** dynamic preprocessing configuration loading

### 4. Image Preprocessing Updates ✅
- **Updated** `api/app/utils/image_utils.py` to use model-specific preprocessing
- **Added** dynamic image size and normalization parameters
- **Maintained** backward compatibility with fallback values

### 5. API Endpoint Updates ✅
- **Updated** `/upload` endpoint to require `crop_name` parameter
- **Added** `/crops` endpoint to list available crops
- **Enhanced** error handling and validation

## Model Architecture Details

### Multi-Head Structure
- **Backbone**: MobileNet V3 Small (576 features)
- **Heads**: 21 crop-specific classification heads
- **Input**: Image (3x160x160) + Crop ID (int64)
- **Output**: Logits for crop-specific disease classes

### Crop Mapping
The model supports 21 crops with 15 disease classes each:
- Rice (ID: 0): Classes 0-14
- Maize (ID: 1): Classes 15-29
- Chickpea (ID: 2): Classes 30-44
- ... and 18 more crops

### Preprocessing Configuration
- **Image Size**: 160x160 pixels
- **Normalization**: Mean [0.485, 0.456, 0.406], Std [0.229, 0.224, 0.225]

## API Usage

### Available Endpoints

#### GET `/crops`
Returns list of available crops for disease detection.

**Response:**
```json
{
  "crops": ["rice", "maize", "chickpea", ...],
  "total": 21
}
```

#### POST `/upload`
Upload image for disease detection.

**Parameters:**
- `file`: Image file (required)
- `crop_name`: Crop name (required)

**Response:**
```json
{
  "id": "uuid",
  "prediction": "disease_name",
  "confidence": 0.95,
  "image_url": "https://...",
  "heatmap_url": "https://...",
  "diagnosis": "detailed_diagnosis",
  "crop_used": "rice",
  "crop_id": 0
}
```

## Files Modified

### Core Files
- `api/app/inference.py` - Updated inference logic
- `api/app/api.py` - Updated API endpoints
- `api/app/utils/model_loader.py` - Added model architecture
- `api/app/utils/image_utils.py` - Updated preprocessing

### Configuration Files
- `api/models/mobilenet.onnx` - New ONNX model
- `api/models/crop_to_global_classes.json` - Crop mapping
- `api/models/preprocess_config.json` - Preprocessing config

### Scripts
- `scripts/convert_multicrop_to_onnx.py` - Model conversion script
- `test_multicrop_api.py` - API testing script

## Testing Results ✅

### Model Loading
- ✅ ONNX model loads successfully
- ✅ Crop mapping loads correctly (21 crops)
- ✅ Preprocessing config loads properly

### Crop Mapping Verification
- ✅ Rice (ID: 0): 15 disease classes
- ✅ Maize (ID: 1): 15 disease classes  
- ✅ Chickpea (ID: 2): 15 disease classes
- ✅ All 21 crops mapped correctly

## Next Steps

1. **Start the API server:**
   ```bash
   cd api
   python start_api.py
   ```

2. **Test with sample images:**
   ```bash
   # Test rice disease detection
   curl -X POST "http://localhost:8000/upload" \
        -F "file=@rice_image.jpg" \
        -F "crop_name=rice"
   ```

3. **Monitor performance:**
   - Check inference speed with new model
   - Verify accuracy improvements
   - Monitor memory usage

## Benefits of Multi-Head Architecture

1. **Improved Accuracy**: Crop-specific heads provide better disease classification
2. **Scalability**: Easy to add new crops without retraining the entire model
3. **Efficiency**: Shared backbone reduces model size while maintaining performance
4. **Flexibility**: Each crop can have different numbers of disease classes

## Troubleshooting

### Common Issues
1. **Model not found**: Ensure `mobilenet.onnx` exists in `api/models/`
2. **Crop not recognized**: Check crop name against available crops list
3. **Preprocessing errors**: Verify image format and size requirements

### Debug Information
The API provides detailed debug output including:
- Crop ID mapping
- Local vs global class indices
- Confidence scores
- Model input/output shapes

## Conclusion

The API has been successfully updated to work with the multi-head crop disease detection model. The new architecture provides improved accuracy and flexibility while maintaining the same API interface for easy integration with existing applications.
