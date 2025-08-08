# Render Deployment Guide

## 🚀 Deploy Your Crop Disease Detection API to Render

### Prerequisites
- ✅ Render account created
- ✅ GitHub repository ready
- ✅ Supabase credentials configured
- ✅ Model files uploaded

### Step 1: Connect Your Repository

1. **Log into Render Dashboard**
   - Go to https://dashboard.render.com
   - Sign in with your account

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account if not already connected

3. **Select Repository**
   - Choose your repository: `Krish9676/ZUTO-GeoTech-Solutions`
   - Render will automatically detect it's a Python application

### Step 2: Configure the Service

#### Basic Settings
- **Name**: `crop-disease-detection-api`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `master`
- **Root Directory**: Leave empty (root of repo)

#### Build & Deploy Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables

Click "Advanced" and add these environment variables:

#### Required Variables
```
API_HOST=0.0.0.0
MODEL_PATH=models/mobilenet.onnx
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
SUPABASE_STORAGE_BUCKET=crop-images
SUPABASE_HEATMAP_BUCKET=heatmaps
```

#### Optional Variables
```
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
LOG_LEVEL=info
```

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for Build**: This may take 5-10 minutes
3. **Monitor Logs**: Check the build logs for any errors
4. **Verify Deployment**: Once complete, you'll get a URL like `https://your-app-name.onrender.com`

### Step 5: Test Your Deployment

#### Health Check
```bash
curl https://your-app-name.onrender.com/
# Should return: {"status":"ok","message":"Crop Disease Detection API is running"}
```

#### API Documentation
- Visit: `https://your-app-name.onrender.com/docs`
- Test the upload endpoint with a sample image

### Step 6: Configure Custom Domain (Optional)

1. **Go to Settings** in your Render service
2. **Click "Custom Domains"**
3. **Add your domain** (e.g., `api.yourdomain.com`)
4. **Configure DNS** as instructed by Render

### Step 7: Update Mobile App

Update your Flutter app's API base URL:
```dart
// In your mobile app configuration
const String apiBaseUrl = 'https://your-app-name.onrender.com';
```

## 🔧 Troubleshooting

### Common Issues

#### Build Failures
- **Missing Dependencies**: Check `requirements.txt` is complete
- **Model File Issues**: Ensure `models/mobilenet.onnx` is in the repository
- **Python Version**: Make sure you're using Python 3.10+

#### Runtime Errors
- **Environment Variables**: Verify all required env vars are set
- **Database Connection**: Check Supabase credentials
- **Model Loading**: Ensure model file path is correct

#### Performance Issues
- **Cold Starts**: Render has cold start delays (normal for free tier)
- **Memory Limits**: Free tier has 512MB RAM limit
- **Timeout**: Requests may timeout on free tier

### Monitoring

#### Render Dashboard
- **Logs**: View real-time application logs
- **Metrics**: Monitor CPU, memory, and request count
- **Deployments**: Track deployment history

#### Health Checks
- **Automatic**: Render checks `/` endpoint
- **Manual**: Test endpoints regularly
- **Alerts**: Set up notifications for failures

## 📊 Performance Optimization

### Free Tier Limitations
- **512MB RAM**: Monitor memory usage
- **Cold Starts**: 15-30 second delays
- **Request Timeout**: 30 seconds max
- **Bandwidth**: 750GB/month

### Upgrade Options
- **Paid Plans**: Start at $7/month for better performance
- **Auto-scaling**: Handle traffic spikes
- **Custom Domains**: Professional URLs
- **SSL Certificates**: Automatic HTTPS

## 🔒 Security Considerations

### Environment Variables
- ✅ Never commit `.env` files
- ✅ Use Render's environment variable system
- ✅ Rotate API keys regularly

### API Security
- [ ] Add API authentication
- [ ] Implement rate limiting
- [ ] Configure CORS for your domain
- [ ] Set up request validation

## 📈 Scaling

### When to Upgrade
- **High Traffic**: >1000 requests/day
- **Memory Issues**: Frequent crashes
- **Performance**: Slow response times
- **Reliability**: Need 99.9% uptime

### Scaling Strategies
1. **Upgrade Plan**: Move to paid tier
2. **Load Balancing**: Multiple instances
3. **CDN**: Static asset optimization
4. **Caching**: Redis for session data

## 🎯 Success Metrics

### Deployment Checklist
- [ ] Service builds successfully
- [ ] Health check passes
- [ ] API documentation accessible
- [ ] Image upload works
- [ ] Model inference functions
- [ ] Database connections work
- [ ] Mobile app can connect

### Performance Targets
- **Response Time**: <5 seconds for image upload
- **Uptime**: >99% availability
- **Error Rate**: <1% failed requests
- **Memory Usage**: <400MB average

---

**Your API will be live at**: `https://your-app-name.onrender.com`
**API Documentation**: `https://your-app-name.onrender.com/docs`
**Health Check**: `https://your-app-name.onrender.com/`

🎉 **Congratulations! Your Crop Disease Detection API is now deployed and ready to serve farmers worldwide!**
