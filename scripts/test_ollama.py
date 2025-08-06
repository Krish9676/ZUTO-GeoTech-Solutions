#!/usr/bin/env python3

import os
import sys
import argparse
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def test_ollama_connection():
    """Test connection to Ollama server"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.RequestException as e:
        return False, str(e)

def list_available_models():
    """List available models in Ollama"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        response.raise_for_status()
        return response.json().get("models", [])
    except requests.exceptions.RequestException as e:
        print(f"Error listing models: {e}", file=sys.stderr)
        return []

def test_prompt(prompt, model=None, stream=False):
    """Test a prompt with Ollama"""
    model = model or OLLAMA_MODEL
    
    try:
        if stream:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True
                },
                stream=True
            )
            response.raise_for_status()
            
            # Process streaming response
            print("\nResponse:")
            for line in response.iter_lines():
                if line:
                    import json
                    chunk = json.loads(line)
                    if "response" in chunk:
                        print(chunk["response"], end="")
                        sys.stdout.flush()
            print("\n")
            return True, None
        else:
            start_time = time.time()
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            end_time = time.time()
            
            result = response.json()
            return True, {
                "response": result.get("response", ""),
                "time_taken": end_time - start_time
            }
    except requests.exceptions.RequestException as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description='Test Ollama LLM integration')
    parser.add_argument('--prompt', default=None,
                        help='Prompt to test')
    parser.add_argument('--model', default=None,
                        help=f'Model to use (default: {OLLAMA_MODEL})')
    parser.add_argument('--stream', action='store_true',
                        help='Use streaming mode')
    parser.add_argument('--list-models', action='store_true',
                        help='List available models')
    
    args = parser.parse_args()
    
    # Test connection
    print(f"Testing connection to Ollama server at {OLLAMA_BASE_URL}...")
    success, result = test_ollama_connection()
    
    if not success:
        print(f"Error connecting to Ollama server: {result}", file=sys.stderr)
        print("\nMake sure Ollama is running. You can start it with:")
        print("  ollama serve")
        sys.exit(1)
    
    print("Connection successful!")
    
    # List models
    if args.list_models:
        print("\nAvailable models:")
        models = list_available_models()
        if not models:
            print("No models found or error listing models.")
        else:
            for model in models:
                print(f"- {model['name']}")
        sys.exit(0)
    
    # Test prompt
    if args.prompt:
        model = args.model or OLLAMA_MODEL
        print(f"\nTesting prompt with model '{model}'...")
        print(f"Prompt: {args.prompt}")
        
        success, result = test_prompt(args.prompt, model, args.stream)
        
        if not success:
            print(f"Error: {result}", file=sys.stderr)
            sys.exit(1)
        
        if not args.stream:
            print(f"\nResponse: {result['response']}")
            print(f"Time taken: {result['time_taken']:.2f} seconds")
    else:
        # Use a default crop disease prompt
        model = args.model or OLLAMA_MODEL
        default_prompt = f"""A farmer uploaded an image of a maize crop. Our AI model detected 'Fall Armyworm' with 92.5% confidence.

Please provide a detailed response with the following information:
1. What is Fall Armyworm and how does it affect maize crops?
2. What are the typical symptoms that can be observed?
3. What are the recommended treatments or management practices?
4. What preventive measures can farmers take to avoid this issue in the future?

Keep your response concise but informative, focusing on practical advice for farmers."""
        
        print(f"\nTesting default crop disease prompt with model '{model}'...")
        print(f"Prompt: {default_prompt}")
        
        success, result = test_prompt(default_prompt, model, args.stream)
        
        if not success:
            print(f"Error: {result}", file=sys.stderr)
            sys.exit(1)
        
        if not args.stream:
            print(f"\nResponse: {result['response']}")
            print(f"Time taken: {result['time_taken']:.2f} seconds")

if __name__ == '__main__':
    main()