# Design Document

## Overview

The AI-Enabled Research Support Platform (ARSP) is architected as a modern, serverless web application leveraging React 18 with Vite for the frontend, Supabase as the Backend-as-a-Service (BaaS), and Lingo.dev for comprehensive multilingual support. The system follows a component-based architecture with clear separation of concerns between presentation, business logic, and data layers.

### Design Principles

1. **Modularity**: Each feature module (Topic Selection, Literature Review, Citation/Plagiarism, Journal Recommendation) operates as an independent, self-contained unit with minimal coupling
2. **Multilingual-First**: Lingo.dev integration at every layer ensures seamless localization without retrofitting
3. **Privacy-by-Design**: Row Level Security (RLS) and encryption enforced at the database layer
4. **Performance-Optimized**: Caching strategies, lazy loading, and edge functions minimize latency
5. **Accessibility-Compliant**: WCAG 2.1 AA standards through shadcn/ui components and semantic HTML
6. **Scalability**: Serverless architecture with auto-scaling capabilities for 10K+ concurrent users

### Technology Stack Rationale

- **React 18 + Vite**: Fast development with Hot Module Replacement (HMR), optimal bundle sizes, and modern React features (Suspense, Concurrent Rendering)
- **TypeScript**: Type safety reduces runtime errors and improves developer experience
- **shadcn/ui + Tailwind CSS**: Accessible, customizable components with consistent design system
- **Supabase**: Integrated auth, database, storage, and edge functions eliminate backend complexity
- **Clerk**: Enterprise-grade authentication with federation support for APCCE integration
- **Lingo.dev**: AI-powered localization with context-awareness and glossary support for academic terminology
- **Hugging Face Inference API**: Free, high-quality NLP models for summarization and text analysis

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface Layer                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  React 18 + Vite + TypeScript + shadcn/ui Components    │  │
│  │  - Topic Selection Module                                │  │
│  │  - Literature Review Module                              │  │
│  │  - Citation/Plagiarism Module                            │  │
│  │  - Journal Recommendation Module                         │  │
│  │  - Dashboard & Navigation                                │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    Localization Layer (Lingo.dev)                │
│  ┌──────────────┬──────────────┬──────────────────────────┐    │
│  │  CLI (Build) │  SDK (Runtime)│  API (Backend)          │    │
│  │  - Static UI │  - Dynamic    │  - Input Translation    │    │
│  │  - CI/CD     │    Content    │  - Context-Aware        │    │
│  │              │  - Plurals    │  - Glossary Support     │    │
│  └──────────────┴──────────────┴──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    Authentication Layer (Clerk)                  │
│  - OAuth/Email Authentication                                    │
│  - Session Management                                            │
│  - User Metadata & Profiles                                      │
│  - APCCE Federation (Mock)                                       │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  Business Logic Layer (Edge Functions)           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Supabase Edge Functions (Deno Runtime)                  │  │
│  │  - /topics/recommend                                      │  │
│  │  - /lit/review                                            │  │
│  │  - /citation/plagcheck                                    │  │
│  │  - /journals/recommend                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                      AI/NLP Processing Layer                     │
│  ┌──────────────────┬──────────────────┬──────────────────┐    │
│  │  Hugging Face    │  TF-IDF Engine   │  Semantic Scholar│    │
│  │  Inference API   │  (Plagiarism)    │  arXiv, CrossRef │    │
│  │  - Summarization │  - Similarity    │  - Topic Data    │    │
│  │  - Classification│  - Originality   │  - Citations     │    │
│  └──────────────────┴──────────────────┴──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    Data Layer (Supabase)                         │
│  ┌──────────────────┬──────────────────┬──────────────────┐    │
│  │  PostgreSQL DB   │  Storage Buckets │  Realtime Sync   │    │
│  │  - profiles      │  - papers        │  - Draft Sync    │    │
│  │  - journals      │  - uploads       │  - Collaboration │    │
│  │  - drafts        │                  │                  │    │
│  │  - uploads       │                  │                  │    │
│  │  (RLS Enabled)   │  (RLS Policies)  │  (Subscriptions) │    │
│  └──────────────────┴──────────────────┴──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```


### Data Flow

#### User Authentication Flow
1. User accesses ARSP → Clerk detects unauthenticated state
2. Clerk presents login UI (email/OAuth)
3. User provides credentials → Clerk validates
4. Clerk creates session token → Returns to client
5. Client stores token in memory (NOT localStorage for security)
6. Supabase client configured with Clerk token for RLS enforcement
7. Profile record created/updated in Supabase `profiles` table
8. User redirected to dashboard with language auto-detection

#### Research Workflow Data Flow
1. **Topic Selection**: User query (any language) → Lingo API translates to English → Semantic Scholar/arXiv API → Results → Lingo SDK translates back → Display
2. **Literature Review**: PDF upload → Supabase Storage → Edge Function extracts text → HF Inference summarizes → Lingo SDK translates → Store in DB → Display
3. **Plagiarism Check**: Draft text → Edge Function → TF-IDF similarity → CrossRef citations → Lingo translates report → Real-time display
4. **Journal Recommendation**: Abstract → Edge Function → DB query with filters → Scoring algorithm → Lingo translates metadata → Sortable table

## Components and Interfaces

### Frontend Component Structure

```
src/
├── components/
│   ├── ui/                          # shadcn/ui components (auto-generated)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── table.tsx
│   │   ├── dialog.tsx
│   │   ├── dropdown-menu.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── select.tsx
│   │   ├── accordion.tsx
│   │   ├── badge.tsx
│   │   ├── alert.tsx
│   │   ├── skeleton.tsx
│   │   └── toast.tsx
│   ├── modules/                     # Feature modules
│   │   ├── TopicSelection/
│   │   │   ├── TopicSelector.tsx    # Main component
│   │   │   ├── TopicCard.tsx        # Individual topic display
│   │   │   ├── TopicFilters.tsx     # Filter controls
│   │   │   └── useTopics.ts         # Custom hook for data
│   │   ├── LiteratureReview/
│   │   │   ├── ReviewUploader.tsx   # File upload interface
│   │   │   ├── ReviewSummary.tsx    # Summary display
│   │   │   ├── InsightsList.tsx     # Key insights
│   │   │   ├── ReferenceExport.tsx  # Export functionality
│   │   │   └── useLitReview.ts      # Custom hook
│   │   ├── PlagiarismCheck/
│   │   │   ├── DraftEditor.tsx      # Text editor
│   │   │   ├── ScoreDisplay.tsx     # Originality score
│   │   │   ├── CitationSuggestions.tsx
│   │   │   └── usePlagiarism.ts
│   │   └── JournalRecommendation/
│   │       ├── JournalTable.tsx     # Results table
│   │       ├── JournalFilters.tsx   # Filter controls
│   │       ├── JournalCard.tsx      # Individual journal
│   │       └── useJournals.ts
│   ├── layout/
│   │   ├── DashboardLayout.tsx      # Main layout wrapper
│   │   ├── Header.tsx               # Top navigation
│   │   ├── Sidebar.tsx              # Side navigation
│   │   └── Footer.tsx
│   └── shared/
│       ├── LanguageSelector.tsx     # Language dropdown
│       ├── ConsentDialog.tsx        # DPDP consent
│       ├── LoadingState.tsx         # Loading indicators
│       └── ErrorBoundary.tsx        # Error handling
├── hooks/
│   ├── useAuth.ts                   # Clerk authentication
│   ├── useSupabase.ts               # Supabase client
│   ├── useLingo.ts                  # Lingo SDK wrapper
│   └── useLocalStorage.ts           # Offline storage
├── lib/
│   ├── supabase.ts                  # Supabase client config
│   ├── lingo.ts                     # Lingo SDK config
│   ├── api.ts                       # API client functions
│   ├── utils.ts                     # Utility functions
│   └── cn.ts                        # Class name utility
├── contexts/
│   ├── AuthContext.tsx              # Auth state management
│   ├── LanguageContext.tsx          # Language state
│   └── ThemeContext.tsx             # Dark mode
├── types/
│   ├── database.types.ts            # Supabase generated types
│   ├── api.types.ts                 # API response types
│   └── index.ts                     # Shared types
└── styles/
    └── globals.css                  # Global styles + Tailwind
```


### Key Component Interfaces

#### TopicSelector Component
```typescript
interface TopicSelectorProps {
  onTopicSelect: (topic: Topic) => void;
  initialQuery?: string;
}

interface Topic {
  id: string;
  title: string;
  brief: string;
  impact: number;
  source: 'arxiv' | 'semantic_scholar';
  url: string;
}

// Usage
<TopicSelector 
  onTopicSelect={(topic) => console.log(topic)}
  initialQuery="AI Ethics"
/>
```

#### ReviewUploader Component
```typescript
interface ReviewUploaderProps {
  onReviewComplete: (review: LiteratureReview) => void;
  maxFiles?: number;
  maxSizeMB?: number;
}

interface LiteratureReview {
  id: string;
  summary: string;
  insights: string[];
  references: Reference[];
  uploadedFiles: string[];
  createdAt: Date;
}

interface Reference {
  doi?: string;
  title: string;
  authors: string[];
  year: number;
  journal?: string;
}
```

#### DraftEditor Component
```typescript
interface DraftEditorProps {
  initialContent?: string;
  onScoreUpdate: (score: PlagiarismScore) => void;
  autoSave?: boolean;
}

interface PlagiarismScore {
  originality: number; // 0-100
  flaggedSections: FlaggedSection[];
  citations: CitationSuggestion[];
  lastChecked: Date;
}

interface FlaggedSection {
  text: string;
  startIndex: number;
  endIndex: number;
  similarity: number;
  source?: string;
}

interface CitationSuggestion {
  doi: string;
  title: string;
  relevance: number;
  snippet: string;
}
```

#### JournalTable Component
```typescript
interface JournalTableProps {
  abstract: string;
  filters?: JournalFilters;
  onJournalSelect: (journal: Journal) => void;
}

interface Journal {
  id: string;
  name: string;
  description: string;
  impactFactor: number;
  hIndex: number;
  isOpenAccess: boolean;
  publicationTime: number; // months
  fitScore: number; // 0-100
  domain: string;
  url: string;
}

interface JournalFilters {
  openAccessOnly?: boolean;
  minImpactFactor?: number;
  maxPublicationTime?: number;
  domain?: string;
}
```

### Custom Hooks

#### useAuth Hook
```typescript
interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
  updateProfile: (data: Partial<Profile>) => Promise<void>;
}

// Implementation leverages Clerk's useUser and useAuth hooks
```

#### useLingo Hook
```typescript
interface UseLingoReturn {
  translate: (params: TranslateParams) => Promise<string>;
  pluralize: (params: PluralizeParams) => string;
  currentLanguage: string;
  setLanguage: (lang: string) => void;
  supportedLanguages: Language[];
}

interface TranslateParams {
  text: string;
  target?: string;
  context?: string;
  glossary?: Record<string, string>;
  voice?: 'formal_academic' | 'casual';
}

interface PluralizeParams {
  count: number;
  key: string;
  target?: string;
}
```

#### useSupabase Hook
```typescript
interface UseSupabaseReturn {
  client: SupabaseClient;
  upload: (file: File, bucket: string) => Promise<string>;
  download: (path: string, bucket: string) => Promise<Blob>;
  query: <T>(table: string, options?: QueryOptions) => Promise<T[]>;
  upsert: <T>(table: string, data: T) => Promise<T>;
}
```


## Data Models

### Database Schema (Supabase PostgreSQL)

#### profiles Table
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  full_name TEXT,
  discipline TEXT,
  institution TEXT,
  publication_count INTEGER DEFAULT 0,
  preferred_language TEXT DEFAULT 'en',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
  ON profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);
```

#### drafts Table
```sql
CREATE TABLE drafts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT,
  content TEXT NOT NULL,
  plagiarism_score NUMERIC(5,2),
  last_checked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE drafts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own drafts"
  ON drafts FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Indexes
CREATE INDEX idx_drafts_user_id ON drafts(user_id);
CREATE INDEX idx_drafts_updated_at ON drafts(updated_at DESC);
```

#### uploads Table
```sql
CREATE TABLE uploads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  file_name TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER NOT NULL,
  mime_type TEXT NOT NULL,
  review_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE uploads ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own uploads"
  ON uploads FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Indexes
CREATE INDEX idx_uploads_user_id ON uploads(user_id);
CREATE INDEX idx_uploads_review_id ON uploads(review_id);
```

#### literature_reviews Table
```sql
CREATE TABLE literature_reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT,
  summary TEXT NOT NULL,
  insights JSONB DEFAULT '[]'::jsonb,
  references JSONB DEFAULT '[]'::jsonb,
  language TEXT DEFAULT 'en',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE literature_reviews ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage own reviews"
  ON literature_reviews FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Indexes
CREATE INDEX idx_reviews_user_id ON literature_reviews(user_id);
CREATE INDEX idx_reviews_created_at ON literature_reviews(created_at DESC);
```

#### journals Table (Mock Data)
```sql
CREATE TABLE journals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  impact_factor NUMERIC(5,2) NOT NULL,
  h_index INTEGER,
  is_open_access BOOLEAN DEFAULT false,
  publication_time_months INTEGER,
  domain TEXT NOT NULL,
  url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Public read access for journal data
ALTER TABLE journals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view journals"
  ON journals FOR SELECT
  USING (true);

-- Indexes
CREATE INDEX idx_journals_domain ON journals(domain);
CREATE INDEX idx_journals_impact_factor ON journals(impact_factor DESC);
CREATE INDEX idx_journals_open_access ON journals(is_open_access);
```


### Storage Buckets

#### papers Bucket
```sql
-- Storage bucket for uploaded research papers
INSERT INTO storage.buckets (id, name, public)
VALUES ('papers', 'papers', false);

-- RLS Policies for papers bucket
CREATE POLICY "Users can upload own papers"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'papers' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can view own papers"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'papers' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );

CREATE POLICY "Users can delete own papers"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'papers' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
```

### TypeScript Types

```typescript
// Database types (auto-generated by Supabase CLI)
export interface Database {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          email: string;
          full_name: string | null;
          discipline: string | null;
          institution: string | null;
          publication_count: number;
          preferred_language: string;
          created_at: string;
          updated_at: string;
        };
        Insert: Omit<Row, 'id' | 'created_at' | 'updated_at'>;
        Update: Partial<Insert>;
      };
      drafts: {
        Row: {
          id: string;
          user_id: string;
          title: string | null;
          content: string;
          plagiarism_score: number | null;
          last_checked_at: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: Omit<Row, 'id' | 'created_at' | 'updated_at'>;
        Update: Partial<Insert>;
      };
      // ... other tables
    };
  };
}

// Application types
export type Profile = Database['public']['Tables']['profiles']['Row'];
export type Draft = Database['public']['Tables']['drafts']['Row'];
export type LiteratureReview = Database['public']['Tables']['literature_reviews']['Row'];
export type Journal = Database['public']['Tables']['journals']['Row'];
```

## Error Handling

### Error Handling Strategy

1. **Network Errors**: Retry with exponential backoff (3 attempts max)
2. **API Errors**: Display user-friendly messages via toast notifications (Lingo-translated)
3. **Validation Errors**: Inline form validation with clear error messages
4. **Authentication Errors**: Redirect to login with return URL preservation
5. **Rate Limiting**: Queue requests and display progress indicators
6. **Offline Mode**: Store drafts locally, sync when online

### Error Boundary Implementation

```typescript
class ErrorBoundary extends React.Component<Props, State> {
  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Log to monitoring service (e.g., Sentry)
    console.error('Error caught by boundary:', error, errorInfo);
    
    // Display user-friendly error via Lingo
    const { translate } = useLingo();
    toast.error(translate({
      text: 'An unexpected error occurred. Please try again.',
      context: 'error_message'
    }));
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onReset={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

### API Error Handling

```typescript
async function handleApiCall<T>(
  apiCall: () => Promise<T>,
  options?: ErrorHandlingOptions
): Promise<T> {
  const maxRetries = options?.maxRetries ?? 3;
  let lastError: Error;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await apiCall();
    } catch (error) {
      lastError = error as Error;
      
      // Don't retry on client errors (4xx)
      if (error.status >= 400 && error.status < 500) {
        break;
      }
      
      // Exponential backoff
      if (attempt < maxRetries - 1) {
        await sleep(Math.pow(2, attempt) * 1000);
      }
    }
  }

  // Translate and display error
  const { translate } = useLingo();
  const errorMessage = await translate({
    text: getErrorMessage(lastError),
    context: 'error_message'
  });
  
  toast.error(errorMessage);
  throw lastError;
}
```


## Testing Strategy

### Testing Pyramid

```
                    ┌─────────────┐
                    │   E2E Tests │  (10%)
                    │  Cypress    │
                    └─────────────┘
                  ┌───────────────────┐
                  │ Integration Tests │  (30%)
                  │  React Testing    │
                  │     Library       │
                  └───────────────────┘
              ┌─────────────────────────────┐
              │      Unit Tests             │  (60%)
              │  Jest + Vitest              │
              │  - Utilities                │
              │  - Hooks                    │
              │  - API Functions            │
              └─────────────────────────────┘
```

### Unit Testing

**Target**: 80% code coverage minimum

```typescript
// Example: useLingo hook test
describe('useLingo', () => {
  it('should translate text with context', async () => {
    const { result } = renderHook(() => useLingo());
    
    const translated = await result.current.translate({
      text: 'Hello',
      target: 'es',
      context: 'greeting'
    });
    
    expect(translated).toBe('Hola');
  });

  it('should apply pluralization rules', () => {
    const { result } = renderHook(() => useLingo());
    
    const singular = result.current.pluralize({
      count: 1,
      key: 'papers_found',
      target: 'en'
    });
    
    const plural = result.current.pluralize({
      count: 5,
      key: 'papers_found',
      target: 'en'
    });
    
    expect(singular).toBe('1 paper found');
    expect(plural).toBe('5 papers found');
  });
});

// Example: Plagiarism detection test
describe('calculatePlagiarismScore', () => {
  it('should return 100 for completely original text', () => {
    const score = calculatePlagiarismScore(
      'This is completely unique text',
      []
    );
    expect(score).toBe(100);
  });

  it('should flag sections with >20% similarity', () => {
    const result = calculatePlagiarismScore(
      'The quick brown fox jumps over the lazy dog',
      ['The quick brown fox jumps over the lazy dog']
    );
    expect(result.flaggedSections).toHaveLength(1);
    expect(result.flaggedSections[0].similarity).toBeGreaterThan(20);
  });

  it('should achieve 95% accuracy threshold', () => {
    const testCases = loadTestCases('plagiarism_test_data.json');
    const results = testCases.map(tc => 
      calculatePlagiarismScore(tc.text, tc.corpus)
    );
    
    const accuracy = calculateAccuracy(results, testCases);
    expect(accuracy).toBeGreaterThanOrEqual(0.95);
  });
});
```

### Integration Testing

```typescript
// Example: Topic selection flow
describe('TopicSelector Integration', () => {
  it('should fetch and display topics in user language', async () => {
    const { user } = renderWithProviders(
      <TopicSelector onTopicSelect={jest.fn()} />,
      { language: 'zh-CN' }
    );
    
    // Enter query
    const input = screen.getByPlaceholderText(/search topics/i);
    await user.type(input, 'AI Ethics');
    
    // Submit
    await user.click(screen.getByRole('button', { name: /search/i }));
    
    // Wait for results
    await waitFor(() => {
      expect(screen.getByText(/5 topics found/i)).toBeInTheDocument();
    });
    
    // Verify Chinese translation
    const topics = screen.getAllByTestId('topic-card');
    expect(topics[0]).toHaveTextContent(/人工智能伦理/);
  });
});

// Example: Literature review flow
describe('Literature Review Integration', () => {
  it('should upload, process, and display review', async () => {
    const { user } = renderWithProviders(<ReviewUploader />);
    
    // Upload file
    const file = new File(['test content'], 'paper.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText(/upload papers/i);
    await user.upload(input, file);
    
    // Wait for processing
    await waitFor(() => {
      expect(screen.getByText(/processing/i)).toBeInTheDocument();
    }, { timeout: 10000 });
    
    // Verify summary displayed
    await waitFor(() => {
      expect(screen.getByTestId('review-summary')).toBeInTheDocument();
    });
    
    // Verify insights
    const insights = screen.getAllByTestId('insight-item');
    expect(insights.length).toBeGreaterThanOrEqual(5);
  });
});
```

### End-to-End Testing

```typescript
// Example: Complete research workflow
describe('Complete Research Workflow', () => {
  it('should complete full workflow from login to journal recommendation', () => {
    // Login
    cy.visit('/');
    cy.get('[data-testid="email-input"]').type('test@example.com');
    cy.get('[data-testid="password-input"]').type('password123');
    cy.get('[data-testid="login-button"]').click();
    
    // Select language
    cy.get('[data-testid="language-selector"]').click();
    cy.get('[data-value="zh-CN"]').click();
    
    // Topic selection
    cy.get('[data-testid="topic-search"]').type('AI Ethics');
    cy.get('[data-testid="search-button"]').click();
    cy.get('[data-testid="topic-card"]').first().click();
    
    // Literature review
    cy.get('[data-testid="lit-review-tab"]').click();
    cy.get('[data-testid="file-upload"]').attachFile('sample-paper.pdf');
    cy.get('[data-testid="review-summary"]', { timeout: 60000 }).should('be.visible');
    
    // Plagiarism check
    cy.get('[data-testid="plagiarism-tab"]').click();
    cy.get('[data-testid="draft-editor"]').type('This is my research draft...');
    cy.get('[data-testid="check-button"]').click();
    cy.get('[data-testid="originality-score"]').should('contain', '%');
    
    // Journal recommendation
    cy.get('[data-testid="journals-tab"]').click();
    cy.get('[data-testid="abstract-input"]').type('Abstract text...');
    cy.get('[data-testid="recommend-button"]').click();
    cy.get('[data-testid="journal-table"]').should('be.visible');
    cy.get('[data-testid="journal-row"]').should('have.length.at.least', 5);
  });
});
```

### Performance Testing

```typescript
// Example: Load testing with Artillery
// artillery.yml
config:
  target: 'https://arsp.vercel.app'
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Peak load"

scenarios:
  - name: "Research workflow"
    flow:
      - post:
          url: "/api/auth/login"
          json:
            email: "test@example.com"
            password: "password123"
      - post:
          url: "/api/topics/recommend"
          json:
            query: "AI Ethics"
            lang: "en"
      - post:
          url: "/api/journals/recommend"
          json:
            abstract: "This paper explores..."
            filters: { openAccessOnly: true }
```

### Accessibility Testing

```typescript
// Example: WCAG compliance test
describe('Accessibility', () => {
  it('should have no accessibility violations', async () => {
    const { container } = render(<TopicSelector />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should support keyboard navigation', async () => {
    const { user } = render(<JournalTable journals={mockJournals} />);
    
    // Tab through table
    await user.tab();
    expect(screen.getByRole('row', { name: /journal 1/i })).toHaveFocus();
    
    await user.tab();
    expect(screen.getByRole('row', { name: /journal 2/i })).toHaveFocus();
  });

  it('should provide screen reader labels', () => {
    render(<DraftEditor />);
    
    expect(screen.getByLabelText(/draft content/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/originality score/i)).toBeInTheDocument();
  });
});
```


## Multilingual Implementation (Lingo.dev)

### Lingo.dev Integration Architecture

ARSP implements a three-tier Lingo.dev integration strategy to maximize the WeMakeDevs hackathon scoring:

#### 1. CLI Integration (Build-Time)

**Purpose**: Translate static UI strings during build process

```json
// i18n.config.json
{
  "$schema": "https://lingo.dev/schema/i18n.json",
  "version": 1.5,
  "locale": {
    "source": "en",
    "targets": [
      "es-ES", "es-419", "fr-FR", "fr-CA", "de", 
      "ja", "zh-CN", "zh-TW", "ko", "pt", "it", "ru"
    ]
  },
  "buckets": {
    "json": {
      "include": ["src/locales/[locale].json"]
    }
  }
}
```

```json
// src/locales/en.json (source)
{
  "nav": {
    "dashboard": "Dashboard",
    "topics": "Topic Selection",
    "literature": "Literature Review",
    "plagiarism": "Plagiarism Check",
    "journals": "Journal Recommendations"
  },
  "common": {
    "loading": "Loading...",
    "error": "An error occurred",
    "save": "Save",
    "cancel": "Cancel",
    "submit": "Submit"
  },
  "topics": {
    "search_placeholder": "Search research topics...",
    "no_results": "No topics found",
    "impact_score": "Impact Score"
  }
}
```

```bash
# Build script with Lingo CLI
npx lingo.dev@latest i18n --frozen

# CI/CD integration (GitHub Actions)
- name: Translate UI strings
  run: npx lingo.dev@latest i18n --frozen
  
- name: Verify translations
  run: |
    if [ ! -f "src/locales/zh-CN.json" ]; then
      echo "Translation failed"
      exit 1
    fi
```

#### 2. SDK Integration (Runtime)

**Purpose**: Translate dynamic, user-generated content with context awareness

```typescript
// lib/lingo.ts
import { LingoDotDevEngine } from 'lingo.dev/sdk';

export const lingoClient = new LingoDotDevEngine({
  apiKey: import.meta.env.VITE_LINGO_API_KEY,
  defaultSourceLocale: 'en',
});

// Academic glossary for consistent terminology
export const academicGlossary = {
  'H-index': {
    'zh-CN': 'H指数',
    'ja': 'H指数',
    'es': 'Índice H',
    'fr': 'Indice H',
    'de': 'H-Index',
    'ru': 'Индекс Хирша'
  },
  'Impact Factor': {
    'zh-CN': '影响因子',
    'ja': 'インパクトファクター',
    'es': 'Factor de Impacto',
    'fr': 'Facteur d\'Impact',
    'de': 'Impact-Faktor',
    'ru': 'Импакт-фактор'
  },
  'Plagiarism Score': {
    'zh-CN': '剽窃分数',
    'ja': '盗用スコア',
    'es': 'Puntuación de Plagio',
    'fr': 'Score de Plagiat',
    'de': 'Plagiatswert',
    'ru': 'Оценка плагиата'
  },
  'Citation Analysis': {
    'zh-CN': '引用分析',
    'ja': '引用分析',
    'es': 'Análisis de Citas',
    'fr': 'Analyse des Citations',
    'de': 'Zitationsanalyse',
    'ru': 'Анализ цитирования'
  }
};
```

```typescript
// hooks/useLingo.ts
import { useContext, useCallback } from 'react';
import { LanguageContext } from '@/contexts/LanguageContext';
import { lingoClient, academicGlossary } from '@/lib/lingo';

export function useLingo() {
  const { currentLanguage, setLanguage } = useContext(LanguageContext);

  const translate = useCallback(async (params: {
    text: string;
    target?: string;
    context?: string;
    glossary?: Record<string, string>;
    voice?: 'formal_academic' | 'casual';
  }) => {
    const targetLang = params.target || currentLanguage;
    
    try {
      const result = await lingoClient.localizeObject(
        { text: params.text },
        {
          sourceLocale: 'en',
          targetLocale: targetLang,
          context: params.context || 'academic_research',
          glossary: { ...academicGlossary, ...params.glossary },
          tone: params.voice || 'formal_academic'
        }
      );
      
      return result.text;
    } catch (error) {
      console.error('Translation error:', error);
      return params.text; // Fallback to original
    }
  }, [currentLanguage]);

  const pluralize = useCallback((params: {
    count: number;
    key: string;
    target?: string;
  }) => {
    const targetLang = params.target || currentLanguage;
    
    // Lingo SDK handles pluralization rules per language
    return lingoClient.pluralize({
      count: params.count,
      key: params.key,
      locale: targetLang
    });
  }, [currentLanguage]);

  return {
    translate,
    pluralize,
    currentLanguage,
    setLanguage,
    supportedLanguages: [
      { code: 'en', name: 'English' },
      { code: 'es', name: 'Español' },
      { code: 'fr', name: 'Français' },
      { code: 'de', name: 'Deutsch' },
      { code: 'ja', name: '日本語' },
      { code: 'zh-CN', name: '简体中文' },
      { code: 'zh-TW', name: '繁體中文' },
      { code: 'ko', name: '한국어' },
      { code: 'pt', name: 'Português' },
      { code: 'it', name: 'Italiano' },
      { code: 'ru', name: 'Русский' }
    ]
  };
}
```

#### 3. API Integration (Backend)

**Purpose**: Translate user inputs and API responses in edge functions

```typescript
// supabase/functions/topics-recommend/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { LingoDotDevEngine } from 'npm:lingo.dev/sdk';

const lingo = new LingoDotDevEngine({
  apiKey: Deno.env.get('LINGO_API_KEY')!
});

serve(async (req) => {
  const { query, lang } = await req.json();
  
  // Translate user query to English for API calls
  const translatedQuery = await lingo.localizeObject(
    { text: query },
    {
      sourceLocale: lang,
      targetLocale: 'en',
      context: 'academic_research_query'
    }
  );
  
  // Fetch topics from Semantic Scholar
  const topics = await fetchTopics(translatedQuery.text);
  
  // Translate results back to user's language
  const translatedTopics = await Promise.all(
    topics.map(async (topic) => ({
      ...topic,
      title: await lingo.localizeObject(
        { text: topic.title },
        {
          sourceLocale: 'en',
          targetLocale: lang,
          context: 'research_topic_title'
        }
      ).then(r => r.text),
      brief: await lingo.localizeObject(
        { text: topic.brief },
        {
          sourceLocale: 'en',
          targetLocale: lang,
          context: 'research_topic_description',
          tone: 'formal_academic'
        }
      ).then(r => r.text)
    }))
  );
  
  return new Response(JSON.stringify({ topics: translatedTopics }), {
    headers: { 'Content-Type': 'application/json' }
  });
});
```

### Context-Aware Translation Examples

```typescript
// Example 1: Literature review summary
const summary = await translate({
  text: 'This paper explores the ethical implications of AI in healthcare...',
  context: 'literature_review_summary',
  voice: 'formal_academic',
  glossary: {
    'AI': 'Artificial Intelligence',
    'healthcare': 'medical care system'
  }
});

// Example 2: Plagiarism report
const report = await translate({
  text: '8% similarity detected in section 3. Review flagged passages.',
  context: 'plagiarism_report',
  voice: 'formal_academic'
});

// Example 3: Journal description
const description = await translate({
  text: 'High-impact journal focusing on computational linguistics',
  context: 'journal_description',
  glossary: {
    'High-impact': 'prestigious',
    'computational linguistics': 'NLP research'
  }
});
```

### Pluralization Implementation

```typescript
// English
pluralize({ count: 1, key: 'papers_found' }) 
// → "1 paper found"

pluralize({ count: 5, key: 'papers_found' }) 
// → "5 papers found"

// Chinese (no plural form)
pluralize({ count: 1, key: 'papers_found', target: 'zh-CN' }) 
// → "找到 1 篇论文"

pluralize({ count: 5, key: 'papers_found', target: 'zh-CN' }) 
// → "找到 5 篇论文"

// Russian (complex plural rules)
pluralize({ count: 1, key: 'papers_found', target: 'ru' }) 
// → "Найдена 1 статья"

pluralize({ count: 2, key: 'papers_found', target: 'ru' }) 
// → "Найдены 2 статьи"

pluralize({ count: 5, key: 'papers_found', target: 'ru' }) 
// → "Найдено 5 статей"
```


## Security and Privacy

### Authentication Security

#### Clerk Integration
```typescript
// main.tsx
import { ClerkProvider } from '@clerk/clerk-react';

const clerkPubKey = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={clerkPubKey}>
      <App />
    </ClerkProvider>
  </React.StrictMode>
);
```

#### Session Management
- Tokens stored in memory only (NOT localStorage)
- Automatic token refresh via Clerk
- Session timeout: 30 minutes of inactivity
- Secure cookie flags: HttpOnly, Secure, SameSite=Strict

#### Supabase Auth Integration
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';
import { useAuth } from '@clerk/clerk-react';

export function useSupabaseClient() {
  const { getToken } = useAuth();
  
  const supabase = createClient(
    import.meta.env.VITE_SUPABASE_URL,
    import.meta.env.VITE_SUPABASE_ANON_KEY,
    {
      global: {
        headers: async () => {
          const token = await getToken({ template: 'supabase' });
          return token ? { Authorization: `Bearer ${token}` } : {};
        }
      }
    }
  );
  
  return supabase;
}
```

### Data Encryption

#### At Rest
- Database: PostgreSQL native encryption (AES-256)
- Storage: Supabase Storage encryption enabled
- Backups: Encrypted with separate keys

#### In Transit
- All connections: TLS 1.3
- API calls: HTTPS only
- WebSocket (Realtime): WSS protocol

#### Client-Side Encryption for Sensitive Data
```typescript
// lib/encryption.ts
export async function encryptFile(file: File): Promise<ArrayBuffer> {
  const key = await crypto.subtle.generateKey(
    { name: 'AES-GCM', length: 256 },
    true,
    ['encrypt', 'decrypt']
  );
  
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const fileBuffer = await file.arrayBuffer();
  
  const encrypted = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    fileBuffer
  );
  
  // Store key securely (e.g., in Supabase with RLS)
  await storeEncryptionKey(key, file.name);
  
  return encrypted;
}
```

### Row Level Security (RLS) Policies

#### Security Definer Functions
```sql
-- Helper function to check user ownership
CREATE OR REPLACE FUNCTION private.is_owner(user_id UUID, resource_user_id UUID)
RETURNS BOOLEAN
LANGUAGE SQL
SECURITY DEFINER
AS $$
  SELECT user_id = resource_user_id;
$$;

-- Helper function to check if user can access review
CREATE OR REPLACE FUNCTION private.can_access_review(review_id UUID, user_id UUID)
RETURNS BOOLEAN
LANGUAGE SQL
SECURITY DEFINER
AS $$
  SELECT EXISTS (
    SELECT 1 FROM literature_reviews
    WHERE id = review_id AND user_id = user_id
  );
$$;
```

#### Complex RLS Policy Example
```sql
-- Drafts table with time-based access
CREATE POLICY "Users can access own recent drafts"
  ON drafts FOR SELECT
  USING (
    auth.uid() = user_id AND
    updated_at > NOW() - INTERVAL '90 days'
  );

-- Uploads table with size limits
CREATE POLICY "Users can upload files within quota"
  ON uploads FOR INSERT
  WITH CHECK (
    auth.uid() = user_id AND
    (
      SELECT COALESCE(SUM(file_size), 0) + NEW.file_size
      FROM uploads
      WHERE user_id = auth.uid()
    ) <= 500 * 1024 * 1024 -- 500MB limit
  );
```

### DPDP Compliance

#### Consent Management
```typescript
// components/shared/ConsentDialog.tsx
export function ConsentDialog() {
  const { translate } = useLingo();
  const [open, setOpen] = useState(false);
  
  useEffect(() => {
    const hasConsented = localStorage.getItem('dpdp_consent');
    if (!hasConsented) {
      setOpen(true);
    }
  }, []);
  
  const handleAccept = async () => {
    // Log consent to database
    await supabase.from('consent_logs').insert({
      user_id: user.id,
      consent_type: 'data_processing',
      consent_given: true,
      ip_address: await getClientIP(),
      timestamp: new Date().toISOString()
    });
    
    localStorage.setItem('dpdp_consent', 'true');
    setOpen(false);
  };
  
  return (
    <Dialog open={open}>
      <DialogContent>
        <DialogTitle>
          {await translate({ text: 'Data Privacy Notice', context: 'legal' })}
        </DialogTitle>
        <DialogDescription>
          {await translate({ 
            text: 'We collect and process your research data to provide AI-powered assistance. Your data is encrypted and never shared with third parties.',
            context: 'privacy_notice',
            voice: 'formal_academic'
          })}
        </DialogDescription>
        <DialogFooter>
          <Button onClick={handleAccept}>
            {await translate({ text: 'I Accept', context: 'legal' })}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

#### Data Retention Policy
```sql
-- Auto-delete old drafts after 90 days
CREATE OR REPLACE FUNCTION delete_old_drafts()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM drafts
  WHERE updated_at < NOW() - INTERVAL '90 days';
END;
$$;

-- Schedule daily cleanup
SELECT cron.schedule(
  'delete-old-drafts',
  '0 2 * * *', -- 2 AM daily
  'SELECT delete_old_drafts();'
);
```

#### Data Export (Right to Data Portability)
```typescript
// API endpoint: /api/export-data
export async function exportUserData(userId: string) {
  const supabase = createClient();
  
  const [profile, drafts, reviews, uploads] = await Promise.all([
    supabase.from('profiles').select('*').eq('id', userId).single(),
    supabase.from('drafts').select('*').eq('user_id', userId),
    supabase.from('literature_reviews').select('*').eq('user_id', userId),
    supabase.from('uploads').select('*').eq('user_id', userId)
  ]);
  
  const exportData = {
    profile: profile.data,
    drafts: drafts.data,
    reviews: reviews.data,
    uploads: uploads.data,
    exported_at: new Date().toISOString()
  };
  
  return new Response(JSON.stringify(exportData, null, 2), {
    headers: {
      'Content-Type': 'application/json',
      'Content-Disposition': `attachment; filename="arsp-data-${userId}.json"`
    }
  });
}
```

### Rate Limiting

```typescript
// middleware/rateLimit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(50, '1 m'), // 50 requests per minute
  analytics: true
});

export async function rateLimitMiddleware(req: Request) {
  const identifier = req.headers.get('x-forwarded-for') || 'anonymous';
  const { success, limit, reset, remaining } = await ratelimit.limit(identifier);
  
  if (!success) {
    return new Response('Rate limit exceeded', {
      status: 429,
      headers: {
        'X-RateLimit-Limit': limit.toString(),
        'X-RateLimit-Remaining': remaining.toString(),
        'X-RateLimit-Reset': reset.toString()
      }
    });
  }
  
  return null; // Continue
}
```

### Input Validation and Sanitization

```typescript
// lib/validation.ts
import { z } from 'zod';
import DOMPurify from 'dompurify';

// Schema validation
export const topicQuerySchema = z.object({
  query: z.string().min(3).max(200),
  lang: z.enum(['en', 'es', 'fr', 'de', 'ja', 'zh-CN', 'zh-TW', 'ko', 'pt', 'it', 'ru'])
});

export const draftSchema = z.object({
  title: z.string().max(200).optional(),
  content: z.string().min(10).max(50000),
  user_id: z.string().uuid()
});

// Sanitize HTML content
export function sanitizeHTML(html: string): string {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'u', 'a'],
    ALLOWED_ATTR: ['href', 'target']
  });
}

// Sanitize file names
export function sanitizeFileName(fileName: string): string {
  return fileName
    .replace(/[^a-zA-Z0-9.-]/g, '_')
    .substring(0, 255);
}
```


## Performance Optimization

### Caching Strategy

#### Client-Side Caching
```typescript
// lib/cache.ts
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: false,
      retry: 3
    }
  }
});

// Example: Cached topic query
export function useTopics(query: string) {
  return useQuery({
    queryKey: ['topics', query],
    queryFn: () => fetchTopics(query),
    staleTime: 10 * 60 * 1000, // Topics don't change frequently
    enabled: query.length >= 3
  });
}
```

#### Server-Side Caching (Supabase Edge Functions)
```typescript
// supabase/functions/_shared/cache.ts
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export function getCached<T>(key: string): T | null {
  const cached = cache.get(key);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data as T;
  }
  cache.delete(key);
  return null;
}

export function setCache<T>(key: string, data: T): void {
  cache.set(key, { data, timestamp: Date.now() });
}

// Usage in edge function
const cacheKey = `topics:${query}:${lang}`;
const cached = getCached<Topic[]>(cacheKey);
if (cached) {
  return new Response(JSON.stringify({ topics: cached }));
}

const topics = await fetchTopics(query);
setCache(cacheKey, topics);
```

### Code Splitting and Lazy Loading

```typescript
// App.tsx
import { lazy, Suspense } from 'react';
import { LoadingState } from '@/components/shared/LoadingState';

// Lazy load feature modules
const TopicSelection = lazy(() => import('@/components/modules/TopicSelection'));
const LiteratureReview = lazy(() => import('@/components/modules/LiteratureReview'));
const PlagiarismCheck = lazy(() => import('@/components/modules/PlagiarismCheck'));
const JournalRecommendation = lazy(() => import('@/components/modules/JournalRecommendation'));

export function App() {
  return (
    <Router>
      <Routes>
        <Route path="/topics" element={
          <Suspense fallback={<LoadingState />}>
            <TopicSelection />
          </Suspense>
        } />
        <Route path="/literature" element={
          <Suspense fallback={<LoadingState />}>
            <LiteratureReview />
          </Suspense>
        } />
        {/* ... other routes */}
      </Routes>
    </Router>
  );
}
```

### Bundle Optimization

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true }) // Analyze bundle size
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-react': ['react', 'react-dom', 'react-router-dom'],
          'vendor-ui': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          'vendor-supabase': ['@supabase/supabase-js'],
          'vendor-clerk': ['@clerk/clerk-react'],
          'vendor-lingo': ['lingo.dev/sdk']
        }
      }
    },
    chunkSizeWarningLimit: 1000,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
        drop_debugger: true
      }
    }
  }
});
```

### Image and Asset Optimization

```typescript
// components/shared/OptimizedImage.tsx
export function OptimizedImage({ src, alt, ...props }: ImageProps) {
  return (
    <img
      src={src}
      alt={alt}
      loading="lazy"
      decoding="async"
      {...props}
    />
  );
}

// Compress uploaded PDFs
export async function compressPDF(file: File): Promise<File> {
  if (file.size < 5 * 1024 * 1024) return file; // Skip if < 5MB
  
  // Use PDF compression library
  const compressed = await compressPDFLib(file);
  return new File([compressed], file.name, { type: 'application/pdf' });
}
```

### Database Query Optimization

```sql
-- Indexes for common queries
CREATE INDEX CONCURRENTLY idx_drafts_user_updated 
  ON drafts(user_id, updated_at DESC);

CREATE INDEX CONCURRENTLY idx_reviews_user_created 
  ON literature_reviews(user_id, created_at DESC);

CREATE INDEX CONCURRENTLY idx_journals_domain_impact 
  ON journals(domain, impact_factor DESC);

-- Materialized view for journal statistics
CREATE MATERIALIZED VIEW journal_stats AS
SELECT 
  domain,
  COUNT(*) as journal_count,
  AVG(impact_factor) as avg_impact,
  MAX(impact_factor) as max_impact
FROM journals
GROUP BY domain;

CREATE UNIQUE INDEX ON journal_stats(domain);

-- Refresh periodically
REFRESH MATERIALIZED VIEW CONCURRENTLY journal_stats;
```

### Realtime Optimization

```typescript
// Selective realtime subscriptions
export function useDraftSync(draftId: string) {
  const supabase = useSupabaseClient();
  
  useEffect(() => {
    // Only subscribe to specific draft
    const subscription = supabase
      .channel(`draft:${draftId}`)
      .on(
        'postgres_changes',
        {
          event: 'UPDATE',
          schema: 'public',
          table: 'drafts',
          filter: `id=eq.${draftId}`
        },
        (payload) => {
          // Update local state
          updateDraft(payload.new);
        }
      )
      .subscribe();
    
    return () => {
      subscription.unsubscribe();
    };
  }, [draftId]);
}
```

## Deployment and DevOps

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linter
        run: npm run lint
      
      - name: Run type check
        run: npm run type-check
      
      - name: Run tests
        run: npm run test:ci
        env:
          VITE_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          VITE_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  translate:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run Lingo CLI
        run: npx lingo.dev@latest i18n --frozen
        env:
          LINGO_API_KEY: ${{ secrets.LINGO_API_KEY }}
      
      - name: Verify translations
        run: |
          for lang in es fr de ja zh-CN ko pt it ru; do
            if [ ! -f "src/locales/${lang}.json" ]; then
              echo "Missing translation for ${lang}"
              exit 1
            fi
          done
      
      - name: Upload translation artifacts
        uses: actions/upload-artifact@v3
        with:
          name: translations
          path: src/locales/

  build:
    runs-on: ubuntu-latest
    needs: translate
    steps:
      - uses: actions/checkout@v3
      
      - name: Download translations
        uses: actions/download-artifact@v3
        with:
          name: translations
          path: src/locales/
      
      - name: Build application
        run: npm run build
        env:
          VITE_CLERK_PUBLISHABLE_KEY: ${{ secrets.CLERK_PUBLISHABLE_KEY }}
          VITE_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          VITE_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
          VITE_LINGO_API_KEY: ${{ secrets.LINGO_API_KEY }}
      
      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Download build
        uses: actions/download-artifact@v3
        with:
          name: dist
          path: dist/
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### Environment Configuration

```bash
# .env.example
# Clerk Authentication
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...

# Supabase
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGc...

# Lingo.dev
VITE_LINGO_API_KEY=lingo_...

# Hugging Face (optional, for local testing)
VITE_HF_API_KEY=hf_...

# Environment
VITE_ENV=production
```

### Monitoring and Observability

```typescript
// lib/monitoring.ts
import * as Sentry from '@sentry/react';

Sentry.init({
  dsn: import.meta.env.VITE_SENTRY_DSN,
  environment: import.meta.env.VITE_ENV,
  tracesSampleRate: 0.1,
  integrations: [
    new Sentry.BrowserTracing(),
    new Sentry.Replay()
  ],
  beforeSend(event) {
    // Remove sensitive data
    if (event.request) {
      delete event.request.cookies;
      delete event.request.headers?.Authorization;
    }
    return event;
  }
});

// Performance monitoring
export function trackPerformance(metric: string, value: number) {
  Sentry.metrics.distribution(metric, value, {
    unit: 'millisecond'
  });
}

// Usage
trackPerformance('api.topics.response_time', responseTime);
trackPerformance('translation.lingo.duration', translationTime);
```

## Design Decisions and Rationale

### Why Supabase over Custom Backend?
- **Rapid Development**: Built-in auth, database, storage, and edge functions eliminate boilerplate
- **RLS Security**: Database-level security policies prevent data leaks
- **Realtime**: Native WebSocket support for collaborative features
- **Scalability**: Auto-scaling PostgreSQL with connection pooling
- **Cost**: Free tier sufficient for PoC (500MB storage, 50K monthly active users)

### Why Clerk over Supabase Auth?
- **Federation Support**: APCCE integration requires SAML/OAuth federation
- **User Management**: Rich admin dashboard for user analytics
- **Session Management**: Automatic token refresh and security best practices
- **Metadata**: Flexible user metadata for profiles and preferences

### Why Lingo.dev over react-i18next?
- **AI-Powered**: Context-aware translations with academic glossary support
- **Developer Experience**: CLI, SDK, and API for all use cases
- **Accuracy**: 95%+ translation fidelity with domain-specific terminology
- **Hackathon Alignment**: Maximizes WeMakeDevs scoring criteria

### Why shadcn/ui over Material-UI?
- **Customization**: Copy-paste components, full control over styling
- **Accessibility**: Built on Radix UI primitives with WCAG compliance
- **Bundle Size**: Tree-shakeable, only include what you use
- **Modern**: Tailwind CSS integration, TypeScript-first

### Why Vite over Create React App?
- **Performance**: 10-100x faster HMR and build times
- **Modern**: Native ESM, optimized for modern browsers
- **Flexibility**: Plugin ecosystem for advanced use cases
- **Future-Proof**: Active development, CRA is deprecated



## Plagiarism Detection Implementation

### Recommended Approach: Sentence Transformers + Hugging Face

For the MVP and hackathon demo, we'll use **Sentence Transformers** via Hugging Face Inference API for semantic similarity detection. This provides accurate plagiarism detection without external API costs.

#### Architecture

```typescript
// Edge Function: /citation/plagcheck
import { HfInference } from '@huggingface/inference';

const hf = new HfInference(Deno.env.get('HF_API_KEY'));

async function detectPlagiarism(draftText: string, lang: string) {
  // 1. Chunk text into sentences/paragraphs
  const chunks = chunkText(draftText, maxLength: 500);
  
  // 2. Generate embeddings using Sentence Transformers
  const draftEmbeddings = await Promise.all(
    chunks.map(chunk => 
      hf.featureExtraction({
        model: 'sentence-transformers/all-mpnet-base-v2',
        inputs: chunk
      })
    )
  );
  
  // 3. Compare against reference corpus (academic papers, web content)
  // For MVP: Use Semantic Scholar API to fetch similar papers
  const similarPapers = await searchSemanticScholar(draftText);
  
  // 4. Calculate cosine similarity
  const similarities = [];
  for (const paper of similarPapers) {
    const paperEmbedding = await hf.featureExtraction({
      model: 'sentence-transformers/all-mpnet-base-v2',
      inputs: paper.abstract
    });
    
    const similarity = cosineSimilarity(draftEmbeddings[0], paperEmbedding);
    if (similarity > 0.8) { // 80% threshold
      similarities.push({
        text: chunks[0],
        source: paper.title,
        url: paper.url,
        similarity: similarity * 100
      });
    }
  }
  
  // 5. Calculate originality score
  const maxSimilarity = Math.max(...similarities.map(s => s.similarity), 0);
  const originalityScore = 100 - maxSimilarity;
  
  // 6. Get citation suggestions from CrossRef
  const citations = await getCitationSuggestions(draftText);
  
  return {
    originality_score: originalityScore,
    flagged_sections: similarities.filter(s => s.similarity > 20),
    citations: citations,
    checked_at: new Date().toISOString()
  };
}

function cosineSimilarity(vecA: number[], vecB: number[]): number {
  const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
  const magnitudeA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
  const magnitudeB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
  return dotProduct / (magnitudeA * magnitudeB);
}

async function getCitationSuggestions(text: string) {
  // CrossRef API - free, no authentication required
  const keywords = extractKeywords(text);
  const response = await fetch(
    `https://api.crossref.org/works?query=${encodeURIComponent(keywords)}&rows=10`
  );
  const data = await response.json();
  
  return data.message.items.map(item => ({
    doi: item.DOI,
    title: item.title[0],
    authors: item.author?.map(a => `${a.given} ${a.family}`).join(', '),
    year: item.published?.['date-parts']?.[0]?.[0],
    relevance: calculateRelevance(text, item.title[0])
  }));
}
```

#### Model Details

**Sentence Transformer: `all-mpnet-base-v2`**
- **Embedding Dimension**: 768
- **Max Sequence Length**: 384 tokens
- **Performance**: State-of-the-art on semantic similarity tasks
- **Advantages**:
  - Detects paraphrased content (not just exact matches)
  - Works across languages with multilingual variants
  - Free via Hugging Face Inference API
  - No rate limits for reasonable usage

#### Accuracy Validation

```typescript
// Test with known plagiarism cases
const testCases = [
  {
    original: "Climate change poses significant risks to global ecosystems.",
    plagiarized: "Global ecosystems face considerable threats from climate change.",
    expectedSimilarity: 0.85 // Should detect as similar
  },
  {
    original: "Machine learning algorithms require large datasets.",
    different: "The weather today is sunny and warm.",
    expectedSimilarity: 0.1 // Should detect as different
  }
];

async function validateAccuracy() {
  let correct = 0;
  for (const test of testCases) {
    const similarity = await calculateSimilarity(test.original, test.plagiarized || test.different);
    const isCorrect = Math.abs(similarity - test.expectedSimilarity) < 0.15;
    if (isCorrect) correct++;
  }
  const accuracy = (correct / testCases.length) * 100;
  console.log(`Accuracy: ${accuracy}%`); // Target: ≥95%
}
```

### Production Alternative: Copyleaks API

For production deployment or if higher accuracy is needed:

```typescript
// Copyleaks Integration
import { Copyleaks } from 'copyleaks-sdk';

const copyleaks = new Copyleaks({
  email: Deno.env.get('COPYLEAKS_EMAIL'),
  key: Deno.env.get('COPYLEAKS_API_KEY')
});

async function detectPlagiarismWithCopyleaks(text: string) {
  // Submit scan
  const scanId = crypto.randomUUID();
  await copyleaks.submitFile({
    base64: btoa(text),
    filename: 'draft.txt',
    properties: {
      webhooks: {
        status: `${BASE_URL}/webhooks/copyleaks/status/${scanId}`
      },
      scanning: {
        internet: true,
        internalDatabase: true,
        academicPublications: true // Key feature!
      }
    }
  }, scanId);
  
  // Results delivered via webhook
  return { scanId, status: 'processing' };
}

// Webhook handler
async function handleCopyleaksWebhook(scanId: string, results: any) {
  const originalityScore = 100 - results.statistics.identicalWords;
  const flaggedSections = results.results.internet.map(match => ({
    text: match.matchedWords,
    source: match.url,
    similarity: match.identicalWords
  }));
  
  // Store in Supabase
  await supabase.from('plagiarism_checks').update({
    originality_score: originalityScore,
    flagged_sections: flaggedSections,
    status: 'completed'
  }).eq('scan_id', scanId);
}
```

**Copyleaks Pricing**:
- **Plagiarism Detector**: $10.99/month
- **Features**: 
  - Academic publications database
  - 99% accuracy
  - Cross-language detection
  - API access included
  - 1,000 scan credits (250,000 words/month)

### Comparison Matrix

| Feature | Sentence Transformers (HF) | Copyleaks API |
|---------|---------------------------|---------------|
| **Cost** | Free | $10.99/month |
| **Accuracy** | 85-90% | 99% |
| **Academic Papers** | Via Semantic Scholar | Built-in database |
| **Paraphrase Detection** | ✅ Excellent | ✅ Excellent |
| **Cross-Language** | ✅ With multilingual models | ✅ Native support |
| **Rate Limits** | Reasonable (HF free tier) | 1,000 scans/month |
| **Setup Complexity** | Medium | Low (API-first) |
| **Best For** | MVP, PoC, Hackathon | Production, High accuracy |

### Recommendation

**For Hackathon (Nov 13-16)**:
- Use **Sentence Transformers via HF Inference API**
- Demonstrates technical capability
- No external costs
- Sufficient accuracy for demo (85-90%)
- Can compare against Semantic Scholar papers

**For Production (Post-Hackathon)**:
- Upgrade to **Copyleaks API**
- 99% accuracy meets requirements
- Access to academic publication database
- Professional plagiarism reports
- Worth the $10.99/month investment

### Implementation Timeline

1. **Day 1**: Implement Sentence Transformers integration
2. **Day 2**: Add CrossRef citation suggestions
3. **Day 3**: Test accuracy with sample papers
4. **Day 4**: Demo with Chinese/Spanish translations
5. **Post-Hackathon**: Evaluate Copyleaks upgrade

