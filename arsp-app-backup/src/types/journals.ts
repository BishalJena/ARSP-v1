export interface Journal {
  id: string
  name: string
  description: string
  impactFactor: number
  hIndex: number
  isOpenAccess: boolean
  publicationTimeMonths: number
  fitScore?: number // 0-100, calculated based on abstract match
  domain: string
  url: string
}

export interface JournalFilters {
  openAccessOnly?: boolean
  minImpactFactor?: number
  maxPublicationTime?: number
  domain?: string
  searchQuery?: string
}

export type SortField = 'name' | 'impactFactor' | 'fitScore' | 'publicationTimeMonths'
export type SortDirection = 'asc' | 'desc'
