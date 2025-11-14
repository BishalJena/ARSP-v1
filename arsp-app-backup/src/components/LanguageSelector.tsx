import { Globe } from 'lucide-react'
import { useLanguage } from '@/contexts/LanguageContext'
import { supportedLanguages } from '@/lib/lingo'

export function LanguageSelector() {
  const { currentLanguage, setLanguage } = useLanguage()

  return (
    <div className="relative inline-block">
      <select
        value={currentLanguage}
        onChange={(e) => setLanguage(e.target.value)}
        className="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {supportedLanguages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>
      <Globe className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
    </div>
  )
}
