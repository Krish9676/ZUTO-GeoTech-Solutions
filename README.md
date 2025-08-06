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

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables in `.env`
4. Run the API: `uvicorn app.main:app --reload`

## API Endpoints

- `POST /upload`: Upload an image for pest/disease detection
  - Returns prediction, confidence, image URL, heatmap URL, and diagnosis

## Mobile App

The mobile app allows farmers to:
- Upload crop images
- Optionally enter crop name
- Receive pest/disease diagnosis
- View treatment recommendations

## Deployment

The application can be deployed using Docker and GitHub Actions to services like Render.