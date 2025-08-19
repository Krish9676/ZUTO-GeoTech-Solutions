#!/usr/bin/env python3
"""
Startup script for the Crop Disease Detection API
This script validates configuration and initializes the API
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def validate_startup():
    """Validate that the API can start properly"""
    print("🔍 Validating API startup...")
    
    try:
        # Import and validate configuration
        from app.config import validate_config, get_model_paths, get_class_map_paths
        
        # Check configuration
        config_errors = validate_config()
        if config_errors:
            print("❌ Configuration errors found:")
            for error in config_errors:
                print(f"   - {error}")
            return False
        
        # Check model files
        model_paths = get_model_paths()
        model_found = False
        for path in model_paths:
            if os.path.exists(path):
                print(f"✅ Model found at: {path}")
                model_found = True
                break
        
        if not model_found:
            print("❌ Model file not found in any expected location")
            print("Searched in:")
            for path in model_paths:
                print(f"   - {path} (exists: {os.path.exists(path)})")
            return False
        
        # Check class map
        class_map_paths = get_class_map_paths()
        class_map_found = False
        for path in class_map_paths:
            if os.path.exists(path):
                print(f"✅ Class map found at: {path}")
                class_map_found = True
                break
        
        if not class_map_found:
            print("❌ Class map file not found")
            return False
        
        # Check temp directory
        from app.config import get_temp_dir
        temp_dir = get_temp_dir()
        os.makedirs(temp_dir, exist_ok=True)
        print(f"✅ Temp directory ready: {temp_dir}")
        
        print("✅ All startup validations passed!")
        return True
        
    except Exception as e:
        print(f"❌ Startup validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main startup function"""
    print("🚀 Starting Crop Disease Detection API...")
    
    # Validate startup
    if not validate_startup():
        print("❌ Startup validation failed. Exiting.")
        sys.exit(1)
    
    # Import and start the API
    try:
        from app.main import app
        import uvicorn
        
        host = os.getenv('API_HOST', '0.0.0.0')
        port = os.getenv('API_PORT', '8000')
        print(f"📍 Server will run on: {host}:{port}")
        
        # Show accessible URLs
        if host == "0.0.0.0":
            print("🌐 API accessible at:")
            print(f"   - http://localhost:{port}")
            print(f"   - http://127.0.0.1:{port}")
            print(f"   - http://[your-local-ip]:{port}")
        else:
            print(f"🌐 API accessible at: http://{host}:{port}")
        
        print(f"🔧 API Documentation: http://localhost:{port}/docs")
        
        # Use import string for uvicorn to enable reload
        uvicorn.run(
            "app.main:app",
            host=os.getenv("API_HOST", "0.0.0.0"),
            port=int(os.getenv("API_PORT", "8000")),
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Failed to start API: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
