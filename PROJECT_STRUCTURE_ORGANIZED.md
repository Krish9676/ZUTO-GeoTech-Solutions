# 🏗️ PROJECT STRUCTURE - ORGANIZED & COMPLETE

## 📁 **PROJECT OVERVIEW**
This is a **Crop Disease Detection API** that uses a custom-trained MobileNetV3 model with crop-aware disease classification.

## 🗂️ **DIRECTORY STRUCTURE**

```
PD_application/
├── 📁 api/                          # Main API application
│   ├── 📁 app/                      # FastAPI application code
│   │   ├── 📄 main.py              # FastAPI app entry point
│   │   ├── 📄 api.py               # API routes and endpoints
│   │   ├── 📄 inference.py         # Model inference logic
│   │   ├── 📄 llama_prompt.py      # LLaMA integration
│   │   └── 📁 utils/               # Utility modules
│   │       ├── 📄 image_utils.py   # Image preprocessing
│   │       ├── 📄 heatmap.py       # Heatmap generation
│   │       └── 📄 heatmap_simple.py # Simple heatmap fallback
│   ├── 📁 models/                  # Model files
│   │   ├── 📄 mobilenet.onnx       # ONNX model (converted)
│   │   ├── 📄 mobilenet.pth        # PyTorch model (original)
│   │   ├── 📄 class_map.json       # 315 class labels
│   │   └── 📄 crop_map.json        # 21 crop labels
│   ├── 📄 start_api.py             # API startup script
│   ├── 📄 test_complete_setup.py   # Complete setup test
│   └── 📄 requirements.txt         # Python dependencies
├── 📁 scripts/                      # Utility scripts
│   └── 📄 convert_to_onnx.py       # PyTorch to ONNX converter
├── 📄 test_onnx_conversion.py      # ONNX model test
└── 📄 MODEL_CONVERSION_GUIDE.md    # Conversion guide
```

## 🔧 **MODEL ARCHITECTURE**

### **Input Format:**
- **Image**: 3×160×160 RGB tensor (160×160 resolution)
- **Crop ID**: Integer (0-20) representing crop type

### **Model Structure:**
```
MobileNetV3-Small Features → 576 channels
Crop Embedding (21 crops × 64) → 64 channels
Concatenated → 640 channels → Linear → 315 classes
```

### **Output:**
- **315 classes** representing crop-disease combinations
- Confidence scores for each class

## 🚀 **HOW TO RUN - STEP BY STEP**

### **Step 1: Verify Project Structure**
```bash
cd PD_application
python api/test_complete_setup.py
```

### **Step 2: Start the API Server**
```bash
cd api
python start_api.py
```

### **Step 3: Test the API**
- **Health Check**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Root**: http://localhost:8000/

## 📋 **API ENDPOINTS**

### **Core Endpoints:**
- `GET /` - Health check
- `GET /health` - Health status
- `GET /ready` - Readiness check
- `GET /api/history` - Get detection history
- `GET /api/detections/{id}` - Get specific detection
- `POST /api/upload` - Upload image for detection

### **Upload Endpoint Usage:**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@your_image.jpg" \
  -F "crop_name=rice"
```

## 🧪 **TESTING & VERIFICATION**

### **1. Complete Setup Test:**
```bash
cd api
python test_complete_setup.py
```

### **2. ONNX Model Test:**
```bash
cd ..
python test_onnx_conversion.py
```

### **3. API Health Check:**
```bash
curl http://localhost:8000/health
```

## 🔍 **TROUBLESHOOTING**

### **Common Issues:**

1. **Import Errors:**
   - Ensure you're running from the correct directory
   - Use `start_api.py` for proper module resolution

2. **Model Loading Errors:**
   - Check if `mobilenet.onnx` exists in `api/models/`
   - Verify `class_map.json` and `crop_map.json` are present

3. **Port Already in Use:**
   - Change port in `start_api.py` or kill existing process
   - Default port: 8000

4. **Missing Dependencies:**
   - Install requirements: `pip install -r api/requirements.txt`

## 📊 **MODEL CONFIGURATION**

### **Crops (21):**
```json
["rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", 
 "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate", 
 "banana", "mango", "grapes", "watermelon", "muskmelon", 
 "apple", "orange", "papaya", "coconut", "cotton", "jute"]
```

### **Classes (315):**
- Generic class names: `class_0` to `class_314`
- Can be updated with actual crop-disease names later

## 🔄 **WORKFLOW**

1. **Image Upload** → Preprocess to 160×160
2. **Crop Selection** → Convert to crop ID (0-20)
3. **Model Inference** → Run ONNX model with both inputs
4. **Result Processing** → Apply softmax, get confidence
5. **Response** → Return prediction, confidence, crop used

## 📝 **NEXT STEPS**

1. **Update Class Names**: Replace generic class names with actual crop-disease combinations
2. **Add Authentication**: Implement API key or user authentication
3. **Database Integration**: Connect to Supabase for data persistence
4. **Mobile App**: Integrate with Flutter mobile application
5. **Deployment**: Deploy to cloud platform (Render, AWS, etc.)

## ✅ **VERIFICATION CHECKLIST**

- [ ] All model files present (`mobilenet.onnx`, `class_map.json`, `crop_map.json`)
- [ ] Complete setup test passes (`test_complete_setup.py`)
- [ ] ONNX model loads and runs inference
- [ ] API server starts without errors
- [ ] Health endpoints respond correctly
- [ ] Upload endpoint accepts images and crop names
- [ ] Model returns predictions with confidence scores

---

**🎯 Goal**: A fully functional, production-ready Crop Disease Detection API that matches your training process exactly.
