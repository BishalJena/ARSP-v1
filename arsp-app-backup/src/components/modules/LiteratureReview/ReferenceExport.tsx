import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Download, BookOpen } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'
import type { Reference } from '@/types/literature'

interface ReferenceExportProps {
  references: Reference[]
}

export function ReferenceExport({ references }: ReferenceExportProps) {
  const { t } = useLingo()

  const exportToZotero = () => {
    // Convert references to Zotero JSON format
    const zoteroData = references.map((ref) => ({
      itemType: 'journalArticle',
      title: ref.title,
      creators: ref.authors.map((author) => ({
        creatorType: 'author',
        name: author,
      })),
      date: ref.year.toString(),
      publicationTitle: ref.journal || '',
      DOI: ref.doi || '',
      url: ref.url || '',
    }))

    // Create and download JSON file
    const blob = new Blob([JSON.stringify(zoteroData, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `references-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (references.length === 0) {
    return null
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            {t('literature.references')} ({references.length})
          </CardTitle>
          <Button onClick={exportToZotero} variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            {t('literature.exportZotero')}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {references.map((ref, index) => (
            <div key={index} className="border-l-2 border-blue-500 pl-4">
              <p className="font-medium text-gray-900">{ref.title}</p>
              <p className="text-sm text-gray-600 mt-1">
                {ref.authors.join(', ')} ({ref.year})
              </p>
              {ref.journal && (
                <p className="text-sm text-gray-500 italic mt-1">
                  {ref.journal}
                </p>
              )}
              {ref.doi && (
                <p className="text-xs text-blue-600 mt-1">DOI: {ref.doi}</p>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
