# 🚀 Render Deployment Checklist

## ✅ Pre-Deployment (Completed)
- [x] GitHub repository ready
- [x] Model files uploaded (`models/mobilenet.onnx`)
- [x] Class labels configured (`models/class_map.json`)
- [x] Dependencies listed (`requirements.txt`)
- [x] Docker configuration optimized
- [x] Environment variables documented
- [x] API endpoints tested locally

## 🔧 Render Setup (Do Now)

### Step 1: Connect Repository
- [ ] Go to https://dashboard.render.com
- [ ] Sign in to your Render account
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub account (if not already)
- [ ] Select repository: `Krish9676/ZUTO-GeoTech-Solutions`

### Step 2: Configure Service
- [ ] **Name**: `crop-disease-detection-api`
- [ ] **Environment**: `Python 3`
- [ ] **Region**: Choose closest to users
- [ ] **Branch**: `master`
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables
**Click "Advanced" and add these:**

#### Required Variables:
- [ ] `API_HOST=0.0.0.0`
- [ ] `MODEL_PATH=models/mobilenet.onnx`
- [ ] `SUPABASE_URL=your_actual_supabase_url`
- [ ] `SUPABASE_KEY=your_actual_supabase_anon_key`
- [ ] `SUPABASE_STORAGE_BUCKET=crop-images`
- [ ] `SUPABASE_HEATMAP_BUCKET=heatmaps`

#### Optional Variables:
- [ ] `OLLAMA_BASE_URL=http://localhost:11434`
- [ ] `OLLAMA_MODEL=llama3`
- [ ] `LOG_LEVEL=info`

### Step 4: Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build (5-10 minutes)
- [ ] Monitor build logs for errors
- [ ] Note your deployment URL

## 🧪 Post-Deployment Testing

### Health Check
- [ ] Test: `https://your-app-name.onrender.com/`
- [ ] Expected: `{"status":"ok","message":"Crop Disease Detection API is running"}`

### API Documentation
- [ ] Visit: `https://your-app-name.onrender.com/docs`
- [ ] Verify all endpoints are listed
- [ ] Test upload endpoint with sample image

### Model Testing
- [ ] Upload a test crop image
- [ ] Verify prediction works
- [ ] Check confidence scores
- [ ] Confirm database storage

### Database Integration
- [ ] Verify Supabase connection
- [ ] Test image upload to storage
- [ ] Check database records created
- [ ] Confirm heatmap generation (if enabled)

## 📱 Mobile App Integration

### Update API URL
- [ ] Change mobile app API base URL
- [ ] Test image upload from mobile app
- [ ] Verify error handling
- [ ] Test offline scenarios

### App Store Updates
- [ ] Update app description
- [ ] Add new screenshots
- [ ] Update version number
- [ ] Submit for review

## 🔒 Security & Performance

### Security Checklist
- [ ] Environment variables secured
- [ ] API keys rotated
- [ ] CORS configured properly
- [ ] Input validation working

### Performance Monitoring
- [ ] Response time < 5 seconds
- [ ] Memory usage < 400MB
- [ ] Error rate < 1%
- [ ] Uptime > 99%

## 📊 Monitoring Setup

### Render Dashboard
- [ ] Monitor CPU usage
- [ ] Track memory consumption
- [ ] Watch request count
- [ ] Set up alerts

### Health Checks
- [ ] Automatic health checks enabled
- [ ] Manual testing scheduled
- [ ] Error notifications configured
- [ ] Performance metrics tracked

## 🎯 Success Criteria

### Deployment Success
- [ ] ✅ Service builds without errors
- [ ] ✅ Health check passes
- [ ] ✅ API documentation accessible
- [ ] ✅ Image upload works
- [ ] ✅ Model inference functions
- [ ] ✅ Database connections work
- [ ] ✅ Mobile app can connect

### Performance Targets
- [ ] ✅ Response time < 5 seconds
- [ ] ✅ Uptime > 99%
- [ ] ✅ Error rate < 1%
- [ ] ✅ Memory usage optimized

## 🚨 Troubleshooting

### If Build Fails:
1. Check `requirements.txt` completeness
2. Verify model file exists in repo
3. Check Python version compatibility
4. Review build logs for specific errors

### If Runtime Errors:
1. Verify environment variables
2. Check Supabase credentials
3. Ensure model file path correct
4. Review application logs

### If Performance Issues:
1. Monitor memory usage
2. Check for memory leaks
3. Optimize model loading
4. Consider upgrading plan

---

## 🎉 Deployment Complete!

**Your API URL**: `https://your-app-name.onrender.com`
**API Documentation**: `https://your-app-name.onrender.com/docs`
**Health Check**: `https://your-app-name.onrender.com/`

**Next Steps**:
1. Test all endpoints thoroughly
2. Update mobile app with new API URL
3. Monitor performance and errors
4. Set up regular maintenance schedule

**Congratulations! Your Crop Disease Detection API is now live and ready to help farmers worldwide! 🌱**
