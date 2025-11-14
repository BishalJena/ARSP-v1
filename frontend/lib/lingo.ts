import { LingoDotDevEngine } from 'lingo.dev/sdk';

// Academic terminology glossary for context-aware translation
export const academicGlossary = {
  plagiarism: {
    en: 'plagiarism',
    hi: 'साहित्यिक चोरी',
    te: 'సాహిత్య దొంగతనం',
    ta: 'இலக்கிய திருட்டு',
    bn: 'সাহিত্যিক চুরি',
    mr: 'साहित्यिक चोरी',
    zh: '剽窃',
    es: 'plagio',
    fr: 'plagiat',
    ar: 'انتحال',
    ru: 'плагиат',
    pt: 'plágio',
    de: 'Plagiat',
  },
  'literature review': {
    en: 'literature review',
    hi: 'साहित्य समीक्षा',
    te: 'సాహిత్య సమీక్ష',
    ta: 'இலக்கிய மதிப்பாய்வு',
    bn: 'সাহিত্য পর্যালোচনা',
    mr: 'साहित्य पुनरावलोकन',
    zh: '文献综述',
    es: 'revisión de literatura',
    fr: 'revue de littérature',
    ar: 'مراجعة الأدبيات',
    ru: 'обзор литературы',
    pt: 'revisão de literatura',
    de: 'Literaturübersicht',
  },
  citation: {
    en: 'citation',
    hi: 'उद्धरण',
    te: 'ఉల్లేఖనం',
    ta: 'மேற்கோள்',
    bn: 'উদ্ধৃতি',
    mr: 'उद्धरण',
    zh: '引用',
    es: 'cita',
    fr: 'citation',
    ar: 'اقتباس',
    ru: 'цитирование',
    pt: 'citação',
    de: 'Zitat',
  },
  journal: {
    en: 'journal',
    hi: 'पत्रिका',
    te: 'పత్రిక',
    ta: 'இதழ்',
    bn: 'সাময়িকী',
    mr: 'जर्नल',
    zh: '期刊',
    es: 'revista',
    fr: 'journal',
    ar: 'مجلة',
    ru: 'журнал',
    pt: 'revista',
    de: 'Zeitschrift',
  },
  research: {
    en: 'research',
    hi: 'अनुसंधान',
    te: 'పరిశోధన',
    ta: 'ஆராய்ச்சி',
    bn: 'গবেষণা',
    mr: 'संशोधन',
    zh: '研究',
    es: 'investigación',
    fr: 'recherche',
    ar: 'بحث',
    ru: 'исследование',
    pt: 'pesquisa',
    de: 'Forschung',
  },
  abstract: {
    en: 'abstract',
    hi: 'सार',
    te: 'సారం',
    ta: 'சுருக்கம்',
    bn: 'সার',
    mr: 'सारांश',
    zh: '摘要',
    es: 'resumen',
    fr: 'résumé',
    ar: 'ملخص',
    ru: 'аннотация',
    pt: 'resumo',
    de: 'Zusammenfassung',
  },
  manuscript: {
    en: 'manuscript',
    hi: 'पांडुलिपि',
    te: 'మాన్యుస్క్రిప్ట్',
    ta: 'கையெழுத்துப் பிரதி',
    bn: 'পাণ্ডুলিপি',
    mr: 'हस्तलिखित',
    zh: '手稿',
    es: 'manuscrito',
    fr: 'manuscrit',
    ar: 'مخطوطة',
    ru: 'рукопись',
    pt: 'manuscrito',
    de: 'Manuskript',
  },
};

// Initialize Lingo.dev engine
export const lingoEngine = new LingoDotDevEngine({
  apiKey: process.env.NEXT_PUBLIC_LINGO_API_KEY || '',
  sourceLocale: 'en',
  targetLocales: [
    'hi', // Hindi
    'te', // Telugu
    'ta', // Tamil
    'bn', // Bengali
    'mr', // Marathi
    'zh', // Chinese
    'es', // Spanish
    'fr', // French
    'ar', // Arabic
    'ru', // Russian
    'pt', // Portuguese
    'de', // German
  ],
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

// Helper function to get language name
export const getLanguageName = (locale: string): string => {
  const languageNames: Record<string, string> = {
    en: 'English',
    hi: 'हिंदी',
    te: 'తెలుగు',
    ta: 'தமிழ்',
    bn: 'বাংলা',
    mr: 'मराठी',
    zh: '中文',
    es: 'Español',
    fr: 'Français',
    ar: 'العربية',
    ru: 'Русский',
    pt: 'Português',
    de: 'Deutsch',
  };
  return languageNames[locale] || locale;
};

// Helper function to get language flag emoji
export const getLanguageFlag = (locale: string): string => {
  const flags: Record<string, string> = {
    en: '🇬🇧',
    hi: '🇮🇳',
    te: '🇮🇳',
    ta: '🇮🇳',
    bn: '🇮🇳',
    mr: '🇮🇳',
    zh: '🇨🇳',
    es: '🇪🇸',
    fr: '🇫🇷',
    ar: '🇸🇦',
    ru: '🇷🇺',
    pt: '🇵🇹',
    de: '🇩🇪',
  };
  return flags[locale] || '🌐';
};

// Supported locales list
export const supportedLocales = [
  'en',
  'hi',
  'te',
  'ta',
  'bn',
  'mr',
  'zh',
  'es',
  'fr',
  'ar',
  'ru',
  'pt',
  'de',
];
