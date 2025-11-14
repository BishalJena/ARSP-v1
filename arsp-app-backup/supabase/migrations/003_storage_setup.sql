-- Create storage bucket for papers
INSERT INTO storage.buckets (id, name, public)
VALUES ('papers', 'papers', false)
ON CONFLICT DO NOTHING;

-- Storage policies for papers bucket
CREATE POLICY "Users can upload own papers"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'papers' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can view own papers"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'papers' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can delete own papers"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'papers' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
