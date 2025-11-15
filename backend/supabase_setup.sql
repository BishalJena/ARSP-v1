-- ARSP Supabase Database Setup
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Profiles table (for user data)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Uploads table (for papers)
CREATE TABLE IF NOT EXISTS public.uploads (
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
);

-- 3. Drafts table (for plagiarism checks)
CREATE TABLE IF NOT EXISTS public.drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    plagiarism_score NUMERIC(5,2),
    last_checked_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Journals table (for journal recommendations)
CREATE TABLE IF NOT EXISTS public.journals (
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
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_uploads_user_id ON public.uploads(user_id);
CREATE INDEX IF NOT EXISTS idx_uploads_created_at ON public.uploads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_drafts_user_id ON public.drafts(user_id);
CREATE INDEX IF NOT EXISTS idx_drafts_last_checked ON public.drafts(last_checked_at DESC);
CREATE INDEX IF NOT EXISTS idx_journals_domain ON public.journals(domain);
CREATE INDEX IF NOT EXISTS idx_journals_impact_factor ON public.journals(impact_factor DESC);

-- Enable Row Level Security (RLS) - but allow all operations for demo
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.drafts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.journals ENABLE ROW LEVEL SECURITY;

-- Create permissive policies for demo (allow all operations)
CREATE POLICY "Allow all for profiles" ON public.profiles FOR ALL USING (true);
CREATE POLICY "Allow all for uploads" ON public.uploads FOR ALL USING (true);
CREATE POLICY "Allow all for drafts" ON public.drafts FOR ALL USING (true);
CREATE POLICY "Allow all for journals" ON public.journals FOR ALL USING (true);

-- Seed some journal data for testing
INSERT INTO public.journals (name, description, publisher, impact_factor, h_index, is_open_access, publication_time_months, domain, url)
VALUES
    ('Nature Machine Intelligence', 'Leading journal for AI and machine learning research', 'Nature Publishing Group', 25.898, 89, FALSE, 6, 'Computer Science', 'https://www.nature.com/natmachintell/'),
    ('Journal of Machine Learning Research', 'Premier open-access journal for machine learning', 'JMLR', 6.071, 145, TRUE, 4, 'Computer Science', 'https://jmlr.org/'),
    ('IEEE Transactions on Pattern Analysis and Machine Intelligence', 'Top journal for pattern recognition and computer vision', 'IEEE', 24.314, 287, FALSE, 8, 'Computer Science', 'https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=34'),
    ('Neural Computation', 'Journal covering computational neuroscience and neural networks', 'MIT Press', 2.740, 114, FALSE, 5, 'Computer Science', 'https://direct.mit.edu/neco'),
    ('Artificial Intelligence', 'Long-established journal for AI research', 'Elsevier', 14.050, 174, FALSE, 7, 'Computer Science', 'https://www.sciencedirect.com/journal/artificial-intelligence'),

    ('Nature', 'Multidisciplinary science journal', 'Nature Publishing Group', 69.504, 1152, FALSE, 5, 'Multidisciplinary', 'https://www.nature.com/'),
    ('Science', 'Premier multidisciplinary research journal', 'AAAS', 63.714, 1221, FALSE, 6, 'Multidisciplinary', 'https://www.science.org/'),
    ('Cell', 'Leading journal in life sciences', 'Cell Press', 64.500, 825, FALSE, 6, 'Biology', 'https://www.cell.com/cell/home'),
    ('The Lancet', 'Top medical journal', 'Elsevier', 202.731, 687, FALSE, 8, 'Medicine', 'https://www.thelancet.com/'),
    ('PLOS ONE', 'Open-access multidisciplinary journal', 'PLOS', 3.752, 368, TRUE, 3, 'Multidisciplinary', 'https://journals.plos.org/plosone/'),

    ('Physical Review Letters', 'Leading physics journal', 'American Physical Society', 9.161, 511, FALSE, 4, 'Physics', 'https://journals.aps.org/prl/'),
    ('Journal of the American Chemical Society', 'Premier chemistry journal', 'ACS', 16.383, 734, FALSE, 6, 'Chemistry', 'https://pubs.acs.org/journal/jacsat'),
    ('Proceedings of the National Academy of Sciences', 'Multidisciplinary science journal', 'PNAS', 11.205, 753, FALSE, 5, 'Multidisciplinary', 'https://www.pnas.org/'),
    ('Nature Communications', 'Open-access multidisciplinary journal', 'Nature Publishing Group', 16.600, 281, TRUE, 4, 'Multidisciplinary', 'https://www.nature.com/ncomms/'),
    ('ACM Computing Surveys', 'Survey journal for computer science', 'ACM', 16.600, 154, FALSE, 7, 'Computer Science', 'https://dl.acm.org/journal/csur')
ON CONFLICT DO NOTHING;

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers for updated_at
CREATE TRIGGER set_uploads_updated_at
    BEFORE UPDATE ON public.uploads
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_drafts_updated_at
    BEFORE UPDATE ON public.drafts
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

CREATE TRIGGER set_journals_updated_at
    BEFORE UPDATE ON public.journals
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- Grant permissions (for service role)
GRANT ALL ON ALL TABLES IN SCHEMA public TO postgres, anon, authenticated, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO postgres, anon, authenticated, service_role;

-- Success message
SELECT 'ARSP Database Setup Complete! Created: profiles, uploads, drafts, journals tables + 15 sample journals' AS status;
