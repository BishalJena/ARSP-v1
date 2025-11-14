import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'

interface ReviewSummaryProps {
  summary: string
  title?: string
}

export function ReviewSummary({ summary, title }: ReviewSummaryProps) {
  const { t } = useLingo()

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="w-5 h-5" />
          {title || t('literature.summary')}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
          {summary}
        </p>
      </CardContent>
    </Card>
  )
}
