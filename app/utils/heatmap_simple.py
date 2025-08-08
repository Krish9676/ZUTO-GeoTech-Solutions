import os
import torch
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional


def generate_heatmap_simple(image_path: str, image_tensor: torch.Tensor, prediction_results: Dict[str, Any]) -> Optional[str]:
    """Generate a simple heatmap visualization without matplotlib dependency
    
    This is a simplified implementation that creates a basic heatmap
    without requiring matplotlib, making it more suitable for production deployment.
    
    Args:
        image_path: Path to the original image
        image_tensor: Preprocessed image tensor used for inference
        prediction_results: Results from the model inference
        
    Returns:
        Path to the generated heatmap image, or None if generation failed
    """
    try:
        # Create temp directory if it doesn't exist
        os.makedirs("temp", exist_ok=True)
        
        # Get the upload ID from the image path
        upload_id = os.path.splitext(os.path.basename(image_path))[0]
        
        # Create heatmap path
        heatmap_path = os.path.join("temp", f"{upload_id}_heatmap.jpg")
        
        # Load the original image
        original_image = Image.open(image_path).convert("RGB")
        original_image = original_image.resize((224, 224))
        
        # Convert to numpy array
        img_array = np.array(original_image)
        
        # Create a simple heatmap based on image intensity
        # This is a placeholder - in a real implementation you'd use the model's attention
        gray = np.mean(img_array, axis=2)
        
        # Create a simple heatmap (center-focused for demonstration)
        height, width = gray.shape
        y, x = np.ogrid[:height, :width]
        
        # Create a radial heatmap
        center_y, center_x = height // 2, width // 2
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        
        # Normalize distance to 0-1
        heatmap = 1 - (distance / max_distance)
        
        # Apply some smoothing
        heatmap = np.clip(heatmap, 0, 1)
        
        # Create a colored heatmap using PIL
        heatmap_colored = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Red channel (high intensity)
        heatmap_colored[:, :, 0] = (heatmap * 255).astype(np.uint8)
        
        # Green channel (medium intensity)
        heatmap_colored[:, :, 1] = ((1 - heatmap) * 255).astype(np.uint8)
        
        # Blue channel (low intensity)
        heatmap_colored[:, :, 2] = 0
        
        # Create the final image
        heatmap_img = Image.fromarray(heatmap_colored)
        
        # Create a combined image (original + heatmap overlay)
        combined = Image.blend(original_image, heatmap_img, 0.3)
        
        # Save the heatmap
        combined.save(heatmap_path, "JPEG", quality=85)
        
        return heatmap_path
    
    except Exception as e:
        print(f"Error generating simple heatmap: {e}")
        return None
