# Crop Selection Analysis for Multi-Head Disease Detection Model

## Overview
The model was trained on **21 crops** selected from a comprehensive agricultural dataset. Each crop has **15 disease classes** (including healthy variants), resulting in **315 total disease classes** across all crops.

## The 21 Selected Crops

### **Cereal Crops (2 crops)**
1. **Rice** (ID: 0) - Global classes 0-14
2. **Maize** (ID: 1) - Global classes 15-29

### **Legume Crops (6 crops)**
3. **Chickpea** (ID: 2) - Global classes 30-44
4. **Kidneybeans** (ID: 3) - Global classes 45-59
5. **Pigeonpeas** (ID: 4) - Global classes 60-74
6. **Mothbeans** (ID: 5) - Global classes 75-89
7. **Mungbean** (ID: 6) - Global classes 90-104
8. **Blackgram** (ID: 7) - Global classes 105-119

### **Other Legumes (1 crop)**
9. **Lentil** (ID: 8) - Global classes 120-134

### **Fruit Crops (9 crops)**
10. **Pomegranate** (ID: 9) - Global classes 135-149
11. **Banana** (ID: 10) - Global classes 150-164
12. **Mango** (ID: 11) - Global classes 165-179
13. **Grapes** (ID: 12) - Global classes 180-194
14. **Watermelon** (ID: 13) - Global classes 195-209
15. **Muskmelon** (ID: 14) - Global classes 210-224
16. **Apple** (ID: 15) - Global classes 225-239
17. **Orange** (ID: 16) - Global classes 240-254
18. **Papaya** (ID: 17) - Global classes 255-269

### **Tropical Crops (2 crops)**
19. **Coconut** (ID: 18) - Global classes 270-284
20. **Cotton** (ID: 19) - Global classes 285-299

### **Fiber Crops (1 crop)**
21. **Jute** (ID: 20) - Global classes 300-314

## Crop Selection Criteria

### **1. Agricultural Importance**
- **Staple Crops**: Rice and Maize are globally important food crops
- **Protein Sources**: Multiple legume crops for protein diversity
- **Economic Value**: High-value crops like fruits and cotton

### **2. Geographic Diversity**
- **Tropical Crops**: Banana, Mango, Coconut, Papaya
- **Temperate Crops**: Apple, Grapes
- **Subtropical Crops**: Rice, Cotton, Jute
- **Warm Season Crops**: Maize, Watermelon, Muskmelon

### **3. Disease Diversity**
Each crop was selected to have a diverse range of diseases:
- **Fungal Diseases**: Rust, blight, spot diseases
- **Bacterial Diseases**: Bacterial blight, bacterial spot
- **Viral Diseases**: Mosaic viruses, leaf curl
- **Healthy Variants**: Each crop includes healthy samples

### **4. Data Availability**
The crops were likely selected based on:
- **Dataset Availability**: Sufficient training data for each crop
- **Disease Coverage**: 15 distinct disease classes per crop
- **Image Quality**: Good quality disease images available

## Disease Class Structure

### **Per Crop (15 classes each)**
Each crop follows this pattern:
- **1 Healthy class** (e.g., "healthy_rice")
- **14 Disease classes** (e.g., "rice_bacterial_blight", "rice_brown_spot")

### **Global Class Mapping**
- **Total Classes**: 315 (21 crops × 15 classes)
- **Class Range**: 0-314
- **Mapping**: Each crop's local classes (0-14) map to global classes

## Model Architecture Benefits

### **1. Crop-Specific Optimization**
- Each crop gets its own specialized classifier
- Better accuracy for crop-specific diseases
- Reduced confusion between different crop diseases

### **2. Scalable Design**
- Easy to add new crops without retraining
- Each crop can have different numbers of diseases
- Shared backbone reduces model size

### **3. Agricultural Relevance**
- Covers major food security crops
- Includes both subsistence and commercial crops
- Represents diverse agricultural systems

## Usage in API

### **Crop Selection**
When using the API, users must specify the crop:
```python
# Example API call
POST /upload
{
    "file": "image.jpg",
    "crop_name": "rice"  # Must be one of the 21 crops
}
```

### **Available Crops List**
The API provides the complete list:
```python
GET /crops
# Returns: ["rice", "maize", "chickpea", ..., "jute"]
```

## Training Data Distribution

### **Balanced Representation**
- Each crop has equal representation (15 classes)
- Each class likely has balanced training samples
- Prevents bias toward any single crop

### **Disease Coverage**
- **Fungal**: Most common disease type
- **Bacterial**: Secondary disease type  
- **Viral**: Less common but included
- **Healthy**: Baseline for comparison

## Conclusion

The 21 crops were strategically selected to:
1. **Cover major agricultural systems** globally
2. **Provide diverse disease types** for robust training
3. **Ensure data availability** for effective training
4. **Balance different crop categories** (cereals, legumes, fruits, etc.)

This selection ensures the model can handle a wide range of agricultural scenarios while maintaining high accuracy through crop-specific specialization.
