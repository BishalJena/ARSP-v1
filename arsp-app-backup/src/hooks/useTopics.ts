import { useQuery } from '@tanstack/react-query'
import { searchTopics } from '@/lib/api/topics'
import type { TopicSearchParams } from '@/types/topics'

export function useTopics(params: TopicSearchParams, enabled: boolean = true) {
  return useQuery({
    queryKey: ['topics', params.query, params.limit],
    queryFn: () => searchTopics(params),
    enabled: enabled && params.query.length > 0,
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
  })
}
