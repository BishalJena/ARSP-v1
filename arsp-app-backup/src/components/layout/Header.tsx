import { UserButton } from '@clerk/clerk-react'
import { LanguageSelector } from '../LanguageSelector'
import { Menu } from 'lucide-react'
import { Link } from 'react-router-dom'

interface HeaderProps {
  onMenuClick: () => void
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label="Toggle menu"
          >
            <Menu className="w-5 h-5 text-gray-600" />
          </button>
          <Link to="/" className="text-2xl font-bold text-blue-600">
            ARSP
          </Link>
        </div>
        <div className="flex items-center gap-4">
          <LanguageSelector />
          <UserButton afterSignOutUrl="/" />
        </div>
      </div>
    </header>
  )
}
