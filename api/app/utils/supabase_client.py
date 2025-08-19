import os
from typing import Dict, Any, Optional, List
import uuid
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Import config here to avoid circular imports
from ..config import SUPABASE_URL, SUPABASE_KEY, STORAGE_BUCKET

# Heatmap bucket configuration
HEATMAP_BUCKET = "heatmaps"  # Default heatmap bucket

# Singleton pattern for Supabase client
class SupabaseClient:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._client = cls._create_client()
        return cls._instance
    
    @staticmethod
    def _create_client() -> Client:
        """Create and return a Supabase client"""
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    
    @property
    def client(self) -> Client:
        """Get the Supabase client"""
        return self._client
    
    def upload_image(self, file_path: str, bucket_name: Optional[str] = None) -> Dict[str, Any]:
        """Upload an image to Supabase Storage
        
        Args:
            file_path: Path to the image file
            bucket_name: Storage bucket name (default: STORAGE_BUCKET)
            
        Returns:
            Dict with file_name and file_url
        """
        bucket = bucket_name or STORAGE_BUCKET
        
        # Generate a unique file name
        file_name = f"{uuid.uuid4()}_{os.path.basename(file_path)}"
        
        # Upload the file
        with open(file_path, "rb") as f:
            self._client.storage.from_(bucket).upload(file_name, f)
        
        # Get the public URL
        file_url = self._client.storage.from_(bucket).get_public_url(file_name)
        
        return {
            "file_name": file_name,
            "file_url": file_url
        }
    
    def save_detection(self, 
                      image_url: str, 
                      pest_name: str, 
                      confidence: float, 
                      crop_name: Optional[str] = None,
                      diagnosis: Optional[str] = None,
                      heatmap_url: Optional[str] = None) -> Dict[str, Any]:
        """Save detection results to Supabase Database
        
        Args:
            image_url: URL of the uploaded image
            pest_name: Detected pest/disease name
            confidence: Confidence score (0-100)
            crop_name: Name of the crop (optional)
            diagnosis: LLM-generated diagnosis (optional)
            heatmap_url: URL of the heatmap image (optional)
            
        Returns:
            The created detection record
        """
        # Create detection record
        detection_data = {
            "image_url": image_url,
            "pest_name": pest_name,
            "confidence": confidence,
            "created_at": datetime.now().isoformat()
        }
        
        # Add optional fields if provided
        if crop_name:
            detection_data["crop_name"] = crop_name
        
        if diagnosis:
            detection_data["diagnosis"] = diagnosis
        
        if heatmap_url:
            detection_data["heatmap_url"] = heatmap_url
        
        # Insert into database
        result = self._client.table("detections").insert(detection_data).execute()
        
        # Return the created record
        return result.data[0] if result.data else {}
    
    def get_detections(self, limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """Get recent detections from the database
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of detection records
        """
        result = self._client.table("detections") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .offset(offset) \
            .execute()
        
        return result.data if result.data else []
    
    def get_detection_by_id(self, detection_id: str) -> Optional[Dict[str, Any]]:
        """Get a detection by ID
        
        Args:
            detection_id: UUID of the detection
            
        Returns:
            Detection record or None if not found
        """
        result = self._client.table("detections") \
            .select("*") \
            .eq("id", detection_id) \
            .execute()
        
        return result.data[0] if result.data else None
    
    def get_detections_by_crop(self, crop_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get detections by crop name
        
        Args:
            crop_name: Name of the crop
            limit: Maximum number of records to return
            
        Returns:
            List of detection records
        """
        result = self._client.table("detections") \
            .select("*") \
            .ilike("crop_name", f"%{crop_name}%") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return result.data if result.data else []
    
    def get_detections_by_pest(self, pest_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get detections by pest/disease name
        
        Args:
            pest_name: Name of the pest/disease
            limit: Maximum number of records to return
            
        Returns:
            List of detection records
        """
        result = self._client.table("detections") \
            .select("*") \
            .ilike("pest_name", f"%{pest_name}%") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return result.data if result.data else []

# Create a singleton instance
supabase_client = SupabaseClient()

def get_supabase_client() -> SupabaseClient:
    """Get the singleton Supabase client instance"""
    return supabase_client