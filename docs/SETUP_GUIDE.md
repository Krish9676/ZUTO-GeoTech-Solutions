# Crop Disease Detection System - Setup Guide

This guide will walk you through setting up and running the Crop Disease Detection System. Follow these steps to get the system up and running.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) with LLaMA-3 model
- [Supabase](https://supabase.com/) account
- Flutter SDK (for mobile app)
- Git

## Step 1: Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd PD_application
```

## Step 2: Set Up Python Environment

### Create a Virtual Environment

```bash
python -m venv venv
```

### Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 3: Initialize Project Structure

If you're starting from scratch, you can use the initialization script to create the project structure:

```bash
python scripts/init_project.py
```

## Step 4: Set Up Environment Variables

1. Copy the example environment file:

```bash
copy .env.example .env
```

2. Edit the `.env` file with your Supabase credentials, Ollama configuration, and other settings.

## Step 5: Download ONNX Model

Download a pre-trained ONNX model for crop disease detection:

```bash
python scripts/download_model.py --model mobilenet
```

This will download a MobileNet model trained for crop disease detection and save it to the `models` directory.

## Step 6: Generate Class Labels

Generate class labels for the model:

```bash
python scripts/generate_labels.py --crop maize --output models/labels.json
```

You can replace `maize` with another crop type if needed.

## Step 7: Set Up Supabase

### Create Supabase Project

1. Sign up or log in to [Supabase](https://supabase.com/)
2. Create a new project
3. Get your project URL and anon key from the project settings
4. Update the `.env` file with these credentials

### Set Up Database Schema

Run the database setup SQL script in the Supabase SQL Editor:

1. Go to your Supabase project dashboard
2. Navigate to the SQL Editor
3. Copy the contents of `scripts/setup_database.sql`
4. Paste and run the SQL in the editor

Alternatively, you can use the Supabase CLI if you have it installed.

### Set Up Storage Buckets

Run the storage setup script:

```bash
python scripts/setup_storage.py
```

## Step 8: Test Components

### Test Ollama Integration

Make sure Ollama is running with the LLaMA-3 model:

```bash
# Start Ollama (in a separate terminal)
ollama serve

# In another terminal, pull the LLaMA-3 model
ollama pull llama3

# Test the integration
python scripts/test_ollama.py
```

### Test Supabase Integration

```bash
python scripts/test_supabase.py
```

### Test ONNX Model

```bash
python scripts/test_model.py --image <path-to-test-image>
```

## Step 9: Run the API

Start the FastAPI application:

```bash
python run.py
```

By default, the API will run on `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Step 10: Set Up the Mobile App

### Navigate to the Mobile App Directory

```bash
cd mobile_app
```

### Install Flutter Dependencies

```bash
flutter pub get
```

### Update API Endpoint

Edit the `mobile_app/lib/services/api_service.dart` file to point to your API endpoint.

### Run the Mobile App

```bash
flutter run
```

## Step 11: Docker Deployment (Optional)

If you want to deploy the API using Docker:

```bash
# Build the Docker image
docker build -t crop-disease-detection .

# Run the Docker container
docker run -p 8000:8000 --env-file .env crop-disease-detection
```

## Troubleshooting

### Common Issues

1. **ONNX Model Not Found**
   - Make sure you've downloaded the model using the `download_model.py` script
   - Check that the `MODEL_PATH` in your `.env` file points to the correct location

2. **Ollama Connection Issues**
   - Ensure Ollama is running (`ollama serve`)
   - Verify that you've pulled the LLaMA-3 model (`ollama pull llama3`)
   - Check the `OLLAMA_BASE_URL` and `OLLAMA_MODEL` in your `.env` file

3. **Supabase Connection Issues**
   - Verify your Supabase URL and key in the `.env` file
   - Check that you've set up the database schema and storage buckets
   - Ensure your Supabase project is active

4. **API Not Starting**
   - Check for error messages in the console
   - Verify that all dependencies are installed
   - Make sure no other service is using port 8000

5. **Mobile App Issues**
   - Ensure Flutter is properly installed
   - Check that you've updated the API endpoint in the mobile app
   - Run `flutter doctor` to diagnose Flutter installation issues

## Next Steps

- Customize the model for your specific crops and diseases
- Enhance the mobile app with additional features
- Set up continuous integration and deployment using GitHub Actions
- Deploy the API to a cloud provider like Render, Heroku, or AWS

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository or contact the project maintainers.