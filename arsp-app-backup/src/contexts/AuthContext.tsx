import { createContext, useContext } from 'react'
import type { ReactNode } from 'react'
import { useUser, useAuth as useClerkAuth } from '@clerk/clerk-react'

interface AuthContextType {
  user: any
  isLoading: boolean
  isAuthenticated: boolean
  signOut: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const { user, isLoaded } = useUser()
  const { signOut } = useClerkAuth()

  const value = {
    user,
    isLoading: !isLoaded,
    isAuthenticated: !!user,
    signOut,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
