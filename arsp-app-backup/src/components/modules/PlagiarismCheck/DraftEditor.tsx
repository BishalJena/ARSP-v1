import { useState, useEffect } from 'react'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText, Save, Loader2 } from 'lucide-react'
import { useLingo } from '@/hooks/useLingo'
import { useDebounce } from '@/hooks/useDebounce'

interface DraftEditorProps {
  initialContent?: string
  initialTitle?: string
  onContentChange: (content: string) => void
  onSave?: (title: string, content: string) => Promise<void>
  isSaving?: boolean
}

export function DraftEditor({
  initialContent = '',
  initialTitle = '',
  onContentChange,
  onSave,
  isSaving = false,
}: DraftEditorProps) {
  const [title, setTitle] = useState(initialTitle)
  const [content, setContent] = useState(initialContent)
  const [lastSaved, setLastSaved] = useState<Date | null>(null)
  const { t } = useLingo()

  // Debounce content changes for auto-save
  const debouncedContent = useDebounce(content, 2000)

  useEffect(() => {
    onContentChange(content)
  }, [content, onContentChange])

  // Auto-save effect
  useEffect(() => {
    if (debouncedContent && debouncedContent !== initialContent && onSave) {
      handleAutoSave()
    }
  }, [debouncedContent])

  const handleAutoSave = async () => {
    if (onSave) {
      try {
        await onSave(title, content)
        setLastSaved(new Date())
      } catch (error) {
        console.error('Auto-save failed:', error)
      }
    }
  }

  const handleManualSave = async () => {
    if (onSave) {
      try {
        await onSave(title, content)
        setLastSaved(new Date())
      } catch (error) {
        console.error('Save failed:', error)
      }
    }
  }

  const wordCount = content.trim().split(/\s+/).filter(Boolean).length
  const charCount = content.length

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5" />
            {t('plagiarism.draftEditor')}
          </CardTitle>
          <div className="flex items-center gap-2">
            {lastSaved && (
              <span className="text-xs text-muted-foreground">
                {t('plagiarism.lastSaved')}:{' '}
                {lastSaved.toLocaleTimeString()}
              </span>
            )}
            {onSave && (
              <Button
                onClick={handleManualSave}
                disabled={isSaving}
                size="sm"
                variant="outline"
              >
                {isSaving ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    {t('common.saving')}
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4 mr-2" />
                    {t('common.save')}
                  </>
                )}
              </Button>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <label
            htmlFor="draft-title"
            className="text-sm font-medium text-gray-700 mb-1 block"
          >
            {t('plagiarism.title')}
          </label>
          <Input
            id="draft-title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder={t('plagiarism.titlePlaceholder')}
          />
        </div>

        <div>
          <label
            htmlFor="draft-content"
            className="text-sm font-medium text-gray-700 mb-1 block"
          >
            {t('plagiarism.content')}
          </label>
          <Textarea
            id="draft-content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={t('plagiarism.contentPlaceholder')}
            className="min-h-[400px] font-mono text-sm"
          />
        </div>

        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>
            {t('plagiarism.wordCount')}: {wordCount}
          </span>
          <span>
            {t('plagiarism.charCount')}: {charCount}
          </span>
        </div>
      </CardContent>
    </Card>
  )
}
