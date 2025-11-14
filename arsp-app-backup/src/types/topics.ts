export interface Topic {
  id: string
  title: string
  brief: string
  impactScore: number
  source: 'arxiv' | 'semantic_scholar'
  url: string
  authors?: string[]
  year?: number
  citationCount?: number
}

export interface TopicSearchParams {
  query: string
  limit?: number
}

export interface TopicSearchResponse {
  topics: Topic[]
  totalCount: number
  query: string
}
