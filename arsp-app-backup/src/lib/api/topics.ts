import type { Topic, TopicSearchParams, TopicSearchResponse } from '@/types/topics'

// Semantic Scholar API endpoint
const SEMANTIC_SCHOLAR_API = 'https://api.semanticscholar.org/graph/v1'

/**
 * Search for research topics using Semantic Scholar API
 * Note: In production, this should go through a backend API that handles
 * Lingo translation and rate limiting
 */
export async function searchTopics(
  params: TopicSearchParams
): Promise<TopicSearchResponse> {
  const { query, limit = 5 } = params

  try {
    // Search for papers related to the query
    const response = await fetch(
      `${SEMANTIC_SCHOLAR_API}/paper/search?query=${encodeURIComponent(query)}&limit=${limit}&fields=title,abstract,authors,year,citationCount,url,externalIds`,
      {
        headers: {
          'Accept': 'application/json',
        },
      }
    )

    if (!response.ok) {
      throw new Error(`Semantic Scholar API error: ${response.statusText}`)
    }

    const data = await response.json()

    // Transform Semantic Scholar response to our Topic format
    const topics: Topic[] = (data.data || []).map((paper: any) => ({
      id: paper.paperId || paper.externalIds?.ArXiv || `ss-${Date.now()}-${Math.random()}`,
      title: paper.title || 'Untitled',
      brief: paper.abstract || 'No abstract available',
      impactScore: calculateImpactScore(paper.citationCount, paper.year),
      source: 'semantic_scholar' as const,
      url: paper.url || `https://www.semanticscholar.org/paper/${paper.paperId}`,
      authors: paper.authors?.map((a: any) => a.name) || [],
      year: paper.year,
      citationCount: paper.citationCount || 0,
    }))

    return {
      topics,
      totalCount: data.total || topics.length,
      query,
    }
  } catch (error) {
    console.error('Error fetching topics:', error)
    throw error
  }
}

/**
 * Calculate impact score based on citations and recency
 * Score = (citations / age_factor) normalized to 0-100
 */
function calculateImpactScore(citations: number = 0, year?: number): number {
  const currentYear = new Date().getFullYear()
  const age = year ? currentYear - year + 1 : 5 // Default to 5 years if no year
  
  // Newer papers get a boost
  const ageFactor = Math.max(1, age / 2)
  const rawScore = citations / ageFactor
  
  // Normalize to 0-100 scale (assuming 100+ citations/year is top tier)
  const normalized = Math.min(100, (rawScore / 100) * 100)
  
  return Math.round(normalized)
}
