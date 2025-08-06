import os
import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import supabase
from dotenv import load_dotenv

# Import local modules
from app.inference import run_inference
from app.llama_prompt import llama_prompt
from app.utils.image_utils import preprocess_image, save_image_locally
from app.utils.heatmap import generate_heatmap

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase_client = supabase.create_client(supabase_url, supabase_key)

# Create router
router = APIRouter()


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    crop_name: Optional[str] = Form(None)
):
    """Upload an image for pest/disease detection"""
    try:
        # Generate a unique ID for this upload
        upload_id = str(uuid.uuid4())
        
        # Save image locally for processing
        image_path = await save_image_locally(file, upload_id)
        
        # Preprocess image for model inference
        image_tensor = preprocess_image(image_path)
        
        # Run model inference
        prediction_results = run_inference(image_tensor)
        
        # Get the top prediction
        pest_name = prediction_results["label"]
        confidence = prediction_results["confidence"]
        
        # Generate heatmap (optional)
        heatmap_path = generate_heatmap(image_path, image_tensor, prediction_results)
        
        # Upload original image to Supabase Storage
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        image_path_in_bucket = f"images/{upload_id}.jpg"
        supabase_client.storage.from_(os.getenv("STORAGE_BUCKET")).upload(
            image_path_in_bucket,
            image_data
        )
        
        # Get the public URL
        image_url = supabase_client.storage.from_(os.getenv("STORAGE_BUCKET")).get_public_url(image_path_in_bucket)
        
        # Upload heatmap to Supabase Storage if available
        heatmap_url = None
        if heatmap_path:
            with open(heatmap_path, "rb") as f:
                heatmap_data = f.read()
            
            heatmap_path_in_bucket = f"heatmaps/{upload_id}.jpg"
            supabase_client.storage.from_(os.getenv("STORAGE_BUCKET")).upload(
                heatmap_path_in_bucket,
                heatmap_data
            )
            
            heatmap_url = supabase_client.storage.from_(os.getenv("STORAGE_BUCKET")).get_public_url(heatmap_path_in_bucket)
        
        # Get diagnosis from LLaMA
        diagnosis = llama_prompt(image_url, pest_name, confidence, crop_name)
        
        # Store results in database
        supabase_client.table("detections").insert({
            "id": upload_id,
            "image_url": image_url,
            "heatmap_url": heatmap_url,
            "pest_name": pest_name,
            "confidence": confidence,
            "crop_name": crop_name,
            "diagnosis": diagnosis
        }).execute()
        
        # Clean up local files
        os.remove(image_path)
        if heatmap_path:
            os.remove(heatmap_path)
        
        # Return results
        return {
            "id": upload_id,
            "prediction": pest_name,
            "confidence": confidence,
            "image_url": image_url,
            "heatmap_url": heatmap_url,
            "diagnosis": diagnosis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))