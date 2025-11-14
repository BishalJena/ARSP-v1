import { useState, useMemo } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { Loader2, Search } from 'lucide-react'
import { JournalFilters } from './JournalFilters'
import { JournalTable } from './JournalTable'
import { useLingo } from '@/hooks/useLingo'
import { mockJournals } from '@/lib/mockJournals'
import { calculateRelevanceScore } from '@/lib/relevance'
import type { JournalFilters as Filters } from '@/types/journals'

export function JournalRecommendation() {
  const [abstract, setAbstract] = useState('')
  const [filters, setFilters] = useState<Filters>({})
  const [hasSearched, setHasSearched] = useState(false)
  const [isSearching, setIsSearching] = useState(false)
  const { t } = useLingo()

  const handleSearch = async () => {
    if (!abstract.trim()) return

    setIsSearching(true)
    setHasSearched(true)

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    setIsSearching(false)
  }

  // Calculate fit scores and apply filters
  const filteredJournals = useMemo(() => {
    let journals = mockJournals.map((journal) => ({
      ...journal,
      fitScore: abstract.trim()
        ? calculateRelevanceScore(abstract, journal.name, journal.description)
        : undefined,
    }))

    // Apply filters
    if (filters.openAccessOnly) {
      journals = journals.filter((j) => j.isOpenAccess)
    }

    if (filters.minImpactFactor) {
      journals = journals.filter((j) => j.impactFactor >= filters.minImpactFactor!)
    }

    if (filters.maxPublicationTime) {
      journals = journals.filter(
        (j) => j.publicationTimeMonths <= filters.maxPublicationTime!
      )
    }

    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase()
      journals = journals.filter(
        (j) =>
          j.name.toLowerCase().includes(query) ||
          j.description.toLowerCase().includes(query)
      )
    }

    return journals
  }, [abstract, filters])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {t('nav.journals')}
        </h1>
        <p className="mt-2 text-gray-600">{t('journals.subtitle')}</p>
      </div>

      {/* Abstract Input */}
      <div className="space-y-2">
        <label
          htmlFor="abstract"
          className="text-sm font-medium text-gray-700 block"
        >
          {t('journals.abstractLabel')}
        </label>
        <Textarea
          id="abstract"
          value={abstract}
          onChange={(e) => setAbstract(e.target.value)}
          placeholder={t('journals.abstractPlaceholder')}
          className="min-h-[150px]"
        />
        <p className="text-xs text-muted-foreground">
          {abstract.trim().split(/\s+/).filter(Boolean).length} {t('plagiarism.wordCount')}
        </p>
      </div>

      {/* Search Button */}
      <div className="flex justify-center">
        <Button
          onClick={handleSearch}
          disabled={isSearching || !abstract.trim()}
          size="lg"
        >
          {isSearching ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              {t('journals.searching')}
            </>
          ) : (
            <>
              <Search className="w-5 h-5 mr-2" />
              {t('journals.findJournals')}
            </>
          )}
        </Button>
      </div>

      {/* Results */}
      {hasSearched && !isSearching && (
        <div className="space-y-6">
          <JournalFilters filters={filters} onFiltersChange={setFilters} />

          <div>
            <h2 className="text-lg font-semibold mb-4">
              {t('journals.recommendations')} ({filteredJournals.length})
            </h2>
            <JournalTable journals={filteredJournals} />
          </div>
        </div>
      )}
    </div>
  )
}
