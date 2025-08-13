# Crop Disease Detection API

A FastAPI-based REST API for detecting crop diseases from images using machine learning models.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- ONNX Runtime
- PyTorch
- FastAPI
- Supabase (for database)

### Installation

1. **Clone the repository and navigate to the API directory:**
   ```bash
   cd api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the `api/` directory:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   MODEL_PATH=models/mobilenet_crop_pest_model.pth
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

4. **Download the model:**
   ```bash
   python scripts/download_model.py
   ```

### Running the API

#### Development Mode
```bash
python run.py --reload
```

#### Production Mode
```bash
python run.py --host 0.0.0.0 --port 8000 --workers 4
```

#### Using Docker
```bash
docker build -t crop-disease-api .
docker run -p 8000:8000 crop-disease-api
```

## 📁 Project Structure

```
api/
├── app/                    # Main application code
│   ├── api.py             # API endpoints and routes
│   ├── inference.py       # Model inference logic
│   ├── llama_prompt.py    # LLM prompt handling
│   ├── main.py            # FastAPI app initialization
│   └── utils/             # Utility functions
│       ├── image_utils.py # Image processing utilities
│       ├── heatmap.py     # Heatmap generation
│       └── ...
├── models/                 # ML model files
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── run.py                 # CLI runner script
└── README.md              # This file
```

## 🔌 API Endpoints

### Health Check
- `GET /` - API status check

### Core Endpoints
- `POST /api/upload` - Upload image for disease detection
- `GET /api/history` - Get detection history
- `GET /api/detections/{id}` - Get specific detection details

## 🧪 Testing

Run the test suite:
```bash
cd api
python -m pytest tests/
```

## 🚀 Deployment

### Render
The API is configured for deployment on Render. See `render.yaml` for configuration.

### Other Platforms
- **Heroku**: Use the provided Dockerfile
- **AWS/GCP**: Use the Dockerfile with your preferred container service

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SUPABASE_URL` | Supabase project URL | Required |
| `SUPABASE_KEY` | Supabase API key | Required |
| `MODEL_PATH` | Path to ML model | `models/mobilenet.onnx` |
| `API_HOST` | API host address | `0.0.0.0` |
| `API_PORT` | API port | `8000` |

## 🔧 Development

### Adding New Endpoints
1. Add new routes in `app/api.py`
2. Update tests in `tests/`
3. Update this README

### Model Updates
1. Place new models in `models/`
2. Update `MODEL_PATH` in `.env`
3. Test inference in `app/inference.py`

## 📞 Support

For issues and questions, please check the main project documentation or create an issue in the repository.
