import { useState, useCallback } from 'react'
import { Upload, FileText, X, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { useLingo } from '@/hooks/useLingo'
import type { UploadProgress } from '@/types/literature'

interface ReviewUploaderProps {
  onUploadComplete: (fileUrls: string[]) => void
  maxFiles?: number
  maxSizeMB?: number
}

export function ReviewUploader({
  onUploadComplete,
  maxFiles = 5,
  maxSizeMB = 10,
}: ReviewUploaderProps) {
  const [files, setFiles] = useState<File[]>([])
  const [uploadProgress, setUploadProgress] = useState<
    Record<string, UploadProgress>
  >({})
  const [isDragging, setIsDragging] = useState(false)
  const { t } = useLingo()

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragging(false)

      const droppedFiles = Array.from(e.dataTransfer.files).filter(
        (file) => file.type === 'application/pdf'
      )

      if (files.length + droppedFiles.length > maxFiles) {
        alert(t('literature.maxFilesError', { max: maxFiles }))
        return
      }

      const validFiles = droppedFiles.filter((file) => {
        const sizeMB = file.size / (1024 * 1024)
        if (sizeMB > maxSizeMB) {
          alert(
            t('literature.fileTooLarge', {
              name: file.name,
              max: maxSizeMB,
            })
          )
          return false
        }
        return true
      })

      setFiles((prev) => [...prev, ...validFiles])
    },
    [files.length, maxFiles, maxSizeMB, t]
  )

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || [])

    if (files.length + selectedFiles.length > maxFiles) {
      alert(t('literature.maxFilesError', { max: maxFiles }))
      return
    }

    const validFiles = selectedFiles.filter((file) => {
      const sizeMB = file.size / (1024 * 1024)
      if (sizeMB > maxSizeMB) {
        alert(
          t('literature.fileTooLarge', {
            name: file.name,
            max: maxSizeMB,
          })
        )
        return false
      }
      return true
    })

    setFiles((prev) => [...prev, ...validFiles])
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleUpload = async () => {
    // TODO: Implement actual upload to Supabase
    // For now, simulate upload progress
    const fileUrls: string[] = []

    for (const file of files) {
      setUploadProgress((prev) => ({
        ...prev,
        [file.name]: {
          fileName: file.name,
          progress: 0,
          status: 'uploading',
        },
      }))

      // Simulate upload progress
      for (let i = 0; i <= 100; i += 10) {
        await new Promise((resolve) => setTimeout(resolve, 100))
        setUploadProgress((prev) => ({
          ...prev,
          [file.name]: {
            ...prev[file.name],
            progress: i,
          },
        }))
      }

      setUploadProgress((prev) => ({
        ...prev,
        [file.name]: {
          ...prev[file.name],
          status: 'complete',
        },
      }))

      fileUrls.push(`/uploads/${file.name}`)
    }

    onUploadComplete(fileUrls)
  }

  const isUploading = Object.values(uploadProgress).some(
    (p) => p.status === 'uploading' || p.status === 'processing'
  )

  return (
    <div className="space-y-4">
      {/* Drop Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${
            isDragging
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-gray-400'
          }
        `}
      >
        <Upload className="w-12 h-12 mx-auto text-gray-400 mb-4" />
        <p className="text-lg font-medium text-gray-700 mb-2">
          {t('literature.dropZoneTitle')}
        </p>
        <p className="text-sm text-gray-500 mb-4">
          {t('literature.dropZoneSubtitle', { max: maxFiles, size: maxSizeMB })}
        </p>
        <label htmlFor="file-upload">
          <Button type="button" variant="outline" asChild>
            <span className="cursor-pointer">
              {t('literature.browseFiles')}
            </span>
          </Button>
        </label>
        <input
          id="file-upload"
          type="file"
          accept=".pdf"
          multiple
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-2">
          <h3 className="font-medium text-gray-900">
            {t('literature.selectedFiles')} ({files.length}/{maxFiles})
          </h3>
          {files.map((file, index) => (
            <div
              key={`${file.name}-${index}`}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
            >
              <FileText className="w-5 h-5 text-gray-500 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {file.name}
                </p>
                <p className="text-xs text-gray-500">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB
                </p>
                {uploadProgress[file.name] && (
                  <div className="mt-2">
                    <Progress value={uploadProgress[file.name].progress} />
                    <p className="text-xs text-gray-500 mt-1">
                      {uploadProgress[file.name].status === 'uploading' &&
                        t('common.uploading')}
                      {uploadProgress[file.name].status === 'processing' &&
                        t('common.processing')}
                      {uploadProgress[file.name].status === 'complete' &&
                        t('common.complete')}
                    </p>
                  </div>
                )}
              </div>
              {!uploadProgress[file.name] && (
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => removeFile(index)}
                >
                  <X className="w-4 h-4" />
                </Button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Upload Button */}
      {files.length > 0 && (
        <Button
          onClick={handleUpload}
          disabled={isUploading}
          className="w-full"
        >
          {isUploading ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              {t('common.processing')}
            </>
          ) : (
            t('literature.uploadAndAnalyze')
          )}
        </Button>
      )}
    </div>
  )
}
