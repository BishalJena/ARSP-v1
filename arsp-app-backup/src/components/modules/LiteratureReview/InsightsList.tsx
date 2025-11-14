import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Lightbulb } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'

interface InsightsListProps {
  insights: string[]
}

export function InsightsList({ insights }: InsightsListProps) {
  const { t } = useLingo()

  if (insights.length === 0) {
    return null
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="w-5 h-5" />
          {t('literature.insights')} ({insights.length})
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Accordion type="single" collapsible className="w-full">
          {insights.map((insight, index) => (
            <AccordionItem key={index} value={`insight-${index}`}>
              <AccordionTrigger className="text-left">
                {t('literature.insightNumber', { number: index + 1 })}
              </AccordionTrigger>
              <AccordionContent>
                <p className="text-gray-700 leading-relaxed">{insight}</p>
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </CardContent>
    </Card>
  )
}
