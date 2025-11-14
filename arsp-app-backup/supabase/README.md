# Database Setup

## Quick Setup

1. Create a Supabase project at https://supabase.com
2. Go to SQL Editor in your Supabase dashboard
3. Run migrations in order:
   - `001_create_tables.sql`
   - `002_enable_rls.sql`
   - `003_storage_setup.sql`
4. (Optional) Run `seed.sql` to populate journals

## Tables

- **profiles** - User profiles with language preferences
- **drafts** - Research paper drafts
- **uploads** - Uploaded PDF files
- **literature_reviews** - AI-generated literature reviews
- **journals** - Journal database for recommendations

## Storage

- **papers** bucket - User-uploaded research papers (RLS protected)

## Security

All tables have Row Level Security (RLS) enabled:
- Users can only access their own data
- Journals table is publicly readable
- Storage bucket is user-scoped
