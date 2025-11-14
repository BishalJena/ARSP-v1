import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Shield, AlertTriangle, CheckCircle } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'

interface ScoreDisplayProps {
  score: number // 0-100
  lastChecked?: Date
}

export function ScoreDisplay({ score, lastChecked }: ScoreDisplayProps) {
  const { t } = useLingo()

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreIcon = (score: number) => {
    if (score >= 80)
      return <CheckCircle className="w-8 h-8 text-green-600" />
    if (score >= 60)
      return <AlertTriangle className="w-8 h-8 text-yellow-600" />
    return <AlertTriangle className="w-8 h-8 text-red-600" />
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return t('plagiarism.scoreExcellent')
    if (score >= 60) return t('plagiarism.scoreGood')
    return t('plagiarism.scorePoor')
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Shield className="w-5 h-5" />
          {t('plagiarism.originalityScore')}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              {getScoreIcon(score)}
              <div>
                <div className={`text-4xl font-bold ${getScoreColor(score)}`}>
                  {score}%
                </div>
                <div className="text-sm text-muted-foreground">
                  {getScoreLabel(score)}
                </div>
              </div>
            </div>
          </div>

          <Progress value={score} className="h-2" />

          {lastChecked && (
            <p className="text-xs text-muted-foreground">
              {t('plagiarism.lastChecked')}:{' '}
              {lastChecked.toLocaleString()}
            </p>
          )}

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm text-blue-900">
              {score >= 80 && t('plagiarism.scoreExcellentDesc')}
              {score >= 60 && score < 80 && t('plagiarism.scoreGoodDesc')}
              {score < 60 && t('plagiarism.scorePoorDesc')}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
