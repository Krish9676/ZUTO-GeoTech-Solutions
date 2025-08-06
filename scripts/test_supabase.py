#!/usr/bin/env python3

import os
import sys
import argparse
import json
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
STORAGE_BUCKET = os.getenv("SUPABASE_STORAGE_BUCKET", "crop-images")
HEATMAP_BUCKET = os.getenv("SUPABASE_HEATMAP_BUCKET", "heatmaps")

def create_supabase_client() -> Client:
    """Create and return a Supabase client"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file", file=sys.stderr)
        sys.exit(1)
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def test_connection(client: Client):
    """Test connection to Supabase"""
    try:
        # Try to get the current user to test authentication
        response = client.auth.get_user()
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)

def test_storage(client: Client, bucket_name: str, test_file_path: str = None):
    """Test Supabase Storage"""
    try:
        # Check if bucket exists
        buckets = client.storage.list_buckets()
        bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
        
        if not bucket_exists:
            return False, f"Bucket '{bucket_name}' does not exist"
        
        # If a test file is provided, upload it
        if test_file_path:
            if not os.path.exists(test_file_path):
                return False, f"Test file '{test_file_path}' does not exist"
            
            # Generate a unique file name
            file_name = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(test_file_path)}"
            
            # Upload the file
            with open(test_file_path, "rb") as f:
                result = client.storage.from_(bucket_name).upload(file_name, f)
            
            # Get the public URL
            file_url = client.storage.from_(bucket_name).get_public_url(file_name)
            
            return True, {
                "message": f"File uploaded successfully to bucket '{bucket_name}'",
                "file_name": file_name,
                "file_url": file_url
            }
        
        return True, f"Bucket '{bucket_name}' exists"
    except Exception as e:
        return False, str(e)

def test_database(client: Client):
    """Test Supabase Database"""
    try:
        # Check if detections table exists by trying to select from it
        result = client.table("detections").select("id").limit(1).execute()
        
        # Try to insert a test record
        test_data = {
            "image_url": "https://example.com/test.jpg",
            "pest_name": "Test Pest",
            "confidence": 99.9,
            "crop_name": "Test Crop",
            "diagnosis": "This is a test diagnosis"
        }
        
        insert_result = client.table("detections").insert(test_data).execute()
        
        # Get the inserted record ID
        record_id = insert_result.data[0]["id"]
        
        # Delete the test record
        client.table("detections").delete().eq("id", record_id).execute()
        
        return True, {
            "message": "Database test successful",
            "table": "detections",
            "record_id": record_id
        }
    except Exception as e:
        return False, str(e)

def main():
    parser = argparse.ArgumentParser(description='Test Supabase integration')
    parser.add_argument('--test-storage', action='store_true',
                        help='Test Supabase Storage')
    parser.add_argument('--test-database', action='store_true',
                        help='Test Supabase Database')
    parser.add_argument('--upload-file', type=str, default=None,
                        help='Path to a file to upload to Supabase Storage')
    parser.add_argument('--bucket', type=str, default=STORAGE_BUCKET,
                        help=f'Storage bucket name (default: {STORAGE_BUCKET})')
    
    args = parser.parse_args()
    
    # Create Supabase client
    print(f"Connecting to Supabase at {SUPABASE_URL}...")
    client = create_supabase_client()
    
    # Test connection
    success, result = test_connection(client)
    if not success:
        print(f"Error connecting to Supabase: {result}", file=sys.stderr)
        sys.exit(1)
    
    print("Connection successful!")
    
    # Test storage
    if args.test_storage or args.upload_file:
        print(f"\nTesting Supabase Storage (bucket: {args.bucket})...")
        success, result = test_storage(client, args.bucket, args.upload_file)
        
        if not success:
            print(f"Storage test failed: {result}", file=sys.stderr)
        else:
            if isinstance(result, dict):
                print(f"Storage test successful: {result['message']}")
                print(f"File name: {result['file_name']}")
                print(f"File URL: {result['file_url']}")
            else:
                print(f"Storage test successful: {result}")
    
    # Test database
    if args.test_database:
        print("\nTesting Supabase Database...")
        success, result = test_database(client)
        
        if not success:
            print(f"Database test failed: {result}", file=sys.stderr)
        else:
            print(f"Database test successful: {result['message']}")
            print(f"Table: {result['table']}")
            print(f"Test record ID: {result['record_id']}")
    
    # If no specific tests were requested, run all tests
    if not (args.test_storage or args.upload_file or args.test_database):
        # Test storage
        print(f"\nTesting Supabase Storage (bucket: {args.bucket})...")
        success, result = test_storage(client, args.bucket)
        
        if not success:
            print(f"Storage test failed: {result}", file=sys.stderr)
        else:
            print(f"Storage test successful: {result}")
        
        # Test database
        print("\nTesting Supabase Database...")
        success, result = test_database(client)
        
        if not success:
            print(f"Database test failed: {result}", file=sys.stderr)
        else:
            print(f"Database test successful: {result['message']}")
            print(f"Table: {result['table']}")
            print(f"Test record ID: {result['record_id']}")

if __name__ == '__main__':
    main()