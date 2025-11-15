#!/usr/bin/env python3
"""
Setup Supabase database tables and storage for ARSP
Run this script to initialize the database schema
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # Use service key for admin operations

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_KEY in .env file")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("🚀 Setting up Supabase database for ARSP...")
print(f"📍 URL: {SUPABASE_URL}")

# Read SQL file
with open("supabase_setup.sql", "r") as f:
    sql_content = f.read()

# Split into individual statements and execute
# Note: Supabase Python client doesn't have direct SQL execution
# We'll need to use the REST API or run this in Supabase SQL Editor

print("\n⚠️  Important: Please run the SQL script manually:")
print("1. Go to your Supabase dashboard: https://supabase.com/dashboard")
print(f"2. Open project: {SUPABASE_URL}")
print("3. Navigate to: SQL Editor")
print("4. Copy and paste the contents of: supabase_setup.sql")
print("5. Click 'Run' to execute the script")
print("\n✅ This will create:")
print("   - profiles table")
print("   - uploads table (for papers)")
print("   - drafts table (for plagiarism checks)")
print("   - journals table (with 15 sample journals)")
print("   - Storage bucket: papers")

print("\n📦 Creating storage bucket for papers...")

try:
    # Create storage bucket for papers
    bucket_name = "papers"

    # Check if bucket exists
    buckets = supabase.storage.list_buckets()
    bucket_exists = any(b.name == bucket_name for b in buckets)

    if not bucket_exists:
        # Create bucket
        supabase.storage.create_bucket(
            bucket_name,
            options={
                "public": False,  # Private bucket
                "file_size_limit": 10485760,  # 10MB
                "allowed_mime_types": ["application/pdf"]
            }
        )
        print(f"✅ Created storage bucket: {bucket_name}")
    else:
        print(f"ℹ️  Storage bucket '{bucket_name}' already exists")

    # Set bucket to public (for easier testing)
    try:
        supabase.storage.update_bucket(
            bucket_name,
            options={"public": True}
        )
        print(f"✅ Made bucket '{bucket_name}' public")
    except Exception as e:
        print(f"⚠️  Could not update bucket permissions: {e}")
        print("   (This is okay - you can set this manually in Supabase dashboard)")

except Exception as e:
    print(f"❌ Error creating storage bucket: {e}")
    print("\n⚠️  Manual setup required:")
    print("1. Go to Supabase Dashboard → Storage")
    print("2. Click 'New bucket'")
    print("3. Name: papers")
    print("4. Public: Yes (for demo)")
    print("5. File size limit: 10MB")
    print("6. Allowed MIME types: application/pdf")

print("\n" + "="*60)
print("📋 Next Steps:")
print("="*60)
print("1. Run the SQL script in Supabase SQL Editor (see above)")
print("2. Verify tables were created: Dashboard → Database → Tables")
print("3. Verify storage bucket: Dashboard → Storage")
print("4. Test the backend endpoints")
print("\n✨ Setup complete!")
