'use client';

import { useLingo } from '@/lib/useLingo';
import { getLanguageName, getLanguageFlag, supportedLocales } from '@/lib/lingo-config';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Button } from '@/components/ui/button';
import { Globe } from 'lucide-react';

export function LanguageSelector() {
  const { locale, setLocale, t } = useLingo();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size="sm" className="gap-2">
          <Globe className="h-4 w-4" />
          <span className="hidden sm:inline-block">
            {getLanguageFlag(locale)} {getLanguageName(locale)}
          </span>
          <span className="sm:hidden">{getLanguageFlag(locale)}</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-56 max-h-96 overflow-y-auto">
        <DropdownMenuLabel>Select Language</DropdownMenuLabel>
        <DropdownMenuSeparator />

        {/* Indian Languages */}
        <DropdownMenuLabel className="text-xs text-muted-foreground font-normal px-2">
          Indian Languages
        </DropdownMenuLabel>
        {['hi', 'te', 'ta', 'bn', 'mr'].map((loc) => (
          <DropdownMenuItem
            key={loc}
            onClick={() => setLocale(loc)}
            className={`cursor-pointer ${locale === loc ? 'bg-accent' : ''}`}
          >
            <span className="mr-2">{getLanguageFlag(loc)}</span>
            <span>{getLanguageName(loc)}</span>
            {locale === loc && <span className="ml-auto text-primary">✓</span>}
          </DropdownMenuItem>
        ))}

        <DropdownMenuSeparator />

        {/* International Languages */}
        <DropdownMenuLabel className="text-xs text-muted-foreground font-normal px-2">
          International Languages
        </DropdownMenuLabel>
        {['en', 'zh', 'es', 'fr', 'ar', 'ru', 'pt', 'de'].map((loc) => (
          <DropdownMenuItem
            key={loc}
            onClick={() => setLocale(loc)}
            className={`cursor-pointer ${locale === loc ? 'bg-accent' : ''}`}
          >
            <span className="mr-2">{getLanguageFlag(loc)}</span>
            <span>{getLanguageName(loc)}</span>
            {locale === loc && <span className="ml-auto text-primary">✓</span>}
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
