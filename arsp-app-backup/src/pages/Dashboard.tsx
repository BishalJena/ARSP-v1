import { useAuth } from '@/contexts/AuthContext'
import { useLingo } from '@/hooks/useLingo'
import { Search, FileText, CheckCircle, BookOpen } from 'lucide-react'
import { Link } from 'react-router-dom'

const features = [
  {
    titleKey: 'nav.topics',
    descriptionKey: 'dashboard.topicsDesc',
    icon: Search,
    path: '/topics',
    color: 'bg-blue-50 text-blue-600',
  },
  {
    titleKey: 'nav.literature',
    descriptionKey: 'dashboard.literatureDesc',
    icon: FileText,
    path: '/literature',
    color: 'bg-green-50 text-green-600',
  },
  {
    titleKey: 'nav.plagiarism',
    descriptionKey: 'dashboard.plagiarismDesc',
    icon: CheckCircle,
    path: '/plagiarism',
    color: 'bg-purple-50 text-purple-600',
  },
  {
    titleKey: 'nav.journals',
    descriptionKey: 'dashboard.journalsDesc',
    icon: BookOpen,
    path: '/journals',
    color: 'bg-orange-50 text-orange-600',
  },
]

export function Dashboard() {
  const { user } = useAuth()
  const { t } = useLingo()

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          {t('dashboard.welcome', { name: user?.firstName || 'Researcher' })}
        </h1>
        <p className="mt-2 text-gray-600">
          {t('dashboard.subtitle')}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon
          return (
            <Link
              key={feature.path}
              to={feature.path}
              className="bg-white rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow border border-gray-200"
            >
              <div className={`w-12 h-12 rounded-lg ${feature.color} flex items-center justify-center mb-4`}>
                <Icon className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {t(feature.titleKey)}
              </h3>
              <p className="text-gray-600">{t(feature.descriptionKey)}</p>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
