# ARSP Technical Architecture

**Version:** 2.1.0
**Last Updated:** 2025-11-16

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Technology Stack](#technology-stack)
4. [API Integrations](#api-integrations)
5. [Data Flow](#data-flow)
6. [Database Schema](#database-schema)
7. [Authentication Flow](#authentication-flow)
8. [Translation System](#translation-system)
9. [Feature Workflows](#feature-workflows)
10. [Deployment Architecture](#deployment-architecture)
11. [Security Considerations](#security-considerations)

---

## System Overview

ARSP is a full-stack research support platform built with a modern microservices-inspired architecture:

- **Frontend**: Next.js 16 (React 19) with TypeScript
- **Backend**: FastAPI (Python 3.10+) with async/await
- **Database**: Supabase (PostgreSQL with Row-Level Security)
- **Authentication**: Clerk (OAuth2 + JWT)
- **AI Services**: Gemini 2.0 Flash Lite, Winston AI
- **Translation**: Lingo.dev (static) + Google Translate (dynamic)

### Design Principles

- **API-First**: Backend exposes RESTful APIs consumed by frontend
- **Async Processing**: Non-blocking I/O for external API calls
- **Caching**: Translation caching to minimize API costs
- **Fallback Mechanisms**: Graceful degradation when premium APIs unavailable
- **Type Safety**: TypeScript (frontend) + Pydantic (backend)
- **Security**: JWT authentication, RLS, API key validation

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           Next.js 16 Frontend (Port 3000)                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │ Dashboard  │  │ Language   │  │  Clerk Auth      │   │  │
│  │  │ Components │  │ Selector   │  │  Integration     │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │ Papers UI  │  │ Plagiarism │  │  Journals UI     │   │  │
│  │  │            │  │ UI         │  │                  │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────────┘
                        │ HTTP/REST API
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Layer (v1)                        │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │ Papers API │  │ Plagiarism │  │  Journals API    │   │  │
│  │  │ (Enhanced) │  │ API        │  │                  │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Service Layer                          │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │ Gemini     │  │ Winston    │  │  Translation     │   │  │
│  │  │ Service    │  │ Service    │  │  Service         │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────────┐   │  │
│  │  │ Papers     │  │ Journals   │  │  Topics          │   │  │
│  │  │ Service    │  │ Service    │  │  Service         │   │  │
│  │  └────────────┘  └────────────┘  └──────────────────┘   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────┬─────────────────────────────────┬───────────────────┘
            │                                 │
            ▼                                 ▼
┌────────────────────────┐      ┌─────────────────────────────────┐
│   Supabase Database    │      │   External AI Services          │
│   ┌────────────────┐   │      │  ┌──────────────────────────┐  │
│   │ papers         │   │      │  │ OpenRouter (Gemini 2.0)  │  │
│   │ plagiarism_    │   │      │  │ Winston AI               │  │
│   │   checks       │   │      │  │ Google Translate         │  │
│   │ journals       │   │      │  │ Semantic Scholar         │  │
│   │ topics         │   │      │  │ arXiv API                │  │
│   │ users          │   │      │  │ CrossRef                 │  │
│   └────────────────┘   │      │  └──────────────────────────┘  │
│   (PostgreSQL + RLS)   │      │                                 │
└────────────────────────┘      └─────────────────────────────────┘
            │                                 │
            │                                 │
            ▼                                 ▼
┌────────────────────────┐      ┌─────────────────────────────────┐
│    Clerk Auth          │      │   Lingo.dev Translation         │
│  ┌──────────────────┐  │      │  ┌──────────────────────────┐  │
│  │ User Management  │  │      │  │ Static UI Translations   │  │
│  │ JWT Tokens       │  │      │  │ 13 Language Locales      │  │
│  │ OAuth Providers  │  │      │  │ Academic Glossary        │  │
│  └──────────────────┘  │      │  └──────────────────────────┘  │
└────────────────────────┘      └─────────────────────────────────┘
```

---

## Technology Stack

### Frontend Technologies

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| **Next.js** | 16.x | React framework with App Router | [nextjs.org](https://nextjs.org) |
| **React** | 19.x | UI component library | [react.dev](https://react.dev) |
| **TypeScript** | 5.x | Type-safe JavaScript | [typescriptlang.org](https://www.typescriptlang.org) |
| **Tailwind CSS** | 3.x | Utility-first CSS framework | [tailwindcss.com](https://tailwindcss.com) |
| **shadcn/ui** | Latest | Reusable component library | [ui.shadcn.com](https://ui.shadcn.com) |
| **Clerk** | Latest | Authentication provider | [clerk.com](https://clerk.com) |
| **Lingo.dev** | Latest | Internationalization platform | [lingo.dev](https://lingo.dev) |
| **Lucide Icons** | Latest | Icon library | [lucide.dev](https://lucide.dev) |

### Backend Technologies

| Technology | Version | Purpose | Documentation |
|------------|---------|---------|---------------|
| **FastAPI** | 0.100+ | Modern Python web framework | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| **Python** | 3.10+ | Programming language | [python.org](https://www.python.org) |
| **Pydantic** | 2.x | Data validation using Python type hints | [docs.pydantic.dev](https://docs.pydantic.dev) |
| **Uvicorn** | Latest | ASGI server | [uvicorn.org](https://www.uvicorn.org) |
| **Supabase** | Latest | PostgreSQL database + auth | [supabase.com](https://supabase.com) |
| **deep-translator** | Latest | Google Translate integration | [pypi.org](https://pypi.org/project/deep-translator/) |
| **httpx** | Latest | Async HTTP client | [python-httpx.org](https://www.python-httpx.org) |
| **python-dotenv** | Latest | Environment variable management | [pypi.org](https://pypi.org/project/python-dotenv/) |

### Development Tools

| Tool | Purpose |
|------|---------|
| **npm** | Frontend package manager |
| **pip** | Python package manager |
| **Git** | Version control |
| **VS Code** | Recommended IDE |
| **Postman** | API testing |
| **Swagger UI** | Interactive API documentation (built-in) |

---

## API Integrations

### 1. OpenRouter (Gemini 2.0 Flash Lite)

**Purpose**: Paper analysis with 17-section comprehensive breakdown

**Endpoint**: `https://openrouter.ai/api/v1/chat/completions`

**Authentication**: Bearer token (API key)

**Usage**:
- Upload PDF via multipart/form-data
- Send to Gemini with structured prompt
- Parse JSON response with 17 sections
- Cache translations in Supabase

**Pricing**: ~$0.0015 per paper

**Key Files**:
- `backend/app/services/gemini_service_v2.py`
- `backend/app/prompts/paper_analysis_prompt.py`

---

### 2. Winston AI

**Purpose**: Internet-wide plagiarism detection

**Endpoint**: `https://api.gowinston.ai/v2/plagiarism`

**Authentication**: API key in headers

**Features**:
- 45+ language support
- Attack detection (zero-width spaces, homoglyphs)
- Source attribution with snippets
- Batch similarity scoring

**Request Format**:
```json
{
  "text": "Research paper text to check...",
  "language": "en"
}
```

**Response Format**:
```json
{
  "score": 85.5,
  "plagiarism_score": 14.5,
  "sources": [...],
  "flagged_sections": [...],
  "scan_info": {
    "language_detected": "en",
    "sources_checked": 20
  }
}
```

**Pricing**: 2 credits per word

**Key Files**:
- `backend/app/services/winston_service.py`
- `backend/app/api/v1/plagiarism.py`

---

### 3. Semantic Scholar

**Purpose**: Academic paper search and metadata

**Endpoint**: `https://api.semanticscholar.org/graph/v1`

**Authentication**: Optional API key (higher rate limits)

**Usage**:
- Topic discovery (trending papers)
- Journal recommendations (paper metadata)
- Citation data
- Author information

**Rate Limits**:
- Without key: 100 requests/5 minutes
- With key: 1000 requests/5 minutes

**Key Files**:
- `backend/app/services/semantic_scholar_service.py`
- `backend/app/services/topics_service.py`

---

### 4. arXiv API

**Purpose**: Preprint paper discovery

**Endpoint**: `http://export.arxiv.org/api/query`

**Authentication**: None (public API)

**Usage**:
- Search recent preprints
- Topic discovery in STEM fields
- Author and category filtering

**Key Files**:
- `backend/app/services/arxiv_service.py`

---

### 5. CrossRef

**Purpose**: Citation metadata and journal information

**Endpoint**: `https://api.crossref.org`

**Authentication**: Polite pool with email

**Usage**:
- Journal metadata
- Citation suggestions
- DOI resolution

**Key Files**:
- `backend/app/services/crossref_service.py`

---

### 6. Google Translate (deep-translator)

**Purpose**: Dynamic content translation (Winston AI results)

**Implementation**: Python library (no API key needed)

**Supported Languages**: 100+ languages

**Usage**:
- Translate Winston AI source titles
- Translate flagged section text
- Preserve matching source text

**Key Files**:
- `backend/app/services/translation_service.py`

---

### 7. Lingo.dev

**Purpose**: Static UI translations (frontend)

**Implementation**: CLI tool + JSON locale files

**Workflow**:
1. Add translation keys to `locales/en.json`
2. Run `npx lingo.dev@latest run`
3. AI translates to all 13 languages
4. Import via `useLingo()` hook

**Key Files**:
- `frontend/locales/*.json` (13 files)
- `frontend/lib/useLingo.ts`
- `frontend/lib/lingo-config.ts`

---

### 8. Clerk

**Purpose**: User authentication and management

**Features**:
- Email/password authentication
- OAuth (Google, GitHub, etc.)
- JWT token generation
- User session management

**Integration Points**:
- Frontend: `@clerk/nextjs` components
- Backend: JWT validation via `CLERK_SECRET_KEY`

**Key Files**:
- `frontend/app/layout.tsx` (ClerkProvider)
- `backend/app/core/auth.py` (JWT validation)

---

### 9. Supabase

**Purpose**: PostgreSQL database with Row-Level Security

**Features**:
- Managed PostgreSQL database
- Real-time subscriptions (not used yet)
- Row-Level Security (RLS) for user data isolation
- Storage for future file uploads

**Tables**:
- `users` - User profiles synced from Clerk
- `papers` - Uploaded research papers
- `paper_translations` - Cached translations
- `plagiarism_checks` - Plagiarism check history
- `journals` - Journal metadata
- `topics` - Discovered topics

**Key Files**:
- `backend/app/core/database.py`
- `backend/supabase_setup.sql`

---

## Data Flow

### 1. Paper Analysis Flow (Enhanced API)

```
User uploads PDF
    ↓
Frontend sends to POST /api/v1/papers-enhanced/upload
    ↓
Backend validates auth (Clerk JWT)
    ↓
Save paper metadata to Supabase
    ↓
Send PDF to Gemini API (OpenRouter)
    ↓
Gemini analyzes with structured prompt (17 sections)
    ↓
Parse JSON response, validate with Pydantic
    ↓
Save analysis to Supabase (papers table)
    ↓
Return paper_id + analysis to frontend
    ↓
Frontend displays 17 sections in UI
    ↓
User requests translation to language X
    ↓
Backend checks translation cache
    ↓
If cached: Return immediately
    ↓
If not cached: Translate via Google Translate
    ↓
Cache translation in Supabase
    ↓
Return translated content to frontend
```

**Performance**: 1-3 seconds (3-5x faster than legacy)

---

### 2. Plagiarism Detection Flow

```
User pastes text (min 100 characters)
    ↓
Frontend sends to POST /api/v1/plagiarism/check
    ↓
Backend validates auth (Clerk JWT)
    ↓
Try Winston AI (primary):
    ↓
    Check WINSTON_API_KEY configured
    ↓
    Send text to Winston API
    ↓
    Parse response (sources, flagged sections, scores)
    ↓
    Calculate word counts and severity levels
    ↓
    Translate source titles/snippets to user's language
    ↓
    Save check to Supabase (plagiarism_checks)
    ↓
    Return enriched response to frontend
    ↓
If Winston fails: Fallback to legacy (Semantic Scholar)
    ↓
Frontend displays:
    - Originality score card (sticky sidebar)
    - Scrollable sources list (severity-based colors)
    - Flagged sections (sorted by severity)
    - Stats (word counts, scan time)
    - Tips for researchers
```

**Performance**: 2-3 seconds for internet-wide scan

---

### 3. Journal Recommendation Flow

```
User enters abstract + keywords
    ↓
Frontend sends to POST /api/v1/journals/recommend
    ↓
Backend validates auth
    ↓
Query Semantic Scholar for relevant journals
    ↓
Calculate semantic similarity (abstract vs journal scope)
    ↓
Score each journal (0-100%)
    ↓
Fetch metadata from CrossRef (impact factor, etc.)
    ↓
Rank by fit score + impact factor
    ↓
Return top 10 recommendations
    ↓
Frontend displays ranked journals with filters
```

---

### 4. Topic Discovery Flow

```
User searches for discipline (optional)
    ↓
Frontend sends to GET /api/v1/topics/trending
    ↓
Backend validates auth
    ↓
Parallel queries:
    - Semantic Scholar (recent high-citation papers)
    - arXiv (recent preprints)
    ↓
Calculate impact scores (citations × recency factor)
    ↓
Filter by discipline if specified
    ↓
Rank by impact score
    ↓
Return top N topics
    ↓
Frontend displays with citation counts and sources
```

---

## Database Schema

### Core Tables

#### `users`
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clerk_user_id TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy: Users can only see their own data
CREATE POLICY "Users can view own data"
  ON users FOR SELECT
  USING (clerk_user_id = current_setting('request.jwt.claim.sub'));
```

#### `papers`
```sql
CREATE TABLE papers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  authors TEXT,
  abstract TEXT,

  -- Gemini analysis (17 sections as JSONB)
  analysis JSONB,

  -- Metadata
  file_url TEXT,
  file_size INTEGER,
  paper_type TEXT, -- 'research', 'review', 'conference', etc.

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ,

  -- Full-text search
  search_vector TSVECTOR
);

-- RLS Policy: Users can only access their own papers
CREATE POLICY "Users can view own papers"
  ON papers FOR SELECT
  USING (user_id = (SELECT id FROM users WHERE clerk_user_id = current_setting('request.jwt.claim.sub')));
```

#### `paper_translations`
```sql
CREATE TABLE paper_translations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  paper_id UUID REFERENCES papers(id) ON DELETE CASCADE,
  language_code TEXT NOT NULL, -- 'en', 'hi', 'te', etc.
  translated_content JSONB NOT NULL, -- All 17 sections translated
  created_at TIMESTAMPTZ DEFAULT NOW(),

  UNIQUE(paper_id, language_code)
);

-- Index for fast lookups
CREATE INDEX idx_paper_translations_lookup ON paper_translations(paper_id, language_code);
```

#### `plagiarism_checks`
```sql
CREATE TABLE plagiarism_checks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Input
  text_content TEXT NOT NULL,
  language TEXT DEFAULT 'en',

  -- Results
  originality_score DECIMAL(5,2),
  plagiarism_score DECIMAL(5,2),
  total_word_count INTEGER,
  plagiarized_word_count INTEGER,

  -- Detailed results (JSONB)
  sources JSONB, -- Array of sources with match details
  flagged_sections JSONB, -- Array of flagged text segments
  scan_info JSONB, -- Language detected, sources checked, etc.

  -- Metadata
  provider TEXT DEFAULT 'winston_ai', -- 'winston_ai' or 'legacy'
  processing_time_seconds DECIMAL(5,2),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy
CREATE POLICY "Users can view own checks"
  ON plagiarism_checks FOR SELECT
  USING (user_id = (SELECT id FROM users WHERE clerk_user_id = current_setting('request.jwt.claim.sub')));
```

#### `journals`
```sql
CREATE TABLE journals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  publisher TEXT,
  issn TEXT,
  impact_factor DECIMAL(5,2),
  open_access BOOLEAN DEFAULT false,
  acceptance_rate DECIMAL(5,2),
  avg_review_time_days INTEGER,
  fields TEXT[], -- Array of research fields
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `topics`
```sql
CREATE TABLE topics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT,
  field TEXT,
  citation_count INTEGER DEFAULT 0,
  impact_score DECIMAL(10,2),
  source TEXT, -- 'semantic_scholar' or 'arxiv'
  source_id TEXT, -- External ID for reference
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Authentication Flow

### 1. Frontend Authentication (Clerk)

```
User visits app
    ↓
ClerkProvider wraps entire app (layout.tsx)
    ↓
User signs in (email/password or OAuth)
    ↓
Clerk creates session + JWT token
    ↓
JWT stored in HTTP-only cookie
    ↓
Every API request includes JWT in Authorization header
    ↓
Frontend uses useUser() hook to access user info
```

### 2. Backend JWT Validation

```
Request arrives at FastAPI endpoint
    ↓
Extract JWT from Authorization header
    ↓
Validate JWT signature using CLERK_SECRET_KEY
    ↓
Extract user ID (clerk_user_id) from JWT claims
    ↓
Look up user in Supabase users table
    ↓
If not found: Create user record (first-time login)
    ↓
Attach user object to request context
    ↓
Proceed with business logic (RLS enforced)
```

**Key Files**:
- `backend/app/core/auth.py` - JWT validation
- `backend/app/api/dependencies.py` - Auth dependency injection

---

## Translation System

### Architecture: Hybrid Approach

**Static UI (Lingo.dev)**:
- Translation keys defined in `locales/*.json`
- Translated once via Lingo.dev CLI
- Loaded client-side at runtime
- Fast, no API calls

**Dynamic Content (Google Translate)**:
- Winston AI results (source titles, snippets)
- Gemini analysis (if not cached)
- Translated on-demand server-side
- Cached in Supabase for reuse

### Translation Flow

```
Frontend Component
    ↓
Calls t('key') from useLingo() hook
    ↓
If static UI key: Return from loaded locale file
    ↓
If dynamic content (API response):
    ↓
    Backend receives language_code param
    ↓
    Check translation cache in Supabase
    ↓
    If cached: Return immediately
    ↓
    If not cached: Translate via Google Translate
    ↓
    Cache in Supabase (paper_translations table)
    ↓
    Return translated content
```

### Supported Languages (13)

| Code | Language | Native Name | Lingo.dev | Google Translate |
|------|----------|-------------|-----------|------------------|
| en | English | English | ✅ | ✅ |
| hi | Hindi | हिंदी | ✅ | ✅ |
| te | Telugu | తెలుగు | ✅ | ✅ |
| ta | Tamil | தமிழ் | ✅ | ✅ |
| bn | Bengali | বাংলা | ✅ | ✅ |
| mr | Marathi | मराठी | ✅ | ✅ |
| zh | Chinese | 中文 | ✅ | ✅ |
| es | Spanish | Español | ✅ | ✅ |
| fr | French | Français | ✅ | ✅ |
| pt | Portuguese | Português | ✅ | ✅ |
| de | German | Deutsch | ✅ | ✅ |
| ja | Japanese | 日本語 | ✅ | ✅ |
| ko | Korean | 한국어 | ✅ | ✅ |

---

## Feature Workflows

### Paper Analysis Workflow (v2.0 Enhanced)

**Input**: PDF file (multipart/form-data)

**Processing**:
1. Extract metadata (title, authors from PDF)
2. Send entire PDF to Gemini API (OpenRouter)
3. Use structured prompt for 17-section analysis
4. Parse JSON response, validate with Pydantic
5. Store in Supabase (`papers` table)

**17 Sections Analyzed**:
1. Title
2. Authors
3. Affiliations
4. Keywords
5. Abstract
6. Introduction
7. Literature Review
8. Research Gap
9. Research Questions
10. Methodology
11. Results
12. Discussion
13. Limitations
14. Future Work
15. Conclusion
16. References
17. Supplementary Materials

**Output**: JSON with all sections + metadata

**Translation**:
- User requests translation to language X
- Check `paper_translations` table for cache
- If missing: Translate all 17 sections via Google Translate
- Cache in `paper_translations` table
- Return translated content

**Performance**:
- Analysis: 1-3 seconds
- Translation (first time): 2-4 seconds
- Translation (cached): <100ms

---

### Plagiarism Detection Workflow (Winston AI)

**Input**: Text content (min 100 characters)

**Processing**:
1. Validate WINSTON_API_KEY configured
2. Send text to Winston AI API
3. Receive detailed analysis:
   - Originality score (0-100%)
   - Plagiarism score (0-100%)
   - Sources with URLs and snippets
   - Flagged sections with similarity scores
   - Language detection
4. Enrich response:
   - Calculate word counts
   - Classify severity (High/Medium/Low)
   - Translate source titles to user's language
   - Sort flagged sections by severity
5. Store in `plagiarism_checks` table
6. Return enhanced response

**Fallback**: If Winston unavailable, use legacy Semantic Scholar approach

**Output**:
```json
{
  "originality_score": 85.5,
  "plagiarism_score": 14.5,
  "total_word_count": 123,
  "plagiarized_word_count": 18,
  "sources": [...],
  "flagged_sections": [...],
  "scan_info": {
    "language_detected": "en",
    "sources_checked": 20
  },
  "processing_time_seconds": 2.3,
  "provider": "winston_ai"
}
```

---

## Deployment Architecture

### Production Setup

```
┌──────────────────────────────────────────────────────────┐
│                    Vercel (Frontend)                     │
│                                                          │
│  - Next.js 16 static/SSR pages                          │
│  - Edge functions for API routes                        │
│  - CDN for static assets                                │
│  - Auto-scaling                                          │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ HTTPS
                     ▼
┌──────────────────────────────────────────────────────────┐
│              Render/Railway (Backend)                    │
│                                                          │
│  - FastAPI app running on Uvicorn                       │
│  - Auto-scaling based on load                           │
│  - Health checks + auto-restart                         │
│  - Environment variables securely stored                │
└────────────────────┬─────────────────────────────────────┘
                     │
                     │ PostgreSQL Connection
                     ▼
┌──────────────────────────────────────────────────────────┐
│              Supabase (Database + Auth)                  │
│                                                          │
│  - Managed PostgreSQL database                          │
│  - Row-Level Security (RLS) enabled                     │
│  - Automatic backups                                     │
│  - Connection pooling                                    │
└──────────────────────────────────────────────────────────┘
```

### Environment Variables

**Frontend (Vercel)**:
```bash
NEXT_PUBLIC_API_URL=https://arsp-backend.onrender.com/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_xxx
CLERK_SECRET_KEY=sk_live_xxx
```

**Backend (Render/Railway)**:
```bash
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJxxx...
SUPABASE_SERVICE_KEY=eyJxxx...
CLERK_SECRET_KEY=sk_live_xxx
OPENROUTER_API_KEY=sk-or-v1-xxx
WINSTON_API_KEY=xxx
CORS_ORIGINS=https://arsp.vercel.app
PORT=8000
```

---

## Security Considerations

### 1. Authentication Security

- **JWT Validation**: All backend endpoints validate Clerk JWT
- **HTTP-Only Cookies**: Frontend stores tokens securely
- **CSRF Protection**: SameSite cookie attribute
- **OAuth Security**: Clerk handles OAuth flow securely

### 2. Database Security

- **Row-Level Security (RLS)**: Users can only access their own data
- **SQL Injection Prevention**: Supabase client sanitizes queries
- **Prepared Statements**: All queries use parameterized inputs
- **Connection Pooling**: Prevents connection exhaustion attacks

### 3. API Security

- **Rate Limiting**: Implement rate limiting on backend endpoints
- **API Key Rotation**: Support for key rotation without downtime
- **Input Validation**: Pydantic models validate all inputs
- **Output Sanitization**: XSS prevention on all outputs

### 4. Data Privacy (DPDP Compliance)

- **Consent Management**: Users consent before data processing
- **Data Minimization**: Only collect necessary data
- **Right to Deletion**: Users can delete their data
- **Data Portability**: Users can export their data

### 5. File Upload Security

- **File Type Validation**: Only PDF files accepted
- **File Size Limits**: Max 10MB per upload
- **Virus Scanning**: Future enhancement (ClamAV integration)
- **Secure Storage**: Files stored in Supabase Storage with RLS

---

## Performance Optimizations

### 1. Caching Strategy

- **Translation Cache**: Store translations in database (instant reuse)
- **HTTP Caching**: Cache-Control headers on static assets
- **Client-Side Caching**: React Query for API responses (future)

### 2. Async Processing

- **Async/Await**: All I/O operations are non-blocking
- **Parallel API Calls**: Use `asyncio.gather()` for concurrent requests
- **Background Tasks**: FastAPI background tasks for non-critical work

### 3. Database Optimization

- **Indexes**: B-tree indexes on frequently queried columns
- **Full-Text Search**: GIN indexes on text search vectors
- **Connection Pooling**: Reuse database connections

### 4. Frontend Optimization

- **Code Splitting**: Next.js automatic code splitting
- **Image Optimization**: Next.js Image component with lazy loading
- **Tree Shaking**: Remove unused code from bundles
- **Prefetching**: Prefetch data for likely next pages

---

## Monitoring and Logging

### Backend Logging

- **Structured Logging**: JSON logs with timestamps, levels, context
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Log Aggregation**: Send to centralized logging service (future)

### Error Tracking

- **Sentry Integration**: Capture and track errors (future)
- **Custom Error Handlers**: User-friendly error messages
- **Error Logging**: All exceptions logged with stack traces

### Performance Monitoring

- **API Latency**: Track response times for all endpoints
- **Database Query Performance**: Monitor slow queries
- **External API Latency**: Track third-party API response times

---

## Development Workflow

### Local Development

1. **Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn app.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Database**: Connect to Supabase cloud instance

### Testing Strategy

- **Unit Tests**: Test individual functions (future)
- **Integration Tests**: Test API endpoints (future)
- **E2E Tests**: Playwright/Cypress for full user flows (future)
- **Manual Testing**: Test via Swagger UI at `/docs`

### Deployment Process

1. **Push to GitHub**: `git push origin main`
2. **Automatic Deployment**:
   - Vercel deploys frontend automatically
   - Render/Railway deploys backend automatically
3. **Health Checks**: Verify deployments via `/health` endpoint
4. **Rollback**: Revert Git commit if issues detected

---

## Future Enhancements

### Planned Features

1. **Real-time Collaboration**: Multi-user paper editing
2. **Citation Formatter**: APA, MLA, Chicago styles
3. **Analytics Dashboard**: Research impact visualization
4. **Automated Testing**: Unit + Integration + E2E tests
5. **Mobile Apps**: React Native iOS/Android apps
6. **Browser Extension**: Quick plagiarism check from browser

### Performance Improvements

1. **Redis Caching**: Cache API responses for faster lookups
2. **CDN Integration**: CloudFlare for global asset delivery
3. **GraphQL API**: Alternative to REST for flexible queries
4. **WebSocket Support**: Real-time updates for long-running tasks

### Security Enhancements

1. **API Rate Limiting**: Protect against abuse
2. **DDoS Protection**: CloudFlare or similar
3. **Audit Logs**: Track all user actions
4. **Penetration Testing**: Regular security audits

---

## Support and Maintenance

### Contact

- **GitHub Issues**: [github.com/BishalJena/ARSP-v1/issues](https://github.com/BishalJena/ARSP-v1/issues)
- **Documentation**: See README.md and CHANGELOG.md
- **API Docs**: http://localhost:8000/docs (development)

### Versioning

- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Changelog**: All changes documented in CHANGELOG.md
- **Git Tags**: Each release tagged in Git

---

**Last Updated**: 2025-11-16
**Version**: 2.1.0
**Authors**: Bishal Jena
