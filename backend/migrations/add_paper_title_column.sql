-- Add paper_title column to uploads table
ALTER TABLE uploads ADD COLUMN IF NOT EXISTS paper_title TEXT DEFAULT NULL;
