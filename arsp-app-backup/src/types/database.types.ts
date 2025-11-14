export interface Profile {
  id: string
  email: string
  full_name: string | null
  discipline: string | null
  institution: string | null
  publication_count: number
  preferred_language: string
  created_at: string
  updated_at: string
}

export interface Draft {
  id: string
  user_id: string
  title: string | null
  content: string
  plagiarism_score: number | null
  last_checked_at: string | null
  created_at: string
  updated_at: string
}

export interface LiteratureReview {
  id: string
  user_id: string
  title: string | null
  summary: string
  insights: string[]
  references: any[]
  language: string
  created_at: string
  updated_at: string
}

export interface Journal {
  id: string
  name: string
  description: string | null
  impact_factor: number
  h_index: number | null
  is_open_access: boolean
  publication_time_months: number | null
  domain: string
  url: string | null
  created_at: string
}
