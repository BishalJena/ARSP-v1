# ARSP Implementation Plan - Updated for Next.js Frontend

## Overview

This updated implementation plan reflects the current state with the Next.js frontend from Smart-Research-Hub. The frontend UI is complete with all 6 modules. Focus is now on backend integration, tooling setup, and connecting services.

## Current Status

### ✅ COMPLETED (Frontend UI)
- **Next.js 16 Frontend**: Complete with App Router, Tailwind CSS, shadcn/ui
- **All Pages**: Dashboard, Topics, Papers, Plagiarism, Journals, Government, Impact
- **API Client**: Complete with all endpoint definitions
- **Auth Flow**: Login/Register pages with context management
- **Components**: Full shadcn/ui component library

### ❌ PENDING (Integration & Backend)

## Priority Tasks

### Phase 1: Core Infrastructure Setup

- [ ] **1. Supabase Project Setup**
  - Create Supabase project and obtain credentials
  - Configure environment variables in frontend/.env.local
  - Set up Supabase client in Next.js
  - Test database connection
  - _Requirements: 1.2, 1.3, 9.1_

- [ ] **2. Database Schema Implementation**
  - [ ] 2.1 Create users/profiles table with RLS policies
  - [ ] 2.2 Create papers/uploads table with file metadata
  - [ ] 2.3 Create literature_reviews table with JSONB fields
  - [ ] 2.4 Create plagiarism_checks table
  - [ ] 2.5 Create journals table with seed data
  - [ ] 2.6 Create government_priorities table (AP Govt data)
  - [ ] 2.7 Create consent_logs table for DPDP compliance
  - [ ] 2.8 Implement RLS policies for all tables
  - [ ] 2.9 Create indexes on frequently queried columns
  - _Requirements: 1.3, 9.1, 9.2, 9.3, 10.6_

- [ ] **3. Supabase Storage Configuration**
  - [ ] 3.1 Create 'papers' storage bucket
  - [ ] 3.2 Implement RLS policies for user-scoped file access
  - [ ] 3.3 Configure file size limits (10MB per file)
  - [ ] 3.4 Test file upload and download with RLS
  - [ ] 3.5 Update frontend API client to use Supabase storage
  - _Requirements: 4.1, 9.1, 9.2_

- [ ] **4. Authentication Integration**
  - [ ] 4.1 Choose auth provider (Clerk vs Supabase Auth vs Backend JWT)
  - [ ] 4.2 If Clerk: Install @clerk/nextjs and configure
  - [ ] 4.3 If Supabase Auth: Configure auth providers
  - [ ] 4.4 Update frontend auth-context.tsx with chosen provider
  - [ ] 4.5 Implement protected routes middleware
  - [ ] 4.6 Create user profile on first login
  - [ ] 4.7 Test authentication flow end-to-end
  - _Requirements: 1.1, 1.2, 1.3, 9.1, 9.6_

### Phase 2: Lingo.dev Multilingual Integration

- [ ] **5. Lingo.dev Setup**
  - [ ] 5.1 Sign up for Lingo.dev and obtain API key
  - [ ] 5.2 Install lingo.dev CLI and SDK packages
  - [ ] 5.3 Create i18n.config.json with target languages
    - Languages: en-US, en-GB, es-ES, es-419, fr-FR, fr-CA, de, ja, zh-CN, zh-TW, ko, pt, it, ru
  - [ ] 5.4 Create source locale file (locales/en.json) with all UI strings
  - [ ] 5.5 Extract all hardcoded strings from Next.js components
  - [ ] 5.6 Run Lingo CLI to generate translations
  - [ ] 5.7 Verify translation files for all languages
  - _Requirements: 2.1, 2.2, 10.2, 10.3_

- [ ] **6. Lingo SDK Runtime Integration**
  - [ ] 6.1 Create lib/lingo.ts with configuration
  - [ ] 6.2 Define academicGlossary with key terminology
    - Terms: H-index, Impact Factor, Plagiarism Score, Citation Analysis, etc.
  - [ ] 6.3 Create LanguageContext for global language state
  - [ ] 6.4 Build LanguageSelector component
  - [ ] 6.5 Wrap Next.js app with LanguageProvider
  - [ ] 6.6 Update all components to use translation hooks
  - [ ] 6.7 Test language switching across all pages
  - _Requirements: 2.3, 2.4, 2.5, 2.6, 8.7_

- [ ] **7. Lingo CI/CD Integration**
  - [ ] 7.1 Create .github/workflows/lingo-validation.yml
  - [ ] 7.2 Add Lingo CLI step with --frozen flag
  - [ ] 7.3 Implement translation completeness check
  - [ ] 7.4 Configure to run on PRs and main branch
  - [ ] 7.5 Test workflow with incomplete translations
  - _Requirements: 2.7, 10.2, 10.3_

### Phase 3: DPDP Compliance

- [ ] **8. DPDP Consent Dialog**
  - [ ] 8.1 Create ConsentDialog component using shadcn Dialog
  - [ ] 8.2 Implement consent logging to consent_logs table
  - [ ] 8.3 Add localStorage check to prevent repeated prompts
  - [ ] 8.4 Translate consent text using Lingo SDK with legal context
  - [ ] 8.5 Display on first visit before allowing app access
  - [ ] 8.6 Add consent management page in user settings
  - _Requirements: 9.3, 9.4, 9.5_

### Phase 4: Backend Services (Supabase Edge Functions)

- [ ] **9. Literature Review Processing**
  - [ ] 9.1 Create Supabase Edge Function: /lit/review
  - [ ] 9.2 Implement PDF text extraction (pdf.js or similar)
  - [ ] 9.3 Integrate Hugging Face Inference API for summarization
  - [ ] 9.4 Chain Lingo API translation with context and glossary
  - [ ] 9.5 Store results in literature_reviews table
  - [ ] 9.6 Return translated summary, insights, and references
  - [ ] 9.7 Implement caching for repeated file processing
  - [ ] 9.8 Add loading states with progress indicators
  - [ ] 9.9 Ensure <60 second total processing time
  - [ ] 9.10 Handle large files (up to 10MB) efficiently
  - _Requirements: 4.2, 4.3, 4.4, 4.6, 4.7, 7.1, 7.5_

- [ ] **10. Plagiarism Detection**
  - [ ] 10.1 Create Supabase Edge Function: /plagiarism/check
  - [ ] 10.2 Integrate Sentence Transformers via HF Inference API
    - Model: sentence-transformers/all-mpnet-base-v2
  - [ ] 10.3 Implement text chunking (sentences/paragraphs)
  - [ ] 10.4 Calculate cosine similarity between embeddings
  - [ ] 10.5 Add threshold-based flagging (>20% similarity)
  - [ ] 10.6 Integrate CrossRef API for citation suggestions
  - [ ] 10.7 Translate plagiarism reports using Lingo SDK
  - [ ] 10.8 Apply pluralization to suggestion counts
  - [ ] 10.9 Return originality score, flagged sections, citations
  - [ ] 10.10 Ensure ≥95% accuracy with test dataset
  - _Requirements: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_

- [ ] **11. Journal Recommendations**
  - [ ] 11.1 Create Supabase Edge Function: /journals/recommend
  - [ ] 11.2 Implement abstract-journal matching (cosine similarity)
  - [ ] 11.3 Create domain classification for filtering
  - [ ] 11.4 Calculate fit scores (0-100) based on content alignment
  - [ ] 11.5 Apply filters (impact factor ≥1.0, pub time ≤6 months)
  - [ ] 11.6 Query journals table with user filters
  - [ ] 11.7 Translate journal metadata using Lingo SDK with glossary
  - [ ] 11.8 Apply pluralization to result counts
  - [ ] 11.9 Return ranked list of 10 journals
  - [ ] 11.10 Ensure ≥80% accuracy with validation dataset
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

- [ ] **12. Topic Discovery Service**
  - [ ] 12.1 Create Supabase Edge Function: /topics/trending
  - [ ] 12.2 Integrate Semantic Scholar API
  - [ ] 12.3 Integrate arXiv API
  - [ ] 12.4 Implement topic relevance scoring
  - [ ] 12.5 Translate user queries (any language → English) via Lingo API
  - [ ] 12.6 Translate results back to user's language
  - [ ] 12.7 Cache results for 5 minutes
  - [ ] 12.8 Return 5 topic recommendations with impact scores
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

### Phase 5: Frontend-Backend Integration

- [ ] **13. Connect Frontend to Backend**
  - [ ] 13.1 Update API client to use Supabase Edge Functions
  - [ ] 13.2 Test Topics page with real API
  - [ ] 13.3 Test Papers page with file upload
  - [ ] 13.4 Test Plagiarism page with detection
  - [ ] 13.5 Test Journals page with recommendations
  - [ ] 13.6 Test Government page with alignment analysis
  - [ ] 13.7 Test Impact page with predictions
  - [ ] 13.8 Add error handling and loading states
  - [ ] 13.9 Implement retry logic for failed requests
  - _Requirements: All_

### Phase 6: Testing & Deployment

- [ ] **14. Testing**
  - [ ] 14.1 Write unit tests for Edge Functions
  - [ ] 14.2 Write integration tests for API endpoints
  - [ ] 14.3 Test multilingual functionality (Chinese, Spanish)
  - [ ] 14.4 Test with 8 PoC users (4 AP, 4 global)
  - [ ] 14.5 Measure time savings (target: 30% reduction)
  - [ ] 14.6 Collect user satisfaction feedback (NPS ≥8)
  - _Requirements: 11.3, 11.6, 11.7, 11.8_

- [ ] **15. Deployment**
  - [ ] 15.1 Deploy Supabase project to production
  - [ ] 15.2 Deploy Next.js frontend to Vercel
  - [ ] 15.3 Configure environment variables
  - [ ] 15.4 Set up custom domain
  - [ ] 15.5 Configure CORS and security headers
  - [ ] 15.6 Set up monitoring and error tracking
  - [ ] 15.7 Create deployment documentation
  - _Requirements: 10.4_

## Notes

- **Frontend**: Complete Next.js app with all UI modules ready
- **Backend**: Focus on Supabase Edge Functions for serverless architecture
- **Auth**: Decision needed on Clerk vs Supabase Auth vs custom JWT
- **AI/ML**: Use Hugging Face Inference API (free tier) for MVP
- **APIs**: Semantic Scholar, arXiv, CrossRef (all free)
- **i18n**: Lingo.dev for professional multilingual support

## Success Criteria

- ✅ All 6 modules functional with real backend
- ✅ 10+ languages supported with ≥95% translation accuracy
- ✅ AI accuracy ≥80% for recommendations
- ✅ Response times <5 seconds for 95% of requests
- ✅ DPDP compliant with consent tracking
- ✅ Successfully tested with 8 PoC users
