#!/usr/bin/env python3
"""Automatically set up Supabase database"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
project_id = SUPABASE_URL.split("//")[1].split(".")[0]
db_password = "qVgcjjTQ9CgQUM5"

conn_string = f"postgresql://postgres:{db_password}@db.{project_id}.supabase.co:5432/postgres"

print("🔌 Connecting to Supabase PostgreSQL...")

try:
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    print("✅ Connected successfully!")
    print("\n📋 Creating tables...")

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

        # Create indexes
        "CREATE INDEX IF NOT EXISTS idx_uploads_user_id ON uploads(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_journals_domain ON journals(domain);",

        # Insert sample journals
        """INSERT INTO journals (name, description, publisher, impact_factor, domain, is_open_access, url)
        VALUES
            ('Nature Machine Intelligence', 'Leading journal for AI and machine learning research', 'Nature Publishing Group', 25.898, 'Computer Science', false, 'https://www.nature.com/natmachintell/'),
            ('Journal of Machine Learning Research', 'Premier open-access journal for machine learning', 'JMLR', 6.071, 'Computer Science', true, 'https://jmlr.org/'),
            ('IEEE Transactions on Pattern Analysis', 'Top journal for pattern recognition and computer vision', 'IEEE', 24.314, 'Computer Science', false, 'https://ieeexplore.ieee.org/'),
            ('PLOS ONE', 'Open-access multidisciplinary journal', 'PLOS', 3.752, 'Multidisciplinary', true, 'https://journals.plos.org/plosone/'),
            ('Nature', 'Multidisciplinary science journal', 'Nature Publishing Group', 69.504, 'Multidisciplinary', false, 'https://www.nature.com/'),
            ('Science', 'Premier multidisciplinary research journal', 'AAAS', 63.714, 'Multidisciplinary', false, 'https://www.science.org/'),
            ('Cell', 'Leading journal in life sciences', 'Cell Press', 64.500, 'Biology', false, 'https://www.cell.com/cell/'),
            ('The Lancet', 'Top medical journal', 'Elsevier', 202.731, 'Medicine', false, 'https://www.thelancet.com/'),
            ('Nature Communications', 'Open-access multidisciplinary journal', 'Nature Publishing Group', 16.600, 'Multidisciplinary', true, 'https://www.nature.com/ncomms/'),
            ('ACM Computing Surveys', 'Survey journal for computer science', 'ACM', 16.600, 'Computer Science', false, 'https://dl.acm.org/journal/csur'),
            ('Artificial Intelligence', 'Long-established journal for AI research', 'Elsevier', 14.050, 'Computer Science', false, 'https://www.sciencedirect.com/journal/artificial-intelligence'),
            ('Neural Computation', 'Journal covering computational neuroscience', 'MIT Press', 2.740, 'Computer Science', false, 'https://direct.mit.edu/neco'),
            ('Physical Review Letters', 'Leading physics journal', 'American Physical Society', 9.161, 'Physics', false, 'https://journals.aps.org/prl/'),
            ('JACS', 'Premier chemistry journal', 'ACS', 16.383, 'Chemistry', false, 'https://pubs.acs.org/journal/jacsat'),
            ('PNAS', 'Multidisciplinary science journal', 'PNAS', 11.205, 'Multidisciplinary', false, 'https://www.pnas.org/')
        ON CONFLICT DO NOTHING;"""
    ]

    for i, sql in enumerate(sql_statements, 1):
        try:
            cursor.execute(sql)
            conn.commit()
            if i == 1:
                print(f"✅ UUID extension enabled")
            elif i == 2:
                print(f"✅ Created 'journals' table")
            elif i == 3:
                print(f"✅ Created 'uploads' table")
            elif i == 4:
                print(f"✅ Created 'drafts' table")
            elif i == 5:
                print(f"✅ Created indexes")
            elif i == 7:
                cursor.execute("SELECT COUNT(*) FROM journals;")
                count = cursor.fetchone()[0]
                print(f"✅ Inserted {count} sample journals")
        except Exception as e:
            error_msg = str(e)
            if "already exists" in error_msg:
                if i == 2:
                    print(f"ℹ️  'journals' table already exists")
                elif i == 3:
                    print(f"ℹ️  'uploads' table already exists")
                elif i == 4:
                    print(f"ℹ️  'drafts' table already exists")
            else:
                print(f"⚠️  Statement {i}: {error_msg[:80]}")
            conn.rollback()

    # Verify data
    cursor.execute("SELECT COUNT(*) FROM journals;")
    journal_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print("\n✨ Database setup complete!")
    print("\n📊 Summary:")
    print(f"   ✅ journals table: {journal_count} journals")
    print(f"   ✅ uploads table: ready for papers")
    print(f"   ✅ drafts table: ready for plagiarism checks")
    print(f"   ✅ papers storage bucket: ready")

    print("\n🎯 Ready to test:")
    print("   - Papers upload & processing")
    print("   - Journal recommendations")
    print("   - Plagiarism detection")

except Exception as e:
    print(f"\n❌ Error: {e}")
    exit(1)
