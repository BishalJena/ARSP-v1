# Frontend Integration Guide - Enhanced Papers API

## Overview

This guide shows how to integrate the new Gemini-powered papers API (`/api/v1/papers-enhanced/`) into the Next.js frontend.

**Performance**: 3-5x faster, 70% cheaper, 15 languages, instant translation switching!

## Quick Start

### 1. Update API Base URL

The enhanced API is at `/api/v1/papers-enhanced/` (legacy is still available at `/api/v1/papers/`).

```typescript
// lib/api.ts or constants.ts
export const API_ENDPOINTS = {
  // Legacy API (still works)
  papers: '/api/v1/papers',

  // Enhanced API (Gemini 2.0 Flash Lite)
  papersEnhanced: '/api/v1/papers-enhanced',
}
```

## Core Functions

### Upload Paper

```typescript
// lib/api/papers.ts
export async function uploadPaper(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/api/v1/papers-enhanced/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error(`Upload failed: ${response.statusText}`);
  }

  return response.json();
}

// Response type
interface UploadResponse {
  success: boolean;
  id: string;
  file_name: string;
  file_url: string;
  uploaded_at: string;
  status: string;
  next_step: string;
}
```

### Process Paper

```typescript
export async function processPaper(
  paperId: string,
  language: string = 'en',
  paperType: 'research' | 'ml' | 'clinical' | 'review' = 'research'
): Promise<ProcessResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/papers-enhanced/${paperId}/process?` +
    new URLSearchParams({ language, paper_type: paperType }),
    { method: 'POST' }
  );

  if (!response.ok) {
    throw new Error(`Processing failed: ${response.statusText}`);
  }

  return response.json();
}

// Response type
interface ProcessResponse {
  success: boolean;
  paper_id: string;
  analysis: PaperAnalysis;
  language: string;
  processing_method: string;
  performance: string;
}
```

### Get Analysis (with language switching)

```typescript
export async function getAnalysis(
  paperId: string,
  language: string = 'en'
): Promise<AnalysisResponse> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/papers-enhanced/${paperId}?language=${language}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get analysis: ${response.statusText}`);
  }

  return response.json();
}

// Response type
interface AnalysisResponse {
  paper_id: string;
  analysis: PaperAnalysis;
  language: string;
  from_cache: boolean;
  translation_time?: string;
}
```

## TypeScript Types

```typescript
// types/papers.ts

export interface PaperAnalysis {
  title: string;
  citation: string;
  tldr: string;
  background: string;
  research_question: string;

  methods: {
    overview: string;
    data_sources: string;
    sample_size: string;
    study_design: string;
    statistical_analysis: string;
  };

  results: {
    summary: string;
    key_findings: string[];
    quantitative_results: string[];
  };

  discussion: string;
  limitations: string[];

  related_work: Array<{
    citation: string;
    comparison: string;
  }>;

  contributions: string[];
  ethical_considerations: string;

  reproducibility: {
    code_availability: string;
    data_availability: string;
    hyperparameters: string;
    compute_budget: string;
    license: string;
  };

  practical_takeaways: string[];
  future_work: string[];

  glossary: Record<string, string>;

  qa_pairs: Array<{
    question: string;
    answer: string;
  }>;

  plain_summary: string;
  practitioner_summary: string;

  paper_type: 'research' | 'ml' | 'clinical' | 'review';
  field: string;
  word_count: number;
}

export type Language =
  | 'en' | 'hi' | 'te' | 'ta' | 'bn' | 'mr'
  | 'zh' | 'es' | 'fr' | 'de' | 'pt'
  | 'ja' | 'ko' | 'ru' | 'ar';

export const LANGUAGE_NAMES: Record<Language, string> = {
  en: 'English',
  hi: 'Hindi',
  te: 'Telugu',
  ta: 'Tamil',
  bn: 'Bengali',
  mr: 'Marathi',
  zh: 'Chinese',
  es: 'Spanish',
  fr: 'French',
  de: 'German',
  pt: 'Portuguese',
  ja: 'Japanese',
  ko: 'Korean',
  ru: 'Russian',
  ar: 'Arabic',
};
```

## React Components

### Language Selector

```typescript
// components/LanguageSelector.tsx
'use client';

import { Language, LANGUAGE_NAMES } from '@/types/papers';

interface LanguageSelectorProps {
  currentLanguage: Language;
  onLanguageChange: (lang: Language) => void;
  loading?: boolean;
}

export function LanguageSelector({
  currentLanguage,
  onLanguageChange,
  loading = false,
}: LanguageSelectorProps) {
  return (
    <select
      value={currentLanguage}
      onChange={(e) => onLanguageChange(e.target.value as Language)}
      disabled={loading}
      className="px-4 py-2 border rounded-lg"
    >
      {Object.entries(LANGUAGE_NAMES).map(([code, name]) => (
        <option key={code} value={code}>
          {name}
        </option>
      ))}
    </select>
  );
}
```

### Paper Upload Component

```typescript
// components/PaperUpload.tsx
'use client';

import { useState } from 'react';
import { uploadPaper, processPaper } from '@/lib/api/papers';

export function PaperUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [paperId, setPaperId] = useState<string | null>(null);

  const handleUploadAndProcess = async () => {
    if (!file) return;

    try {
      // Upload
      setUploading(true);
      const uploadResult = await uploadPaper(file);
      setPaperId(uploadResult.id);

      // Process
      setUploading(false);
      setProcessing(true);
      const processResult = await processPaper(uploadResult.id, 'en', 'research');

      console.log('Analysis:', processResult.analysis);
      // Navigate to analysis page or show results

    } catch (error) {
      console.error('Error:', error);
    } finally {
      setUploading(false);
      setProcessing(false);
    }
  };

  return (
    <div className="space-y-4">
      <input
        type="file"
        accept=".pdf"
        onChange={(e) => setFile(e.files?.[0] || null)}
        disabled={uploading || processing}
      />

      <button
        onClick={handleUploadAndProcess}
        disabled={!file || uploading || processing}
        className="px-4 py-2 bg-blue-500 text-white rounded"
      >
        {uploading && 'Uploading...'}
        {processing && 'Processing (1-3s)...'}
        {!uploading && !processing && 'Upload & Analyze'}
      </button>
    </div>
  );
}
```

### Paper Analysis Display

```typescript
// components/PaperAnalysis.tsx
'use client';

import { useState, useEffect } from 'react';
import { Language } from '@/types/papers';
import { getAnalysis } from '@/lib/api/papers';
import { LanguageSelector } from './LanguageSelector';

interface PaperAnalysisProps {
  paperId: string;
}

export function PaperAnalysis({ paperId }: PaperAnalysisProps) {
  const [language, setLanguage] = useState<Language>('en');
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [fromCache, setFromCache] = useState(false);

  // Fetch analysis when language changes
  useEffect(() => {
    const fetchAnalysis = async () => {
      setLoading(true);
      try {
        const result = await getAnalysis(paperId, language);
        setAnalysis(result.analysis);
        setFromCache(result.from_cache);
      } catch (error) {
        console.error('Error fetching analysis:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [paperId, language]);

  return (
    <div className="space-y-6">
      {/* Language Selector */}
      <div className="flex items-center gap-4">
        <LanguageSelector
          currentLanguage={language}
          onLanguageChange={setLanguage}
          loading={loading}
        />
        {fromCache && (
          <span className="text-sm text-green-600">✓ Cached (instant)</span>
        )}
        {loading && !fromCache && (
          <span className="text-sm text-blue-600">⚡ Translating...</span>
        )}
      </div>

      {/* Analysis Content */}
      {analysis && (
        <div className="space-y-4">
          <h1 className="text-2xl font-bold">{analysis.title}</h1>

          <div className="bg-blue-50 p-4 rounded">
            <h3 className="font-semibold">TL;DR</h3>
            <p>{analysis.tldr}</p>
          </div>

          <section>
            <h3 className="font-semibold">Background</h3>
            <p>{analysis.background}</p>
          </section>

          <section>
            <h3 className="font-semibold">Research Question</h3>
            <p>{analysis.research_question}</p>
          </section>

          <section>
            <h3 className="font-semibold">Methods</h3>
            <p>{analysis.methods.overview}</p>
          </section>

          <section>
            <h3 className="font-semibold">Key Findings</h3>
            <ul className="list-disc pl-6">
              {analysis.results.key_findings.map((finding: string, i: number) => (
                <li key={i}>{finding}</li>
              ))}
            </ul>
          </section>

          <section>
            <h3 className="font-semibold">Practical Takeaways</h3>
            <ul className="list-disc pl-6">
              {analysis.practical_takeaways.map((takeaway: string, i: number) => (
                <li key={i}>{takeaway}</li>
              ))}
            </ul>
          </section>

          {/* Add more sections as needed */}
        </div>
      )}
    </div>
  );
}
```

## Complete Workflow Example

```typescript
// pages/papers/[id].tsx or app/papers/[id]/page.tsx

'use client';

import { useState } from 'react';
import { PaperAnalysis } from '@/components/PaperAnalysis';

export default function PaperPage({ params }: { params: { id: string } }) {
  return (
    <div className="container mx-auto p-6">
      <PaperAnalysis paperId={params.id} />
    </div>
  );
}
```

## Performance Optimization

### 1. Pre-cache Common Languages

```typescript
// Pre-cache translations for common languages when paper is processed
async function processPaperWithCaching(paperId: string) {
  // Process in English first
  await processPaper(paperId, 'en');

  // Pre-cache common languages in background
  const commonLanguages: Language[] = ['hi', 'es', 'fr'];

  await Promise.all(
    commonLanguages.map(lang => getAnalysis(paperId, lang))
  );
}
```

### 2. Optimistic UI Updates

```typescript
// Show cached content immediately while fetching new translation
const [cachedAnalysis, setCachedAnalysis] = useState(null);

async function changeLanguage(newLang: Language) {
  // Show loading state but keep current content
  setLoading(true);

  const result = await getAnalysis(paperId, newLang);

  setAnalysis(result.analysis);
  setLoading(false);
}
```

### 3. Loading States

```typescript
{loading && !analysis && <Skeleton />}
{loading && analysis && <div className="opacity-50">{/* Current content */}</div>}
{!loading && analysis && <div>{/* Analysis */}</div>}
```

## Migration from Legacy API

### Before (Legacy)

```typescript
// Old way - slow, English only
const result = await fetch('/api/v1/papers/123/process', { method: 'POST' });
// Takes 5-15 seconds, returns simple summary
```

### After (Enhanced)

```typescript
// New way - fast, 15 languages
const result = await fetch('/api/v1/papers-enhanced/123/process?language=en', {
  method: 'POST'
});
// Takes 1-3 seconds, returns comprehensive analysis

// Change language instantly
const hindi = await fetch('/api/v1/papers-enhanced/123?language=hi');
// Instant if cached, ~1 second if new
```

## Error Handling

```typescript
try {
  const result = await processPaper(paperId, language);
  setAnalysis(result.analysis);
} catch (error) {
  if (error.message.includes('OPENROUTER_API_KEY')) {
    // API key not configured
    showError('API configuration error. Please contact support.');
  } else if (error.message.includes('File size')) {
    // File too large
    showError('PDF must be less than 20MB');
  } else {
    showError('Processing failed. Please try again.');
  }
}
```

## Testing

```typescript
// __tests__/papers.test.ts
import { uploadPaper, processPaper, getAnalysis } from '@/lib/api/papers';

describe('Enhanced Papers API', () => {
  it('should upload and process paper', async () => {
    const file = new File(['test'], 'test.pdf', { type: 'application/pdf' });

    const upload = await uploadPaper(file);
    expect(upload.success).toBe(true);

    const process = await processPaper(upload.id);
    expect(process.analysis).toBeDefined();
    expect(process.analysis.title).toBeTruthy();
  });

  it('should cache translations', async () => {
    const result1 = await getAnalysis('paper123', 'hi');
    expect(result1.from_cache).toBe(false);

    const result2 = await getAnalysis('paper123', 'hi');
    expect(result2.from_cache).toBe(true);
  });
});
```

## Next Steps

1. **Update existing papers page** to use enhanced API
2. **Add language selector** to paper view
3. **Update UI** to show 17-section analysis
4. **Add loading states** for processing and translation
5. **Test with real PDFs** to verify workflow

## Resources

- **API Documentation**: http://localhost:8000/api/docs
- **Backend Guide**: `backend/ENHANCED_PAPERS_API.md`
- **Test Script**: `backend/test_enhanced_api.py`
- **CHANGELOG**: `CHANGELOG.md`
