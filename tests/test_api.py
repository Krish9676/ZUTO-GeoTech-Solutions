import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

# Create test client
client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch('app.api.run_inference')
@patch('app.api.llama_prompt')
@patch('app.api.generate_heatmap')
@patch('app.api.save_image_locally')
@patch('app.api.supabase_client')
def test_upload_endpoint(mock_supabase, mock_save_image, mock_generate_heatmap, 
                        mock_llama_prompt, mock_run_inference):
    """Test the upload endpoint with mocked dependencies"""
    # Configure mocks
    mock_save_image.return_value = "test_image.jpg"
    mock_generate_heatmap.return_value = "test_heatmap.jpg"
    mock_run_inference.return_value = {
        "label": "Fall Armyworm",
        "confidence": 95.5,
        "class_index": 1,
        "raw_scores": [0.01, 0.955, 0.02, 0.01, 0.005]
    }
    mock_llama_prompt.return_value = "This is a test diagnosis."
    
    # Mock Supabase storage and database operations
    storage_mock = MagicMock()
    storage_mock.from_.return_value.upload.return_value = None
    storage_mock.from_.return_value.get_public_url.return_value = "https://example.com/test.jpg"
    mock_supabase.storage = storage_mock
    
    table_mock = MagicMock()
    table_mock.insert.return_value.execute.return_value = None
    mock_supabase.table.return_value = table_mock
    
    # Create a test image file
    with open("test_image.jpg", "wb") as f:
        f.write(b"test image content")
    
    # Test the endpoint
    with open("test_image.jpg", "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("test.jpg", f, "image/jpeg")},
            data={"crop_name": "Maize"}
        )
    
    # Clean up test file
    if os.path.exists("test_image.jpg"):
        os.remove("test_image.jpg")
    
    # Check response
    assert response.status_code == 200
    assert response.json()["prediction"] == "Fall Armyworm"
    assert response.json()["confidence"] == 95.5
    assert response.json()["diagnosis"] == "This is a test diagnosis."
    assert "image_url" in response.json()
    assert "heatmap_url" in response.json()