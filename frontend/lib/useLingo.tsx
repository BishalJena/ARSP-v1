'use client';

import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { supportedLocales } from './lingo-config';

// Load translations dynamically
const loadTranslations = async (locale: string) => {
  try {
    const translations = await import(`@/locales/${locale}.json`);
    return translations.default;
  } catch (error) {
    console.warn(`Failed to load translations for ${locale}, falling back to English`);
    const fallback = await import('@/locales/en.json');
    return fallback.default;
  }
};

interface LanguageContextType {
  locale: string;
  setLocale: (locale: string) => void;
  t: (key: string, params?: Record<string, any>) => string;
  plural: (key: string, count: number, params?: Record<string, any>) => string;
  isLoading: boolean;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [locale, setLocaleState] = useState<string>('en');
  const [translations, setTranslations] = useState<any>({});
  const [isLoading, setIsLoading] = useState(true);

  // Load locale from localStorage on mount
  useEffect(() => {
    const savedLocale = localStorage.getItem('locale');
    if (savedLocale && supportedLocales.includes(savedLocale)) {
      setLocaleState(savedLocale);
    }
  }, []);

  // Load translations when locale changes
  useEffect(() => {
    const loadLocale = async () => {
      setIsLoading(true);
      try {
        const newTranslations = await loadTranslations(locale);
        setTranslations(newTranslations);
      } catch (error) {
        console.error('Failed to load translations:', error);
      } finally {
        setIsLoading(false);
      }
    };
    loadLocale();
  }, [locale]);

  const setLocale = (newLocale: string) => {
    if (supportedLocales.includes(newLocale)) {
      setLocaleState(newLocale);
      localStorage.setItem('locale', newLocale);
      // Update HTML lang attribute for accessibility
      document.documentElement.lang = newLocale;
    }
  };

  // Translation function with nested key support
  const t = (key: string, params?: Record<string, any>): string => {
    const keys = key.split('.');
    let value: any = translations;

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        console.warn(`Translation key not found: ${key}`);
        return key;
      }
    }

    if (typeof value !== 'string') {
      console.warn(`Translation value is not a string: ${key}`);
      return key;
    }

    // Replace parameters in the translation
    if (params) {
      return value.replace(/\{\{(\w+)\}\}/g, (match: string, paramKey: string) => {
        return params[paramKey]?.toString() || match;
      });
    }

    return value;
  };

  // Pluralization function
  const plural = (key: string, count: number, params?: Record<string, any>): string => {
    const pluralKey = `plurals.${key}`;
    const keys = pluralKey.split('.');
    let value: any = translations;

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        console.warn(`Plural translation key not found: ${pluralKey}`);
        return `${count} ${key}`;
      }
    }

    // Determine plural form based on count
    let form: string;
    if (locale === 'en') {
      form = count === 0 ? 'zero' : count === 1 ? 'one' : 'other';
    } else if (['hi', 'te', 'ta', 'bn', 'mr', 'es', 'fr', 'pt', 'de', 'ru'].includes(locale)) {
      form = count === 1 ? 'one' : 'other';
    } else if (locale === 'zh') {
      form = 'other'; // Chinese doesn't have plural forms
    } else {
      form = count === 1 ? 'one' : 'other';
    }

    const translation = value[form];
    if (!translation) {
      console.warn(`Plural form ${form} not found for ${key}`);
      return `${count} ${key}`;
    }

    // Replace parameters
    const mergedParams: Record<string, any> = { ...params, count };
    return translation.replace(/\{\{(\w+)\}\}/g, (match: string, paramKey: string) => {
      return mergedParams[paramKey]?.toString() || match;
    });
  };

  return (
    <LanguageContext.Provider value={{ locale, setLocale, t, plural, isLoading }}>
      {children}
    </LanguageContext.Provider>
  );
}

// Custom hook to use the language context
export function useLingo(): LanguageContextType {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLingo must be used within a LanguageProvider');
  }
  return context;
}
