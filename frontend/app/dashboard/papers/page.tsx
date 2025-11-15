'use client';

import { useState, useEffect } from 'react';
import { DashboardLayout } from '@/components/dashboard-layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { useAuthenticatedAPI } from '@/lib/api-client-auth';
import { useLingo } from '@/lib/useLingo';
import { FileText, Upload, Loader2, Trash2, Eye } from 'lucide-react';
import { Input } from '@/components/ui/input';

interface Paper {
  id: number;
  title: string;
  filename: string;
  uploaded_at: string;
  processed: boolean;
  summary?: string;
  key_findings?: string[];
  methodology?: string;
  created_at: string;
}

export default function PapersPage() {
  const apiClient = useAuthenticatedAPI();
  const { locale, t } = useLingo();
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [processingIds, setProcessingIds] = useState<Set<number>>(new Set());
  const [error, setError] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  useEffect(() => {
    fetchPapers();
  }, []);

  const fetchPapers = async () => {
    setLoading(true);
    try {
      const response: any = await apiClient.listPapers({ language: locale });
      setPapers(response.papers || []);
    } catch (err: any) {
      setError(err.message || t('errors.generic'));
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError(t('errors.upload_failed') + ': No file selected');
      return;
    }

    setUploading(true);
    setError('');

    try {
      await apiClient.uploadPaper(selectedFile, { language: locale });
      setSelectedFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-upload') as HTMLInputElement;
      if (fileInput) fileInput.value = '';

      await fetchPapers();
    } catch (err: any) {
      setError(err.message || t('errors.upload_failed'));
    } finally {
      setUploading(false);
    }
  };

  const handleProcess = async (paperId: number) => {
    setProcessingIds(prev => new Set(prev).add(paperId));
    setError('');

    try {
      await apiClient.processPaper(paperId, { language: locale });
      await fetchPapers();
    } catch (err: any) {
      setError(err.message || t('errors.process_failed'));
    } finally {
      setProcessingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(paperId);
        return newSet;
      });
    }
  };

  const handleDelete = async (paperId: number) => {
    if (!confirm(t('common.delete') + '?')) {
      return;
    }

    try {
      await apiClient.deletePaper(paperId, { language: locale });
      await fetchPapers();
    } catch (err: any) {
      setError(err.message || t('errors.generic'));
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('papers.title')}</h2>
          <p className="text-gray-600 mt-2">
            {t('papers.description')}
          </p>
        </div>

        {/* Upload Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5" />
              {t('papers.upload_title')}
            </CardTitle>
            <CardDescription>
              {t('papers.upload_description')}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-end gap-4">
              <div className="flex-1">
                <Input
                  id="file-upload"
                  type="file"
                  accept=".pdf"
                  onChange={handleFileChange}
                  disabled={uploading}
                />
              </div>
              <Button onClick={handleUpload} disabled={uploading || !selectedFile}>
                {uploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {t('papers.uploading')}
                  </>
                ) : (
                  <>
                    <Upload className="mr-2 h-4 w-4" />
                    {t('papers.upload_button')}
                  </>
                )}
              </Button>
            </div>
            {selectedFile && (
              <p className="text-sm text-muted-foreground">
                {t('papers.selected_file').replace('{filename}', selectedFile.name)}
              </p>
            )}
          </CardContent>
        </Card>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Papers List */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        ) : papers.length > 0 ? (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">
              {t('papers.your_papers').replace('{count}', papers.length.toString())}
            </h3>

            <div className="space-y-4">
              {papers.map((paper) => (
                <Card key={paper.id}>
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg">{paper.title}</CardTitle>
                        <CardDescription className="mt-1">
                          {paper.filename} • {t('papers.uploaded').replace('{date}', new Date(paper.uploaded_at).toLocaleDateString())}
                        </CardDescription>
                      </div>
                      <div className="flex items-center gap-2">
                        {paper.processed ? (
                          <Badge variant="default" className="bg-green-600">
                            {t('papers.status_processed')}
                          </Badge>
                        ) : (
                          <Badge variant="outline">{t('papers.status_pending')}</Badge>
                        )}
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {paper.processed && paper.summary && (
                      <div className="space-y-2">
                        <h4 className="font-semibold text-sm">{t('papers.summary')}</h4>
                        <p className="text-sm text-gray-700">{paper.summary}</p>
                      </div>
                    )}

                    {paper.processed && paper.methodology && (
                      <div className="space-y-2">
                        <h4 className="font-semibold text-sm">{t('papers.methodology')}</h4>
                        <p className="text-sm text-gray-700">{paper.methodology}</p>
                      </div>
                    )}

                    {paper.processed && paper.key_findings && paper.key_findings.length > 0 && (
                      <div className="space-y-2">
                        <h4 className="font-semibold text-sm">{t('papers.key_findings')}</h4>
                        <ul className="list-disc list-inside space-y-1">
                          {paper.key_findings.map((finding, idx) => (
                            <li key={idx} className="text-sm text-gray-700">
                              {finding}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    <div className="flex items-center gap-2 pt-2">
                      {!paper.processed && (
                        <Button
                          size="sm"
                          onClick={() => handleProcess(paper.id)}
                          disabled={processingIds.has(paper.id)}
                        >
                          {processingIds.has(paper.id) ? (
                            <>
                              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                              {t('papers.processing')}
                            </>
                          ) : (
                            <>
                              <Eye className="mr-2 h-4 w-4" />
                              {t('papers.process_button')}
                            </>
                          )}
                        </Button>
                      )}
                      <Button
                        size="sm"
                        variant="destructive"
                        onClick={() => handleDelete(paper.id)}
                      >
                        <Trash2 className="mr-2 h-4 w-4" />
                        {t('common.delete')}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ) : (
          <Card className="text-center py-12">
            <CardContent>
              <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('papers.no_papers')}
              </h3>
              <p className="text-gray-600 mb-4">
                {t('papers.empty_message')}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
