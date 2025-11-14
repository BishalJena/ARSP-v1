import { useState } from 'react'
import { ReviewUploader } from './ReviewUploader'
import { ReviewSummary } from './ReviewSummary'
import { InsightsList } from './InsightsList'
import { ReferenceExport } from './ReferenceExport'
import { useLingo } from '@/hooks/useLingo'
import type { LiteratureReview as LiteratureReviewType } from '@/types/literature'

export function LiteratureReview() {
  const [review, setReview] = useState<LiteratureReviewType | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const { t } = useLingo()

  const handleUploadComplete = async (fileUrls: string[]) => {
    setIsProcessing(true)

    // TODO: Call Supabase Edge Function to process files
    // For now, simulate processing with mock data
    await new Promise((resolve) => setTimeout(resolve, 2000))

    const mockReview: LiteratureReviewType = {
      id: '1',
      userId: 'user-1',
      title: 'Literature Review',
      summary:
        'This comprehensive literature review examines recent advances in machine learning and artificial intelligence. The papers collectively demonstrate significant progress in deep learning architectures, natural language processing, and computer vision applications. Key themes include the development of transformer-based models, improvements in training efficiency, and novel applications in healthcare and autonomous systems. The research highlights both the tremendous potential and current limitations of AI technologies, emphasizing the need for continued innovation in areas such as explainability, robustness, and ethical considerations.',
      insights: [
        'Transformer architectures have revolutionized natural language processing, achieving state-of-the-art results across multiple benchmarks and enabling more sophisticated language understanding capabilities.',
        'Transfer learning and pre-training strategies have significantly reduced the data requirements for training effective models, making AI more accessible for domain-specific applications.',
        'Attention mechanisms provide interpretability benefits by highlighting which parts of the input the model focuses on, though full explainability remains an open challenge.',
        'Recent advances in few-shot and zero-shot learning demonstrate promising directions for reducing annotation costs and improving model generalization.',
        'Ethical considerations around bias, fairness, and privacy are increasingly central to AI research, with growing emphasis on developing responsible AI systems.',
      ],
      references: [
        {
          title:
            'Attention Is All You Need',
          authors: ['Vaswani, A.', 'Shazeer, N.', 'Parmar, N.'],
          year: 2017,
          journal: 'Advances in Neural Information Processing Systems',
          doi: '10.48550/arXiv.1706.03762',
        },
        {
          title: 'BERT: Pre-training of Deep Bidirectional Transformers',
          authors: ['Devlin, J.', 'Chang, M.', 'Lee, K.'],
          year: 2019,
          journal: 'NAACL-HLT',
          doi: '10.18653/v1/N19-1423',
        },
        {
          title: 'Language Models are Few-Shot Learners',
          authors: ['Brown, T.', 'Mann, B.', 'Ryder, N.'],
          year: 2020,
          journal: 'Advances in Neural Information Processing Systems',
          doi: '10.48550/arXiv.2005.14165',
        },
      ],
      uploadedFiles: fileUrls,
      language: 'en',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }

    setReview(mockReview)
    setIsProcessing(false)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">
          {t('nav.literature')}
        </h1>
        <p className="mt-2 text-gray-600">{t('literature.subtitle')}</p>
      </div>

      {/* Uploader */}
      {!review && (
        <ReviewUploader
          onUploadComplete={handleUploadComplete}
          maxFiles={5}
          maxSizeMB={10}
        />
      )}

      {/* Processing State */}
      {isProcessing && (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">{t('literature.processing')}</p>
        </div>
      )}

      {/* Results */}
      {review && !isProcessing && (
        <div className="space-y-6">
          <ReviewSummary summary={review.summary} />
          <InsightsList insights={review.insights} />
          <ReferenceExport references={review.references} />

          {/* Start New Review */}
          <div className="text-center">
            <button
              onClick={() => setReview(null)}
              className="text-blue-600 hover:underline text-sm"
            >
              {t('literature.startNew')}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
