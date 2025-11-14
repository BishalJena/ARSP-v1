import { useState } from 'react'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { ArrowUpDown, ExternalLink, CheckCircle } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'
import type { Journal, SortField, SortDirection } from '@/types/journals'

interface JournalTableProps {
  journals: Journal[]
}

export function JournalTable({ journals }: JournalTableProps) {
  const [sortField, setSortField] = useState<SortField>('fitScore')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')
  const { t } = useLingo()

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const sortedJournals = [...journals].sort((a, b) => {
    const aValue = a[sortField] ?? 0
    const bValue = b[sortField] ?? 0

    if (sortField === 'name') {
      return sortDirection === 'asc'
        ? String(aValue).localeCompare(String(bValue))
        : String(bValue).localeCompare(String(aValue))
    }

    return sortDirection === 'asc'
      ? Number(aValue) - Number(bValue)
      : Number(bValue) - Number(aValue)
  })

  const getFitScoreColor = (score?: number) => {
    if (!score) return 'secondary'
    if (score >= 80) return 'default'
    if (score >= 60) return 'secondary'
    return 'outline'
  }

  return (
    <div className="border rounded-lg overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSort('name')}
                className="font-semibold"
              >
                {t('journals.name')}
                <ArrowUpDown className="ml-2 w-4 h-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSort('fitScore')}
                className="font-semibold"
              >
                {t('journals.fitScore')}
                <ArrowUpDown className="ml-2 w-4 h-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSort('impactFactor')}
                className="font-semibold"
              >
                {t('journals.impactFactor')}
                <ArrowUpDown className="ml-2 w-4 h-4" />
              </Button>
            </TableHead>
            <TableHead>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => handleSort('publicationTimeMonths')}
                className="font-semibold"
              >
                {t('journals.publicationTime')}
                <ArrowUpDown className="ml-2 w-4 h-4" />
              </Button>
            </TableHead>
            <TableHead>{t('journals.access')}</TableHead>
            <TableHead className="text-right">{t('journals.actions')}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedJournals.length === 0 ? (
            <TableRow>
              <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                {t('journals.noResults')}
              </TableCell>
            </TableRow>
          ) : (
            sortedJournals.map((journal) => (
              <TableRow key={journal.id} className="hover:bg-gray-50">
                <TableCell>
                  <div>
                    <div className="font-medium">{journal.name}</div>
                    <div className="text-sm text-muted-foreground line-clamp-1">
                      {journal.description}
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  {journal.fitScore ? (
                    <Badge variant={getFitScoreColor(journal.fitScore)}>
                      {journal.fitScore}%
                    </Badge>
                  ) : (
                    <span className="text-muted-foreground">-</span>
                  )}
                </TableCell>
                <TableCell>
                  <span className="font-medium">{journal.impactFactor.toFixed(3)}</span>
                </TableCell>
                <TableCell>
                  {journal.publicationTimeMonths} {t('journals.months')}
                </TableCell>
                <TableCell>
                  {journal.isOpenAccess ? (
                    <Badge variant="outline" className="gap-1">
                      <CheckCircle className="w-3 h-3" />
                      {t('journals.openAccess')}
                    </Badge>
                  ) : (
                    <span className="text-muted-foreground text-sm">
                      {t('journals.subscription')}
                    </span>
                  )}
                </TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" asChild>
                    <a
                      href={journal.url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <ExternalLink className="w-4 h-4 mr-1" />
                      {t('journals.visit')}
                    </a>
                  </Button>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  )
}
