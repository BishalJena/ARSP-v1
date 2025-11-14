# Database Migrations

This directory contains SQL migrations for the ARSP database schema.

## Running Migrations

### Option 1: Using Supabase CLI (Recommended)
```bash
# Install Supabase CLI if not already installed
npm install -g supabase

# Link to your Supabase project
supabase link --project-ref YOUR_PROJECT_REF

# Run migrations
supabase db push
```

### Option 2: Manual Execution via Supabase Dashboard
1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Copy and paste the contents of each migration file
4. Execute the SQL

## Migrations

### 20241114_consent_logs.sql
Creates the `consent_logs` table for DPDP compliance tracking.

**Purpose**: Store user consent records for data usage, marketing, etc.

**Tables Created**:
- `consent_logs`: Audit log for user consent with RLS policies

**Features**:
- Row Level Security (RLS) enabled
- Users can only view/insert their own consent logs
- Indexed for performance
- Tracks consent type, timestamp, IP address, and user agent
