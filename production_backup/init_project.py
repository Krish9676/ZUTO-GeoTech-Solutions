#!/usr/bin/env python3

import os
import sys
import argparse
import shutil
from pathlib import Path

def create_directory(path):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {path}: {e}", file=sys.stderr)
        return False

def create_file(path, content=""):
    """Create file with content"""
    try:
        with open(path, "w") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error creating file {path}: {e}", file=sys.stderr)
        return False

def create_project_structure(base_dir, include_mobile=True):
    """Create project directory structure"""
    # Create base directories
    directories = [
        "app",
        "app/utils",
        "models",
        "scripts",
        "tests",
        ".github/workflows"
    ]
    
    if include_mobile:
        directories.extend([
            "mobile_app",
            "mobile_app/lib",
            "mobile_app/lib/models",
            "mobile_app/lib/screens",
            "mobile_app/lib/services",
            "mobile_app/lib/widgets",
            "mobile_app/assets",
            "mobile_app/assets/images"
        ])
    
    # Create directories
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        if not create_directory(dir_path):
            return False
    
    print("✅ Created project directories")
    return True

def create_empty_files(base_dir, include_mobile=True):
    """Create empty files for the project"""
    # Create empty files
    files = [
        "app/__init__.py",
        "app/utils/__init__.py",
        "tests/__init__.py"
    ]
    
    # Create files
    for file in files:
        file_path = os.path.join(base_dir, file)
        if not create_file(file_path):
            return False
    
    print("✅ Created empty Python package files")
    return True

def create_env_example(base_dir):
    """Create .env.example file"""
    content = """# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_STORAGE_BUCKET=crop-images
SUPABASE_HEATMAP_BUCKET=heatmaps

# Database Configuration
DB_HOST=db.your-project-id.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-database-password

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# ONNX Model Configuration
MODEL_PATH=models/mobilenet.onnx
MODEL_INPUT_SIZE=224

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Storage Configuration
UPLOAD_DIR=uploads
"""
    
    file_path = os.path.join(base_dir, ".env.example")
    if not create_file(file_path, content):
        return False
    
    print("✅ Created .env.example file")
    return True

def create_gitignore(base_dir):
    """Create .gitignore file"""
    content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# Environment Variables
.env

# IDE
.idea/
.vscode/
*.swp
*.swo

# Logs
logs/
*.log

# Temporary files
*.tmp

# ONNX models (large files)
models/*.onnx

# Uploaded images
uploads/

# Flutter/Dart
mobile_app/.dart_tool/
mobile_app/.flutter-plugins
mobile_app/.flutter-plugins-dependencies
mobile_app/.packages
mobile_app/build/
mobile_app/.pub-cache/
mobile_app/.pub/
mobile_app/coverage/

# Android
mobile_app/android/app/debug
mobile_app/android/app/profile
mobile_app/android/app/release
mobile_app/android/.gradle
mobile_app/android/captures/
mobile_app/android/local.properties
mobile_app/android/**/gradle-wrapper.jar
mobile_app/android/.gradle/
mobile_app/android/gradlew
mobile_app/android/gradlew.bat

# iOS
mobile_app/ios/Flutter/ephemeral
mobile_app/ios/Flutter/app.flx
mobile_app/ios/Flutter/app.zip
mobile_app/ios/Flutter/flutter_assets/
mobile_app/ios/Flutter/flutter_export_environment.sh
mobile_app/ios/ServiceDefinitions.json
mobile_app/ios/Runner/GeneratedPluginRegistrant.*
mobile_app/ios/.symlinks/
mobile_app/ios/Pods/

# macOS
mobile_app/macos/Flutter/ephemeral
mobile_app/macos/Flutter/GeneratedPluginRegistrant.*
mobile_app/macos/Pods/
"""
    
    file_path = os.path.join(base_dir, ".gitignore")
    if not create_file(file_path, content):
        return False
    
    print("✅ Created .gitignore file")
    return True

def create_requirements(base_dir):
    """Create requirements.txt file"""
    content = """fastapi==0.104.1
uvicorn==0.23.2
onnxruntime==1.16.0
torchvision==0.16.0
supabase==1.0.4
psycopg2-binary==2.9.9
python-multipart==0.0.6
Pillow==10.0.1
python-dotenv==1.0.0
numpy==1.24.3
requests==2.31.0
pydantic==2.4.2
"""
    
    file_path = os.path.join(base_dir, "requirements.txt")
    if not create_file(file_path, content):
        return False
    
    print("✅ Created requirements.txt file")
    return True

def create_readme(base_dir):
    """Create README.md file"""
    content = """# Crop Disease Detection System

A system that allows farmers to upload crop images via a mobile app and receive pest/disease diagnoses, using a combination of image classification models, LLMs for interpretability, and cloud storage.

## 🌟 Features

- Upload crop images via mobile app
- Detect pests and diseases using ONNX models
- Generate detailed diagnosis using LLaMA-3 via Ollama
- Store images and results in Supabase
- View detection history and results

## 🧱 System Components

| Component | Tech Stack | Purpose |
|-----------|------------|--------|
| API backend | FastAPI + ONNX + Ollama | Accept images, run detection & diagnosis |
| Model runtime | ResNet/MobileNet via ONNX | Fast local inference of pests/diseases |
| LLM Engine | LLaMA-3 (Ollama HTTP server) | Generate diagnosis explanation |
| Storage | Supabase Storage | Save uploaded image + heatmap |
| Database | PostgreSQL (via Supabase) | Store image URLs, results, confidence |
| Frontend | Flutter App | Let farmers upload images & see results |
| Deployment | Docker, GitHub Actions, Render | CI/CD + cloud hosting |

## 📋 Project Structure

```
project/
├── app/
│   ├── main.py
│   ├── api.py
│   ├── inference.py
│   ├── llama_prompt.py
│   └── utils/
│       ├── image_utils.py
│       ├── heatmap.py
│       └── model_loader.py
├── models/
│   └── mobilenet.onnx  # OR resnet.onnx
├── scripts/
│   ├── download_model.py
│   ├── test_model.py
│   ├── test_ollama.py
│   └── test_supabase.py
├── mobile_app/
│   └── ... (Flutter app)
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://github.com/ollama/ollama) with LLaMA-3 model
- [Supabase](https://supabase.com/) account
- Flutter SDK (for mobile app)

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/crop-disease-detection.git
cd crop-disease-detection
```

2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Download the ONNX model

```bash
python scripts/download_model.py --model mobilenet
```

4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

5. Run the API

```bash
python run.py
```

## 📱 Mobile App

See the [mobile_app/README.md](mobile_app/README.md) for instructions on setting up and running the Flutter mobile app.

## 🧪 Testing

```bash
# Test ONNX model inference
python scripts/test_model.py --image path/to/test/image.jpg

# Test Ollama integration
python scripts/test_ollama.py

# Test Supabase integration
python scripts/test_supabase.py
```

## 🐳 Docker

```bash
# Build Docker image
docker build -t crop-disease-detection .

# Run Docker container
docker run -p 8000:8000 --env-file .env crop-disease-detection
```

## 📄 API Endpoints

- `GET /` - Health check
- `POST /api/upload` - Upload image and get diagnosis

## 📊 Data Flow

```
[Mobile App] ── Upload image ──▶ [FastAPI API]
                                 │
                                 ├─▶ Save to Supabase
                                 ├─▶ Inference with MobileNet (ONNX)
                                 ├─▶ Heatmap generation
                                 ├─▶ Prompt LLaMA via Ollama for diagnosis
                                 └─▶ Save all info to PostgreSQL
                                 ↓
                            Return prediction + diagnosis to app
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
"""
    
    file_path = os.path.join(base_dir, "README.md")
    if not create_file(file_path, content):
        return False
    
    print("✅ Created README.md file")
    return True

def main():
    parser = argparse.ArgumentParser(description='Initialize project structure')
    parser.add_argument('--dir', type=str, default='.',
                        help='Base directory for the project')
    parser.add_argument('--no-mobile', action='store_true',
                        help='Skip creating mobile app structure')
    
    args = parser.parse_args()
    
    # Resolve base directory
    base_dir = os.path.abspath(args.dir)
    include_mobile = not args.no_mobile
    
    print(f"Initializing project structure in {base_dir}")
    print(f"Include mobile app: {include_mobile}")
    
    # Create project structure
    if not create_project_structure(base_dir, include_mobile):
        sys.exit(1)
    
    # Create empty files
    if not create_empty_files(base_dir, include_mobile):
        sys.exit(1)
    
    # Create .env.example
    if not create_env_example(base_dir):
        sys.exit(1)
    
    # Create .gitignore
    if not create_gitignore(base_dir):
        sys.exit(1)
    
    # Create requirements.txt
    if not create_requirements(base_dir):
        sys.exit(1)
    
    # Create README.md
    if not create_readme(base_dir):
        sys.exit(1)
    
    print("\n✅ Project structure initialized successfully!")
    print("\nNext steps:")
    print("1. Create a virtual environment: python -m venv venv")
    print("2. Activate the virtual environment:")
    print("   - Windows: venv\\Scripts\\activate")
    print("   - Unix/MacOS: source venv/bin/activate")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Download ONNX model: python scripts/download_model.py --model mobilenet")
    print("5. Create .env file from .env.example and update with your credentials")
    print("6. Run the API: python run.py")

if __name__ == '__main__':
    main()