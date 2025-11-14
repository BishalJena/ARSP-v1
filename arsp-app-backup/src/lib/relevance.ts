/**
 * Calculate relevance score between a query and a topic
 * Uses keyword matching with weighted scoring
 * Returns a score between 0-100
 */
export function calculateRelevanceScore(
  query: string,
  topicTitle: string,
  topicAbstract: string
): number {
  const queryTerms = tokenize(query.toLowerCase())
  const titleTerms = tokenize(topicTitle.toLowerCase())
  const abstractTerms = tokenize(topicAbstract.toLowerCase())

  if (queryTerms.length === 0) return 0

  let matchedTerms = 0
  let titleMatches = 0
  let abstractMatches = 0
  let partialMatches = 0

  for (const term of queryTerms) {
    let matched = false

    // Exact title match (highest weight)
    if (titleTerms.includes(term)) {
      titleMatches++
      matched = true
    }
    // Exact abstract match
    else if (abstractTerms.includes(term)) {
      abstractMatches++
      matched = true
    }
    // Partial title match
    else if (titleTerms.some((t) => t.includes(term) || term.includes(t))) {
      partialMatches++
      matched = true
    }
    // Partial abstract match
    else if (abstractTerms.some((t) => t.includes(term) || term.includes(t))) {
      partialMatches += 0.5
      matched = true
    }

    if (matched) matchedTerms++
  }

  // Calculate score with weighted components
  const matchRatio = matchedTerms / queryTerms.length
  const titleWeight = (titleMatches / queryTerms.length) * 0.5
  const abstractWeight = (abstractMatches / queryTerms.length) * 0.3
  const partialWeight = (partialMatches / queryTerms.length) * 0.2

  const score = (matchRatio * 50) + (titleWeight * 100) + (abstractWeight * 100) + (partialWeight * 100)
  
  return Math.min(100, Math.round(score))
}

/**
 * Tokenize text into words, removing common stop words
 */
function tokenize(text: string): string[] {
  const stopWords = new Set([
    'a',
    'an',
    'and',
    'are',
    'as',
    'at',
    'be',
    'by',
    'for',
    'from',
    'has',
    'he',
    'in',
    'is',
    'it',
    'its',
    'of',
    'on',
    'that',
    'the',
    'to',
    'was',
    'will',
    'with',
  ])

  return text
    .split(/\W+/)
    .filter((word) => word.length > 2 && !stopWords.has(word))
}

/**
 * Calculate average relevance score for a set of topics
 */
export function calculateAverageRelevance(
  query: string,
  topics: Array<{ title: string; brief: string }>
): number {
  if (topics.length === 0) return 0

  const scores = topics.map((topic) =>
    calculateRelevanceScore(query, topic.title, topic.brief)
  )

  const average = scores.reduce((sum, score) => sum + score, 0) / scores.length
  return Math.round(average)
}

/**
 * Check if relevance meets the 80% accuracy threshold
 */
export function meetsAccuracyThreshold(relevanceScore: number): boolean {
  return relevanceScore >= 80
}
