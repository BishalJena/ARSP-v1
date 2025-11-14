import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Loader2, Search } from 'lucide-react'
import { DraftEditor } from './DraftEditor'
import { ScoreDisplay } from './ScoreDisplay'
import { FlaggedSections } from './FlaggedSections'
import { CitationSuggestions } from './CitationSuggestions'
import { useLingo } from '@/hooks/useLingo'
import type { PlagiarismResult } from '@/types/plagiarism'

export function PlagiarismCheck() {
  const [content, setContent] = useState('')
  const [result, setResult] = useState<PlagiarismResult | null>(null)
  const [isChecking, setIsChecking] = useState(false)
  const { t } = useLingo()

  const handleCheck = async () => {
    if (!content.trim()) return

    setIsChecking(true)

    // TODO: Call Supabase Edge Function for plagiarism check
    // For now, simulate with mock data
    await new Promise((resolve) => setTimeout(resolve, 2000))

    const mockResult: PlagiarismResult = {
      originality: 75,
      flaggedSections: [
        {
          text: 'Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience.',
          startIndex: 0,
          endIndex: 120,
          similarity: 85,
          source: 'Wikipedia - Machine Learning',
        },
        {
          text: 'Deep learning algorithms use neural networks with multiple layers to progressively extract higher-level features.',
          startIndex: 200,
          endIndex: 310,
          similarity: 65,
          source: 'Nature - Deep Learning Review',
        },
      ],
      citations: [
        {
          doi: '10.1038/nature14539',
          title: 'Deep learning',
          authors: ['LeCun, Y.', 'Bengio, Y.', 'Hinton, G.'],
          year: 2015,
          relevance: 92,
          snippet:
            'Deep learning allows computational models composed of multiple processing layers...',
          url: 'https://doi.org/10.1038/nature14539',
        },
        {
          doi: '10.1126/science.aaa8415',
          title: 'Machine learning: Trends, perspectives, and prospects',
          authors: ['Jordan, M.I.', 'Mitchell, T.M.'],
          year: 2015,
          relevance: 88,
          snippet:
            'Machine learning addresses the question of how to build computers that improve automatically...',
          url: 'https://doi.org/10.1126/science.aaa8415',
        },
        {
          doi: '10.1145/3065386',
          title: 'ImageNet classification with deep convolutional neural networks',
          authors: ['Krizhevsky, A.', 'Sutskever, I.', 'Hinton, G.E.'],
          year: 2017,
          relevance: 75,
          snippet:
            'We trained a large, deep convolutional neural network to classify images...',
          url: 'https://doi.org/10.1145/3065386',
        },
      ],
      lastChecked: new Date(),
    }

    setResult(mockResult)
    setIsChecking(false)
  }

  const handleSave = async (title: string, content: string) => {
    // TODO: Save to Supabase drafts table
    console.log('Saving draft:', { title, content })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {t('nav.plagiarism')}
        </h1>
        <p className="mt-2 text-gray-600">{t('plagiarism.subtitle')}</p>
      </div>

      {/* Editor */}
      <DraftEditor
        onContentChange={setContent}
        onSave={handleSave}
      />

      {/* Check Button */}
      <div className="flex justify-center">
        <Button
          onClick={handleCheck}
          disabled={isChecking || !content.trim()}
          size="lg"
        >
          {isChecking ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              {t('plagiarism.checking')}
            </>
          ) : (
            <>
              <Search className="w-5 h-5 mr-2" />
              {t('plagiarism.checkNow')}
            </>
          )}
        </Button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          <ScoreDisplay
            score={result.originality}
            lastChecked={result.lastChecked}
          />
          <FlaggedSections sections={result.flaggedSections} />
          <CitationSuggestions suggestions={result.citations} />
        </div>
      )}
    </div>
  )
}
