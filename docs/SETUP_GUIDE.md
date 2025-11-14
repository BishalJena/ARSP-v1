# ARSP Setup Guide

Complete guide to set up and run the AI-Enabled Research Support Platform.

## Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.11+ (for backend)
- **Git**
- **Supabase Account** (free tier is sufficient)
- **Clerk Account** (free tier is sufficient)
- **Lingo.dev Account** (required for multilingual support)

## Step 1: Get API Keys (30 minutes)

###  1.1 Supabase

1. Go to https://supabase.com
2. Create a new account (if you don't have one)
3. Click "New Project"
4. Fill in:
   - Project name: `arsp` (or any name you prefer)
   - Database password: (save this)
   - Region: Choose closest to you
5. Wait 2-3 minutes for project to initialize
6. Go to **Project Settings** > **API**
7. Copy these values:
   - **Project URL** (e.g., `https://xxx.supabase.co`)
   - **API Keys** > **anon** **public** key
   - **API Keys** > **service_role** key (⚠️ Keep this secret!)

### 1.2 Clerk

1. Go to https://clerk.com
2. Create account and sign in
3. Click "+ Create Application"
4. Application name: `ARSP`
5. Select sign-in methods: **Email**, **Google** (optional)
6. Click **Create Application**
7. You'll see the Quick start page
8. Copy these values:
   - **Publishable Key** (starts with `pk_test_...`)
   - Go to **API Keys** in sidebar
   - Copy **Secret Key** (starts with `sk_test_...`)

### 1.3 Lingo.dev

1. Go to https://lingo.dev
2. Sign up for free account
3. Complete onboarding
4. Go to **Settings** > **API Keys**
5. Click **Create API Key**
6. Copy the API key (starts with `lingo_...`)

### 1.4 Hugging Face (Optional)

1. Go to https://huggingface.co
2. Sign up / Sign in
3. Go to **Settings** > **Access Tokens**
4. Click **New Token**
5. Name: `ARSP`
6. Role: **Read**
7. Copy the token (starts with `hf_...`)

**Note**: Hugging Face API key is optional but recommended. It increases rate limits for AI models.

## Step 2: Database Setup (30 minutes)

### 2.1 Apply Migrations

1. Go to your Supabase project dashboard
2. Click **SQL Editor** in the left sidebar
3. Click **+ New Query**

4. Copy and paste the contents of `arsp-app-backup/supabase/migrations/001_create_tables.sql`
5. Click **Run** (or Ctrl/Cmd + Enter)
6. You should see "Success. No rows returned"

7. Repeat for these files in order:
   - `002_enable_rls.sql`
   - `003_storage_setup.sql`
   - `20241114_consent_logs.sql`

8. Finally, run `seed.sql` to populate journals table with sample data

### 2.2 Verify Database Setup

1. In Supabase dashboard, click **Table Editor**
2. You should see these tables:
   - `profiles`
   - `drafts`
   - `uploads`
   - `literature_reviews`
   - `journals` (should have ~30 rows)
   - `consent_logs`

3. Click **Storage** in sidebar
4. You should see a bucket named `papers`

## Step 3: Backend Setup (15 minutes)

### 3.1 Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Note**: Installing PyTorch and Sentence Transformers may take 5-10 minutes.

### 3.2 Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env` and fill in all the API keys you collected:

```bash
# Environment
ENVIRONMENT=development

# Supabase (from Step 1.1)
SUPABASE_URL=https://YOUR_PROJECT.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Clerk (from Step 1.2)
CLERK_SECRET_KEY=sk_test_...
CLERK_PUBLISHABLE_KEY=pk_test_...

# Lingo.dev (from Step 1.3)
LINGO_API_KEY=lingo_...

# Hugging Face (from Step 1.4 - optional)
HF_API_KEY=hf_...

# API Keys (Optional - all free)
SEMANTIC_SCHOLAR_API_KEY=  # Leave empty for now
CROSSREF_EMAIL=your@email.com  # Your email for polite pool access

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000
```

### 3.3 Test Backend

```bash
# Make sure you're in backend/ directory with venv activated
python -m app.main
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Open http://localhost:8000/api/docs - you should see the API documentation (Swagger UI).

## Step 4: Frontend Setup (10 minutes)

### 4.1 Install Dependencies

```bash
cd frontend
npm install
```

### 4.2 Configure Environment

```bash
cd frontend
touch .env.local
```

Edit `.env.local`:

```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Clerk (from Step 1.2)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...

# Supabase (from Step 1.1)
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

# Lingo.dev (from Step 1.3)
NEXT_PUBLIC_LINGO_API_KEY=lingo_...
```

### 4.3 Set up Clerk in Next.js

1. Install Clerk for Next.js:
```bash
npm install @clerk/nextjs
```

2. The frontend code expects Clerk to be set up. The integration will be completed in the next steps.

### 4.4 Test Frontend

```bash
cd frontend
npm run dev
```

You should see:
```
   ▲ Next.js 16.0.1
   - Local:        http://localhost:3000
   - Environments: .env.local

 ✓ Ready in 2.3s
```

Open http://localhost:3000

## Step 5: Running the Application

### 5.1 Start Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
```

Leave this terminal running.

### 5.2 Start Frontend (in new terminal)

```bash
cd frontend
npm run dev
```

Leave this terminal running.

### 5.3 Access the Application

1. Open http://localhost:3000
2. You should see the ARSP landing page
3. Click "Get Started" or "Login"
4. Clerk will handle authentication

## Step 6: Testing Features

### 6.1 Test Topics Discovery

1. Log in to the application
2. Navigate to **Topics** from the sidebar
3. Enter a search query (e.g., "artificial intelligence ethics")
4. Click **Search**
5. You should see 5 trending topics from Semantic Scholar and arXiv

### 6.2 Test Paper Upload

1. Navigate to **Papers**
2. Click **Upload Paper** or drag-and-drop a PDF
3. Wait for upload to complete
4. Click **Process** to analyze the paper
5. You should see:
   - AI-generated summary
   - Key insights (5-10 points)
   - References in JSON format

### 6.3 Test Plagiarism Check

1. Navigate to **Plagiarism**
2. Paste some text in the editor (or type)
3. Click **Check for Plagiarism**
4. You should see:
   - Originality score (0-100%)
   - Flagged sections (if any)
   - Citation suggestions from CrossRef

### 6.4 Test Journal Recommendations

1. Navigate to **Journals**
2. Paste an abstract (or write one)
3. Add keywords
4. Apply filters (optional):
   - Open access only
   - Minimum impact factor
   - Maximum publication time
5. Click **Recommend**
6. You should see 10 ranked journals with fit scores

## Step 7: Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'app'`
**Solution**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Problem**: Database connection errors
**Solution**:
- Check `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Verify database is running in Supabase dashboard
- Check if migrations were applied correctly

**Problem**: "401 Unauthorized" errors
**Solution**:
- Verify `CLERK_SECRET_KEY` is correct
- Make sure you're logged in through Clerk on the frontend
- Check that Clerk JWT tokens are being sent

**Problem**: Slow AI processing / Timeouts
**Solution**:
- Add `HF_API_KEY` to increase Hugging Face rate limits
- Reduce text length for summarization/plagiarism checks
- Check internet connection

### Frontend Issues

**Problem**: "Cannot find module '@clerk/nextjs'"
**Solution**:
```bash
cd frontend
npm install @clerk/nextjs
```

**Problem**: "API request failed"
**Solution**:
- Make sure backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS is enabled in backend

**Problem**: Authentication not working
**Solution**:
- Verify `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` matches your Clerk app
- Check Clerk dashboard for any configuration issues
- Clear browser cookies and try again

## Step 8: Next Steps

### For Development

1. **Implement Lingo.dev Integration** (Task 3)
   - Create `i18n.config.json`
   - Extract UI strings to `locales/en.json`
   - Run Lingo CLI to generate translations
   - Add language selector component

2. **Add DPDP Consent Dialog** (Task 5.1)
   - Create consent dialog component
   - Log consent to database
   - Display on first visit

3. **Implement Government Alignment Module**
   - Create API endpoints
   - Integrate with AP Government data
   - Add SDG alignment logic

4. **Add Tests**
   - Unit tests for services
   - Integration tests for API endpoints
   - E2E tests for workflows

### For Production

1. **Deploy Backend**
   - Use Railway, Render, or Fly.io
   - Set environment variables
   - Configure production database

2. **Deploy Frontend**
   - Deploy to Vercel
   - Set environment variables
   - Configure custom domain

3. **Monitoring**
   - Set up Sentry for error tracking
   - Add analytics
   - Configure logging

## Appendix

### Useful Commands

```bash
# Backend
cd backend
source venv/bin/activate
python -m app.main                    # Start server
pytest tests/                         # Run tests
black app/                            # Format code

# Frontend
cd frontend
npm run dev                           # Start dev server
npm run build                         # Build for production
npm run start                         # Start production server
npm run lint                          # Lint code

# Database
# Via Supabase Dashboard > SQL Editor
SELECT * FROM profiles;               # View users
SELECT * FROM journals;               # View journals
SELECT * FROM uploads;                # View uploaded papers
```

### Environment Variables Reference

See `.env.example` files in `backend/` and `frontend/` directories.

### API Endpoints

Full API documentation available at: http://localhost:8000/api/docs

Key endpoints:
- `POST /api/v1/topics/trending` - Get trending topics
- `POST /api/v1/papers/upload` - Upload paper
- `POST /api/v1/plagiarism/check` - Check plagiarism
- `POST /api/v1/journals/recommend` - Get journal recommendations

### Support

- **GitHub Issues**: https://github.com/BishalJena/ARSP-v1/issues
- **Documentation**: See `.kiro/specs/` folder

---

**Estimated Setup Time**: 1-2 hours (depending on experience)

**Congratulations!** You now have a fully functional ARSP installation. 🎉
