# Crop Disease Detection API

A FastAPI-based REST API for detecting crop diseases from uploaded images using ONNX models and LLaMA integration.

## 🏗️ Project Structure

```
api/
├── app/                    # Main application code
│   ├── __init__.py        # Package initialization
│   ├── main.py            # FastAPI app and health checks
│   ├── api.py             # API routes and endpoints
│   ├── inference.py       # Model inference engine
│   ├── llama_prompt.py    # LLaMA integration for diagnosis
│   ├── config.py          # Centralized configuration
│   └── utils/             # Utility modules
│       ├── __init__.py    # Utils package initialization
│       ├── image_utils.py # Image processing utilities
│       ├── model_loader.py # Model loading and management
│       ├── heatmap.py     # Heatmap generation
│       ├── heatmap_simple.py # Simple heatmap generation
│       └── supabase_client.py # Supabase database client
├── models/                 # Model files
│   ├── mobilenet.onnx     # ONNX model for inference
│   ├── class_map.json     # Class labels mapping
│   └── crop_map.json      # Crop labels mapping
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── startup.py             # Startup validation script
├── run.py                 # Alternative run script
└── env.example            # Environment configuration template
```

## 🚀 Quick Start

### 1. Environment Setup

Copy the environment template and configure your settings:

```bash
# Copy environment template
cp env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_KEY`: Your Supabase anon key
- `STORAGE_BUCKET`: Supabase storage bucket name
- `MODEL_PATH`: Path to your ONNX model (default: `models/mobilenet.onnx`)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

#### Option 1: Using startup script (recommended)
```bash
python startup.py
```

#### Option 2: Using run script
```bash
python run.py
```

#### Option 3: Using start_api script
```bash
python start_api.py
```

#### Option 4: Direct uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 API Endpoints

### Health Checks
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /ready` - Readiness check

### Main Endpoints
- `POST /api/upload` - Upload image for disease detection
- `GET /api/history` - Get detection history
- `GET /api/detections/{id}` - Get specific detection

## 🔧 Configuration

The API uses a centralized configuration system in `app/config.py` that:

- Loads environment variables
- Provides fallback paths for models and files
- Validates configuration on startup
- Manages file paths consistently

## 🧪 Testing

Run the test suite to verify your setup:

```bash
# Test model loading
python test_model_loading.py

# Test complete setup
python test_complete_setup.py

# Test Supabase connection
python test_supabase_connection.py
```

## 🐳 Docker

Build and run with Docker:

```bash
# Build image
docker build -t crop-disease-detection .

# Run container
docker run -p 8000:8000 --env-file .env crop-disease-detection
```

## 📁 File Paths

The API automatically resolves file paths using multiple fallback strategies:

1. Environment variable `MODEL_PATH`
2. Relative to API directory: `models/mobilenet.onnx`
3. Relative to current working directory: `models/mobilenet.onnx`
4. Fallback: `models/mobilenet.onnx`

## 🔍 Troubleshooting

### Common Issues

1. **Model not found**: Check `MODEL_PATH` in `.env` or ensure model exists in `models/` directory
2. **Configuration errors**: Run `python startup.py` to validate configuration
3. **Import errors**: Ensure you're running from the `api/` directory or have proper Python path

### Debug Mode

Enable debug logging by setting log level:

```bash
python run.py --log-level debug
```

## 📖 Documentation

- API documentation available at `http://localhost:8000/docs` when running
- OpenAPI schema at `http://localhost:8000/openapi.json`
- Interactive testing at `http://localhost:8000/docs`

## 🤝 Contributing

1. Follow the existing code structure
2. Update configuration in `app/config.py` for new settings
3. Add tests for new functionality
4. Update this README for any structural changes
