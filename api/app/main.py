import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import API routes
from .api import router as api_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Crop Disease Detection API",
    description="API for detecting crop diseases from images",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Crop Disease Detection API is running"}


@app.get("/health")
async def health_check():
    """Quick health check for load balancers"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.get("/ready")
async def ready_check():
    """Readiness check - verifies the API is ready to handle requests"""
    try:
        # Import config here to avoid circular imports
        from .config import get_model_paths, validate_config
        
        # Check configuration
        config_errors = validate_config()
        if config_errors:
            return {"status": "not_ready", "errors": config_errors}
        
        # Check if we can access the models directory
        from pathlib import Path
        models_dir = Path(__file__).parent.parent / "models"
        
        if models_dir.exists():
            return {"status": "ready", "models": "available"}
        else:
            return {"status": "not_ready", "models": "missing"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=True
    )