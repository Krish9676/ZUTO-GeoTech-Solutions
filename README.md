# Crop Disease Detection System

A system that allows farmers to upload crop images via a mobile app and receive pest/disease diagnoses.

## System Components

| Component | Tech Stack | Purpose |
|-----------|------------|----------|
| API backend | FastAPI + ONNX + Ollama | Accept images, run detection & diagnosis |
| Model runtime | ResNet/MobileNet via ONNX | Fast local inference of pests/diseases |
| LLM Engine | LLaMA-3 (Ollama HTTP server) | Generate diagnosis explanation |
| Storage | Supabase Storage | Save uploaded image + heatmap |
| Database | PostgreSQL (via Supabase) | Store image URLs, results, confidence |
| Frontend | Flutter/React Native App | Let farmers upload images & see results |
| Deployment | Docker, GitHub Actions, Render | CI/CD + cloud hosting |

## Project Structure

```
project/
├── app/
│   ├── main.py
│   ├── api.py
│   ├── inference.py
│   ├── llama_prompt.py
│   └── utils/
│       ├── image_utils.py
│       ├── heatmap.py
│       └── model_loader.py
├── models/
│   └── mobilenet.onnx  # OR resnet.onnx
├── Dockerfile
├── requirements.txt
├── .env
└── README.md
```

## Flow

```
[Mobile App] ── Upload image ──▶ [FastAPI API]
                                 │
                                 ├─▶ Save to Supabase
                                 ├─▶ Inference with MobileNet (ONNX)
                                 ├─▶ Heatmap generation (optional)
                                 ├─▶ Prompt LLaMA via Ollama for diagnosis
                                 └─▶ Save all info to PostgreSQL
                                 ↓
                            Return prediction + diagnosis to app
```

## Setup and Installation

### Prerequisites
- Python 3.8+
- Supabase account
- Ollama (optional, for LLM diagnosis)

### Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update with your credentials
4. Run the API: `python run.py` or `uvicorn app.main:app --reload`

### Environment Variables
Create a `.env` file with the following variables:
```
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=models/mobilenet.onnx
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_STORAGE_BUCKET=crop-images
SUPABASE_HEATMAP_BUCKET=heatmaps
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

## API Endpoints

### Health Check
- `GET /`: Health check endpoint
  - Returns: `{"status": "ok", "message": "Crop Disease Detection API is running"}`

### Image Upload and Analysis
- `POST /api/upload`: Upload an image for crop disease detection
  - **Parameters:**
    - `file`: Image file (JPEG, PNG)
    - `crop_name`: Optional crop name (string)
  - **Returns:**
    ```json
    {
      "id": "uuid",
      "prediction": "crop_name",
      "confidence": 95.5,
      "image_url": "https://...",
      "heatmap_url": "https://...",
      "diagnosis": "Detailed diagnosis from LLM"
    }
    ```

### Database Endpoints
- `GET /api/detections`: Get recent detections
- `GET /api/detections/{id}`: Get specific detection
- `GET /api/detections/crop/{crop_name}`: Get detections by crop

## Mobile App

The mobile app allows farmers to:
- Upload crop images
- Optionally enter crop name
- Receive pest/disease diagnosis
- View treatment recommendations

## Deployment

### Docker Deployment
```bash
# Build the Docker image
docker build -t crop-disease-detection .

# Run the container
docker run -p 8000:8000 --env-file .env crop-disease-detection
```

### Cloud Deployment
The application can be deployed to:
- **Render**: Easy deployment with automatic scaling
- **Railway**: Simple container deployment
- **Heroku**: Container deployment
- **AWS ECS**: Enterprise-grade container orchestration
- **Google Cloud Run**: Serverless container platform

### Environment Setup for Production
1. Set all environment variables in your cloud platform
2. Ensure model files are included in the deployment
3. Configure CORS settings for your domain
4. Set up monitoring and logging
5. Configure SSL certificates

### Performance Optimization
- Model caching for faster inference
- Image compression for storage efficiency
- Database connection pooling
- CDN for static assets