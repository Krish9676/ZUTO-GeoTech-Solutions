# 🚀 API Update & Redeployment Guide

## 📋 **Overview**
Your API has been updated with new endpoints needed for mobile app integration. This guide will help you redeploy the updated API.

## 🔄 **What's Been Updated**

### **New Endpoints Added:**
1. **`GET /api/history`** - Retrieves all detection history
2. **`GET /api/detections/{id}`** - Retrieves a specific detection by ID

### **Updated Files:**
- `app/api.py` - Added history and detections endpoints
- `render.yaml` - Added missing environment variables

## 🚀 **Step 1: Redeploy Your API**

### **Option A: Automatic Deployment (Recommended)**
If you have GitHub connected to Render:
1. Commit and push your changes to GitHub
2. Render will automatically redeploy your API
3. Monitor the deployment in your Render dashboard

### **Option B: Manual Deployment**
1. Go to your Render dashboard
2. Select your `crop-disease-detection-api` service
3. Click "Manual Deploy" → "Deploy latest commit"

## ⚙️ **Step 2: Verify Environment Variables**

Ensure these environment variables are set in your Render dashboard:

| Variable | Value | Required |
|----------|-------|----------|
| `SUPABASE_URL` | Your Supabase project URL | ✅ Yes |
| `SUPABASE_KEY` | Your Supabase service role key | ✅ Yes |
| `STORAGE_BUCKET` | `crop-images` | ✅ Yes |
| `SUPABASE_STORAGE_BUCKET` | `crop-images` | ✅ Yes |
| `SUPABASE_HEATMAP_BUCKET` | `heatmaps` | ✅ Yes |
| `MODEL_PATH` | `models/mobilenet.onnx` | ✅ Yes |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | ⚠️ Optional |
| `OLLAMA_MODEL` | `llama3` | ⚠️ Optional |

## 🧪 **Step 3: Test the Updated API**

After redeployment, run the test script to verify all endpoints work:

```bash
python test_mobile_integration.py
```

Expected results:
- ✅ Health check: 200
- ✅ History endpoint: 200 (with data or empty array)
- ✅ Detections endpoint: 404 for non-existent ID (expected)

## 📱 **Step 4: Mobile App Integration**

Once the API is updated and tested:

1. **Update Mobile App Configuration:**
   - The mobile app is already configured with your API URL
   - API service has been updated to use the correct endpoints

2. **Test Mobile App:**
   - Build and run the Flutter app
   - Test image upload functionality
   - Verify history and detection viewing

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **Environment Variables Missing:**
   - Check Render dashboard for missing variables
   - Ensure Supabase credentials are correct

2. **Database Connection Issues:**
   - Verify Supabase project is active
   - Check if `detections` table exists

3. **Model Loading Issues:**
   - Ensure model files are in the `models/` directory
   - Check file permissions

### **Debug Commands:**
```bash
# Check API health
curl https://crop-disease-detection-api-0spd.onrender.com/

# Test history endpoint
curl https://crop-disease-detection-api-0spd.onrender.com/api/history

# Test specific detection
curl https://crop-disease-detection-api-0spd.onrender.com/api/detections/test-id
```

## 📊 **Expected API Response Format**

### **History Endpoint (`GET /api/history`):**
```json
[
  {
    "id": "uuid-string",
    "prediction": "pest-name",
    "confidence": 0.95,
    "image_url": "https://...",
    "heatmap_url": "https://...",
    "diagnosis": "Detailed diagnosis...",
    "timestamp": "2024-01-01T00:00:00Z",
    "crop_name": "corn"
  }
]
```

### **Detection Endpoint (`GET /api/detections/{id}`):**
```json
{
  "id": "uuid-string",
  "prediction": "pest-name",
  "confidence": 0.95,
  "image_url": "https://...",
  "heatmap_url": "https://...",
  "diagnosis": "Detailed diagnosis...",
  "timestamp": "2024-01-01T00:00:00Z",
  "crop_name": "corn"
}
```

## 🎯 **Next Steps After API Update**

1. ✅ **API Redeployment** - Complete this guide
2. 📱 **Mobile App Testing** - Test with real devices
3. 🚀 **Mobile App Deployment** - Build and distribute
4. 📊 **Production Monitoring** - Monitor API performance

## 📞 **Support**

If you encounter issues:
1. Check Render deployment logs
2. Verify environment variables
3. Test API endpoints individually
4. Check Supabase database connectivity

---

**Status:** Ready for deployment
**Last Updated:** $(date)
**API Version:** 1.1.0 (with mobile endpoints)
