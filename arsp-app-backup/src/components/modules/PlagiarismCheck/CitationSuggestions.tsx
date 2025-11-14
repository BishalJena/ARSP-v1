import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { BookOpen, ExternalLink } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'
import type { CitationSuggestion } from '@/types/plagiarism'

interface CitationSuggestionsProps {
  suggestions: CitationSuggestion[]
}

export function CitationSuggestions({
  suggestions,
}: CitationSuggestionsProps) {
  const { t } = useLingo()

  if (suggestions.length === 0) {
    return null
  }

  const copyDOI = (doi: string) => {
    navigator.clipboard.writeText(doi)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <BookOpen className="w-5 h-5" />
          {t('plagiarism.citations')} ({suggestions.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <h4 className="font-medium text-gray-900 flex-1">
                  {suggestion.title}
                </h4>
                <Badge variant="outline">
                  {suggestion.relevance}% {t('plagiarism.relevant')}
                </Badge>
              </div>

              <p className="text-sm text-gray-600 mb-2">
                {suggestion.authors.join(', ')} ({suggestion.year})
              </p>

              {suggestion.snippet && (
                <p className="text-sm text-gray-500 italic mb-3">
                  "{suggestion.snippet}"
                </p>
              )}

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => copyDOI(suggestion.doi)}
                >
                  {t('plagiarism.copyDOI')}
                </Button>
                {suggestion.url && (
                  <Button
                    variant="ghost"
                    size="sm"
                    asChild
                  >
                    <a
                      href={suggestion.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <ExternalLink className="w-4 h-4 mr-1" />
                      {t('plagiarism.viewPaper')}
                    </a>
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
