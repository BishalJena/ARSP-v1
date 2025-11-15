// Server-side only - Lingo.dev SDK initialization
// DO NOT import this file in client components - use lingo-config.ts instead
import { LingoDotDevEngine } from 'lingo.dev/sdk';
import { academicGlossary, supportedLocales } from './lingo-config';

// Re-export client-safe items for convenience
export { academicGlossary, supportedLocales, getLanguageName, getLanguageFlag } from './lingo-config';

// Initialize Lingo.dev engine (server-side only)
export const lingoEngine = new LingoDotDevEngine({
  apiKey: process.env.NEXT_PUBLIC_LINGO_API_KEY || '',
  sourceLocale: 'en',
  targetLocales: supportedLocales.filter(locale => locale !== 'en'),
  glossary: academicGlossary,
  contexts: {
    legal: ['consent', 'privacy', 'data protection', 'DPDP'],
    academic: ['research', 'paper', 'journal', 'citation', 'plagiarism'],
    ui: ['button', 'menu', 'dialog', 'form', 'error'],
  },
  pluralization: {
    enabled: true,
  },
  fallbackLocale: 'en',
  cacheStrategy: 'memory', // Use memory cache for better performance
});
