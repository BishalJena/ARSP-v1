'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth-context';
import { useLingo } from '@/lib/useLingo';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { AlertCircle } from 'lucide-react';

interface ConsentDialogProps {
  onConsent: (accepted: boolean) => void;
}

export function ConsentDialog({ onConsent }: ConsentDialogProps) {
  const [open, setOpen] = useState(false);
  const { user } = useAuth();
  const { t } = useLingo();

  useEffect(() => {
    // Check if user has already given consent
    const hasConsented = localStorage.getItem('dpdp_consent');
    if (!hasConsented && user) {
      setOpen(true);
    }
  }, [user]);

  const handleAccept = async () => {
    try {
      // Log consent to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/consent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user?.id,
          accepted: true,
          timestamp: new Date().toISOString(),
        }),
      });

      if (response.ok) {
        localStorage.setItem('dpdp_consent', 'true');
        setOpen(false);
        onConsent(true);
      }
    } catch (error) {
      console.error('Failed to log consent:', error);
    }
  };

  const handleDecline = () => {
    localStorage.setItem('dpdp_consent', 'false');
    setOpen(false);
    onConsent(false);
    // Optionally redirect to logout or info page
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-[550px]" onInteractOutside={(e) => e.preventDefault()}>
        <DialogHeader>
          <div className="flex items-center gap-2 text-blue-600 mb-2">
            <AlertCircle className="h-5 w-5" />
            <DialogTitle>{t('consent.title')}</DialogTitle>
          </div>
          <DialogDescription className="text-base">
            {t('consent.description')}
          </DialogDescription>
        </DialogHeader>

        <div className="py-4 space-y-4 text-sm text-gray-700">
          <p>{t('consent.message')}</p>

          <div className="bg-gray-50 p-4 rounded-lg space-y-2">
            <h4 className="font-semibold">What data we collect:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Research papers and manuscripts you upload</li>
              <li>Search queries and topic preferences</li>
              <li>Plagiarism check results</li>
              <li>Journal recommendations history</li>
              <li>Usage analytics and performance metrics</li>
            </ul>
          </div>

          <div className="bg-gray-50 p-4 rounded-lg space-y-2">
            <h4 className="font-semibold">Your rights under DPDP Act, 2023:</h4>
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Right to access your data</li>
              <li>Right to correction and erasure</li>
              <li>Right to withdraw consent</li>
              <li>Right to nominate a representative</li>
            </ul>
          </div>

          <p className="text-xs text-muted-foreground italic">
            By clicking "I Accept", you acknowledge that you have read and understood this
            consent notice and agree to the collection and processing of your data as
            described above.
          </p>
        </div>

        <DialogFooter className="flex gap-2 sm:gap-0">
          <Button variant="outline" onClick={handleDecline}>
            {t('consent.decline')}
          </Button>
          <Button onClick={handleAccept}>{t('consent.accept')}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
