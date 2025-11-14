import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertCircle } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'
import type { FlaggedSection } from '@/types/plagiarism'

interface FlaggedSectionsProps {
  sections: FlaggedSection[]
}

export function FlaggedSections({ sections }: FlaggedSectionsProps) {
  const { t } = useLingo()

  if (sections.length === 0) {
    return null
  }

  const getSimilarityColor = (similarity: number) => {
    if (similarity >= 80) return 'destructive'
    if (similarity >= 50) return 'default'
    return 'secondary'
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertCircle className="w-5 h-5" />
          {t('plagiarism.flaggedSections')} ({sections.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {sections.map((section, index) => (
            <div
              key={index}
              className="border-l-4 border-red-500 pl-4 py-2 bg-red-50 rounded-r"
            >
              <div className="flex items-start justify-between gap-2 mb-2">
                <Badge variant={getSimilarityColor(section.similarity)}>
                  {section.similarity}% {t('plagiarism.similar')}
                </Badge>
                {section.source && (
                  <span className="text-xs text-muted-foreground">
                    {t('plagiarism.source')}: {section.source}
                  </span>
                )}
              </div>
              <p className="text-sm text-gray-700 italic">"{section.text}"</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
