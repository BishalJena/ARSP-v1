'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { DashboardLayout } from '@/components/dashboard-layout';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { useAuthenticatedAPI } from '@/lib/api-client-auth';
import { useLingo } from '@/lib/useLingo';
import { FileText, Upload, Loader2, Calendar, Users, ArrowRight, Sparkles } from 'lucide-react';
import { Input } from '@/components/ui/input';

interface Paper {
  id: string;
  file_name: string;
  file_size: number;
  processed: boolean;
  summary?: string;
  key_findings?: string[];
  created_at: string;
  paper_title?: string;
  year?: number;
  authors?: string[];
  venue?: string;
}

export default function PapersPage() {
  const apiClient = useAuthenticatedAPI();
  const router = useRouter();
  const { locale, t } = useLingo();
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
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
      setError('No file selected');
      return;
    }

    setUploading(true);
    setError('');

    try {
      // Upload the file
      const uploadResponse = await apiClient.uploadPaper(selectedFile, { language: locale });

      // Process immediately
      await apiClient.processPaper(uploadResponse.id, { language: locale });

      setSelectedFile(null);
      const fileInput = document.getElementById('file-upload') as HTMLInputElement;
      if (fileInput) fileInput.value = '';

      await fetchPapers();
    } catch (err: any) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleCardClick = (paperId: string) => {
    router.push(`/dashboard/papers/${paperId}`);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900">Research Papers</h2>
          <p className="text-gray-600 mt-2">
            Upload and analyze research papers with AI-powered insights
          </p>
        </div>

        {/* Upload Section */}
        <Card className="border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-indigo-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="h-5 w-5 text-blue-600" />
              Upload Research Paper
            </CardTitle>
            <CardDescription>
              Upload a PDF to get comprehensive analysis with bachelor's-level explanations
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
              <Button
                onClick={handleUpload}
                disabled={uploading || !selectedFile}
                size="lg"
              >
                {uploading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2 h-4 w-4" />
                    Analyze Paper
                  </>
                )}
              </Button>
            </div>
            {selectedFile && (
              <p className="text-sm text-gray-600">
                Selected: {selectedFile.name} ({(selectedFile.size / 1024 / 1024).toFixed(2)} MB)
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

        {/* Papers Grid */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        ) : papers.length > 0 ? (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">
              Your Papers ({papers.length})
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {papers.map((paper) => (
                <Card
                  key={paper.id}
                  className="group cursor-pointer hover:shadow-lg transition-all duration-200 border-2 hover:border-blue-400 bg-white"
                  onClick={() => handleCardClick(paper.id)}
                >
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between mb-2">
                      <FileText className="h-6 w-6 text-blue-600" />
                      {paper.processed ? (
                        <Badge variant="default" className="bg-green-600">
                          <Sparkles className="h-3 w-3 mr-1" />
                          Analyzed
                        </Badge>
                      ) : (
                        <Badge variant="outline">Processing</Badge>
                      )}
                    </div>
                    <CardTitle className="text-lg line-clamp-2 group-hover:text-blue-600 transition-colors">
                      {paper.paper_title || paper.file_name.replace('.pdf', '')}
                    </CardTitle>
                  </CardHeader>

                  <CardContent className="space-y-3">
                    {/* Metadata */}
                    <div className="space-y-1.5 text-sm text-gray-600">
                      {paper.year && (
                        <div className="flex items-center gap-2">
                          <Calendar className="h-4 w-4" />
                          <span>{paper.year}</span>
                        </div>
                      )}
                      {paper.authors && paper.authors.length > 0 && (
                        <div className="flex items-center gap-2">
                          <Users className="h-4 w-4" />
                          <span className="truncate">
                            {paper.authors[0]}{paper.authors.length > 1 ? ` +${paper.authors.length - 1}` : ''}
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Summary Preview */}
                    {paper.summary && (
                      <p className="text-sm text-gray-700 line-clamp-3">
                        {paper.summary}
                      </p>
                    )}

                    {/* Key Findings Count */}
                    {paper.key_findings && paper.key_findings.length > 0 && (
                      <div className="flex items-center gap-2 text-sm text-blue-600 font-medium">
                        <span>{paper.key_findings.length} Key Findings</span>
                      </div>
                    )}

                    {/* View Button */}
                    <div className="pt-2 flex items-center justify-between text-sm">
                      <span className="text-gray-500">
                        {new Date(paper.created_at).toLocaleDateString()}
                      </span>
                      <div className="flex items-center gap-1 text-blue-600 font-medium group-hover:gap-2 transition-all">
                        <span>View Analysis</span>
                        <ArrowRight className="h-4 w-4" />
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ) : (
          <Card className="text-center py-12 bg-gray-50">
            <CardContent>
              <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                No Papers Yet
              </h3>
              <p className="text-gray-600 mb-4">
                Upload your first research paper to get started with AI-powered analysis
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
