import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Filter, X } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'
import type { JournalFilters as Filters } from '@/types/journals'

interface JournalFiltersProps {
  filters: Filters
  onFiltersChange: (filters: Filters) => void
}

export function JournalFilters({
  filters,
  onFiltersChange,
}: JournalFiltersProps) {
  const { t } = useLingo()

  const updateFilter = (key: keyof Filters, value: any) => {
    onFiltersChange({ ...filters, [key]: value })
  }

  const clearFilters = () => {
    onFiltersChange({})
  }

  const activeFilterCount = Object.values(filters).filter(Boolean).length

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          <Filter className="w-5 h-5" />
          {t('journals.filters')}
        </h3>
        {activeFilterCount > 0 && (
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            <X className="w-4 h-4 mr-1" />
            {t('journals.clearFilters')}
          </Button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Open Access Filter */}
        <div>
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={filters.openAccessOnly || false}
              onChange={(e) => updateFilter('openAccessOnly', e.target.checked)}
              className="rounded border-gray-300"
            />
            <span className="text-sm font-medium">
              {t('journals.openAccessOnly')}
            </span>
          </label>
        </div>

        {/* Min Impact Factor */}
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">
            {t('journals.minImpactFactor')}
          </label>
          <Input
            type="number"
            min="0"
            step="0.1"
            value={filters.minImpactFactor || ''}
            onChange={(e) =>
              updateFilter(
                'minImpactFactor',
                e.target.value ? parseFloat(e.target.value) : undefined
              )
            }
            placeholder="e.g., 5.0"
          />
        </div>

        {/* Max Publication Time */}
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">
            {t('journals.maxPublicationTime')}
          </label>
          <Input
            type="number"
            min="1"
            value={filters.maxPublicationTime || ''}
            onChange={(e) =>
              updateFilter(
                'maxPublicationTime',
                e.target.value ? parseInt(e.target.value) : undefined
              )
            }
            placeholder={t('journals.months')}
          />
        </div>

        {/* Search */}
        <div>
          <label className="text-sm font-medium text-gray-700 mb-1 block">
            {t('journals.search')}
          </label>
          <Input
            type="text"
            value={filters.searchQuery || ''}
            onChange={(e) => updateFilter('searchQuery', e.target.value)}
            placeholder={t('journals.searchPlaceholder')}
          />
        </div>
      </div>

      {/* Active Filters */}
      {activeFilterCount > 0 && (
        <div className="flex flex-wrap gap-2">
          {filters.openAccessOnly && (
            <Badge variant="secondary">
              {t('journals.openAccess')}
              <button
                onClick={() => updateFilter('openAccessOnly', false)}
                className="ml-1 hover:text-red-600"
              >
                <X className="w-3 h-3" />
              </button>
            </Badge>
          )}
          {filters.minImpactFactor && (
            <Badge variant="secondary">
              IF ≥ {filters.minImpactFactor}
              <button
                onClick={() => updateFilter('minImpactFactor', undefined)}
                className="ml-1 hover:text-red-600"
              >
                <X className="w-3 h-3" />
              </button>
            </Badge>
          )}
          {filters.maxPublicationTime && (
            <Badge variant="secondary">
              ≤ {filters.maxPublicationTime} {t('journals.months')}
              <button
                onClick={() => updateFilter('maxPublicationTime', undefined)}
                className="ml-1 hover:text-red-600"
              >
                <X className="w-3 h-3" />
              </button>
            </Badge>
          )}
        </div>
      )}
    </div>
  )
}
