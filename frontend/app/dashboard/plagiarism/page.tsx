'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/dashboard-layout';
import { useLingo } from '@/lib/useLingo';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { useAuthenticatedAPI } from '@/lib/api-client-auth';
import {
  Shield,
  Loader2,
  AlertTriangle,
  CheckCircle,
  AlertCircle,
  ExternalLink,
  FileText,
  BookOpen,
  ChevronDown,
  ChevronUp,
  Info
} from 'lucide-react';

interface FlaggedSection {
  text: string;
  start_index: number;
  end_index: number;
  similarity: number;
  source: string;
  source_url: string;
  snippet?: string;
}

interface DetailedSource {
  url: string;
  title: string;
  snippet: string;
  plagiarism_score: number;
  word_count: number;
  matched_words: number;
}

interface SimilarWord {
  word: string;
  frequency: number;
  sources: string[];
}

interface ScanInfo {
  word_count: number;
  character_count: number;
  language_detected: string;
  sources_checked: number;
}

interface PlagiarismResult {
  originality_score: number;
  plagiarism_score?: number;
  flagged_sections: FlaggedSection[];
  sources?: DetailedSource[];
  similar_words?: SimilarWord[];
  scan_info?: ScanInfo;
  total_word_count?: number;
  plagiarized_word_count?: number;
  processing_time_seconds: number;
  provider?: string;
}

export default function PlagiarismPage() {
  const apiClient = useAuthenticatedAPI();
  const { locale, t } = useLingo();
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState<PlagiarismResult | null>(null);
  const [showInput, setShowInput] = useState(true);

  const handleCheck = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!text.trim()) {
      setError(t('plagiarism.check_description'));
      return;
    }

    if (text.length < 100) {
      setError(t('plagiarism.text_placeholder'));
      return;
    }

    setError('');
    setLoading(true);
    setResult(null);

    try {
      const response: any = await apiClient.checkPlagiarism({
        text: text.trim(),
        language: locale || 'auto',
        use_winston: true,
      });

      setResult(response);
      setShowInput(false); // Collapse input after getting results
    } catch (err: any) {
      setError(err.message || t('errors.check_failed'));
    } finally {
      setLoading(false);
    }
  };

  const handleCheckAnother = () => {
    setResult(null);
    setText('');
    setShowInput(true);
    setError('');
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-600';
    if (score >= 60) return 'bg-yellow-600';
    return 'bg-red-600';
  };

  const getSeverityColor = (similarity: number) => {
    if (similarity >= 90) return 'destructive';
    if (similarity >= 80) return 'default';
    return 'outline';
  };

  const getSeverityLabel = (similarity: number) => {
    if (similarity >= 90) return 'High';
    if (similarity >= 80) return 'Medium';
    return 'Low';
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900">{t('plagiarism.title')}</h2>
          <p className="text-gray-600 mt-2">
            {t('plagiarism.description')}
          </p>
        </div>

        {/* Input Section - Collapsible after results */}
        {showInput || !result ? (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Shield className="h-5 w-5" />
                {t('plagiarism.check_title')}
              </CardTitle>
              <CardDescription>
                {t('plagiarism.check_description')}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCheck} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="text">{t('plagiarism.check_title')}</Label>
                  <Textarea
                    id="text"
                    placeholder={t('plagiarism.text_placeholder')}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    disabled={loading}
                    className="min-h-[250px]"
                  />
                  <div className="flex items-center justify-between text-sm text-muted-foreground">
                    <span>
                      {text.length} characters
                      {text.length > 0 && text.length < 100 && (
                        <span className="text-yellow-600 ml-2">
                          (minimum 100 required)
                        </span>
                      )}
                    </span>
                    {text.length > 0 && (
                      <span>{Math.ceil(text.split(/\s+/).filter(w => w.length > 0).length)} words</span>
                    )}
                  </div>
                </div>

                <Button type="submit" disabled={loading || text.length < 100}>
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t('plagiarism.checking')}
                    </>
                  ) : (
                    <>
                      <Shield className="mr-2 h-4 w-4" />
                      {t('plagiarism.button_check')}
                    </>
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        ) : (
          /* Collapsed Input - Show after results */
          <Card className="bg-gray-50 border-dashed">
            <CardContent className="py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Shield className="h-5 w-5 text-gray-600" />
                  <div>
                    <p className="text-sm font-medium">{t('common.check')} {result.total_word_count || 0} {t('plagiarism.stats.total_words').toLowerCase()}</p>
                    <p className="text-xs text-muted-foreground">{t('plagiarism.messages.empty_desc')}</p>
                  </div>
                </div>
                <Button variant="outline" onClick={handleCheckAnother}>
                  {t('plagiarism.button_check')}
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Results - Two Column Layout */}
        {result && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Score & Summary (1/3 width) */}
            <div className="lg:col-span-1 space-y-6">
              {/* Originality Score Card */}
              <Card className="sticky top-6">
                <CardHeader className="pb-3">
                  <CardTitle className="flex items-center gap-2 text-lg">
                    {result.originality_score >= 80 ? (
                      <CheckCircle className="h-5 w-5 text-green-600" />
                    ) : result.originality_score >= 60 ? (
                      <AlertTriangle className="h-5 w-5 text-yellow-600" />
                    ) : (
                      <AlertCircle className="h-5 w-5 text-red-600" />
                    )}
                    {t('plagiarism.originality_score')}
                  </CardTitle>
                  {result.scan_info && result.scan_info.language_detected && result.scan_info.language_detected !== 'unknown' && (
                    <div className="pt-2">
                      <Badge variant="outline" className="text-xs">
                        {result.scan_info.language_detected.toUpperCase()}
                      </Badge>
                    </div>
                  )}
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Big Score */}
                  <div className="text-center py-4">
                    <div className={`text-6xl font-bold ${getScoreColor(result.originality_score)}`}>
                      {result.originality_score.toFixed(0)}%
                    </div>
                    <p className="text-sm text-muted-foreground mt-2">{t('academic_terms.originality')}</p>
                  </div>

                  <Progress
                    value={result.originality_score}
                    className={`h-2 ${getScoreBgColor(result.originality_score)}`}
                  />

                  {/* Stats Grid */}
                  <div className="space-y-2 pt-2">
                    <div className="group flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                      <span className="text-xs text-muted-foreground">{t('plagiarism.stats.total_words')}</span>
                      <span className="text-base font-bold text-gray-900">{result.total_word_count || 0}</span>
                    </div>
                    <div className="group flex items-center justify-between p-3 bg-red-50 rounded-lg hover:bg-red-100 transition-colors border border-red-100">
                      <span className="text-xs text-red-700 font-medium">{t('plagiarism.stats.similar_words')}</span>
                      <span className="text-base font-bold text-red-600">{result.plagiarized_word_count || 0}</span>
                    </div>
                    {result.scan_info && (
                      <div className="group flex items-center justify-between p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors border border-blue-100">
                        <span className="text-xs text-blue-700 font-medium">{t('plagiarism.stats.sources_scanned')}</span>
                        <span className="text-base font-bold text-blue-600">{result.scan_info.sources_checked}</span>
                      </div>
                    )}
                    {result.processing_time_seconds && (
                      <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg border border-purple-100">
                        <span className="text-xs text-purple-700 font-medium">{t('plagiarism.stats.scan_time')}</span>
                        <span className="text-base font-bold text-purple-600">{result.processing_time_seconds.toFixed(1)}s</span>
                      </div>
                    )}
                  </div>

                  {/* Verdict */}
                  <div className="pt-2">
                    {result.originality_score >= 80 ? (
                      <div className="text-center p-3 bg-green-50 rounded-lg border border-green-200">
                        <CheckCircle className="h-8 w-8 text-green-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-green-900">{t('plagiarism.plagiarism_level_high')}</p>
                        <p className="text-xs text-green-700 mt-1">{t('plagiarism.messages.no_plagiarism_desc')}</p>
                      </div>
                    ) : result.originality_score >= 60 ? (
                      <div className="text-center p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                        <AlertTriangle className="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-yellow-900">{t('plagiarism.plagiarism_level_medium')}</p>
                        <p className="text-xs text-yellow-700 mt-1">{t('plagiarism.flagged_sections_desc')}</p>
                      </div>
                    ) : (
                      <div className="text-center p-3 bg-red-50 rounded-lg border border-red-200">
                        <AlertCircle className="h-8 w-8 text-red-600 mx-auto mb-2" />
                        <p className="text-sm font-medium text-red-900">{t('plagiarism.plagiarism_level_low')}</p>
                        <p className="text-xs text-red-700 mt-1">{t('plagiarism.messages.action_required_text')}</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* Tips Card */}
              {result.originality_score < 80 && (
                <Card className="border-blue-200 bg-blue-50">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-sm flex items-center gap-2">
                      <Info className="h-4 w-4" />
                      {t('plagiarism.tips.title')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-xs text-blue-900 space-y-2">
                    <div>• {t('plagiarism.tips.paraphrase')}</div>
                    <div>• {t('plagiarism.tips.cite')}</div>
                    <div>• {t('plagiarism.tips.analysis')}</div>
                    <div>• {t('plagiarism.tips.quotes')}</div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Right Column - Detailed Results (2/3 width) */}
            <div className="lg:col-span-2 space-y-6">
              {/* Source Breakdown - NEW! */}
              {result.sources && result.sources.length > 0 && (() => {
                // Filter sources that have valid data (non-zero word counts)
                const validSources = result.sources.filter(s => s.word_count > 0 && s.matched_words >= 0);
                const hasValidSources = validSources.length > 0;

                return (
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <span className="flex items-center gap-2">
                          <BookOpen className="h-5 w-5" />
                          {t('plagiarism.similar_sources')} ({result.sources.length})
                        </span>
                        {result.sources.length > 5 && (
                          <Badge variant="secondary" className="text-xs">
                            {t('plagiarism.messages.scroll_to_see_all')}
                          </Badge>
                        )}
                      </CardTitle>
                      <CardDescription>
                        {hasValidSources
                          ? t('plagiarism.source_breakdown_desc')
                          : t('plagiarism.similar_sources_desc')
                        }
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="relative">
                      {/* Scrollable container with max height */}
                      <div
                        className="max-h-[600px] overflow-y-auto pr-2 scroll-smooth"
                        style={{
                          scrollbarWidth: 'thin',
                          scrollbarColor: '#cbd5e1 #f1f5f9'
                        }}
                      >
                      {hasValidSources ? (
                        // Show detailed breakdown if we have word count data
                        <div className="space-y-3">
                          {validSources.map((source, index) => {
                            const overlapPercent = source.word_count > 0
                              ? Math.round((source.matched_words / source.word_count) * 100)
                              : 0;

                            const isHighSeverity = source.plagiarism_score > 50;
                            const isMediumSeverity = source.plagiarism_score > 20 && source.plagiarism_score <= 50;

                            return (
                              <div
                                key={index}
                                className={`border rounded-lg p-4 transition-all hover:shadow-md ${
                                  isHighSeverity ? 'border-red-200 bg-red-50/30' :
                                  isMediumSeverity ? 'border-yellow-200 bg-yellow-50/30' :
                                  'border-gray-200 hover:bg-gray-50'
                                }`}
                              >
                                <div className="flex items-start justify-between gap-3 mb-2">
                                  <div className="flex-1 min-w-0">
                                    <h4 className="font-medium text-sm truncate">{source.title}</h4>
                                    <a
                                      href={source.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-xs text-blue-600 hover:underline flex items-center gap-1 mt-1 truncate"
                                    >
                                      <span className="truncate">{source.url}</span>
                                      <ExternalLink className="h-3 w-3 flex-shrink-0" />
                                    </a>
                                  </div>
                                  <Badge
                                    variant={isHighSeverity ? 'destructive' : isMediumSeverity ? 'default' : 'outline'}
                                    className="flex-shrink-0"
                                  >
                                    {source.plagiarism_score > 0 ? `${source.plagiarism_score.toFixed(0)}%` : t('plagiarism.labels.match')}
                                  </Badge>
                                </div>

                                {/* Word Match Stats */}
                                <div className="flex items-center gap-4 mt-3 pt-3 border-t">
                                  <div className="flex-1">
                                    <div className="flex items-center justify-between text-xs mb-1">
                                      <span className="text-muted-foreground">{t('plagiarism.labels.words_matched')}</span>
                                      <span className="font-medium">
                                        {source.matched_words} / {source.word_count}
                                      </span>
                                    </div>
                                    <Progress
                                      value={overlapPercent}
                                      className={`h-2 ${
                                        isHighSeverity ? 'bg-red-100' :
                                        isMediumSeverity ? 'bg-yellow-100' :
                                        'bg-gray-100'
                                      }`}
                                    />
                                  </div>
                                  <div className="text-right">
                                    <div className={`text-xl font-bold ${
                                      isHighSeverity ? 'text-red-600' :
                                      isMediumSeverity ? 'text-yellow-600' :
                                      'text-gray-900'
                                    }`}>
                                      {overlapPercent}%
                                    </div>
                                    <div className="text-xs text-muted-foreground">{t('plagiarism.labels.overlap')}</div>
                                  </div>
                                </div>

                                {source.snippet && (
                                  <div className="mt-3 pt-3 border-t">
                                    <p className="text-xs text-gray-600 italic line-clamp-2">
                                      "{source.snippet}"
                                    </p>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      ) : (
                        // Simplified list if no detailed data available
                        <div className="space-y-3">
                          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-3">
                            <p className="text-xs text-blue-900">
                              <Info className="h-3 w-3 inline mr-1" />
                              {t('plagiarism.messages.no_data_banner')}
                            </p>
                          </div>
                          {result.sources.map((source, index) => (
                            <div
                              key={index}
                              className="group border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all"
                            >
                              <div className="flex items-start justify-between gap-3">
                                <div className="flex-1 min-w-0">
                                  <h4 className="font-medium text-sm text-gray-900 group-hover:text-blue-600 transition-colors">
                                    {source.title}
                                  </h4>
                                  <a
                                    href={source.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="text-xs text-blue-600 hover:underline flex items-center gap-1 mt-1"
                                  >
                                    {t('plagiarism.messages.view_source')} <ExternalLink className="h-3 w-3" />
                                  </a>
                                  {source.snippet && (
                                    <p className="text-xs text-gray-600 italic mt-2 line-clamp-2 bg-gray-50 p-2 rounded">
                                      "{source.snippet}"
                                    </p>
                                  )}
                                </div>
                                <Badge variant="secondary" className="flex-shrink-0">
                                  {t('plagiarism.labels.similar')}
                                </Badge>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                      </div>
                      {/* Scroll indicator - shows when content is scrollable */}
                      {result.sources.length > 5 && (
                        <div className="sticky bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-white via-white/50 to-transparent pointer-events-none -mt-12" />
                      )}
                    </CardContent>
                  </Card>
                );
              })()}

              {/* Flagged Sections */}
              {result.flagged_sections && result.flagged_sections.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <AlertTriangle className="h-5 w-5 text-yellow-600" />
                      {t('plagiarism.flagged_sections')} ({result.flagged_sections.length})
                    </CardTitle>
                    <CardDescription>
                      {t('plagiarism.flagged_sections_desc')}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {result.flagged_sections
                        .sort((a, b) => b.similarity - a.similarity) // Sort by highest similarity first
                        .map((section, index) => {
                          const isHighSeverity = section.similarity >= 90;
                          const isMediumSeverity = section.similarity >= 80 && section.similarity < 90;
                          const isLowSeverity = section.similarity < 80;

                          return (
                            <div
                              key={index}
                              className={`border-l-4 rounded-r-lg p-4 space-y-3 transition-all hover:shadow-md ${
                                isHighSeverity
                                  ? 'border-red-500 bg-red-50/50'
                                  : isMediumSeverity
                                  ? 'border-orange-400 bg-orange-50/50'
                                  : 'border-yellow-400 bg-yellow-50/50'
                              }`}
                            >
                              <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2 flex-wrap">
                                  <Badge
                                    variant={getSeverityColor(section.similarity)}
                                    className={`${
                                      isHighSeverity ? 'bg-red-600 text-white' :
                                      isMediumSeverity ? 'bg-orange-500 text-white' : ''
                                    }`}
                                  >
                                    {section.similarity.toFixed(0)}% {t('plagiarism.labels.match').toLowerCase()}
                                  </Badge>
                                  <Badge
                                    variant="outline"
                                    className={`text-xs ${
                                      isHighSeverity ? 'border-red-300 text-red-700' :
                                      isMediumSeverity ? 'border-orange-300 text-orange-700' :
                                      'border-yellow-400 text-yellow-700'
                                    }`}
                                  >
                                    {isHighSeverity && '🔴'} {isHighSeverity && t('plagiarism.severity.high')}
                                    {isMediumSeverity && '🟠'} {isMediumSeverity && t('plagiarism.severity.medium')}
                                    {isLowSeverity && '🟡'} {isLowSeverity && t('plagiarism.severity.low')}
                                  </Badge>
                                </div>
                                <span className="text-xs text-muted-foreground">
                                  {t('plagiarism.labels.section_of', { current: index + 1, total: result.flagged_sections.length })}
                                </span>
                              </div>

                              {/* Action needed message */}
                              {isHighSeverity && (
                                <div className="bg-red-100 border border-red-300 rounded-md p-2">
                                  <p className="text-xs text-red-900 font-medium">
                                    ⚠️ {t('plagiarism.labels.action_required')}: {t('plagiarism.messages.action_required_text')}
                                  </p>
                                </div>
                              )}

                              <div className="space-y-2">
                                <p className="text-xs font-semibold text-gray-700">{t('plagiarism.results.your_text')}:</p>
                                <div className={`bg-white border rounded-md p-3 ${
                                  isHighSeverity ? 'border-red-300' :
                                  isMediumSeverity ? 'border-orange-300' :
                                  'border-yellow-300'
                                }`}>
                                  <p className="text-sm text-gray-800 leading-relaxed">
                                    "{section.text}"
                                  </p>
                                </div>
                              </div>

                              {section.snippet && (
                                <div className="space-y-2">
                                  <p className="text-xs font-semibold text-gray-700 flex items-center gap-1">
                                    <span>{t('plagiarism.results.matching_source')}:</span>
                                    {isHighSeverity && <span className="text-red-600">({t('plagiarism.labels.very_similar')})</span>}
                                  </p>
                                  <div className="bg-gray-50 border border-gray-300 rounded-md p-3">
                                    <p className="text-sm text-gray-700 italic leading-relaxed">
                                      {section.snippet}
                                    </p>
                                  </div>
                                </div>
                              )}

                              <div className={`pt-3 border-t flex items-center justify-between ${
                                isHighSeverity ? 'border-red-200' :
                                isMediumSeverity ? 'border-orange-200' :
                                'border-yellow-200'
                              }`}>
                                <div className="flex-1">
                                  <p className="text-sm font-medium text-gray-900">{section.source}</p>
                                  {section.source_url && (
                                    <a
                                      href={section.source_url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-xs text-blue-600 hover:underline flex items-center gap-1 mt-1"
                                    >
                                      {t('plagiarism.messages.view_original_source')} <ExternalLink className="h-3 w-3" />
                                    </a>
                                  )}
                                </div>
                              </div>
                            </div>
                          );
                        })}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Similar Words */}
              {result.similar_words && result.similar_words.length > 0 && (
                <Card className="border-gray-200">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-base">
                      <FileText className="h-4 w-4" />
                      {t('plagiarism.common_terms')} ({result.similar_words.length})
                    </CardTitle>
                    <CardDescription className="text-xs">
                      {t('plagiarism.common_terms_desc')}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 mb-4">
                      <p className="text-xs text-blue-900">
                        <Info className="h-3 w-3 inline mr-1" />
                        {t('plagiarism.common_terms_desc')}
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {result.similar_words.slice(0, 30).map((word, index) => (
                        <Badge
                          key={index}
                          variant="secondary"
                          className="text-xs font-normal hover:bg-gray-300 transition-colors cursor-default"
                        >
                          {word.word}
                          {word.frequency > 0 && (
                            <span className="ml-1.5 px-1 py-0.5 bg-gray-300 rounded text-xs">
                              {word.frequency}
                            </span>
                          )}
                        </Badge>
                      ))}
                      {result.similar_words.length > 30 && (
                        <Badge variant="outline" className="text-xs">
                          +{result.similar_words.length - 30} more
                        </Badge>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* All Clear Message */}
              {(!result.flagged_sections || result.flagged_sections.length === 0) && result.originality_score >= 80 && (
                <Card className="border-2 border-green-300 bg-gradient-to-br from-green-50 to-emerald-50">
                  <CardContent className="py-12">
                    <div className="text-center space-y-4">
                      <div className="inline-block p-4 bg-green-100 rounded-full mb-2">
                        <CheckCircle className="h-12 w-12 text-green-600" />
                      </div>
                      <h3 className="text-2xl font-bold text-green-900">
                        {t('plagiarism.messages.no_plagiarism_title')}
                      </h3>
                      <p className="text-green-700 max-w-md mx-auto">
                        {t('plagiarism.messages.no_plagiarism_desc')}
                      </p>
                      <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto pt-4">
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600">{result.originality_score.toFixed(0)}%</div>
                          <div className="text-xs text-green-700">{t('academic_terms.originality')}</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600">0</div>
                          <div className="text-xs text-green-700">{t('plagiarism.flagged_sections')}</div>
                        </div>
                        <div className="text-center">
                          <div className="text-2xl font-bold text-green-600">{result.scan_info?.sources_checked || 0}</div>
                          <div className="text-xs text-green-700">{t('plagiarism.results.sources_checked')}</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!loading && !result && !error && (
          <Card className="border-2 border-dashed border-gray-300 bg-gradient-to-br from-gray-50 to-slate-50">
            <CardContent className="py-16">
              <div className="text-center space-y-6">
                <div className="inline-block p-4 bg-blue-100 rounded-full">
                  <Shield className="h-12 w-12 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">
                    {t('plagiarism.messages.empty_title')}
                  </h3>
                  <p className="text-gray-600 max-w-lg mx-auto">
                    {t('plagiarism.check_description')}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto pt-6">
                  <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                    <CheckCircle className="h-6 w-6 text-green-600 mx-auto mb-2" />
                    <h4 className="font-semibold text-sm text-gray-900 mb-1">{t('plagiarism.empty.feature1_title')}</h4>
                    <p className="text-xs text-gray-600">{t('plagiarism.empty.feature1_desc')}</p>
                  </div>
                  <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                    <AlertCircle className="h-6 w-6 text-blue-600 mx-auto mb-2" />
                    <h4 className="font-semibold text-sm text-gray-900 mb-1">{t('plagiarism.empty.feature2_title')}</h4>
                    <p className="text-xs text-gray-600">{t('plagiarism.empty.feature2_desc')}</p>
                  </div>
                  <div className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm">
                    <FileText className="h-6 w-6 text-purple-600 mx-auto mb-2" />
                    <h4 className="font-semibold text-sm text-gray-900 mb-1">{t('plagiarism.empty.feature3_title')}</h4>
                    <p className="text-xs text-gray-600">{t('plagiarism.empty.feature3_desc')}</p>
                  </div>
                </div>

                <div className="pt-4">
                  <p className="text-sm text-gray-500">
                    {t('plagiarism.messages.empty_desc')}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
