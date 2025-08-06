#!/usr/bin/env python3

import os
import sys
import argparse
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

def create_bucket(client: Client, bucket_name: str, is_public: bool = True):
    """Create a storage bucket"""
    try:
        # Check if bucket already exists
        buckets = client.storage.list_buckets()
        bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
        
        if bucket_exists:
            print(f"Bucket '{bucket_name}' already exists")
            return True
        
        # Create the bucket
        client.storage.create_bucket(bucket_name, options={"public": is_public})
        print(f"Created bucket '{bucket_name}' (public: {is_public})")
        return True
    except Exception as e:
        print(f"Error creating bucket '{bucket_name}': {e}", file=sys.stderr)
        return False

def setup_bucket_policy(client: Client, bucket_name: str):
    """Set up storage policies for a bucket"""
    try:
        # Note: This is a simplified version. In a real application, you would use
        # SQL to create RLS policies as shown in setup_database.sql
        print(f"Storage policies for bucket '{bucket_name}' should be set up in the Supabase dashboard or using SQL")
        print("Refer to scripts/setup_database.sql for example SQL policies")
        return True
    except Exception as e:
        print(f"Error setting up policies for bucket '{bucket_name}': {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Set up Supabase storage buckets')
    parser.add_argument('--crop-bucket', type=str, default=STORAGE_BUCKET,
                        help=f'Crop images bucket name (default: {STORAGE_BUCKET})')
    parser.add_argument('--heatmap-bucket', type=str, default=HEATMAP_BUCKET,
                        help=f'Heatmap images bucket name (default: {HEATMAP_BUCKET})')
    parser.add_argument('--private', action='store_true',
                        help='Create private buckets instead of public')
    
    args = parser.parse_args()
    
    # Create Supabase client
    print(f"Connecting to Supabase at {SUPABASE_URL}...")
    client = create_supabase_client()
    
    # Set bucket visibility
    is_public = not args.private
    
    # Create crop images bucket
    print(f"\nSetting up crop images bucket '{args.crop_bucket}'...")
    if not create_bucket(client, args.crop_bucket, is_public):
        sys.exit(1)
    
    # Create heatmap images bucket
    print(f"\nSetting up heatmap images bucket '{args.heatmap_bucket}'...")
    if not create_bucket(client, args.heatmap_bucket, is_public):
        sys.exit(1)
    
    # Set up bucket policies
    print("\nSetting up storage policies...")
    setup_bucket_policy(client, args.crop_bucket)
    setup_bucket_policy(client, args.heatmap_bucket)
    
    print("\n✅ Storage buckets set up successfully!")
    print("\nNext steps:")
    print("1. Set up database schema using scripts/setup_database.sql")
    print("2. Configure RLS policies in the Supabase dashboard")
    print("3. Test the storage with scripts/test_supabase.py")

if __name__ == '__main__':
    main()