'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/dashboard-layout';
import { useLingo } from '@/lib/useLingo';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { apiClient } from '@/lib/api-client';
import { TrendingUp, Search, Loader2 } from 'lucide-react';

interface Topic {
  id: string;
  title: string;
  description: string;
  impact_score: number;
  source: string;
  url?: string;
  citation_count?: number | null;
  year?: number;
}

export default function TopicsPage() {
  const { locale, t } = useLingo();
  const [discipline, setDiscipline] = useState('');
  const [limit, setLimit] = useState('10');
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFetchTopics = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const params: any = {
        limit: parseInt(limit),
        language: locale  // Pass current language to backend
      };
      if (discipline.trim()) {
        params.discipline = discipline.trim();
      }

      const response: any = await apiClient.getTrendingTopics(params);
      setTopics(response.topics || []);
    } catch (err: any) {
      setError(err.message || t('errors.generic'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('topics.title')}</h2>
          <p className="text-gray-600 mt-2">
            {t('topics.description')}
          </p>
        </div>

        {/* Search Form */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Search className="h-5 w-5" />
              {t('topics.button_search')}
            </CardTitle>
            <CardDescription>
              {t('topics.description')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleFetchTopics} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="discipline">{t('topics.search_label')}</Label>
                  <Input
                    id="discipline"
                    type="text"
                    placeholder={t('topics.search_placeholder')}
                    value={discipline}
                    onChange={(e) => setDiscipline(e.target.value)}
                    disabled={loading}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="limit">{t('topics.limit_label')}</Label>
                  <Input
                    id="limit"
                    type="number"
                    min="1"
                    max="50"
                    value={limit}
                    onChange={(e) => setLimit(e.target.value)}
                    disabled={loading}
                  />
                </div>
              </div>

              <Button type="submit" disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {t('topics.searching')}
                  </>
                ) : (
                  <>
                    <TrendingUp className="mr-2 h-4 w-4" />
                    {t('topics.button_search')}
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
        {topics.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">
              {t('topics.found').replace('{count}', topics.length.toString())}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {topics.map((topic, index) => (
                <Card key={index} className="hover:shadow-md transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-lg">{topic.title}</CardTitle>
                      <Badge variant="secondary" className="text-xs">
                        {topic.source}
                      </Badge>
                    </div>
                    {topic.description && (
                      <p className="text-sm text-muted-foreground mt-2">{topic.description}</p>
                    )}
                  </CardHeader>
                  <CardContent className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">{t('topics.impact_score')}</span>
                      <span className="font-semibold">
                        {topic.impact_score.toFixed(1)}/100
                      </span>
                    </div>

                    {topic.citation_count !== undefined && topic.citation_count !== null && (
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">{t('topics.citations')}</span>
                        <span className="font-semibold flex items-center gap-1">
                          <TrendingUp className="h-4 w-4 text-blue-600" />
                          {topic.citation_count}
                        </span>
                      </div>
                    )}

                    {topic.year && (
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">{t('topics.year')}</span>
                        <span className="font-semibold">{topic.year}</span>
                      </div>
                    )}

                    {topic.url && (
                      <a
                        href={topic.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-blue-600 hover:underline flex items-center gap-1"
                      >
                        {t('topics.view_paper')} →
                      </a>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && topics.length === 0 && !error && (
          <Card className="text-center py-12">
            <CardContent>
              <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {t('topics.no_results')}
              </h3>
              <p className="text-gray-600 mb-4">
                {t('topics.empty_message')}
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
