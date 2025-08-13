#!/usr/bin/env python3
"""
Test script to verify Supabase connection and storage access
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import supabase
    
    print("🔍 Testing Supabase connection...")
    print(f"📁 Current working directory: {os.getcwd()}")
    
    # Check environment variables
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    storage_bucket = os.getenv("STORAGE_BUCKET") or os.getenv("SUPABASE_STORAGE_BUCKET", "crop-images")
    
    print(f"🔑 SUPABASE_URL: {'✅ Set' if supabase_url else '❌ Missing'}")
    print(f"🔑 SUPABASE_KEY: {'✅ Set' if supabase_key else '❌ Missing'}")
    print(f"🪣 STORAGE_BUCKET: {storage_bucket}")
    
    if not supabase_url or not supabase_key:
        print("❌ Missing required environment variables!")
        sys.exit(1)
    
    # Test Supabase connection
    print("\n🔌 Testing Supabase connection...")
    client = supabase.create_client(supabase_url, supabase_key)
    
    # Test database access
    print("📊 Testing database access...")
    try:
        response = client.table("detections").select("count", count="exact").execute()
        print(f"✅ Database connection successful! Table has {response.count} records")
    except Exception as e:
        print(f"❌ Database access failed: {e}")
        print("💡 You may need to create the detections table or check RLS policies")
    
    # Test storage access
    print("\n🗄️ Testing storage access...")
    try:
        # List buckets
        buckets = client.storage.list_buckets()
        print(f"✅ Storage access successful! Found {len(buckets)} buckets")
        
        # Check if our bucket exists
        bucket_names = [bucket.name for bucket in buckets]
        if storage_bucket in bucket_names:
            print(f"✅ Storage bucket '{storage_bucket}' exists")
        else:
            print(f"⚠️ Storage bucket '{storage_bucket}' not found")
            print(f"Available buckets: {bucket_names}")
            
    except Exception as e:
        print(f"❌ Storage access failed: {e}")
    
    print("\n✅ Supabase connection test completed!")
    
except ImportError:
    print("❌ Supabase package not installed. Install with: pip install supabase")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
