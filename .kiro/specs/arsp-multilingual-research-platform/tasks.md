# Implementation Plan

## Overview

This implementation plan breaks down the ARSP development into discrete, incremental coding tasks. Each task builds on previous work and includes specific requirements references. Tasks are organized to deliver a working MVP for the WeMakeDevs hackathon (Nov 13-16) followed by AP Govt polish (Nov 17-24).

**Current Status**: Frontend UI complete with Next.js from Smart-Research-Hub. Focus is now on backend integration, Supabase Edge Functions, and service connections.

## Task List

- [x] 1. Project initialization and core infrastructure
  - Initialize Vite + React + TypeScript project with proper configuration
  - Set up Tailwind CSS and shadcn/ui component library
  - Configure path aliases (@/) and TypeScript strict mode
  - Create basic folder structure (components, hooks, lib, types, contexts)
  - _Requirements: 1.1, 1.2, 8.1, 8.2_

- [x] 1.1 Configure development tooling
  - Set up ESLint with Airbnb + TypeScript rules
  - Configure Prettier for code formatting
  - Add Husky pre-commit hooks for linting
  - Create .env.example with all required environment variables
  - _Requirements: 1.1, 10.5_

- [x] 1.2 Initialize shadcn/ui components
  - Run shadcn init with Vite configuration
  - Add core UI components: button, card, input, textarea, select, table, dialog, dropdown-menu, badge, alert, skeleton, toast, accordion
  - Verify components render correctly with Tailwind styles
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 2. Authentication system setup
  - Create Clerk account and configure application
  - Install @clerk/clerk-react and integrate ClerkProvider in main.tsx
  - Implement useAuth custom hook wrapping Clerk's useUser and useAuth
  - Create AuthContext for global auth state management
  - Build ProtectedRoute component for route guarding
  - _Requirements: 1.1, 1.2, 1.3, 9.1, 9.6_

- [x] 2.1 Supabase authentication integration
  - Create Supabase project and obtain credentials
  - Install @supabase/supabase-js client library
  - Implement useSupabaseClient hook that injects Clerk token
  - Configure Supabase client to use Clerk JWT for RLS
  - Test authenticated database queries
  - _Requirements: 1.2, 1.3, 9.1, 9.3_

- [x] 2.2 User profile management
  - Create profiles table in Supabase with RLS policies
  - Implement profile creation trigger on first auth
  - Build ProfileForm component for editing user details
  - Add language preference selection and persistence
  - Implement profile update mutation with optimistic updates
  - _Requirements: 1.2, 1.4, 8.7_

- [x] 3. Lingo.dev multilingual infrastructure
  - Sign up for Lingo.dev Hobby tier and obtain API key
  - Create i18n.config.json with all target languages
  - Set up source locale file (src/locales/en.json) with UI strings
  - Run Lingo CLI to generate translations for all languages
  - Verify translation files created for all 10+ languages
  - _Requirements: 2.1, 2.2, 10.2, 10.3_

- [x] 3.1 Lingo SDK runtime integration
  - Install lingo.dev/sdk package
  - Create lib/lingo.ts with LingoDotDevEngine configuration
  - Define academicGlossary with key terminology mappings
  - Implement useLingo custom hook with translate and pluralize functions
  - Create LanguageContext for global language state
  - Build LanguageSelector dropdown component
  - _Requirements: 2.3, 2.4, 2.5, 2.6, 8.7_

- [x] 3.2 Lingo CI/CD integration
  - Create GitHub Actions workflow for translation validation
  - Add Lingo CLI step with --frozen flag to prevent incomplete builds
  - Implement translation completeness check for all target languages
  - Configure workflow to run on pull requests and main branch
  - _Requirements: 2.7, 10.2, 10.3_

- [x] 4. Database schema and RLS policies
  - Create drafts table with user_id foreign key and RLS policies
  - Create uploads table with file metadata and RLS policies
  - Create literature_reviews table with JSONB fields for insights/references
  - Create journals table with mock data (50+ journals)
  - Implement security definer helper functions for RLS
  - Create indexes on frequently queried columns
  - _Requirements: 1.3, 9.1, 9.2, 9.3, 10.6_

- [x] 4.1 Storage bucket configuration
  - Create 'papers' storage bucket in Supabase
  - Implement RLS policies for user-scoped file access
  - Configure file size limits (10MB per file)
  - Test file upload and download with RLS enforcement
  - _Requirements: 4.1, 9.1, 9.2_

- [x] 5. Dashboard layout and navigation
  - Create DashboardLayout component with header, sidebar, and main content area
  - Build Header component with Clerk UserButton and LanguageSelector
  - Implement Sidebar with navigation links to all modules
  - Add Footer with DPDP compliance link
  - Create responsive layout that works on mobile and desktop
  - Implement useLingo hook for translation support
  - Add ARIA labels for keyboard navigation accessibility
  - _Requirements: 8.1 (partial - basic accessibility), 8.5 (complete - keyboard navigation), 8.6 (deferred to Task 12.1 - dark mode)_
  - _Note: Full WCAG 2.1 AA compliance (8.1) and dark mode (8.6) will be completed in Task 12_

- [x] 5.1 DPDP consent dialog
  - Build ConsentDialog component using shadcn Dialog
  - Implement consent logging to Supabase consent_logs table
  - Add localStorage check to prevent repeated prompts
  - Translate consent text using Lingo SDK with legal context
  - Display on first visit before allowing app access
  - _Requirements: 9.3, 9.4, 9.5_

- [x] 6. Topic Selection module
  - Create TopicSelector component with search input and filters
  - Implement useTopics custom hook with React Query caching
  - Build TopicCard component to display individual topics
  - Integrate Semantic Scholar API for topic data fetching
  - Add Lingo API translation for user queries (any language → English)
  - Translate topic results back to user's language with SDK
  - Display results in shadcn DataTable with pluralized count
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 6.1 Topic selection accuracy validation
  - Implement relevance scoring algorithm for topic matching
  - Add accuracy threshold check (≥80%) with user alerts
  - Create test suite with sample queries and expected results
  - Validate translation fidelity for Chinese and Spanish examples
  - _Requirements: 3.6_

- [x] 7. Literature Review module
  - Create ReviewUploader component with drag-and-drop file upload
  - Implement file upload to Supabase storage with progress indicator
  - Build ReviewSummary component to display AI-generated summary
  - Create InsightsList component with shadcn Accordion
  - Add ReferenceExport component for Zotero JSON download
  - Implement useLitReview custom hook for data management
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8_

- [ ] 7.1 Supabase Edge Function for literature review processing
  - Create /lit/review edge function in Deno runtime
  - Implement PDF text extraction using pdf.js or similar
  - Integrate Hugging Face Inference API for summarization
  - Chain Lingo API translation with context and glossary
  - Store results in literature_reviews table
  - Return translated summary, insights, and references
  - Implement caching for repeated file processing
  - Add loading states with progress indicators
  - Ensure <60 second total processing time
  - Handle large files (up to 10MB) efficiently
  - _Requirements: 4.2, 4.3, 4.4, 4.6, 4.7, 7.1, 7.5_

- [x] 8. Citation and Plagiarism Detection module
  - Create DraftEditor component with real-time text editing
  - Build ScoreDisplay component showing originality percentage
  - Implement CitationSuggestions component with shadcn List
  - Add FlaggedSections highlighting with color-coded badges
  - Create usePlagiarism custom hook for draft management
  - Implement auto-save to Supabase drafts table
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9_

- [ ] 8.1 Plagiarism detection implementation
  - **Recommended Approach**: Use Sentence Transformers via Hugging Face Inference API
  - Integrate `sentence-transformers/all-mpnet-base-v2` model for semantic similarity
  - Implement text chunking (sentences/paragraphs) for efficient comparison
  - Calculate cosine similarity between embeddings (threshold: 0.8 = ~80% similarity)
  - Add threshold-based flagging (>20% similarity triggers review)
  - Integrate CrossRef API for citation suggestions (free, no auth required)
  - Alternative: Copyleaks API integration ($10.99/month for production with 99% accuracy)
  - Ensure ≥95% accuracy with test dataset
  - _Requirements: 5.2, 5.3, 5.4, 5.5_
  - _Resources: https://huggingface.co/sentence-transformers/all-mpnet-base-v2, https://copyleaks.com/api_

- [ ] 8.2 Supabase Edge Function for plagiarism checking
  - Create /plagiarism/check edge function in Deno runtime
  - Implement Sentence Transformer integration via HF Inference API (sentence-transformers/all-mpnet-base-v2)
  - Implement text chunking (sentences/paragraphs) for efficient comparison
  - Generate embeddings for user draft and compare against reference corpus
  - Calculate cosine similarity scores for each text chunk (threshold: 0.8 = ~80% similarity)
  - Add threshold-based flagging (>20% similarity triggers review)
  - Fetch citation suggestions from CrossRef API (https://api.crossref.org/works)
  - Translate plagiarism reports using Lingo SDK with context "plagiarism_report"
  - Apply pluralization to suggestion counts (e.g., "3 similar passages found")
  - Return originality score (0-100), flagged sections with similarity scores, and citation suggestions
  - Ensure ≥95% accuracy with test dataset
  - _Requirements: 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8_
  - _Implementation Note: For production, consider Copyleaks API for access to academic paper database_

- [x] 9. Journal Recommendation module
  - Create JournalTable component with sortable columns
  - Build JournalFilters component for open-access, impact factor, domain
  - Implement JournalCard component for detailed view
  - Add useJournals custom hook with filtering logic
  - Display fit scores with color-coded badges
  - Enable sorting by impact factor, fit score, publication time
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_

- [ ] 9.1 Journal recommendation algorithm
  - Implement abstract-journal matching using cosine similarity
  - Create domain classification for journal filtering
  - Calculate fit scores (0-100) based on content alignment
  - Apply filters (impact factor ≥1.0, publication time ≤6 months)
  - Ensure ≥80% accuracy with validation dataset
  - _Requirements: 6.1, 6.2, 6.3, 6.5, 6.8_

- [ ] 9.2 Supabase Edge Function for journal recommendations
  - Create /journals/recommend edge function in Deno runtime
  - Implement abstract-journal matching using cosine similarity
  - Create domain classification for journal filtering
  - Calculate fit scores (0-100) based on content alignment
  - Apply filters (impact factor ≥1.0, publication time ≤6 months)
  - Query journals table with user filters
  - Translate journal metadata using Lingo SDK with glossary
  - Apply pluralization to result counts
  - Return ranked list of 10 journals
  - Ensure ≥80% accuracy with validation dataset
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_

- [ ] 9.3 Topic Discovery Service
  - Create Supabase Edge Function: /topics/trending
  - Integrate Semantic Scholar API for academic papers
  - Integrate arXiv API for preprints
  - Implement topic relevance scoring algorithm
  - Translate user queries (any language → English) via Lingo API
  - Translate results back to user's language with SDK
  - Cache results for 5 minutes to reduce API calls
  - Return 5 topic recommendations with impact scores
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [ ] 9.4 Frontend-Backend Integration
  - Update Next.js API client to use Supabase Edge Functions
  - Test Topics page with real /topics/trending endpoint
  - Test Papers page with file upload to Supabase storage
  - Test Plagiarism page with /plagiarism/check endpoint
  - Test Journals page with /journals/recommend endpoint
  - Add comprehensive error handling and user feedback
  - Implement retry logic for failed requests
  - Add loading states with progress indicators
  - Test end-to-end workflows across all modules
  - _Requirements: All module requirements_

- [ ] 10. Performance optimization and caching
  - Set up React Query with appropriate stale times
  - Implement server-side caching in edge functions (5-minute TTL)
  - Add code splitting with React.lazy for all modules
  - Configure Vite bundle optimization with manual chunks
  - Implement image lazy loading for all assets
  - Add database query indexes for common patterns
  - _Requirements: 7.1, 7.2, 10.6_

- [ ] 10.1 Offline mode and draft synchronization
  - Implement localStorage for draft persistence
  - Create sync mechanism on network reconnection
  - Add Supabase Realtime subscription for draft updates
  - Display sync status indicator in UI
  - Handle conflict resolution for concurrent edits
  - _Requirements: 7.3, 7.4_

- [ ] 11. Error handling and user feedback
  - Create ErrorBoundary component for graceful error recovery
  - Implement handleApiCall wrapper with retry logic
  - Add toast notifications for all user actions
  - Translate error messages using Lingo with error context
  - Create ErrorFallback component with reset functionality
  - Add loading states with shadcn Skeleton for all async operations
  - _Requirements: 7.5, 8.1, 8.2_

- [ ] 12. Accessibility enhancements
  - Add ARIA labels to all interactive components
  - Implement keyboard navigation for all features
  - Add alt text to all icons and images
  - Test with screen readers (NVDA/JAWS)
  - Ensure WCAG 2.1 AA compliance with axe-core
  - Add focus indicators for keyboard users
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 12.1 Dark mode implementation
  - Create ThemeContext for theme state management
  - Add theme toggle button in header
  - Implement shadcn dark mode with CSS variables
  - Ensure WCAG contrast ratios in both themes
  - Persist theme preference in localStorage
  - _Requirements: 8.6_

- [ ] 13. CI/CD pipeline setup
  - Create GitHub Actions workflow for testing
  - Add linting, type-checking, and test steps
  - Implement Lingo translation validation step
  - Configure Vercel deployment with environment variables
  - Add code coverage reporting with Codecov
  - Set up preview deployments for pull requests
  - _Requirements: 10.2, 10.3, 10.4, 10.5_

- [ ] 14. Monitoring and observability
  - Integrate Sentry for error tracking
  - Add performance monitoring for API calls
  - Implement custom metrics for translation times
  - Create dashboard for key metrics (response times, error rates)
  - Add user analytics with privacy-compliant tracking
  - _Requirements: 10.5_

- [ ] 15. Mock data seeding
  - Create seed script for journals table (50+ entries)
  - Add sample profiles for 8 PoC users (4 AP, 4 global)
  - Generate synthetic drafts and reviews for testing
  - Populate with diverse domains and languages
  - _Requirements: 11.6_

- [ ] 16. End-to-end testing
  - Set up Cypress or Playwright for E2E testing
  - Write unit tests for Supabase Edge Functions
  - Write integration tests for API endpoints
  - Write complete workflow test (login → topic → review → plagiarism → journals)
  - Add multilingual flow tests (Chinese, Spanish)
  - Test offline mode and sync functionality
  - Validate accessibility with axe-core integration
  - Test with 8 PoC users (4 AP, 4 global)
  - _Requirements: 11.3, 11.6_

- [ ] 17. PoC validation and metrics
  - Conduct 8-user testing with synthetic accounts
  - Measure time savings for research workflows
  - Calculate accuracy metrics (≥80% threshold)
  - Collect user satisfaction feedback (NPS ≥8)
  - Document results in PoC report
  - _Requirements: 11.6, 11.7, 11.8_

- [ ] 18. Documentation and deployment
  - Write comprehensive README with setup instructions
  - Create API documentation for Supabase Edge Functions
  - Add inline JSDoc comments to all functions
  - Document Lingo integration patterns and usage
  - Deploy Supabase project to production
  - Deploy Next.js frontend to Vercel
  - Configure environment variables for production
  - Set up custom domain (if applicable)
  - Configure CORS and security headers
  - Set up monitoring and error tracking (Sentry)
  - Create deployment documentation
  - Create demo video (2 minutes) showcasing features
  - _Requirements: 10.4_

- [ ] 19. WeMakeDevs submission preparation
  - Verify all 7+ Lingo features implemented and documented
  - Create demo showcasing CLI, SDK, API, context, glossary, pluralization, CI/CD
  - Test Chinese and Spanish workflows end-to-end
  - Star Lingo.dev GitHub repository
  - Write submission notes highlighting learning and creativity
  - Tweet with #LingoHack tag
  - _Requirements: 2.1-2.7_

- [ ] 20. AP Govt hackathon polish
  - Implement mock APCCE federation in authentication system
  - Add scalability testing with Artillery (50 concurrent users)
  - Enhance privacy audit with full RLS verification
  - Create presentation deck with PoC metrics
  - Record demo video emphasizing global scalability
  - Prepare submission with impact projections
  - _Requirements: 1.5, 9.5, 10.1_

## Implementation Notes

### Frontend Status
- **Complete**: Next.js 16 frontend from Smart-Research-Hub with all 6 modules (Dashboard, Topics, Papers, Plagiarism, Journals, Government, Impact)
- **Complete**: Full shadcn/ui component library integrated
- **Complete**: API client structure with all endpoint definitions
- **Complete**: Auth flow with login/register pages

### Backend Focus
- **Priority**: Supabase Edge Functions for serverless architecture
- **AI/ML**: Hugging Face Inference API (free tier) for MVP
- **APIs**: Semantic Scholar, arXiv, CrossRef (all free)
- **i18n**: Lingo.dev for professional multilingual support
- **Auth**: Decision needed on Clerk vs Supabase Auth vs custom JWT

### Success Criteria
- ✅ All 6 modules functional with real backend
- ✅ 10+ languages supported with ≥95% translation accuracy
- ✅ AI accuracy ≥80% for recommendations
- ✅ Response times <5 seconds for 95% of requests
- ✅ DPDP compliant with consent tracking
- ✅ Successfully tested with 8 PoC users
