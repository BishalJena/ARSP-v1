# Setup Guide

Complete guide to set up ARSP locally for development.

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ARSP-v1
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys (see below)

# Set up database (run SQL schema)
python setup_db_auto.py
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local and add your API keys (see below)
```

## Environment Variables

### How Environment Variables Work

Environment variables let your app behave differently in development vs production:

- **Development**: Your frontend calls `http://localhost:8000` (your local backend)
- **Production**: Your frontend calls `https://your-backend.onrender.com` (deployed backend)

This is controlled by `NEXT_PUBLIC_API_URL`:
```typescript
// In code: process.env.NEXT_PUBLIC_API_URL
// Development (.env.local): http://localhost:8000/api/v1
// Production (Vercel): https://backend.onrender.com/api/v1
```

For deployment details, see [DEPLOYMENT.md](./DEPLOYMENT.md).

### Backend (.env)

```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# Clerk Authentication
CLERK_SECRET_KEY=your_clerk_secret_key

# Optional but recommended
HF_API_KEY=your_huggingface_api_key
LINGO_API_KEY=your_lingo_api_key
SEMANTIC_SCHOLAR_API_KEY=  # Optional
CROSSREF_EMAIL=your_email  # Optional, for polite pool
```

### Frontend (.env.local)

```env
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key

# Lingo.dev
NEXT_PUBLIC_LINGO_API_KEY=your_lingo_api_key
```

## Getting API Keys

### 1. Supabase

1. Go to https://supabase.com
2. Create a new project
3. Go to **Settings** → **API**
4. Copy:
   - Project URL
   - `anon` `public` key
   - `service_role` key (keep secret!)

### 2. Clerk

1. Go to https://clerk.com
2. Create an application
3. Go to **API Keys**
4. Copy:
   - Publishable Key
   - Secret Key

### 3. Hugging Face (Optional but Recommended)

1. Go to https://huggingface.co
2. Sign up and go to **Settings** → **Access Tokens**
3. Create a new token
4. Copy the token

### 4. Lingo.dev (For Multilingual Support)

1. Go to https://lingo.dev
2. Sign up and create a project
3. Copy your API key

## Database Setup

The database schema is in `backend/supabase_setup.sql`. Run it using:

```bash
cd backend
python setup_db_auto.py
```

This creates:
- `profiles` - User profiles
- `uploads` - Paper uploads and analysis
- `drafts` - Plagiarism check results
- `journals` - Journal database (pre-seeded with 15 top journals)

## Running the Application

### Start Backend

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Start Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at http://localhost:3000

## Testing the Application

1. Open http://localhost:3000
2. Sign up/login using Clerk
3. Accept DPDP consent dialog (first visit)
4. Test features:
   - **Topic Discovery**: Search trending research topics
   - **Paper Analysis**: Upload a PDF for AI summarization
   - **Plagiarism Check**: Paste text to check for plagiarism
   - **Journal Finder**: Get journal recommendations
5. Test language switching (15 languages supported)

## Troubleshooting

### Backend won't start

- Verify Python version: `python --version` (should be 3.10+)
- Check if virtual environment is activated
- Ensure all environment variables are set
- Check port 8000 is not in use

### Frontend won't start

- Verify Node.js version: `node --version` (should be 18+)
- Clear cache: `rm -rf .next node_modules && npm install`
- Check port 3000 is not in use

### Authentication errors

- Verify Clerk keys are correct
- Check both frontend and backend are running
- Clear browser cookies/localStorage

### API calls fail

- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in frontend `.env.local`
- Check browser console for CORS errors

### Database errors

- Verify Supabase credentials
- Run database setup script again
- Check Supabase dashboard for any issues

## Development Tips

- Use `npm run build` to test production build
- Backend auto-reloads with `--reload` flag
- Frontend has hot reload enabled
- Check API docs at http://localhost:8000/docs for testing endpoints
- Use browser DevTools Network tab to debug API calls

## Next Steps

After successful setup:

1. Review the [Architecture Documentation](ARCHITECTURE.md)
2. Read the [Deployment Guide](DEPLOYMENT.md) for production deployment
3. Check out [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
4. Explore the codebase in `frontend/app` and `backend/app`

## Need Help?

- Check the [main README](README.md) for project overview
- Review API documentation at http://localhost:8000/docs
- Check backend logs for error details
- Check browser console for frontend errors
