import { useLanguage } from '@/contexts/LanguageContext'
import { useCallback } from 'react'
import enTranslations from '@/locales/en.json'

// Cache for loaded translations
const translationCache: Record<string, Record<string, any>> = {
  en: enTranslations,
}

export function useLingo() {
  const { currentLanguage } = useLanguage()

  // Simple translation function that reads from locale files
  const t = useCallback(
    (key: string, params?: Record<string, string | number>): string => {
      // Get locale, fallback to English
      const locale = translationCache[currentLanguage] || translationCache['en']
      
      // Navigate nested keys (e.g., "nav.dashboard")
      const keys = key.split('.')
      let value: any = locale
      
      for (const k of keys) {
        if (value && typeof value === 'object') {
          value = value[k]
        } else {
          return key // Return key if translation not found
        }
      }

      // Replace parameters if provided
      if (params && typeof value === 'string') {
        return Object.entries(params).reduce(
          (str, [paramKey, paramValue]) =>
            str.replace(`{${paramKey}}`, String(paramValue)),
          value
        )
      }

      return typeof value === 'string' ? value : key
    },
    [currentLanguage]
  )

  // Pluralization function
  const pluralize = useCallback(
    (count: number, key: string): string => {
      const singular = t(`${key}.singular`)
      const plural = t(`${key}.plural`)
      
      return count === 1 ? singular : plural
    },
    [t]
  )

  return {
    t,
    pluralize,
    currentLanguage,
  }
}
