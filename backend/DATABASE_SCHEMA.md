# Database Schema Documentation

## Overview

ARSP uses Supabase (PostgreSQL) for data storage with three main tables and a storage bucket for PDF files.

## Tables

### 1. journals

Stores information about academic journals for recommendations.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | UUID | NO | `uuid_generate_v4()` | Primary key |
| `name` | TEXT | NO | - | Journal name |
| `description` | TEXT | YES | NULL | Brief description |
| `publisher` | TEXT | YES | NULL | Publisher name |
| `impact_factor` | NUMERIC(8,3) | YES | 0 | Journal impact factor |
| `h_index` | INTEGER | YES | NULL | H-index metric |
| `is_open_access` | BOOLEAN | YES | FALSE | Open access status |
| `publication_time_months` | INTEGER | YES | NULL | Average publication time |
| `domain` | TEXT | NO | - | Research domain |
| `url` | TEXT | YES | NULL | Journal website |
| `created_at` | TIMESTAMP | YES | NOW() | Creation timestamp |

**Indexes:**
- `idx_journals_domain` on `domain`

### 2. uploads

Stores uploaded research papers and their analysis.

#### Legacy Columns

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | UUID | NO | `uuid_generate_v4()` | Primary key |
| `user_id` | TEXT | NO | - | Clerk user ID |
| `file_name` | TEXT | NO | - | Original filename |
| `file_path` | TEXT | NO | - | Storage path |
| `file_size` | INTEGER | NO | - | File size in bytes |
| `mime_type` | TEXT | NO | - | MIME type |
| `processed` | BOOLEAN | YES | FALSE | Processing status |
| `summary` | TEXT | YES | NULL | Legacy summary (BART) |
| `methodology` | TEXT | YES | NULL | Legacy methodology |
| `key_findings` | JSONB | YES | NULL | Legacy findings |
| `created_at` | TIMESTAMP | YES | NOW() | Upload timestamp |

#### Enhanced API Columns (Gemini Integration)

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `analysis` | JSONB | YES | NULL | Complete 17-section analysis from Gemini |
| `translation_cache` | JSONB | YES | `{}` | Cached translations by language code |
| `original_language` | TEXT | YES | `'en'` | Original analysis language |
| `paper_type` | TEXT | YES | `'research'` | Paper type (research/ml/clinical/review) |
| `processed_at` | TIMESTAMP | YES | NULL | Processing completion time |
| `error_message` | TEXT | YES | NULL | Error message if processing failed |
| `file_url` | TEXT | YES | NULL | Public URL for PDF access |

**Indexes:**
- `idx_uploads_user_id` on `user_id`
- `idx_uploads_processed` on `processed` (WHERE processed = true)
- `idx_uploads_paper_type` on `paper_type`
- `idx_uploads_created_at` on `created_at DESC`

#### Analysis Structure (JSONB)

The `analysis` column stores a comprehensive analysis with 17 sections:

```json
{
  "title": "Paper Title",
  "citation": "Full APA citation",
  "tldr": "2-3 sentence summary",
  "background": "Background and context",
  "research_question": "Main research question",
  "methods": {
    "overview": "High-level approach",
    "data_sources": "Data sources",
    "sample_size": "Sample size details",
    "study_design": "Experimental design",
    "statistical_analysis": "Statistical methods"
  },
  "results": {
    "summary": "Main findings",
    "key_findings": ["Finding 1", "Finding 2"],
    "quantitative_results": ["Metric: Value"]
  },
  "discussion": "Interpretation and comparison",
  "limitations": ["Limitation 1", "Limitation 2"],
  "related_work": [
    {
      "citation": "Author et al. (2024)",
      "comparison": "How this work differs"
    }
  ],
  "contributions": ["Novel contribution 1"],
  "ethical_considerations": "Ethical concerns",
  "reproducibility": {
    "code_availability": "GitHub link",
    "data_availability": "Dataset info",
    "hyperparameters": "Training details",
    "compute_budget": "GPU hours",
    "license": "MIT License"
  },
  "practical_takeaways": ["Actionable insight 1"],
  "future_work": ["Future direction 1"],
  "glossary": {
    "term": "Definition with context"
  },
  "qa_pairs": [
    {
      "question": "What method was used?",
      "answer": "Detailed answer"
    }
  ],
  "plain_summary": "Non-specialist summary",
  "practitioner_summary": "Actionable summary",
  "paper_type": "research",
  "field": "Computer Science",
  "word_count": 1200
}
```

#### Translation Cache Structure (JSONB)

The `translation_cache` column stores translations:

```json
{
  "hi": {
    "title": "शोध पत्र शीर्षक",
    "citation": "...",
    "tldr": "...",
    ...
  },
  "es": {
    "title": "Título del artículo",
    "citation": "...",
    "tldr": "...",
    ...
  }
}
```

Keys are ISO 639-1 language codes: `en`, `hi`, `te`, `ta`, `bn`, `mr`, `zh`, `es`, `fr`, `de`, `pt`, `ja`, `ko`, `ru`, `ar`

### 3. drafts

Stores user drafts for plagiarism checking.

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| `id` | UUID | NO | `uuid_generate_v4()` | Primary key |
| `user_id` | TEXT | NO | - | Clerk user ID |
| `content` | TEXT | NO | - | Draft content |
| `plagiarism_score` | NUMERIC(5,2) | YES | NULL | Plagiarism percentage |
| `last_checked_at` | TIMESTAMP | YES | NULL | Last check timestamp |
| `created_at` | TIMESTAMP | YES | NOW() | Creation timestamp |

## Storage Buckets

### papers

Stores uploaded PDF files.

**Path Structure:** `{user_id}/{timestamp}_{filename}.pdf`

**Example:** `user_abc123/1700000000_research-paper.pdf`

**Configuration:**
- Public access via signed URLs
- 20MB file size limit
- PDF MIME type only

## Database Setup

### Initial Setup

Run the database setup script:

```bash
python setup_db_auto.py
```

This creates:
- All tables with indexes
- Sample journals (15 entries)
- UUID extension

### Enhanced API Migration

To add columns for the Enhanced Papers API (Gemini integration):

```bash
python migrate_enhanced_api.py
```

This adds:
- `analysis` column for comprehensive analysis
- `translation_cache` column for multilingual support
- `original_language`, `paper_type`, `processed_at` columns
- `error_message` and `file_url` columns
- Performance indexes

## API Compatibility

### Legacy Papers API (`/api/v1/papers/`)

Uses columns:
- `summary`, `methodology`, `key_findings` (BART-based)
- Processing time: 5-15 seconds

### Enhanced Papers API (`/api/v1/papers-enhanced/`)

Uses columns:
- `analysis`, `translation_cache` (Gemini-based)
- Processing time: 1-3 seconds
- 15 language support with caching

Both APIs can coexist and use the same `uploads` table.

## Common Queries

### Get user's papers

```sql
SELECT id, file_name, created_at, processed, paper_type
FROM uploads
WHERE user_id = 'user_abc123'
ORDER BY created_at DESC
LIMIT 50;
```

### Get paper with analysis

```sql
SELECT id, file_name, analysis, translation_cache, original_language, paper_type
FROM uploads
WHERE id = '123e4567-e89b-12d3-a456-426614174000'
AND user_id = 'user_abc123';
```

### Get cached translation

```sql
SELECT translation_cache->'hi' AS hindi_translation
FROM uploads
WHERE id = '123e4567-e89b-12d3-a456-426614174000';
```

### Get unprocessed papers

```sql
SELECT id, file_name, created_at
FROM uploads
WHERE processed = false
ORDER BY created_at ASC;
```

### Get papers by type

```sql
SELECT id, file_name, paper_type, created_at
FROM uploads
WHERE paper_type = 'ml'
AND user_id = 'user_abc123'
ORDER BY created_at DESC;
```

## Performance Considerations

### Indexes

All critical columns are indexed for fast queries:
- `user_id` - User-specific queries
- `processed` - Filter by processing status
- `paper_type` - Filter by paper type
- `created_at` - Chronological sorting
- `domain` (journals) - Domain filtering

### JSONB Queries

For efficient JSONB queries:

```sql
-- Check if translation exists
SELECT EXISTS(
    SELECT 1 FROM uploads
    WHERE id = '...'
    AND translation_cache ? 'hi'
);

-- Get specific field from analysis
SELECT analysis->>'title' AS title
FROM uploads
WHERE id = '...';

-- Query nested fields
SELECT analysis->'methods'->>'overview' AS methods_overview
FROM uploads
WHERE id = '...';
```

### GIN Indexes (Optional)

For heavy JSONB queries, add GIN indexes:

```sql
CREATE INDEX idx_uploads_analysis_gin ON uploads USING GIN (analysis);
CREATE INDEX idx_uploads_translation_cache_gin ON uploads USING GIN (translation_cache);
```

## Backup and Maintenance

### Backup

Supabase provides automatic daily backups. For manual backups:

```bash
pg_dump -h db.{project_id}.supabase.co -U postgres -d postgres > backup.sql
```

### Clean Old Uploads

```sql
-- Delete uploads older than 90 days with no processing
DELETE FROM uploads
WHERE processed = false
AND created_at < NOW() - INTERVAL '90 days';
```

### Storage Cleanup

When deleting uploads, also delete from storage:

```python
# Delete database record
supabase.table("uploads").delete().eq("id", paper_id).execute()

# Delete file from storage
supabase.storage.from_("papers").remove([file_path])
```

## Environment Variables

Required for database access:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
```

## Troubleshooting

### Connection Issues

1. Check `SUPABASE_URL` format
2. Verify project is active on Supabase dashboard
3. Check network/firewall settings

### Migration Errors

1. Ensure tables exist (run `setup_db_auto.py` first)
2. Check database permissions
3. Verify column doesn't already exist

### Storage Issues

1. Ensure "papers" bucket exists in Supabase Storage
2. Check file size limit (20MB)
3. Verify MIME type is `application/pdf`

## Schema Versioning

- **v1.0** (Initial): Legacy columns with BART processing
- **v2.0** (Current): Added Gemini integration columns

To check current schema version:

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'uploads'
AND column_name IN ('analysis', 'translation_cache');
```

If both columns exist, you're on v2.0 (Enhanced API ready).
