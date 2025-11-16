# Backend Scripts

This directory contains utility scripts for database setup and maintenance.

## Scripts

### `setup_db_auto.py`

Automated database setup script that creates all tables and applies migrations.

**Usage**:
```bash
python setup_db_auto.py
```

**Prerequisites**:
- Supabase credentials configured in `.env`
- PostgreSQL connection available

**What it does**:
1. Connects to Supabase database
2. Reads `supabase_setup.sql`
3. Creates all tables (users, papers, plagiarism_checks, etc.)
4. Sets up Row-Level Security (RLS) policies
5. Creates indexes for performance

**When to use**:
- First-time database setup
- Resetting local development database
- Setting up new environment (staging, production)

## Notes

- All migrations are idempotent (safe to run multiple times)
- RLS policies ensure data isolation per user
- Full-text search indexes created for papers
