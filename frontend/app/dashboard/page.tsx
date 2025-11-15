'use client';

import { useAuth } from '@/lib/auth-context';
import { useLingo } from '@/lib/useLingo';
import { DashboardLayout } from '@/components/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TrendingUp, FileText, Shield, BookOpen, Building2, BarChart3 } from 'lucide-react';
import Link from 'next/link';

const features = [
  {
    titleKey: 'dashboard.topics',
    descKey: 'dashboard.topics_desc',
    icon: TrendingUp,
    href: '/dashboard/topics',
    color: 'text-blue-600',
    bgColor: 'bg-blue-50',
  },
  {
    titleKey: 'dashboard.papers',
    descKey: 'dashboard.papers_desc',
    icon: FileText,
    href: '/dashboard/papers',
    color: 'text-green-600',
    bgColor: 'bg-green-50',
  },
  {
    titleKey: 'dashboard.plagiarism',
    descKey: 'dashboard.plagiarism_desc',
    icon: Shield,
    href: '/dashboard/plagiarism',
    color: 'text-red-600',
    bgColor: 'bg-red-50',
  },
  {
    titleKey: 'dashboard.journals',
    descKey: 'dashboard.journals_desc',
    icon: BookOpen,
    href: '/dashboard/journals',
    color: 'text-purple-600',
    bgColor: 'bg-purple-50',
  },
  {
    titleKey: 'dashboard.government',
    descKey: 'dashboard.government_desc',
    icon: Building2,
    href: '/dashboard/government',
    color: 'text-orange-600',
    bgColor: 'bg-orange-50',
  },
  {
    titleKey: 'dashboard.impact',
    descKey: 'dashboard.impact_desc',
    icon: BarChart3,
    href: '/dashboard/impact',
    color: 'text-indigo-600',
    bgColor: 'bg-indigo-50',
  },
];

export default function DashboardPage() {
  const { user } = useAuth();
  const { t } = useLingo();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Welcome Section */}
        <div>
          <h2 className="text-3xl font-bold text-gray-900">
            {user?.full_name?.split(' ')[0]
              ? t('dashboard.welcome').replace('{name}', user.full_name.split(' ')[0])
              : t('dashboard.welcome_default')}
          </h2>
          <p className="text-gray-600 mt-2">
            {t('dashboard.tagline')}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="pb-3">
              <CardDescription>{t('dashboard.stats.active_projects')}</CardDescription>
              <CardTitle className="text-3xl">0</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {t('dashboard.stats.active_projects_hint')}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>{t('dashboard.stats.papers_analyzed')}</CardDescription>
              <CardTitle className="text-3xl">0</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {t('dashboard.stats.papers_analyzed_hint')}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardDescription>{t('dashboard.stats.plagiarism_checks')}</CardDescription>
              <CardTitle className="text-3xl">0</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                {t('dashboard.stats.plagiarism_checks_hint')}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Features Grid */}
        <div>
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            {t('dashboard.research_tools')}
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature) => {
              const Icon = feature.icon;
              return (
                <Link key={feature.href} href={feature.href}>
                  <Card className="hover:shadow-lg transition-shadow cursor-pointer h-full">
                    <CardHeader>
                      <div className={`w-12 h-12 rounded-lg ${feature.bgColor} flex items-center justify-center mb-3`}>
                        <Icon className={`h-6 w-6 ${feature.color}`} />
                      </div>
                      <CardTitle className="text-lg">{t(feature.titleKey)}</CardTitle>
                      <CardDescription>{t(feature.descKey)}</CardDescription>
                    </CardHeader>
                  </Card>
                </Link>
              );
            })}
          </div>
        </div>

        {/* Quick Start Guide */}
        <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
          <CardHeader>
            <CardTitle>{t('dashboard.getting_started.title')}</CardTitle>
            <CardDescription>
              {t('dashboard.getting_started.description')}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
                1
              </div>
              <div>
                <p className="font-medium">{t('dashboard.getting_started.step1_title')}</p>
                <p className="text-sm text-muted-foreground">
                  {t('dashboard.getting_started.step1_desc')}
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
                2
              </div>
              <div>
                <p className="font-medium">{t('dashboard.getting_started.step2_title')}</p>
                <p className="text-sm text-muted-foreground">
                  {t('dashboard.getting_started.step2_desc')}
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
                3
              </div>
              <div>
                <p className="font-medium">{t('dashboard.getting_started.step3_title')}</p>
                <p className="text-sm text-muted-foreground">
                  {t('dashboard.getting_started.step3_desc')}
                </p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-sm font-bold flex-shrink-0">
                4
              </div>
              <div>
                <p className="font-medium">{t('dashboard.getting_started.step4_title')}</p>
                <p className="text-sm text-muted-foreground">
                  {t('dashboard.getting_started.step4_desc')}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
