#!/bin/bash

# Start script for Crop Disease Detection API
echo "Starting Crop Disease Detection API..."

# Set default port if not provided
export PORT=${PORT:-8000}
echo "Using port: $PORT"

# Start the application
python run.py
