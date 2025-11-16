#!/usr/bin/env python3
"""
Database migration for Enhanced Papers API with Gemini 2.0 Flash Lite.
Uses Supabase client instead of direct PostgreSQL connection.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from app.core.supabase import supabase_admin

load_dotenv()

print("🔌 Connecting to Supabase...")

try:
    # Test connection
    result = supabase_admin.table("uploads").select("id").limit(1).execute()
    print("✅ Connected successfully!")
    
    print("\n📋 Migrating uploads table for Enhanced Papers API...")

    # Migration SQL statements (using Supabase RPC or direct SQL)
    migrations = [
        {
            "name": "Add analysis column for comprehensive paper analysis",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS analysis JSONB DEFAULT NULL;
            """
        },
        {
            "name": "Add translation_cache column for multilingual support",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS translation_cache JSONB DEFAULT '{}';
            """
        },
        {
            "name": "Add original_language column",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS original_language TEXT DEFAULT 'en';
            """
        },
        {
            "name": "Add paper_type column",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS paper_type TEXT DEFAULT 'research';
            """
        },
        {
            "name": "Add processed_at timestamp",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS processed_at TIMESTAMP WITH TIME ZONE DEFAULT NULL;
            """
        },
        {
            "name": "Add error_message column for failed processing",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS error_message TEXT DEFAULT NULL;
            """
        },
        {
            "name": "Add file_url column for public access",
            "sql": """
                ALTER TABLE uploads
                ADD COLUMN IF NOT EXISTS file_url TEXT DEFAULT NULL;
            """
        },
        {
            "name": "Create index on processed status",
            "sql": """
                CREATE INDEX IF NOT EXISTS idx_uploads_processed
                ON uploads(processed)
                WHERE processed = true;
            """
        },
        {
            "name": "Create index on paper_type",
            "sql": """
                CREATE INDEX IF NOT EXISTS idx_uploads_paper_type
                ON uploads(paper_type);
            """
        },
        {
            "name": "Create index on created_at for sorting",
            "sql": """
                CREATE INDEX IF NOT EXISTS idx_uploads_created_at
                ON uploads(created_at DESC);
            """
        }
    ]

    # Execute migrations using Supabase RPC (if available) or direct SQL
    # Note: Supabase Python client doesn't support raw SQL directly
    # We'll need to use the Supabase SQL editor or create a migration function
    
    print("\n⚠️  Direct SQL execution not available via Supabase Python client.")
    print("📝 Please run these migrations in Supabase SQL Editor:\n")
    
    for i, migration in enumerate(migrations, 1):
        print(f"-- [{i}/{len(migrations)}] {migration['name']}")
        print(migration['sql'].strip())
        print()
    
    print("\n" + "="*60)
    print("ALTERNATIVE: Run migration via Supabase Dashboard")
    print("="*60)
    print("\n1. Go to your Supabase project dashboard")
    print("2. Navigate to SQL Editor")
    print("3. Copy and paste all the SQL statements above")
    print("4. Click 'Run' to execute")
    print("\nOr use the Supabase CLI:")
    print("  supabase db push")
    print("\n✨ After migration, the Enhanced Papers API will work!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("   1. Check SUPABASE_URL and SUPABASE_SERVICE_KEY in .env file")
    print("   2. Verify Supabase project is active")
    print("   3. Run migrations manually in Supabase SQL Editor")
    exit(1)

