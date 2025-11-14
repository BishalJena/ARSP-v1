import { useState, useEffect } from 'react'
import { Search, Loader2, AlertTriangle } from 'lucide-react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { TopicCard } from './TopicCard'
import { useTopics } from '@/hooks/useTopics'
import { useLingo } from '@/hooks/useLingo'
import {
  calculateAverageRelevance,
  meetsAccuracyThreshold,
} from '@/lib/relevance'
import type { Topic } from '@/types/topics'

export function TopicSelector() {
  const [query, setQuery] = useState('')
  const [searchQuery, setSearchQuery] = useState('')
  const [relevanceScore, setRelevanceScore] = useState<number | null>(null)
  const { t } = useLingo()

  const { data, isLoading, error } = useTopics(
    { query: searchQuery, limit: 5 },
    searchQuery.length > 0
  )

  // Calculate relevance score when results change
  useEffect(() => {
    if (data && data.topics.length > 0) {
      const score = calculateAverageRelevance(searchQuery, data.topics)
      setRelevanceScore(score)
    } else {
      setRelevanceScore(null)
    }
  }, [data, searchQuery])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      setSearchQuery(query.trim())
    }
  }

  const handleTopicSelect = (topic: Topic) => {
    console.log('Selected topic:', topic)
    // In a real app, this might navigate to a detail page or save the selection
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {t('nav.topics')}
        </h1>
        <p className="mt-2 text-gray-600">
          {t('topics.subtitle')}
        </p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            type="text"
            placeholder={t('topics.searchPlaceholder')}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="pl-10"
          />
        </div>
        <Button type="submit" disabled={isLoading || !query.trim()}>
          {isLoading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              {t('common.loading')}
            </>
          ) : (
            t('common.search')
          )}
        </Button>
      </form>

      {/* Results */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-sm text-red-800">
            {t('common.error')}: {error.message}
          </p>
        </div>
      )}

      {data && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold">
              {t('topics.resultsCount', { count: data.topics.length })}
            </h2>
            {data.totalCount > data.topics.length && (
              <p className="text-sm text-muted-foreground">
                Showing {data.topics.length} of {data.totalCount} results
              </p>
            )}
          </div>

          {/* Accuracy Warning */}
          {relevanceScore !== null && !meetsAccuracyThreshold(relevanceScore) && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm font-medium text-yellow-900">
                  {t('topics.lowRelevanceWarning')}
                </p>
                <p className="text-sm text-yellow-700 mt-1">
                  {t('topics.relevanceScore')}: {relevanceScore}% (threshold: 80%)
                </p>
                <p className="text-sm text-yellow-700 mt-1">
                  {t('topics.tryRefining')}
                </p>
              </div>
            </div>
          )}

          {data.topics.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">{t('topics.noResults')}</p>
            </div>
          ) : (
            <div className="grid gap-4">
              {data.topics.map((topic) => (
                <TopicCard
                  key={topic.id}
                  topic={topic}
                  onSelect={handleTopicSelect}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {!searchQuery && !isLoading && (
        <div className="text-center py-12">
          <Search className="w-12 h-12 mx-auto text-gray-300 mb-4" />
          <p className="text-muted-foreground">
            {t('topics.searchPrompt')}
          </p>
        </div>
      )}
    </div>
  )
}
