import os
import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
import supabase
from dotenv import load_dotenv

# Import local modules
from .inference import run_inference
from .llama_prompt import llama_prompt
from .utils.image_utils import preprocess_image, save_image_locally
from .utils.heatmap import generate_heatmap
from .utils.heatmap_simple import generate_heatmap_simple
from .utils.disease_descriptions import generate_diagnosis_summary, format_disease_name

# Import config here to avoid circular imports
from .config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET

# Initialize Supabase client
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Create router
router = APIRouter()


@router.get("/history")
async def get_detection_history():
    """Get all detection history"""
    try:
        response = supabase_client.table("detections").select("*").order("created_at", desc=True).execute()
        detections = response.data
        
        # Format the response for mobile app compatibility
        formatted_detections = []
        for detection in detections:
            formatted_detections.append({
                "id": detection.get("id"),
                "prediction": detection.get("pest_name"),
                "confidence": detection.get("confidence"),
                "image_url": detection.get("image_url"),
                "heatmap_url": detection.get("heatmap_url"),
                "diagnosis": detection.get("diagnosis"),
                "timestamp": detection.get("created_at"),
                "crop_name": detection.get("crop_name")
            })
        
        return formatted_detections
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/detections/{detection_id}")
async def get_detection(detection_id: str):
    """Get a specific detection by ID"""
    try:
        response = supabase_client.table("detections").select("*").eq("id", detection_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Detection not found")
        
        detection = response.data[0]
        
        # Format the response for mobile app compatibility
        return {
            "id": detection.get("id"),
            "prediction": detection.get("pest_name"),
            "confidence": detection.get("confidence"),
            "image_url": detection.get("image_url"),
            "heatmap_url": detection.get("heatmap_url"),
            "diagnosis": detection.get("diagnosis"),
            "timestamp": detection.get("created_at"),
            "crop_name": detection.get("crop_name")
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        prediction_results = run_inference(image_tensor, crop_name)
        
        # Get the top prediction
        pest_name = prediction_results["label"]
        confidence = prediction_results["confidence"]
        
        # Generate heatmap (optional)
        try:
            heatmap_path = generate_heatmap(image_path, image_tensor, prediction_results)
        except Exception as e:
            print(f"Error with matplotlib heatmap, using simple version: {e}")
            heatmap_path = generate_heatmap_simple(image_path, image_tensor, prediction_results)
        
        # Upload original image to Supabase Storage
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        image_path_in_bucket = f"images/{upload_id}.jpg"
        supabase_client.storage.from_(STORAGE_BUCKET).upload(
            image_path_in_bucket,
            image_data
        )
        
        # Get the public URL
        image_url = supabase_client.storage.from_(STORAGE_BUCKET).get_public_url(image_path_in_bucket)
        
        # Upload heatmap to Supabase Storage if available
        heatmap_url = None
        if heatmap_path:
            with open(heatmap_path, "rb") as f:
                heatmap_data = f.read()
            
            heatmap_path_in_bucket = f"heatmaps/{upload_id}.jpg"
            supabase_client.storage.from_(STORAGE_BUCKET).upload(
                heatmap_path_in_bucket,
                heatmap_data
            )
            
            heatmap_url = supabase_client.storage.from_(STORAGE_BUCKET).get_public_url(heatmap_path_in_bucket)
        
        # Generate comprehensive diagnosis using disease descriptions
        diagnosis = generate_diagnosis_summary(pest_name, confidence, crop_name)
        
        # Also try to get LLaMA diagnosis if available (fallback)
        try:
            llama_diagnosis = llama_prompt(image_url, pest_name, confidence, crop_name)
            if llama_diagnosis and "Unable to generate" not in llama_diagnosis:
                diagnosis = f"{diagnosis}\n\n**AI-Generated Additional Insights:**\n{llama_diagnosis}"
        except Exception as e:
            print(f"LLaMA diagnosis failed, using disease descriptions: {e}")
        
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