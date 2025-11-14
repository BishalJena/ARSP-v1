export interface Reference {
  doi?: string
  title: string
  authors: string[]
  year: number
  journal?: string
  url?: string
}

export interface LiteratureReview {
  id: string
  userId: string
  title?: string
  summary: string
  insights: string[]
  references: Reference[]
  uploadedFiles: string[]
  language: string
  createdAt: string
  updatedAt: string
}

export interface UploadProgress {
  fileName: string
  progress: number
  status: 'uploading' | 'processing' | 'complete' | 'error'
  error?: string
}
