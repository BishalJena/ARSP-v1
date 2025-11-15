'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/dashboard-layout';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { useAuthenticatedAPI } from '@/lib/api-client-auth';
import { useLingo } from '@/lib/useLingo';
import { BookOpen, Loader2, Star, TrendingUp, Clock } from 'lucide-react';

interface Journal {
  journal_name: string;
  publisher: string;
  impact_factor: number;
  match_score: number;
  open_access: boolean;
  avg_time_to_publish: number;
  acceptance_rate: number;
  issn: string;
}

export default function JournalsPage() {
  const apiClient = useAuthenticatedAPI();
  const { locale, t } = useLingo();
  const [abstract, setAbstract] = useState('');
  const [keywords, setKeywords] = useState('');
  const [journals, setJournals] = useState<Journal[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleRecommend = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!abstract.trim()) {
      setError(t('journals.abstract_label') + ' is required');
      return;
    }

    if (!keywords.trim()) {
      setError(t('journals.keywords_label') + ' is required');
      return;
    }

    setError('');
    setLoading(true);
    setJournals([]);

    try {
      const keywordArray = keywords.split(',').map(k => k.trim()).filter(k => k);

      const response: any = await apiClient.recommendJournals({
        abstract: abstract.trim(),
        keywords: keywordArray,
        language: locale,
      });

      setJournals(response.recommendations || []);
    } catch (err: any) {
      setError(err.message || t('errors.recommend_failed'));
    } finally {
      setLoading(false);
    }
  };

  const getMatchColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-gray-600';
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('journals.title')}</h2>
          <p className="text-gray-600 mt-2">
            {t('journals.description')}
          </p>
        </div>

        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5" />
              {t('journals.form_title')}
            </CardTitle>
            <CardDescription>
              {t('journals.form_description')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleRecommend} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="abstract">{t('journals.abstract_label')}</Label>
                <Textarea
                  id="abstract"
                  placeholder={t('journals.abstract_placeholder')}
                  value={abstract}
                  onChange={(e) => setAbstract(e.target.value)}
                  disabled={loading}
                  className="min-h-[150px]"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="keywords">{t('journals.keywords_label')}</Label>
                <Input
                  id="keywords"
                  type="text"
                  placeholder={t('journals.keywords_placeholder')}
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                  disabled={loading}
                  required
                />
              </div>

              <Button type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {t('journals.recommending')}
                  </>
                ) : (
                  <>
                    <BookOpen className="mr-2 h-4 w-4" />
                    {t('journals.button_recommend')}
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Results */}
        {journals.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">
              {t('journals.found').replace('{count}', journals.length.toString())}
            </h3>

            <div className="space-y-4">
              {journals.map((journal, index) => (
                <Card key={index} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-lg">{journal.journal_name}</CardTitle>
                        <CardDescription className="mt-1">
                          {journal.publisher} • ISSN: {journal.issn}
                        </CardDescription>
                      </div>
                      <div className="flex flex-col items-end gap-2">
                        {journal.open_access && (
                          <Badge variant="default" className="bg-blue-600">
                            {t('journals.open_access')}
                          </Badge>
                        )}
                        <Badge
                          variant="outline"
                          className={`font-semibold ${getMatchColor(journal.match_score)}`}
                        >
                          {(journal.match_score * 100).toFixed(0)}% {t('journals.match_score')}
                        </Badge>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Star className="h-4 w-4" />
                          <span className="text-sm">{t('journals.impact_factor')}</span>
                        </div>
                        <p className="text-2xl font-bold text-gray-900">
                          {journal.impact_factor.toFixed(2)}
                        </p>
                      </div>

                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <TrendingUp className="h-4 w-4" />
                          <span className="text-sm">{t('journals.acceptance_rate')}</span>
                        </div>
                        <p className="text-2xl font-bold text-gray-900">
                          {(journal.acceptance_rate * 100).toFixed(0)}%
                        </p>
                      </div>

                      <div className="space-y-1">
                        <div className="flex items-center gap-2 text-muted-foreground">
                          <Clock className="h-4 w-4" />
                          <span className="text-sm">{t('journals.time_to_publish')}</span>
                        </div>
                        <p className="text-2xl font-bold text-gray-900">
                          {journal.avg_time_to_publish} days
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && journals.length === 0 && !error && (
          <Card className="text-center py-12">
            <CardContent>
              <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('journals.no_results')}
              </h3>
              <p className="text-gray-600 mb-4">
                {t('journals.empty_message')}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
