export interface FlaggedSection {
  text: string
  startIndex: number
  endIndex: number
  similarity: number
  source?: string
}

export interface CitationSuggestion {
  doi: string
  title: string
  authors: string[]
  year: number
  relevance: number
  snippet: string
  url?: string
}

export interface PlagiarismResult {
  originality: number // 0-100
  flaggedSections: FlaggedSection[]
  citations: CitationSuggestion[]
  lastChecked: Date
}

export interface Draft {
  id: string
  userId: string
  title?: string
  content: string
  plagiarismScore?: number
  lastCheckedAt?: string
  createdAt: string
  updatedAt: string
}
