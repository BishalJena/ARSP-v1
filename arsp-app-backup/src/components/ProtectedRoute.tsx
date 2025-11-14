import type { ReactNode } from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { SignIn } from '@clerk/clerk-react'

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Loading...</div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <SignIn />
      </div>
    )
  }

  return <>{children}</>
}
