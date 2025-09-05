#!/usr/bin/env python3
"""
Convert the trained multi-head crop disease model from PyTorch (.pth) to ONNX format.

This script loads the trained model checkpoint and converts it to ONNX format
for deployment in the API.
"""

import os
import sys
import torch
import torch.nn as nn
import torch.onnx
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Import the model architecture
from api.app.utils.model_loader import MultiHeadCropDiseaseModel

# Create a simplified model for ONNX export
class ONNXMultiHeadCropDiseaseModel(nn.Module):
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

    def forward(self, image):
        """Simplified forward pass for ONNX export - only image input"""
        # Extract features
        x = self.backbone(image)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        
        # For ONNX export, we'll use a simple approach
        # Since ONNX doesn't handle dynamic string lookups well,
        # we'll create a single output that can be post-processed
        # by concatenating all possible outputs
        
        # Get all possible outputs
        all_outputs = []
        for crop_id_str in sorted(self.heads.keys()):
            all_outputs.append(self.heads[crop_id_str](x))
        
        # Concatenate all outputs
        combined_output = torch.cat(all_outputs, dim=1)
        
        return combined_output

def convert_model_to_onnx():
    """Convert the trained .pth model to ONNX format"""
    
    # Paths
    model_dir = project_root / "api" / "models"
    pth_path = model_dir / "cropaware_multicrop_model.pth"
    onnx_path = model_dir / "mobilenet.onnx"
    
    # Check if the .pth file exists
    if not pth_path.exists():
        print(f"❌ Model file not found: {pth_path}")
        return False
    
    print(f"📁 Loading model from: {pth_path}")
    
    try:
        # Load the checkpoint
        checkpoint = torch.load(pth_path, map_location='cpu', weights_only=False)
        
        # Extract the crop_to_global_classes mapping
        crop_to_global_classes = checkpoint["crop_to_global_classes"]
        print(f"📊 Found {len(crop_to_global_classes)} crops in the model")
        
        # Build the model architecture
        crop_id_to_num_local = {cid: len(glist) for cid, glist in crop_to_global_classes.items()}
        model = ONNXMultiHeadCropDiseaseModel(crop_id_to_num_local)
        
        # Load the state dict
        model.load_state_dict(checkpoint["model_state_dict"])
        model.eval()
        
        print("✅ Model loaded successfully")
        
        # Create dummy inputs for ONNX export
        # Image input: batch_size=1, channels=3, height=160, width=160
        dummy_image = torch.randn(1, 3, 160, 160)
        
        print("🔄 Converting to ONNX format...")
        
        # Export to ONNX
        torch.onnx.export(
            model,
            dummy_image,
            onnx_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['image'],
            output_names=['logits'],
            dynamic_axes={
                'image': {0: 'batch_size'},
                'logits': {0: 'batch_size'}
            }
        )
        
        print(f"✅ Model converted successfully to: {onnx_path}")
        
        # Verify the ONNX model
        try:
            import onnx
            onnx_model = onnx.load(str(onnx_path))
            onnx.checker.check_model(onnx_model)
            print("✅ ONNX model verification passed")
        except ImportError:
            print("⚠️ onnx package not available for verification")
        except Exception as e:
            print(f"❌ ONNX model verification failed: {e}")
            return False
        
        # Save the crop mapping for the API
        crop_mapping_path = model_dir / "crop_to_global_classes.json"
        import json
        import numpy as np
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            else:
                return obj
        
        crop_to_global_classes_serializable = convert_numpy_types(crop_to_global_classes)
        
        with open(crop_mapping_path, 'w') as f:
            json.dump(crop_to_global_classes_serializable, f, indent=2)
        print(f"✅ Saved crop mapping to: {crop_mapping_path}")
        
        # Save preprocessing config
        preprocess_config = {
            "img_size": checkpoint.get("img_size", 160),
            "normalize_mean": checkpoint.get("normalize_mean", [0.485, 0.456, 0.406]),
            "normalize_std": checkpoint.get("normalize_std", [0.229, 0.224, 0.225])
        }
        
        config_path = model_dir / "preprocess_config.json"
        with open(config_path, 'w') as f:
            json.dump(preprocess_config, f, indent=2)
        print(f"✅ Saved preprocessing config to: {config_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting model: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting model conversion...")
    success = convert_model_to_onnx()
    
    if success:
        print("🎉 Model conversion completed successfully!")
    else:
        print("💥 Model conversion failed!")
        sys.exit(1)
