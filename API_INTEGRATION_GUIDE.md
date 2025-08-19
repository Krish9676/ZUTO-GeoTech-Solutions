# 🌾 Crop Disease Detection API Integration Guide

Your API is successfully deployed at: **https://crop-disease-detection-api-0spd.onrender.com/**

## 🚀 Quick Start

### 1. Test API Status
```bash
curl https://crop-disease-detection-api-0spd.onrender.com/
```
Expected response: `{"status":"ok","message":"Crop Disease Detection API is running"}`

### 2. View API Documentation
Visit: `https://crop-disease-detection-api-0spd.onrender.com/docs` (Swagger UI)

## 📁 API Structure Overview

### Key Files to Understand Your API:

#### **Core API Files:**
- **`api/app/main.py`** - Main FastAPI application with CORS and health checks
- **`api/app/api.py`** - Core API endpoints and business logic
- **`api/app/inference.py`** - ML model inference engine
- **`api/app/config.py`** - Configuration and environment variables

#### **Utility Files:**
- **`api/app/utils/model_loader.py`** - ML model loading and management
- **`api/app/utils/image_utils.py`** - Image preprocessing utilities
- **`api/app/utils/heatmap.py`** - Heatmap generation for visual analysis
- **`api/app/utils/supabase_client.py`** - Database and storage integration

#### **Model Files:**
- **`api/models/`** - Contains your trained ML models (.onnx and .pth files)
- **`api/models/class_map.json`** - Class labels for predictions
- **`api/models/crop_map.json`** - Crop type mappings

## 🔌 Available Endpoints

### 1. **Health Check** - `GET /`
```javascript
// Check if API is running
const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/');
const data = await response.json();
// Returns: {"status":"ok","message":"Crop Disease Detection API is running"}
```

### 2. **Image Analysis** - `POST /api/upload`
```javascript
// Upload and analyze an image
const formData = new FormData();
formData.append('file', imageFile);
formData.append('crop_name', 'rice'); // Optional

const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/api/upload', {
    method: 'POST',
    body: formData
});

const result = await response.json();
```

**Response Format:**
```json
{
    "id": "uuid-string",
    "prediction": "disease_name",
    "confidence": 0.95,
    "image_url": "https://...",
    "heatmap_url": "https://...",
    "diagnosis": "AI-generated diagnosis text",
    "crop_name": "rice"
}
```

### 3. **Detection History** - `GET /api/history`
```javascript
// Get all previous detections
const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/api/history');
const history = await response.json();
```

### 4. **Specific Detection** - `GET /api/detections/{id}`
```javascript
// Get details of a specific detection
const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/api/detections/uuid-here');
const detection = await response.json();
```

## 🌐 Web Integration Examples

### Basic HTML Integration
```html
<!DOCTYPE html>
<html>
<head>
    <title>Crop Disease Detection</title>
</head>
<body>
    <input type="file" id="imageInput" accept="image/*">
    <button onclick="analyzeImage()">Analyze</button>
    <div id="results"></div>

    <script>
        async function analyzeImage() {
            const file = document.getElementById('imageInput').files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/api/upload', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                document.getElementById('results').innerHTML = `
                    <h3>Prediction: ${result.prediction}</h3>
                    <p>Confidence: ${(result.confidence * 100).toFixed(1)}%</p>
                    <p>Diagnosis: ${result.diagnosis}</p>
                `;
            } catch (error) {
                console.error('Error:', error);
            }
        }
    </script>
</body>
</html>
```

### React Component Example
```jsx
import React, { useState } from 'react';

function CropAnalysis() {
    const [file, setFile] = useState(null);
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);

    const analyzeImage = async () => {
        if (!file) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            setResults(result);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <input 
                type="file" 
                accept="image/*" 
                onChange={(e) => setFile(e.target.files[0])} 
            />
            <button onClick={analyzeImage} disabled={!file || loading}>
                {loading ? 'Analyzing...' : 'Analyze Image'}
            </button>
            
            {results && (
                <div>
                    <h3>Results:</h3>
                    <p>Prediction: {results.prediction}</p>
                    <p>Confidence: {(results.confidence * 100).toFixed(1)}%</p>
                    <p>Diagnosis: {results.diagnosis}</p>
                </div>
            )}
        </div>
    );
}

export default CropAnalysis;
```

### Node.js/Express Backend Integration
```javascript
const express = require('express');
const multer = require('multer');
const fetch = require('node-fetch');
const app = express();

const upload = multer({ dest: 'uploads/' });

app.post('/analyze', upload.single('image'), async (req, res) => {
    try {
        const formData = new FormData();
        formData.append('file', req.file.buffer, req.file.originalname);
        
        if (req.body.crop_name) {
            formData.append('crop_name', req.body.crop_name);
        }

        const response = await fetch('https://crop-disease-detection-api-0spd.onrender.com/api/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        res.json(result);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

## 🔧 API Configuration

### Environment Variables
Your API uses these environment variables (configured in Render):
- `SUPABASE_URL` - Database connection
- `SUPABASE_KEY` - Database authentication
- `STORAGE_BUCKET` - Image storage bucket
- `API_HOST` - Server host (default: 0.0.0.0)
- `API_PORT` - Server port (default: 8000)

### CORS Configuration
The API allows all origins (`*`) for development. In production, you can restrict this to specific domains.

## 📊 Response Data Structure

### Image Analysis Response
```json
{
    "id": "unique-uuid",
    "prediction": "rice_bacterial_blight",
    "confidence": 0.9876,
    "image_url": "https://storage.supabase.co/...",
    "heatmap_url": "https://storage.supabase.co/...",
    "diagnosis": "This image shows symptoms of bacterial blight...",
    "crop_name": "rice"
}
```

### History Response
```json
[
    {
        "id": "uuid-1",
        "prediction": "healthy_rice",
        "confidence": 0.95,
        "image_url": "https://...",
        "heatmap_url": "https://...",
        "diagnosis": "Plant appears healthy...",
        "timestamp": "2024-01-01T12:00:00Z",
        "crop_name": "rice"
    }
]
```

## 🚨 Error Handling

### Common HTTP Status Codes
- **200** - Success
- **400** - Bad Request (invalid file format, missing parameters)
- **500** - Internal Server Error (model inference failed, database error)

### Error Response Format
```json
{
    "detail": "Error message describing what went wrong"
}
```

## 🔍 Testing Your Integration

### 1. Test API Status
```bash
curl https://crop-disease-detection-api-0spd.onrender.com/
```

### 2. Test Image Upload (using curl)
```bash
curl -X POST \
  -F "file=@your_image.jpg" \
  -F "crop_name=rice" \
  https://crop-disease-detection-api-0spd.onrender.com/api/upload
```

### 3. Test History Endpoint
```bash
curl https://crop-disease-detection-api-0spd.onrender.com/api/history
```

## 📱 Mobile App Integration

For mobile apps, you can use the same endpoints. The API returns mobile-friendly response formats with all necessary data for display.

## 🎯 Next Steps

1. **Test the API** with sample images
2. **Integrate into your webpage** using the provided examples
3. **Customize the UI** to match your design
4. **Add error handling** for production use
5. **Implement caching** for better performance
6. **Add user authentication** if needed

## 🆘 Support

If you encounter issues:
1. Check the API status endpoint
2. Verify your image format (JPG, PNG, JPEG)
3. Check the browser console for CORS errors
4. Ensure your image file size is reasonable (< 10MB)

Your API is now live and ready to analyze crop images! 🌱
