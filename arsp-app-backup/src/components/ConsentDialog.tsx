import { useState, useEffect } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/contexts/AuthContext'
import { useLingo } from '@/hooks/useLingo'
import { useSupabaseClient } from '@/lib/supabase'

const CONSENT_KEY = 'arsp_consent_accepted'

export function ConsentDialog() {
  const [open, setOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { user } = useAuth()
  const { t } = useLingo()
  const supabase = useSupabaseClient()

  useEffect(() => {
    // Check if user has already consented
    const hasConsented = localStorage.getItem(CONSENT_KEY)
    if (!hasConsented && user) {
      setOpen(true)
    }
  }, [user])

  const handleAccept = async () => {
    if (!user) return

    setIsLoading(true)
    try {
      // Log consent to database
      const { error } = await supabase.from('consent_logs').insert({
        user_id: user.id,
        consent_type: 'data_usage',
        consent_given: true,
        ip_address: null, // Could be captured if needed
        user_agent: navigator.userAgent,
      })

      if (error) {
        console.error('Error logging consent:', error)
      }

      // Store in localStorage to prevent repeated prompts
      localStorage.setItem(CONSENT_KEY, 'true')
      setOpen(false)
    } catch (error) {
      console.error('Error accepting consent:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={() => {}}>
      <DialogContent className="sm:max-w-[600px] [&>button]:hidden">
        <DialogHeader>
          <DialogTitle className="text-2xl">
            {t('consent.title')}
          </DialogTitle>
          <DialogDescription className="text-base pt-4 space-y-4">
            <p>{t('consent.intro')}</p>
            
            <div className="space-y-2">
              <h4 className="font-semibold text-gray-900">
                {t('consent.dataCollectionTitle')}
              </h4>
              <ul className="list-disc list-inside space-y-1 text-sm">
                <li>{t('consent.dataCollection1')}</li>
                <li>{t('consent.dataCollection2')}</li>
                <li>{t('consent.dataCollection3')}</li>
                <li>{t('consent.dataCollection4')}</li>
              </ul>
            </div>

            <div className="space-y-2">
              <h4 className="font-semibold text-gray-900">
                {t('consent.dataUsageTitle')}
              </h4>
              <ul className="list-disc list-inside space-y-1 text-sm">
                <li>{t('consent.dataUsage1')}</li>
                <li>{t('consent.dataUsage2')}</li>
                <li>{t('consent.dataUsage3')}</li>
              </ul>
            </div>

            <div className="space-y-2">
              <h4 className="font-semibold text-gray-900">
                {t('consent.yourRightsTitle')}
              </h4>
              <p className="text-sm">{t('consent.yourRights')}</p>
            </div>

            <p className="text-sm font-medium text-gray-900">
              {t('consent.dpdpCompliance')}
            </p>
          </DialogDescription>
        </DialogHeader>
        <DialogFooter className="flex-col sm:flex-row gap-2">
          <Button
            onClick={handleAccept}
            disabled={isLoading}
            className="w-full sm:w-auto"
          >
            {isLoading ? t('common.loading') : t('consent.accept')}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
