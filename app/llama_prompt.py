import os
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def llama_prompt(image_url: str, pest_name: str, confidence: float, crop_name: Optional[str] = None) -> str:
    """Generate a diagnosis using LLaMA model via Ollama
    
    Args:
        image_url: URL of the uploaded image
        pest_name: Detected pest/disease name
        confidence: Confidence score of the detection (0-100)
        crop_name: Optional name of the crop
        
    Returns:
        Diagnosis text from LLaMA
    """
    try:
        # Create the prompt
        crop_info = f"{crop_name} crop" if crop_name else "crop"
        
        prompt = f"""
        A farmer uploaded an image of a {crop_info}. Our AI model detected '{pest_name}' with {confidence:.1f}% confidence.
        Image URL: {image_url}

        Please provide a detailed response with the following information:
        1. What is {pest_name} and how does it affect {crop_info}?
        2. What are the typical symptoms that can be observed?
        3. What are the recommended treatments or management practices?
        4. What preventive measures can farmers take to avoid this issue in the future?
        
        Keep your response concise but informative, focusing on practical advice for farmers.
        """
        
        # Call Ollama API
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        # Return the diagnosis
        return result.get("response", "")
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")
        # Fallback response if Ollama is not available
        return f"Detected {pest_name} with {confidence:.1f}% confidence. Unable to generate detailed diagnosis at this time."
    
    except Exception as e:
        print(f"Error generating diagnosis: {e}")
        return f"Detected {pest_name} with {confidence:.1f}% confidence. Unable to generate detailed diagnosis at this time."