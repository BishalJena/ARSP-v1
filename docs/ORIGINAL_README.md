# Building the AI-Enabled Research Support Platform (ARSP): A Dual-Hackathon Winner Strategy for Global Researchers

## The Idea: Empowering Global Researchers with Multilingual AI
ARSP is an innovative, AI-driven web platform designed to transform research workflows for college students and faculty worldwide—targeting over 200 million higher-ed learners where publication rates lag due to language barriers, manual drudgery, and siloed tools. Imagine a Chinese undergraduate in Shanghai struggling with English-dominated literature on "AI Ethics in Asia," spending weeks on translations and citations. ARSP acts as an "intelligent co-pilot," automating these with NLP from open datasets (e.g., arXiv, Semantic Scholar) while leveraging Lingo.dev's AI localization to make every interaction multilingual in supported languages (English, Spanish, French, German, Japanese, Chinese, Korean, Portuguese, Italian, Russian, and key variants like zh-CN, es-419). This isn't just translation—it's equitable access: Preserve technical nuances in Japanese summaries or Russian-friendly journal recs, unlocking 30-50% faster outputs and global visibility for diverse academics.

Built fresh during the WeMakeDevs Multilingual Hackathon (Nov 13-16, 2025), ARSP "builds global from day one" by embedding Lingo's CLI/SDK/API deeply (7+ features: static UI via CLI, dynamic content via SDK, context-aware for academics, pluralization for lists, glossaries for jargon like "H-index," CI/CD hooks, even tooltips). This maximizes WeMakeDevs points while adapting the AP Govt challenge for a broader, global lens (e.g., AP GDCs as a pilot, but scalable to international users). No tech overhauls—just swap Indic langs for Lingo's robust support, keeping the core for universal appeal.

## The Goal: Dual Wins for Global Impact and Innovation
**Primary Goal**: Create a PoC that boosts global research productivity by 30% (simulated via time savings metrics), supports 10+ Lingo-backed languages natively, and achieves ≥80% AI accuracy—positioning ARSP as a NEP 2020-inspired tool for worldwide equity.  
**Hackathon Goals**: 
- **WeMakeDevs**: Secure Top 3 (₹50K + Lingo credits/swag) by demonstrating "Translate Everything" through creative Lingo chaining (e.g., glossary-preserved Chinese summaries), high UX via shadcn, and impact on cross-cultural research.
- **AP Govt**: Win ₹5L + RTGS contract by hitting PoC criteria (8-user test, mock APCCE integration), emphasizing scalability for 300+ GDCs while highlighting global extensibility (e.g., Chinese student demo for innovation).  
**Broader Goal**: Open-source the repo post-hackathons, fostering contributions for Lingo-powered edtech, potentially scaling to 10K international users via Supabase.

## What We're Trying to Do: Guidance for AI Coder (Claude)
You're building a sleek, minimalistic React app (shadcn-powered) that feels like a modern Notion for global researchers—clean cards, intuitive tables, instant lang switches (e.g., from zh-CN to es-419)—backed by Supabase for data magic and Clerk for seamless sign-ins. Focus on **modularity**: Each module (e.g., Lit Review) is a self-contained shadcn component chaining HF AI → Lingo SDK (for dynamic, context-rich translations) → Supabase upsert. To improve/act: 
- **Enhance UX**: Make it "vibe" welcoming for international users—e.g., auto-detect lang from Clerk profile or browser locale, use Lingo pluralization for "1 insight found" vs. "5 insights," shadcn skeletons for loading.
- **Deepen Lingo**: Maximize for WeMakeDevs by weaving in 7+ features everywhere (e.g., CLI in build script for static strings, SDK for runtime queries with `context: 'academic_summary'`, glossary `{ 'plagiarism_score': '剽窃分数' }` for Chinese accuracy). Test with sample multilingual inputs (e.g., Japanese query); fallback gracefully.
- **Global/AP Rigor**: Bake in accuracy checks (e.g., similarity >80% or alert), RLS for privacy (e.g., user-only sees own drafts), offline drafts via localStorage. For AP, include mock GDC profiles but demo global (e.g., Chinese student flow).
- **Iterate Smart**: Generate TypeScript code with JSDoc; always include Lingo inline comments. If a feature feels clunky (e.g., Russian Cyrillic edges), suggest fallbacks like "hybrid mode: Lingo + manual edit." Aim for <5s responses; demo-ready with a Chinese end-to-end flow.
- **Ethics/Impact**: Ensure consent flows (shadcn Dialogs); simulate 8-user PoC (mix: 4 AP, 4 global) to quantify "time saved: 20hrs → 5hrs per paper," emphasizing cross-border equity.

This setup lets you (Claude) generate, refine, and expand—e.g., "Add a mind-map viz to Lit Review using React Flow, Lingo-translated nodes."

## Evaluation Metrics & Expectations
### WeMakeDevs Multilingual Hackathon (Judging Criteria)
- **Potential Impact (25%)**: How it addresses global language barriers in education; expect demo of 100+ simulated papers preserved across langs, partnering potential with international edtech.
- **Creativity & Originality (20%)**: Unique Lingo uses (e.g., glossary for academic idioms in Japanese); expect creative twists like variant-specific UX (zh-CN simplified vs. zh-TW traditional).
- **Learning & Growth (20%)**: Document your Lingo ramp-up (e.g., CLI pitfalls); expect beginner-friendly onboarding in submission notes.
- **Technical Implementation (20%)**: Clean Lingo CLI/SDK integration; expect robust error-handling (e.g., offline mode) and 95%+ translation accuracy.
- **Aesthetics & UX (15%)**: shadcn minimalism; expect intuitive flows (e.g., drag-drop uploads) scoring high on user-friendliness.
**Expectations**: New project only; use Lingo for bonus points (more features = better odds); submit video + repo by Nov 16; community: Star Lingo GitHub, tweet with #LingoHack.

### AP Govt Hackathon (Evaluation Criteria)
- **Innovation and AI Advancement (25%)**: Novelty in multimodal global AI (e.g., Lingo + HF for context); expect ≥80% accuracy in topic/journal matching via user sims (include global variants).
- **Accuracy and Reliability (20%)**: OCR/speech N/A (focus research: plagiarism detection 95%+); expect effective summarization across supported langs.
- **Usability and Accessibility (15%)**: Multi-lang support (Lingo's 10+); expect easy APCCE integration, rural/global-optimized (low-bandwidth).
- **Scalability and Deployment (15%)**: Robust for 10K users; expect 2-month PoC rollout via Supabase/Vercel.
- **Data Privacy and Security (10%)**: DPDP compliance; expect consent logs, encryption.
- **Impact Potential (15%)**: Grievance N/A (focus: 30% pub boost globally/AP); expect metrics like "turnaround: 2 months → 1 week."
**Expectations**: PoC scope: 8 GDC/global users, 2 months duration, Lingo-supported langs; outcomes: Higher pubs, integrity; incentives: ₹5L winner + RTGS contract; submit by Nov 24 with deck/video.

## Project Planning and Documentation

### Product Requirements Document (PRD)

#### Project Overview
**Project Name**: AI-Enabled Research Support Platform (ARSP)  
**Version**: 1.0 (MVP for Hackathons)  
**Date**: Nov 13, 2025  
**Authors**: [Your Team Name]  
**Description**: A web-based, multilingual AI assistant for global college students/faculty, with AP GDCs as a pilot. It streamlines research from topic discovery to publication, using open datasets and Lingo.dev for seamless localization in supported languages: English (en-US/en-GB), Spanish (es-ES/es-419), French (fr-FR/fr-CA), German (de), Japanese (ja), Chinese (zh-CN/zh-TW), Korean (ko), Portuguese (pt), Italian (it), Russian (ru). Built fresh for WeMakeDevs (Lingo-powered global accessibility via CLI/SDK/API) and AP Hackathon (boosting productivity with international scalability). Extensive Lingo use: CLI for UI automation/CI/CD, SDK/API for dynamic content (real-time, context-aware), pluralization for UX lists, glossaries for academic tone/brand voice (e.g., consistent "impact factor" translations).

**Goals**:
- **Primary**: Automate 70% of manual research tasks (e.g., lit reviews in 5 mins vs. 20 hrs), targeting ≥80% accuracy in multilingual outputs; simulate 30% productivity gain for 8 PoC users (global mix).
- **Secondary**: Win WeMakeDevs via extensive Lingo features (7+ integrations: CLI CI/CD, SDK runtime, API backend, context/glossary/pluralization/brand voice for creativity); secure AP contract via PoC scalability and DPDP compliance.
- **Success Metrics**: 
  - WeMakeDevs: Lingo usage demo + user feedback on UX (aim: Top 3, ₹50K); 95%+ translation fidelity.
  - AP: 8-user PoC with ≥80% satisfaction; 30% simulated time savings; ≥80% accuracy in recs/summaries.

**Target Users**:
- Global College Students/Faculty (e.g., Chinese undergrads, Spanish postgrads): Core (80% usage; expect 5-min workflows).
- AP GDC Users: Secondary pilot (co-authoring; expect localized exports).
- Admins (APCCE/Global): Profile management (expect aggregated dashboards post-MVP).

**Scope (MVP)**:
- In: Core modules (Topic Selection, Lit Review, Citation/Plagiarism, Journal Recs), Lingo multilingualism (CLI/SDK/API + advanced: context, pluralization, glossary, CI/CD, brand voice), basic dashboard.
- Out: Full APCCE integration (mock for MVP; add post-Nov 16), advanced analytics/viz (e.g., full mind-maps).

**Assumptions/Dependencies**:
- Free APIs/datasets: Semantic Scholar, arXiv, CrossRef (no keys needed for PoC).
- Lingo Hobby Tier: Free 10K words/month for CLI/API/SDK (unlimited langs/glossaries; monitor usage).
- Clerk/Supabase: Free tiers for auth/DB (expect <100 users in PoC).
- Compliance: All data synthetic/user-consented; no real PII; Lingo's context for ethical translations.

#### Features & Functionalities
##### 1. User Authentication & Profile (Integration Layer)
- Login via Clerk (OAuth/email; mock APCCE federation with user metadata).
- Profile: Auto-pull synthetic data from Supabase (discipline, past pubs; e.g., "2 pubs in Humanities").
- Multilingual: Lingo-localized UI (lang selector; SDK for dynamic profile messages, e.g., pluralized "Welcome back, {count} publications found" with brand voice: formal/academic).

##### 2. AI-Powered Topic Selection
- Input: User query (text, multilingual via Lingo API pre-translate with context: "academic research query in global context").
- Output: 5 trending topics (NLP on arXiv + regional filters, e.g., "AI Ethics in Asia"); Lingo SDK for translated briefs (glossary for terms like "citation analysis" → "引用分析" in zh-CN).
- Lingo Deep Use: API for input translation; pluralization for output lists (e.g., "1 topic" in ja); CI/CD hook to update static filters.

##### 3. AI-Driven Literature Review Automation
- Input: Upload PDF/text (3-5 papers) to Supabase storage (expect <10MB/file).
- Output: Bilingual summary (500 words), key insights mind-map (text-based), auto-refs (Zotero/JSON export); Lingo API for dynamic translation of summaries/insights (context-aware for technical jargon, e.g., "ethics in AI lit").
- Lingo Deep Use: SDK chaining post-HF summarization; glossary for academic tone (e.g., formal Spanish); pluralization for insights list; brand voice for summaries (professional/precise).

##### 4. AI-Based Citation and Plagiarism Detection
- Input: Draft text (Supabase-stored; real-time editor).
- Output: Real-time suggestions (CrossRef API, 10+ cites), originality score (95%+ accuracy via similarity algo), paraphrase flags; Lingo for translated reports (e.g., error messages like "8% similarity detected—review flagged sections").
- Lingo Deep Use: API for translating citations (preserve hyperlinks/accuracy); context for plagiarism explanations (e.g., "academic integrity note"); pluralization for suggestion counts.

##### 5. AI-Powered Journal Recommendation
- Input: Abstract/draft (textarea input).
- Output: 10 journals (Scopus-indexed from Supabase mock DB, filters: open-access, impact factor >1.0, pub time <6 months); ranked table with fit scores.
- Lingo Deep Use: SDK for lang-specific recs (e.g., translate journal metadata/descriptions); glossary for metrics (e.g., "H-index" consistent across langs); CLI pre-translate static filter labels.

#### Non-Functional Requirements
- **Performance**: <5s response (HF caching); offline draft mode (localStorage + Supabase sync on reconnect).
- **Accessibility**: WCAG 2.1 (shadcn ARIA-ready components, alt text for icons); multi-lang via Lingo (screen reader support for pluralized strings).
- **Security**: Clerk/Supabase RLS for DPDP (consent modals via shadcn Dialog, AES-256 encryption on uploads); audit logs in Supabase.
- **Scalability**: Supabase auto-scale to 10K users; Lingo CI/CD for global deploys (prevent incomplete lang builds).
- **Lingo Maximization**: 7+ features per WeMakeDevs—CLI (UI automation/CI/CD with `npx lingo.dev@latest i18n --frozen`), API/SDK (dynamic/runtime for user content), context-awareness (95% accuracy boost), pluralization (UX fluidity), glossary (domain-specific, unlimited in Hobby), brand voice (academic/formal), even translate in-app tooltips/help/docs for "everything translated." Monitor via Lingo dashboard.

#### User Flows
1. **Onboard**: Clerk login (expect 10s) → Lang auto-detect/select (Lingo SDK) → Supabase profile load/setup.
2. **Research Workflow**: Query topic (Lingo input translate, 2s) → Upload to Supabase (drag-drop) → Review summary (Lingo dynamic, 10s) → Check plagiarism (real-time score) → Get journal recs (Lingo lists, sortable) → Export (PDF/Zotero).
3. **Admin**: View global/AP metrics (post-MVP; Lingo for labels, e.g., pluralized "8 users active").

#### Risks & Mitigations
- Risk: Lingo variant accuracy (<90% for zh-TW specifics). Mitigate: Context param + glossary fallback; test with 10 sample phrases.
- Risk: Supabase/Clerk free limits (e.g., 500MB storage). Mitigate: Synthetic data; compress uploads.
- Risk: HF rate limits. Mitigate: Cache in Supabase; queue for PoC.
- Timeline: 3-day MVP (focus Lingo demos) → 1-week polish (AP metrics).

#### Appendix: Hackathon Alignment & Expectations
- **WeMakeDevs**: Lingo in every module for "Build Global" (expect demo CLI commands, SDK calls, CI workflow in video); new code only, 1-4 team.
- **AP**: ≥80% accuracy tests (user sims, global/AP mix); PoC video with 8 synthetic users (expect outcomes: +pub rates, integrity); DPDP full compliance.

### To-Do List

Breakdown into phases for Claude: Daily sprints (Nov 13-16 for MVP; Nov 17-24 polish). Track in GitHub Issues. Prioritize Lingo for WeMakeDevs (e.g., test 7+ features with zh-CN/es); AI accuracy for AP (e.g., threshold checks). Include shadcn/Clerk/Supabase/Lingo setup with deep integrations.

#### Phase 1: Setup & Core Structure (Nov 13 - Day 1, 4-6 hrs)
- [ ] Initialize repo: `npx create-vite@latest arsp-frontend --template react-ts` + Supabase init (`supabase init` + `supabase start` locally).
- [ ] Install deps: Frontend (shadcn/ui via `npx shadcn-ui@latest init`, react-i18next, @clerk/clerk-react, @supabase/supabase-js, lucide-react, react-hot-toast); Lingo (`npm i @lingo.dev/sdk`).
- [ ] Setup Clerk: Create free app in Clerk dashboard; Add <ClerkProvider> in main.tsx; Configure env vars (publishableKey).
- [ ] Setup Supabase: Create free project; Tables (profiles: id, discipline; uploads: user_id, file_path with RLS: `auth.uid() = user_id`); Storage bucket ('papers') with policies.
- [ ] Setup Lingo: Sign up Hobby tier; Test CLI: `npx lingo.dev@latest i18n --frozen` on sample en.json (generate locales for en, es, fr, de, ja, zh, ko, pt, it, ru and variants); Init SDK with API key.
- [ ] Basic dashboard skeleton: shadcn components (Button, Card, NavigationMenu) for screens; Lang selector (useLingo hook for runtime switch).

#### Phase 2: Build Core Modules (Nov 14 - Day 2, 6-8 hrs)
- [ ] Topic Selection: Integrate Semantic Scholar API (axios GET); Lingo API pre-translate input (`lingo.translate({text: query, context: 'academic_query'})`); Output as shadcn DataTable with pluralized rows.
- [ ] Lit Review: HF Inference for summarization (`new HfInference().summarization()`); Pipe to Lingo SDK (`lingo.translate({text: summary, glossary: {academic_terms}})` with context/brand voice); Upload to Supabase storage; Render in shadcn Accordion.
- [ ] Citation/Plagiarism: Implement TF-IDF sim (lodash or simple JS); Lingo for reports (`lingo.pluralize({count: suggestions.length, key: 'suggestions'})`); Store draft in Supabase; shadcn Textarea + Badge for score.
- [ ] Journal Recs: Supabase query mock DB (seed 50 journals); Lingo SDK translate metadata (`context: 'journal_desc'`); shadcn Table with sortable columns (impact factor).
- [ ] Inline docs: Add JSDoc to all functions; Lingo-specific comments (e.g., "// LINGO: Glossary for 95% accuracy").

#### Phase 3: Integration, UX, & Multilingual (Nov 15 - Day 3 AM, 4 hrs)
- [ ] Lingo Deep Dive: Implement 7+ features—CLI in package.json build script; SDK for all dynamic (inputs/outputs); API for backend-like calls; Context in summaries; Pluralization in lists; Glossary for jargon; CI GitHub Actions yaml with CLI hook; Brand voice param for formal tone. Test Chinese/Spanish sample; Demo script (e.g., console.log translated outputs).
- [ ] UX Polish: shadcn for all forms/tables (e.g., Dropzone for uploads); Consent modals (shadcn Dialog integrated with Clerk); Dark mode toggle.
- [ ] Offline Mode: Use localStorage for drafts; Supabase realtime subscribe for sync.
- [ ] API Layer: Supabase edge functions for secure AI calls (e.g., POST /lit/review); Inline Lingo for response localization.

#### Phase 4: Testing & Demo (Nov 15 PM - Nov 16, 4 hrs)
- [ ] Unit Tests: Jest for accuracy (e.g., expect(accuracy).toBeGreaterThan(0.8)); Test Lingo pluralization/glossary with mocks.
- [ ] PoC Sim: Seed 8 synthetic users in Supabase/Clerk (4 AP, 4 global); Run e2e flow (Chinese query → output); Video recording (2-min: full workflow + Lingo CLI/SDK demo).
- [ ] WeMakeDevs Sub: Deploy to Vercel (env: Clerk/Supabase/Lingo keys); Run Lingo CI build; Star Lingo GitHub; Tweet thread tagging @LingoAI.
- [ ] Changelog Update: v1.0.0 release with metrics.

#### Phase 5: AP Polish (Nov 17-24, 10-15 hrs total)
- [ ] APCCE Mock: Clerk federation sim.
- [ ] Scalability: Supabase load test (50 concurrent queries via Artillery); Optimize HF caching.
- [ ] Privacy Audit: Full RLS enforcement; Lingo-translated consent text.
- [ ] Full Tests: Cypress e2e for usability; Sim user feedback (e.g., NPS ≥8/10).
- [ ] AP Sub: Update PRD with PoC metrics (e.g., "80.5% accuracy"); Presentation deck (impact projections: +20% global/AP pubs).

**Global Rules for Claude**: Generate TypeScript code with JSDoc/inline comments. Use shadcn primitives (e.g., <Card><CardContent>). All strings via Lingo (CLI static, SDK dynamic with context/glossary). Ensure DPDP (consent before uploads). Commit per task: "feat: add lingo pluralization". If improving: Suggest enhancements like "Add React Flow for mind-maps, Lingo-node labels."

### Tech Stack Documentation

#### Technologies
| Layer | Tech | Rationale | Notes |
|-------|------|-----------|-------|
| **Frontend** | React 18 + Vite + shadcn/ui | Fast MVP; shadcn for beautiful, minimalistic, customizable components (e.g., Cards for modules, Tables for recs). | i18n via react-i18next + Lingo-generated locales; Tailwind base. |
| **Backend/DB** | Supabase (Postgres DB, Storage, Edge Functions, Realtime) | BaaS for auth-sync, RLS privacy, file uploads; Endorsed for Lingo multilingual apps. | Client-side supabase-js; Seed synthetic data; RLS for DPDP. |
| **Auth** | Clerk | Secure, scalable (email/OAuth federation for APCCE mock); User metadata for profiles. | Free tier; <ClerkProvider>; Env: publishable/secret keys. |
| **AI/ML** | Hugging Face Transformers (Inference API) | Free NLP (summarization/citations); Global models (e.g., multilingual-bert for zh/ja accuracy). | Chain with Lingo SDK; Cache results in Supabase. |
| **Localization** | Lingo.dev CLI/API/SDK (Hobby Free) | Core for WeMakeDevs; CLI (build-time UI/CI/CD: `npx lingo.dev@latest i18n --frozen`), SDK (runtime dynamic/pluralization), API (inputs/responses/context), advanced (glossary/brand voice for academics). 10+ langs/variants. | 7+ uses: UI static, content dynamic, errors/tooltips, CI hooks, lists plural, jargon glossary, formal voice. Monitor 10K words/month. |
| **APIs/Datasets** | Semantic Scholar, arXiv, CrossRef | Open academic data; Axios for calls. | Fallback: Supabase-cached mocks. |
| **Deployment** | Vercel (free) | Instant deploys; GitHub Actions CI with Lingo CLI (yaml: checkout → lingo i18n → build → deploy). | Env vars secure; Preview branches for testing. |
| **Testing** | Jest + React Testing Library + Cypress | Accuracy/unit (≥80% thresholds); e2e multilingual flows. | Mock Lingo/HF; Test pluralization edge cases. |
| **Other** | Axios (HTTP), Lucide-React (icons), react-hot-toast (notifications), pdf.js (extract text) | Efficiency; shadcn-compatible; Toasts for Lingo errors. | WCAG: ARIA in shadcn; Lingo for all messages. |

#### Frontend Guidelines
- **Architecture**: Component-based (e.g., <TopicSelector /> as shadcn Card; Context API for lang/Clerk user state).
- **Styling**: shadcn/ui + Tailwind (minimalistic: whitespace-heavy, sans-serif fonts); Mobile-first (global 4G); Dark mode (shadcn theme).
- **Global Rules**:
  - All text: i18n keys; Lingo CLI for static JSON (pre-build); SDK for dynamic (`useLingo().translate({text, context: 'academic', glossary: academicDict})`).
  - Error Handling: shadcn Toasts (hot-toast); Lingo API for localized msgs (e.g., plural "1 error").
  - Accessibility: shadcn ARIA (e.g., <Button aria-label={t('submit')} />); Lingo plural for screen readers.
  - Performance: Lazy-load (React.lazy for modules); Code-split; <5s via HF streaming.
  - Lingo Deep: Brand voice: `{voice: 'formal_academic'}` in SDK calls; CI: Block deploys if langs incomplete.

#### Screens/Wireframes (Text-Based for Claude)
1. **Login/Dashboard**: shadcn Card for Clerk <SignIn />; Post-login: shadcn Sheet sidebar (NavigationMenu with Lingo labels); Main: Hero Card ("Start Research" CTA).
2. **Topic Selection**: shadcn Form (Input + Select for filters); Results: shadcn DataTable (columns: Title, Brief [Lingo-translated], Impact Badge; plural rows).
3. **Lit Review**: shadcn Upload Dropzone; Output: shadcn Accordion (Summary section with Lingo dynamic text); Export Button (Zotero icon).
4. **Plagiarism Check**: shadcn Textarea (editor); Sidebar: shadcn Alert for score (green/red Badge, Lingo report); Suggestions as shadcn List.
5. **Journal Recs**: shadcn Table (sortable: Name, Impact [glossary], Fit %); Filters: shadcn Select (open-access).
- **Global**: Header (Clerk UserButton + LangDropdown); Footer (DPDP link, Lingo-translated); Loaders: shadcn Skeleton with lang placeholders.

**Dev Notes**: ESLint (Airbnb + TS); Prettier; Husky pre-commit (lint + Lingo test). Inline: `// LINGO: SDK context for 95% global accuracy; CLI for static to hit WeMakeDevs bonus.`

### API and Inline Documentation

#### API Documentation (OpenAPI/Swagger Style - Paste to Claude for Auto-Gen)
Base: Supabase client-side (supabase-js) + Edge Functions for serverless AI (secure keys). Generate via Supabase CLI (`supabase gen types`).

##### Endpoints (Supabase Tables/Functions)
- **POST /auth/login** (Clerk SDK):  
  Description: Auth via Clerk; Sync profile to Supabase.  
  Request: Clerk `signIn.email()` (email/password).  
  Response: `{ user: { id, email, profile: { discipline } } }` (Clerk session); Supabase upsert.  
  Notes: Lingo-localize errors (SDK: `lingo.pluralize('invalid_attempts', {count: 3})`); Expect DPDP consent on first login.

- **POST /topics/recommend** (Supabase Edge Fn):  
  Description: AI topic selection; Lingo pre-translate.  
  Request: `{ query: string, lang: 'zh-CN' }` (via supabase.functions.invoke).  
  Response: `{ topics: [{ title: string, brief: string, impact: number }] }` (200; Lingo SDK translated with pluralization).  
  Accuracy: ≥80% (validate citations); Notes: Context: 'research_trend_analysis'.

- **POST /lit/review** (Supabase Storage + Edge Fn):  
  Description: Automate lit review; Upload + AI chain.  
  Request: FormData (files: PDF[], lang: string) → `supabase.storage.from('papers').upload()`.  
  Response: `{ summary: string, insights: string[], refs: string[] }` (Lingo API-translated, context: 'lit_summary', glossary: academic).  
  Inline Note: `// Chain pdf.js extract → HF.summarization → Lingo SDK (brand voice: 'formal') → Supabase insert; Pluralize insights.`

- **POST /citation/plagcheck** (Supabase Edge Fn):  
  Description: Citation suggest + plagiarism; Real-time.  
  Request: `{ draft: string, userId: string }` (Supabase upsert draft).  
  Response: `{ score: number (0-100), suggestions: string[], citations: {doi: string, title: string}[] }` (Lingo for reports, plural: 'suggestions_count').  
  Reliability: TF-IDF >95%; Flag >20% similarity; Notes: CrossRef fetch.

- **POST /journals/recommend** (Supabase RPC):  
  Description: Journal matching from mock DB.  
  Request: `{ abstract: string, filters: { openAccess: boolean, lang: string } }`.  
  Response: `{ journals: [{ name: string, impact: number, fit: number, desc: string }] }` (Lingo SDK multi-lang metadata, glossary: metrics).  
  Notes: Sortable query.

**Global API Rules**: JSON responses; Errors: `{ error: string (Lingo-localized), code: number }`; Auth: Clerk token in headers (Supabase auth helper). Rate: Supabase defaults (50/sec). Docs: Supabase dashboard auto-gen; Add Lingo examples.

#### Inline Documentation Guidelines
- **JS/TS Comments**: Full JSDoc (e.g., `/** @param {string} query - Lingo-pretranslated user input @returns {Promise<Topics[]>} - Pluralized via Lingo */`).
- **Lingo-Specific**: `// LINGO (WeMakeDevs Bonus): SDK for dynamic/context-aware (e.g., {context: 'academic', voice: 'formal'}); CLI in CI for static; Glossary unlimited in Hobby; Plural for UX (e.g., lingo.pluralize({count, key})); Track words <10K.`
- **AI/Accuracy**: `// AP/Global Metric: if (cosineSimilarity(output, expected) < 0.8) { toast.error(lingo.t('low_accuracy')); }`
- **Privacy**: `// DPDP: Supabase RLS enforce; Clerk metadata consent; Encrypt via crypto.subtle before upload.`
- **shadcn/Clerk/Supabase**: `// UI: <Table> from shadcn; Auth: useUser(); DB: supabase.from('profiles').select('*').eq('id', user.id).single();`
- **Example Snippet** (Feed to Claude):
  ```tsx
  // ARSP: Journal Rec Module - Matches abstracts with Lingo-localized outputs
  // WeMakeDevs: Lingo SDK (context, glossary, plural, voice) for max points; CLI pre-builds filters
  // AP/Global: ≥80% fit accuracy; Supabase query for scalability
  import { HfInference } from '@huggingface/inference'; // Free NLP
  import { createClient } from '@supabase/supabase-js';
  import { useLingo } from '@lingo.dev/sdk'; // Runtime
  import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table'; // shadcn
  import { useUser } from '@clerk/nextjs'; // Auth

  const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_ANON_KEY!);

  /**
   * Recommends journals with multilingual metadata
   * @param {string} abstract - User abstract
   * @param {string} targetLang - e.g., 'zh-CN' for Simplified Chinese
   * @returns {Promise<Journal[]>} - Lingo-translated, plural-ready
   */
  async function recommendJournals(abstract: string, targetLang: string): Promise<Journal[]> {
    const { user } = useUser(); // Clerk: Ensure auth
    // Supabase: Query mock DB with RLS
    let { data: journals, error } = await supabase.from('journals').select('*').eq('user_id', user.id).limit(50);
    if (error) throw error; // DPDP: User-only access

    // HF: Analyze abstract for domain (simplified)
    const hf = new HfInference();
    const domain = await hf.textClassification({ model: 'distilbert-base-uncased', inputs: abstract });

    // Filter & Score (AP/Global Accuracy: >80% fit)
    const scored = journals.filter(j => j.domain === domain.label).map(j => ({
      ...j,
      fit: Math.random() * 100 // Sim; Real: cosine sim
    })).slice(0, 10);

    // LINGO Deep: SDK dynamic translate with context/glossary/voice/plural
    const lingo = useLingo();
    const translated = await Promise.all(scored.map(async (j) => ({
      ...j,
      name: await lingo.translate({ text: j.name, target: targetLang, context: 'journal_title', glossary: { 'H-index': 'H指数' } }), // Chinese example
      desc: await lingo.translate({ text: j.desc, voice: 'formal_academic' }),
      // Plural example: If in list, lingo.pluralize({count: scored.length, key: 'journals_recommended'})
    })));

    if (scored[0]?.fit < 80) {
      // AP/Global Reliability: Fallback alert
      toast.error(lingo.translate('low_fit_warning', { lang: targetLang }));
    }
    return translated;
  }

  // UI: shadcn Table Render
  export const JournalTable: React.FC<{ journals: Journal[] }> = ({ journals }) => (
    <Table>
      <TableBody>
        {journals.map((j) => (
          <TableRow key={j.id}>
            <TableCell>{j.name}</TableCell> {/* Lingo-localized */}
            <TableCell>{j.impact}</TableCell>
            <TableCell aria-label={lingo.t('fit_score')}>{j.fit}%</TableCell> {/* WCAG */}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
  ```

### Changelog.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Initial commit pending.

## [1.0.0] - 2025-11-16 (WeMakeDevs MVP Release)
### Added
- Core modules: Topic selection (Semantic API + Lingo input), Lit review (HF + Lingo dynamic), Citation/plagiarism (TF-IDF + Lingo reports), Journal recs (Supabase + Lingo metadata).
- Lingo integration: 7+ features (CLI UI/CI/CD, SDK dynamic/pluralization/voice, API inputs/context, glossary academic terms) for Multilingual Hackathon bonus; Tested Chinese/Spanish.
- Multilingual support: English, Spanish, French, German, Japanese, Chinese, Korean, Portuguese, Italian, Russian (Lingo 10+ langs/variants).
- shadcn/ui for minimalistic UX (Cards/Tables/Forms); Clerk auth (mock federation); Supabase DB/storage/RLS.
- Basic dashboard with shadcn Navigation; Offline drafts.
- API endpoints with Supabase Edge Fns; JSDoc/inline docs.
- PoC testing: 8 synthetic users (global/AP mix), ≥80% accuracy, 30% time sim.

### Changed
- N/A (initial release).

### Fixed
- N/A.

### WeMakeDevs Wins
- Demo: Chinese workflow video (2-min) + Lingo CLI/SDK/glossary commands.
- Submission: Vercel deploy (CI with Lingo hook); Tagged @LingoAI; Starred repo.

## [1.1.0] - 2025-11-24 (AP Hackathon Polish)
### Added
- Mock APCCE OAuth via Clerk federation.
- Enhanced scalability: Supabase realtime sync, HF caching.
- Full DPDP: Consent Dialogs (shadcn), client-side encryption.
- E2E tests (Cypress): Usability/accuracy/Lingo plural; PoC metrics dashboard.

### Changed
- Journal recs: Added H-index filtering (Lingo-translated); UI mind-map stubs.
- Lingo: Brand voice param for all SDK calls (formal_academic).

### Fixed
- Russian/Portuguese edge cases via Lingo context fallback; Supabase RLS leaks.

### AP Wins
- PoC Metrics: 80.5% accuracy, 35% time savings sim; 8-user feedback (NPS 8.5).
- Submission: Deck with projections (+25% global/AP pubs); Video with privacy demo.
```