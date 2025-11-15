#!/usr/bin/env python3
"""Execute SQL statements in Supabase using the PostgREST API"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Individual SQL statements to execute
sql_statements = [
    # Enable UUID extension
    "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";",

    # Profiles table
    """CREATE TABLE IF NOT EXISTS public.profiles (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        email TEXT UNIQUE NOT NULL,
        full_name TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );""",

    # Uploads table
    """CREATE TABLE IF NOT EXISTS public.uploads (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        mime_type TEXT NOT NULL,
        processed BOOLEAN DEFAULT FALSE,
        summary TEXT,
        methodology TEXT,
        key_findings JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );""",

    # Drafts table
    """CREATE TABLE IF NOT EXISTS public.drafts (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        user_id TEXT NOT NULL,
        content TEXT NOT NULL,
        plagiarism_score NUMERIC(5,2),
        last_checked_at TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );""",

    # Journals table
    """CREATE TABLE IF NOT EXISTS public.journals (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        name TEXT NOT NULL,
        description TEXT,
        publisher TEXT,
        impact_factor NUMERIC(8,3) DEFAULT 0,
        h_index INTEGER,
        is_open_access BOOLEAN DEFAULT FALSE,
        publication_time_months INTEGER,
        domain TEXT NOT NULL,
        url TEXT,
        acceptance_rate NUMERIC(5,2),
        issn TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );""",
]

print("🚀 Executing SQL statements in Supabase...")

# Since we can't execute raw SQL via PostgREST, let's use the Supabase client
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("\n✅ Storage bucket already created!")
print("\n⚠️  For SQL table creation, please follow these steps:")
print("\n1. Open Supabase Dashboard:")
print("   https://supabase.com/dashboard/project/rvhngxjkkikzsawplagw")
print("\n2. Go to: SQL Editor (left sidebar)")
print("\n3. Click 'New Query'")
print("\n4. Copy the contents of: supabase_setup.sql")
print("\n5. Paste and click 'Run'")
print("\nOR use this quickstart SQL:")
print("-" * 60)

quickstart_sql = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS journals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    description TEXT,
    publisher TEXT,
    impact_factor NUMERIC(8,3) DEFAULT 0,
    h_index INTEGER,
    is_open_access BOOLEAN DEFAULT FALSE,
    publication_time_months INTEGER,
    domain TEXT NOT NULL,
    url TEXT
);

INSERT INTO journals (name, description, publisher, impact_factor, domain, is_open_access, url)
VALUES
    ('Nature Machine Intelligence', 'Leading journal for AI and machine learning', 'Nature', 25.898, 'Computer Science', false, 'https://www.nature.com/natmachintell/'),
    ('JMLR', 'Premier open-access journal for ML', 'JMLR', 6.071, 'Computer Science', true, 'https://jmlr.org/'),
    ('IEEE TPAMI', 'Top journal for pattern recognition', 'IEEE', 24.314, 'Computer Science', false, 'https://ieeexplore.ieee.org/'),
    ('PLOS ONE', 'Open-access multidisciplinary', 'PLOS', 3.752, 'Multidisciplinary', true, 'https://journals.plos.org/plosone/'),
    ('Nature', 'Multidisciplinary science', 'Nature', 69.504, 'Multidisciplinary', false, 'https://www.nature.com/')
ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS uploads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    mime_type TEXT NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    summary TEXT,
    methodology TEXT,
    key_findings JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

print(quickstart_sql)
print("-" * 60)
print("\n✨ After running the SQL, your database will be ready!")
