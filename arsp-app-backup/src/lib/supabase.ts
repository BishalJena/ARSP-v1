import { createClient } from '@supabase/supabase-js'
import { useAuth as useClerkAuth } from '@clerk/clerk-react'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

export function useSupabaseClient() {
  const { getToken } = useClerkAuth()

  const getAuthHeaders = async () => {
    const token = await getToken({ template: 'supabase' })
    return token ? { Authorization: `Bearer ${token}` } : {}
  }

  const supabaseWithAuth = createClient(supabaseUrl, supabaseAnonKey, {
    global: {
      headers: getAuthHeaders as any, // Type workaround for Supabase client
    },
  })

  return supabaseWithAuth
}
