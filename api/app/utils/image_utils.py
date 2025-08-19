import os
import torch
import numpy as np
from PIL import Image
from torchvision import transforms
from fastapi import UploadFile
from typing import Tuple

# Define image preprocessing transformations - updated to match training (160x160)
preprocess_transforms = transforms.Compose([
    transforms.Resize((160, 160)),  # Changed from 256 to 160x160
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


async def save_image_locally(file: UploadFile, upload_id: str) -> str:
    """Save uploaded image to a temporary local file
    
    Args:
        file: Uploaded file object
        upload_id: Unique ID for the upload
        
    Returns:
        Path to the saved image
    """
    # Import config here to avoid circular imports
    from ..config import get_temp_dir
    
    # Create temp directory if it doesn't exist
    temp_dir = get_temp_dir()
    os.makedirs(temp_dir, exist_ok=True)
    
    # Determine file extension
    content_type = file.content_type
    extension = "jpg"  # Default extension
    
    if content_type:
        if "jpeg" in content_type or "jpg" in content_type:
            extension = "jpg"
        elif "png" in content_type:
            extension = "png"
    
    # Create file path
    file_path = os.path.join(temp_dir, f"{upload_id}.{extension}")
    
    # Save the file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return file_path


def preprocess_image(image_path: str) -> torch.Tensor:
    """Preprocess image for model inference
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Preprocessed image tensor
    """
    # Open image
    image = Image.open(image_path).convert("RGB")
    
    # Apply preprocessing transformations
    image_tensor = preprocess_transforms(image)
    
    return image_tensor


def resize_image(image_path: str, target_size: Tuple[int, int] = (224, 224)) -> Image.Image:
    """Resize image to target size
    
    Args:
        image_path: Path to the image file
        target_size: Target size (width, height)
        
    Returns:
        Resized PIL Image
    """
    image = Image.open(image_path).convert("RGB")
    resized_image = image.resize(target_size, Image.LANCZOS)
    return resized_image


def tensor_to_image(tensor: torch.Tensor) -> Image.Image:
    """Convert tensor to PIL Image
    
    Args:
        tensor: Image tensor
        
    Returns:
        PIL Image
    """
    # Denormalize
    mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
    std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
    tensor = tensor * std + mean
    
    # Convert to PIL Image
    tensor = tensor.clamp(0, 1) * 255
    tensor = tensor.permute(1, 2, 0).numpy().astype(np.uint8)
    image = Image.fromarray(tensor)
    
    return image