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
    if not os.path.exists(model_path):
        print(f"\nWARNING: Model file not found at {model_path}")
        print("You can download a model using the scripts/download_model.py script:")
        print("  python scripts/download_model.py --model mobilenet")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\nWARNING: .env file not found")
        print("You should create a .env file based on .env.example")
    
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