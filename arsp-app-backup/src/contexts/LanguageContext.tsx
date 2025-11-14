import { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'

interface LanguageContextType {
  currentLanguage: string
  setLanguage: (lang: string) => void
}

const LanguageContext = createContext<LanguageContextType | undefined>(
  undefined
)

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [currentLanguage, setCurrentLanguage] = useState(() => {
    return localStorage.getItem('preferred_language') || 'en'
  })

  useEffect(() => {
    localStorage.setItem('preferred_language', currentLanguage)
  }, [currentLanguage])

  return (
    <LanguageContext.Provider
      value={{ currentLanguage, setLanguage: setCurrentLanguage }}
    >
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider')
  }
  return context
}
