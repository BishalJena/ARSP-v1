#!/usr/bin/env python3
"""Automatically set up Supabase database using direct PostgreSQL connection"""

import os
import re
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Extract project ID from URL
# Format: https://PROJECT_ID.supabase.co
project_id = SUPABASE_URL.split("//")[1].split(".")[0]

# Supabase PostgreSQL connection details
# Format: postgresql://postgres:[YOUR-PASSWORD]@db.PROJECT_ID.supabase.co:5432/postgres
print("⚠️  To connect directly to PostgreSQL, you need your database password.")
print("Find it in: Supabase Dashboard → Settings → Database → Connection string")
print(f"\nProject ID: {project_id}")
print(f"Host: db.{project_id}.supabase.co")
print("Port: 5432")
print("Database: postgres")
print("User: postgres")

db_password = input("\nEnter your Supabase database password: ").strip()

if not db_password:
    print("❌ No password provided. Exiting...")
    exit(1)

try:
    import psycopg2
except ImportError:
    print("❌ psycopg2 not installed. Installing...")
    os.system("pip install psycopg2-binary")
    import psycopg2

# Connection string
conn_string = f"postgresql://postgres:{db_password}@db.{project_id}.supabase.co:5432/postgres"

print("\n🔌 Connecting to Supabase PostgreSQL...")

try:
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    print("✅ Connected successfully!")
    print("\n📋 Creating tables...")

    # Execute SQL statements
    sql_statements = [
        'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";',

        """CREATE TABLE IF NOT EXISTS journals (
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
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );""",

        """CREATE TABLE IF NOT EXISTS uploads (
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
        );""",

        """CREATE TABLE IF NOT EXISTS drafts (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            plagiarism_score NUMERIC(5,2),
            last_checked_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );""",

        """INSERT INTO journals (name, description, publisher, impact_factor, domain, is_open_access, url)
        VALUES
            ('Nature Machine Intelligence', 'Leading journal for AI and machine learning', 'Nature', 25.898, 'Computer Science', false, 'https://www.nature.com/natmachintell/'),
            ('JMLR', 'Premier open-access journal for ML', 'JMLR', 6.071, 'Computer Science', true, 'https://jmlr.org/'),
            ('IEEE TPAMI', 'Top journal for pattern recognition', 'IEEE', 24.314, 'Computer Science', false, 'https://ieeexplore.ieee.org/'),
            ('PLOS ONE', 'Open-access multidisciplinary', 'PLOS', 3.752, 'Multidisciplinary', true, 'https://journals.plos.org/plosone/'),
            ('Nature', 'Multidisciplinary science', 'Nature', 69.504, 'Multidisciplinary', false, 'https://www.nature.com/'),
            ('Science', 'Premier research journal', 'AAAS', 63.714, 'Multidisciplinary', false, 'https://www.science.org/'),
            ('Cell', 'Leading life sciences journal', 'Cell Press', 64.500, 'Biology', false, 'https://www.cell.com/cell/'),
            ('The Lancet', 'Top medical journal', 'Elsevier', 202.731, 'Medicine', false, 'https://www.thelancet.com/'),
            ('Nature Communications', 'Open-access multidisciplinary', 'Nature', 16.600, 'Multidisciplinary', true, 'https://www.nature.com/ncomms/'),
            ('ACM Computing Surveys', 'CS survey journal', 'ACM', 16.600, 'Computer Science', false, 'https://dl.acm.org/journal/csur')
        ON CONFLICT DO NOTHING;"""
    ]

    for i, sql in enumerate(sql_statements, 1):
        try:
            cursor.execute(sql)
            conn.commit()
            print(f"✅ Statement {i} executed")
        except Exception as e:
            print(f"⚠️  Statement {i}: {str(e)[:100]}")
            conn.rollback()

    cursor.close()
    conn.close()

    print("\n✨ Database setup complete!")
    print("\n📊 Created:")
    print("   - journals table (with 10 sample journals)")
    print("   - uploads table (for papers)")
    print("   - drafts table (for plagiarism checks)")

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Alternative: Run SQL manually in Supabase Dashboard")
    print("   Copy: supabase_setup.sql")
    print("   Paste: SQL Editor → New Query → Run")
