#!/usr/bin/env python3

import os
import argparse
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the Crop Disease Detection API')
    parser.add_argument('--host', default=os.getenv('API_HOST', '0.0.0.0'),
                        help='Host to run the API on')
    parser.add_argument('--port', type=int, default=int(os.getenv('API_PORT', 8000)),
                        help='Port to run the API on')
    parser.add_argument('--reload', action='store_true',
                        help='Enable auto-reload for development')
    parser.add_argument('--workers', type=int, default=1,
                        help='Number of worker processes')
    parser.add_argument('--log-level', default='info',
                        choices=['critical', 'error', 'warning', 'info', 'debug', 'trace'],
                        help='Log level')
    
    args = parser.parse_args()
    
    # Print startup message
    print(f"Starting Crop Disease Detection API on {args.host}:{args.port}")
    print(f"Log level: {args.log_level}")
    print(f"Auto-reload: {'enabled' if args.reload else 'disabled'}")
    print(f"Workers: {args.workers}")
    
    # Check if model file exists
    model_path = os.getenv('MODEL_PATH', os.path.join('models', 'mobilenet.onnx'))
    
    # Try multiple possible locations
    possible_model_paths = [
        model_path,
        os.path.join(os.path.dirname(__file__), 'models', 'mobilenet.onnx'),
        os.path.join(os.getcwd(), 'models', 'mobilenet.onnx')
    ]
    
    model_found = False
    for path in possible_model_paths:
        if os.path.exists(path):
            model_found = True
            print(f"✅ Model found at: {path}")
            break
    
    if not model_found:
        print(f"\nWARNING: Model file not found in any expected location")
        print("Searched in:")
        for path in possible_model_paths:
            print(f"  - {path} (exists: {os.path.exists(path)})")
        print("You can download a model using the scripts/download_model.py script:")
        print("  python scripts/download_model.py --model mobilenet")
    
    # Check if .env file exists
    env_files = ['.env', 'env.example']
    env_found = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            env_found = True
            print(f"✅ Environment file found: {env_file}")
            break
    
    if not env_found:
        print("\nWARNING: No environment file found")
        print("You should create a .env file based on env.example")
        print("Available environment files:")
        for env_file in env_files:
            print(f"  - {env_file} (exists: {os.path.exists(env_file)})")
    
    # Run the API
    uvicorn.run(
        "api.app.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level=args.log_level
    )

if __name__ == '__main__':
    main()