#!/usr/bin/env python3
"""Set up Supabase database via Management API"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Extract project ref from URL
project_ref = SUPABASE_URL.split("//")[1].split(".")[0]

# Supabase Management API endpoint
# We'll use the SQL execution endpoint
API_URL = f"https://api.supabase.com/v1/projects/{project_ref}/database/query"

print(f"🚀 Setting up database for project: {project_ref}")
print(f"📍 Supabase URL: {SUPABASE_URL}")

# SQL to execute
sql_query = """
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
    url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

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

CREATE TABLE IF NOT EXISTS drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    plagiarism_score NUMERIC(5,2),
    last_checked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_uploads_user_id ON uploads(user_id);
CREATE INDEX IF NOT EXISTS idx_journals_domain ON journals(domain);

INSERT INTO journals (name, description, publisher, impact_factor, domain, is_open_access, url)
VALUES
    ('Nature Machine Intelligence', 'Leading journal for AI and machine learning research', 'Nature Publishing Group', 25.898, 'Computer Science', false, 'https://www.nature.com/natmachintell/'),
    ('Journal of Machine Learning Research', 'Premier open-access journal for machine learning', 'JMLR', 6.071, 'Computer Science', true, 'https://jmlr.org/'),
    ('IEEE TPAMI', 'Top journal for pattern recognition', 'IEEE', 24.314, 'Computer Science', false, 'https://ieeexplore.ieee.org/'),
    ('PLOS ONE', 'Open-access multidisciplinary', 'PLOS', 3.752, 'Multidisciplinary', true, 'https://journals.plos.org/plosone/'),
    ('Nature', 'Multidisciplinary science', 'Nature', 69.504, 'Multidisciplinary', false, 'https://www.nature.com/'),
    ('Science', 'Premier research journal', 'AAAS', 63.714, 'Multidisciplinary', false, 'https://www.science.org/'),
    ('Cell', 'Leading life sciences journal', 'Cell Press', 64.500, 'Biology', false, 'https://www.cell.com/cell/'),
    ('The Lancet', 'Top medical journal', 'Elsevier', 202.731, 'Medicine', false, 'https://www.thelancet.com/'),
    ('Nature Communications', 'Open-access multidisciplinary', 'Nature', 16.600, 'Multidisciplinary', true, 'https://www.nature.com/ncomms/'),
    ('ACM Computing Surveys', 'CS survey journal', 'ACM', 16.600, 'Computer Science', false, 'https://dl.acm.org/journal/csur'),
    ('Artificial Intelligence', 'AI research journal', 'Elsevier', 14.050, 'Computer Science', false, 'https://www.sciencedirect.com/journal/artificial-intelligence'),
    ('Neural Computation', 'Computational neuroscience', 'MIT Press', 2.740, 'Computer Science', false, 'https://direct.mit.edu/neco'),
    ('Physical Review Letters', 'Leading physics journal', 'APS', 9.161, 'Physics', false, 'https://journals.aps.org/prl/'),
    ('JACS', 'Premier chemistry journal', 'ACS', 16.383, 'Chemistry', false, 'https://pubs.acs.org/journal/jacsat'),
    ('PNAS', 'Multidisciplinary science', 'PNAS', 11.205, 'Multidisciplinary', false, 'https://www.pnas.org/')
ON CONFLICT DO NOTHING;
"""

print("\n⚠️  Supabase Management API requires additional authentication.")
print("Let's use the web-based SQL Editor instead.\n")

print("="*60)
print("COPY THE SQL BELOW:")
print("="*60)
print(sql_query)
print("="*60)

print("\n📋 Steps:")
print("1. Go to: https://supabase.com/dashboard/project/rvhngxjkkikzsawplagw/sql/new")
print("2. Paste the SQL above")
print("3. Click 'Run'")
print("4. Verify success message")

print("\n✨ After running, you'll have:")
print("   - 15 sample journals")
print("   - uploads table for papers")
print("   - drafts table for plagiarism")
