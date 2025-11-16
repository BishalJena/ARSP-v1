# Database Migrations

This directory contains database migration scripts that were used to set up and enhance the database schema.

## Migration Files

### SQL Files

- `add_paper_metadata_columns.sql` - Adds enhanced metadata columns to papers table
- `add_paper_title_column.sql` - Adds title column to papers table
- `create_users_table.sql` - **NEW** Creates users table with password authentication support

### Python Migration Scripts

- `migrate_enhanced_api.py` - Migration script for enhanced API v2.0
- `migrate_enhanced_api_supabase.py` - Supabase-specific migration for enhanced API

## Running Migrations

### Manual SQL Execution

Run SQL files directly in Supabase SQL Editor or via psql:

```bash
# Connect to your Supabase database
psql "postgresql://postgres:[YOUR-PASSWORD]@[YOUR-HOST]:5432/postgres"

# Run migration
\i create_users_table.sql
```

### Automatic Setup

For new database setup, use the main setup script:

```bash
cd ../scripts
python setup_db_auto.py
```

This will apply all migrations from `supabase_setup.sql` automatically.

## Latest Migration: Users Table with Password Authentication

**Date:** 2025-11-16

**File:** `create_users_table.sql`

**Changes:**
- Creates complete `users` table with UUID primary keys
- Adds `password_hash` column (TEXT, NOT NULL) for bcrypt-hashed passwords
- Adds `email` column with unique constraint and index
- Adds `full_name`, `role`, `institution`, `research_interests` columns
- Adds automatic `updated_at` trigger
- Enables Row-Level Security (RLS) with permissive policy for demo
- Grants necessary permissions to Supabase roles

**Why:** Replacing Clerk with self-contained email/password authentication for:
- Hackathon simplicity (no external service)
- Unlimited users/logins (no API limits)
- Full control over authentication flow
- Easier demo for judges

**Schema:**
```sql
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    institution TEXT,
    research_interests TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**Usage:**
```sql
-- Verify migration
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Check constraints
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name = 'users';

-- Check indexes
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users';
```

**Important Notes:**
- After running this migration, wait 10-30 seconds for Supabase PostgREST to refresh its schema cache
- The `password_hash` column stores bcrypt hashes (never plain text passwords)
- Email addresses are automatically validated at the API level
- Minimum password length is 8 characters (enforced at API level)
