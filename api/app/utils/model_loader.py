import os
import onnxruntime as ort
import torch
import torch.nn as nn
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import config here to avoid circular imports
from ..config import get_model_paths

# Multi-head crop disease model architecture
class MultiHeadCropDiseaseModel(nn.Module):
    def __init__(self, crop_id_to_num_classes, weights="DEFAULT"):
        super().__init__()
        # Load MobileNet backbone
        if hasattr(torch.hub, "load_state_dict_from_url"):
            # Use torchvision models
            import torchvision.models as models
            if hasattr(models, "MobileNet_V3_Small_Weights"):
                weight_enum = getattr(models.MobileNet_V3_Small_Weights, weights)
                mobilenet = models.mobilenet_v3_small(weights=weight_enum)
            else:
                mobilenet = models.mobilenet_v3_small(pretrained=True)
        else:
            # Fallback for older torchvision
            import torchvision.models as models
            mobilenet = models.mobilenet_v3_small(pretrained=True)

        self.backbone = mobilenet.features
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # Per-crop classification heads
        self.heads = nn.ModuleDict({
            str(crop_id): nn.Linear(576, num_classes)
            for crop_id, num_classes in crop_id_to_num_classes.items()
        })

    def forward_features(self, x):
        """Extract backbone features"""
        x = self.backbone(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        return x

    def forward_head(self, feats, crop_id: int):
        """Run features through the correct crop-specific head"""
        return self.heads[str(int(crop_id))](feats)

    def forward(self, images, crop_ids):
        feats = self.forward_features(images)
        outputs = []
        for i, cid in enumerate(crop_ids):
            outputs.append(self.forward_head(feats[i].unsqueeze(0), cid))
        return torch.cat(outputs, dim=0)

# Get the resolved model path
MODEL_PATH = None

def get_model_path():
    """Get the correct path to the model file"""
    global MODEL_PATH
    
    if MODEL_PATH is None:
        # Use centralized config paths
        possible_paths = get_model_paths()
        
        for path in possible_paths:
            if path and os.path.exists(path):
                print(f"✅ Found model at: {path}")
                MODEL_PATH = path
                return MODEL_PATH
        
        # If no path found, show available paths for debugging
        print(f"❌ Model file not found. Searched in:")
        for path in possible_paths:
            if path:
                print(f"   - {path} (exists: {os.path.exists(path)})")
        
        raise FileNotFoundError("Model file not found in any expected location")
    
    return MODEL_PATH

# Singleton pattern for model session
_model_session = None


def get_model_session() -> ort.InferenceSession:
    """Get or create the ONNX model inference session
    
    Uses a singleton pattern to avoid loading the model multiple times.
    
    Returns:
        ONNX InferenceSession object
    """
    global _model_session
    
    if _model_session is None:
        try:
            # Check if model file exists
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            
            # Set execution providers - use CUDA if available, otherwise CPU
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            
            # Create session
            _model_session = ort.InferenceSession(MODEL_PATH, providers=providers)
            
            print(f"Model loaded successfully from {MODEL_PATH}")
            print(f"Using providers: {_model_session.get_providers()}")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    
    return _model_session


def get_model_metadata() -> Dict[str, Any]:
    """Get metadata about the loaded model
    
    Returns:
        Dictionary containing model metadata
    """
    session = get_model_session()
    
    # Get input details
    inputs = session.get_inputs()
    input_details = []
    for input in inputs:
        input_details.append({
            "name": input.name,
            "shape": input.shape,
            "type": input.type
        })
    
    # Get output details
    outputs = session.get_outputs()
    output_details = []
    for output in outputs:
        output_details.append({
            "name": output.name,
            "shape": output.shape,
            "type": output.type
        })
    
    return {
        "model_path": MODEL_PATH,
        "providers": session.get_providers(),
        "inputs": input_details,
        "outputs": output_details
    }