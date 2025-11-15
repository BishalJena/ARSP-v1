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
  id: string;
  file_name: string;
  file_size: number;
  processed: boolean;
  summary?: string;
  key_findings?: string[];
  methodology?: string;
  created_at: string;
  paper_title?: string;
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
                <Card key={paper.id} className="border-2 border-gray-200">
                  <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <FileText className="h-5 w-5 text-blue-600" />
                          {paper.processed ? (
                            <Badge variant="default" className="bg-green-600">
                              {t('papers.status_processed')}
                            </Badge>
                          ) : (
                            <Badge variant="outline">{t('papers.status_pending')}</Badge>
                          )}
                        </div>
                        <CardTitle className="text-xl text-gray-900 mb-1">
                          {paper.paper_title || paper.file_name.replace('.pdf', '')}
                        </CardTitle>
                        <CardDescription className="text-sm">
                          📄 {paper.file_name} • {(paper.file_size / 1024).toFixed(1)} KB • {new Date(paper.created_at).toLocaleString()}
                        </CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-6 pt-6">
                    {paper.processed && paper.summary && (
                      <div className="space-y-3 bg-blue-50 p-4 rounded-lg border border-blue-200">
                        <div className="flex items-center gap-2">
                          <div className="h-1 w-1 bg-blue-600 rounded-full"></div>
                          <h4 className="font-bold text-base text-blue-900">{t('papers.summary')}</h4>
                        </div>
                        <p className="text-sm text-gray-800 leading-relaxed pl-3 border-l-2 border-blue-400">
                          {paper.summary}
                        </p>
                      </div>
                    )}

                    {paper.processed && paper.methodology && (
                      <div className="space-y-3 bg-purple-50 p-4 rounded-lg border border-purple-200">
                        <div className="flex items-center gap-2">
                          <div className="h-1 w-1 bg-purple-600 rounded-full"></div>
                          <h4 className="font-bold text-base text-purple-900">{t('papers.methodology')}</h4>
                        </div>
                        <p className="text-sm text-gray-800 leading-relaxed pl-3 border-l-2 border-purple-400">
                          {paper.methodology}
                        </p>
                      </div>
                    )}

                    {paper.processed && paper.key_findings && paper.key_findings.length > 0 && (
                      <div className="space-y-3 bg-green-50 p-4 rounded-lg border border-green-200">
                        <div className="flex items-center gap-2">
                          <div className="h-1 w-1 bg-green-600 rounded-full"></div>
                          <h4 className="font-bold text-base text-green-900">{t('papers.key_findings')}</h4>
                        </div>
                        <ul className="space-y-2 pl-3">
                          {paper.key_findings.map((finding, idx) => (
                            <li key={idx} className="text-sm text-gray-800 leading-relaxed flex gap-2">
                              <span className="text-green-600 font-bold">•</span>
                              <span className="flex-1">{finding}</span>
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
