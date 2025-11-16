# ARSP Deployment Guide

Complete guide to deploy ARSP (AI-Enabled Research Support Platform) to production with Vercel (frontend) and Render (backend).

---

## 📋 Quick Start

```bash
# 1. Deploy Backend (Render) → Get URL
# 2. Deploy Frontend (Vercel) → Set NEXT_PUBLIC_API_URL to backend URL
# 3. Update Backend CORS_ORIGINS with frontend URL
# ✅ Done!
```

---

## 🎯 Deployment Architecture

- **Frontend**: Next.js 16 (React 19) → **Vercel**
- **Backend**: FastAPI (Python) → **Render**
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Email/Password + JWT (Self-contained)

---

## 📦 Pre-Deployment Checklist

### Required Services

- [x] **Supabase**: Database already configured
- [ ] **Hugging Face API Key**: Get from https://huggingface.co/settings/tokens
- [ ] **OpenRouter API Key**: For Gemini AI integration
- [ ] **Winston AI API Key**: For plagiarism detection
- [ ] **Lingo.dev API Key**: For translations (optional)

### Required Migrations

- [ ] Run `backend/migrations/create_users_table.sql` in Supabase SQL Editor
- [ ] Verify users table exists with password_hash column

---

## 🚀 Part 1: Deploy Backend to Render

### Step 1: Prepare Backend

The `render.yaml` file is already in the root directory with all necessary configuration.

### Step 2: Deploy to Render

1. **Sign Up/Login** to https://render.com
2. Click **"New +"** → **"Blueprint"**
3. **Connect GitHub** repository
4. Select **"ARSP-v1"** repository
5. Render will detect `render.yaml` automatically
6. Click **"Apply Blueprint"**

### Step 3: Configure Environment Variables

In Render dashboard, add these environment variables:

```env
# Environment
ENVIRONMENT=production

# Supabase Database
SUPABASE_URL=https://rvhngxjkkikzsawplagw.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2aG5neGpra2lrenNhd3BsYWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxMjg0NjYsImV4cCI6MjA3ODcwNDQ2Nn0.eqYflu69T5Ywo4UJzrp4e3SBq1tWZs5IA1BDHYyJAmI
SUPABASE_SERVICE_KEY=<get-from-supabase-dashboard>
SUPABASE_DB_PASS=<your-db-password>

# JWT Authentication (Render auto-generates JWT_SECRET_KEY)
JWT_ALGORITHM=HS256

# API Keys
OPENROUTER_API_KEY=<your-openrouter-api-key>
WINSTON_API_KEY=<your-winston-api-key>
HF_API_KEY=<your-huggingface-api-key>
SEMANTIC_SCHOLAR_API_KEY=<your-semantic-scholar-key>
LINGO_API_KEY=<your-lingo-api-key>

# CORS (Update after deploying frontend)
CORS_ORIGINS=https://your-frontend.vercel.app

# Server Configuration
HOST=0.0.0.0
PORT=10000
DEBUG=False
```

### Step 4: Deploy and Get URL

1. Click **"Deploy"**
2. Wait 5-10 minutes for first deployment
3. **Copy your backend URL**: `https://arsp-backend-xyz.onrender.com`

**Important:** Save this URL - you'll need it for frontend deployment!

---

## 🎨 Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

1. **Update `.env.production.example`** (if needed):

```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://rvhngxjkkikzsawplagw.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2aG5neGpra2lrenNhd3BsYWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxMjg0NjYsImV4cCI6MjA3ODcwNDQ2Nn0.eqYflu69T5Ywo4UJzrp4e3SBq1tWZs5IA1BDHYyJAmI
NEXT_PUBLIC_LINGO_API_KEY=<your-lingo-api-key>
```

### Step 2: Deploy to Vercel

1. Go to https://vercel.com and sign up/login with GitHub
2. Click **"Add New..."** → **"Project"**
3. Import **"ARSP-v1"** repository
4. Configure:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)

### Step 3: Add Environment Variables

Click **"Environment Variables"** and add:

```env
NEXT_PUBLIC_API_URL=https://arsp-backend-xyz.onrender.com/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://rvhngxjkkikzsawplagw.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
NEXT_PUBLIC_LINGO_API_KEY=api_cevh9pmp5jfz4gjpr8poj1ap
```

**Important:** Add for Production, Preview, and Development environments.

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait 2-5 minutes
3. **Copy your frontend URL**: `https://arsp-v1.vercel.app`

---

## 🔧 Part 3: Update CORS in Backend

1. Go back to **Render dashboard**
2. Find your backend service
3. Go to **Environment** tab
4. Update `CORS_ORIGINS`:

```env
CORS_ORIGINS=https://arsp-v1.vercel.app,https://arsp-v1-*.vercel.app
```

5. Save and **redeploy** backend

---

## 🗄️ Part 4: Verify Supabase Configuration

### Database Migration

1. Go to https://supabase.com/dashboard
2. Select your project: `rvhngxjkkikzsawplagw`
3. Go to **SQL Editor**
4. Run the migration from `backend/migrations/create_users_table.sql`
5. Verify users table was created successfully

### API Configuration

1. Go to **Settings** → **API**
2. Verify:
   - Project URL matches environment variables
   - Anon key is correct
   - Service role key is saved

### URL Configuration

1. Go to **Authentication** → **URL Configuration**
2. Add Site URL: `https://arsp-v1.vercel.app`
3. Add Redirect URLs:
   - `https://arsp-v1.vercel.app/**`

---

## ✅ Part 5: Post-Deployment Testing

### Test Backend

1. **Visit API Documentation**:
   ```
   https://arsp-backend-xyz.onrender.com/docs
   ```

2. **Test Health Endpoint**:
   ```bash
   curl https://arsp-backend-xyz.onrender.com/api/v1/health
   ```
   Expected: `{"status": "healthy"}`

3. **Test Registration**:
   ```bash
   curl -X POST https://arsp-backend-xyz.onrender.com/api/v1/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123", "full_name": "Test User"}'
   ```
   Expected: JWT token and user object

### Test Frontend

1. **Visit**: `https://arsp-v1.vercel.app`
2. **Test Authentication**:
   - Register new account
   - Login with credentials
   - Access dashboard
3. **Test Features**:
   - Paper upload and analysis
   - Plagiarism detection
   - Journal recommendations
   - Multi-language translation

---

## 🐛 Troubleshooting

### Backend Issues

**Problem: Backend won't start**
```bash
# Check Render logs
# Verify Python version is 3.9+
# Verify all environment variables are set
```

**Problem: CORS errors**
```bash
# Solution:
1. Update CORS_ORIGINS in Render
2. Include both production and preview URLs
3. Redeploy backend
```

**Problem: Database connection fails**
```bash
# Verify:
- Supabase credentials are correct
- Users table exists
- Row Level Security policies allow access
```

**Problem: bcrypt/passlib errors**
```bash
# Solution:
1. Verify bcrypt==4.0.1 is in requirements.txt
2. Clear build cache in Render
3. Redeploy
```

### Frontend Issues

**Problem: API calls fail (localhost error)**
```bash
# Solution:
1. Verify NEXT_PUBLIC_API_URL is set in Vercel
2. Must include /api/v1 suffix
3. Redeploy frontend
```

**Problem: Authentication fails**
```bash
# Check:
- Backend /auth/register endpoint works
- JWT_SECRET_KEY is set in backend
- Users table exists in Supabase
```

**Problem: Build fails**
```bash
# Verify:
- Node.js version is 18+ (set in Vercel)
- All dependencies are in package.json
- Check Vercel build logs for specific error
```

**Problem: Environment variables not working**
```bash
# Solution:
1. All frontend env vars must start with NEXT_PUBLIC_
2. Must be set in Vercel dashboard
3. Redeploy after adding variables
```

---

## 🔐 Security Checklist

- [ ] All API keys in environment variables (not in code)
- [ ] `.env` files are in `.gitignore`
- [ ] JWT_SECRET_KEY is randomly generated (Render does this)
- [ ] Supabase Row Level Security (RLS) is enabled
- [ ] CORS is properly configured with specific domains
- [ ] HTTPS is enabled (automatic on Vercel/Render)
- [ ] Database password is strong and secure
- [ ] No secrets committed to git

---

## 💰 Cost Estimate

### Free Tier (Development/Testing)
- **Vercel**: Free (Hobby plan)
- **Render**: Free (sleeps after 15min inactivity)
- **Supabase**: Free (500MB database, 2GB bandwidth)
- **Total**: **$0/month**

### Production Tier (Recommended)
- **Vercel Pro**: $20/month (better performance, analytics)
- **Render Starter**: $7/month (always on, faster)
- **Supabase Pro**: $25/month (8GB database, better support)
- **Total**: **~$52/month**

---

## 🚀 Continuous Deployment

Both Vercel and Render support auto-deployment:

```bash
# Make changes and commit
git add .
git commit -m "Update feature"
git push origin main

# Backend auto-deploys on Render
# Frontend auto-deploys on Vercel
# ✅ Done!
```

---

## 📝 Environment Variables Reference

### Backend (Render)

| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | production | ✅ |
| `SUPABASE_URL` | Supabase project URL | ✅ |
| `SUPABASE_KEY` | Supabase anon key | ✅ |
| `SUPABASE_SERVICE_KEY` | Supabase service role key | ✅ |
| `JWT_SECRET_KEY` | Auto-generated by Render | ✅ |
| `JWT_ALGORITHM` | HS256 | ✅ |
| `OPENROUTER_API_KEY` | For Gemini AI | ✅ |
| `WINSTON_API_KEY` | For plagiarism detection | ✅ |
| `HF_API_KEY` | Hugging Face API key | ✅ |
| `CORS_ORIGINS` | Vercel frontend URL | ✅ |
| `LINGO_API_KEY` | For translations | Optional |
| `SEMANTIC_SCHOLAR_API_KEY` | For paper search | Optional |

### Frontend (Vercel)

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL + /api/v1 | ✅ |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | ✅ |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key | ✅ |
| `NEXT_PUBLIC_LINGO_API_KEY` | Lingo.dev API key | Optional |

---

## 🆘 Common Deployment Errors

### "Cannot find module"
```bash
# Solution: Verify package.json dependencies
npm install
npm run build  # Test locally first
```

### "API URL not defined"
```bash
# Solution: Set NEXT_PUBLIC_API_URL in Vercel
# Must start with NEXT_PUBLIC_
```

### "CORS policy error"
```bash
# Solution: Update CORS_ORIGINS in Render backend
# Format: https://domain1.com,https://domain2.com
```

### "Database connection refused"
```bash
# Solution: Check Supabase credentials
# Verify database is not paused
```

---

## 🎯 Post-Deployment Recommendations

1. **Set up monitoring**:
   - Add Sentry for error tracking
   - Use Vercel Analytics
   - Monitor Render logs

2. **Configure custom domain**:
   - Buy domain (Namecheap, Google Domains)
   - Add to Vercel project settings
   - Update CORS_ORIGINS in backend

3. **Optimize performance**:
   - Enable Vercel Edge Functions for API routes
   - Use Render's cache headers
   - Optimize images with Next.js Image component

4. **Add analytics**:
   - Google Analytics or Plausible
   - Vercel Web Analytics (built-in)

5. **Set up backups**:
   - Supabase automatic backups (Pro plan)
   - Export database regularly

---

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Commit all code to GitHub
- [ ] Run database migration in Supabase
- [ ] Get all required API keys
- [ ] Update `.env.example` files

### Backend Deployment
- [ ] Deploy backend to Render
- [ ] Set all environment variables
- [ ] Test health endpoint
- [ ] Test authentication endpoints
- [ ] Copy backend URL

### Frontend Deployment
- [ ] Set NEXT_PUBLIC_API_URL with backend URL
- [ ] Deploy frontend to Vercel
- [ ] Test registration/login
- [ ] Test all features

### Post-Deployment
- [ ] Update CORS_ORIGINS in backend
- [ ] Redeploy backend
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring
- [ ] Document production URLs

---

**Deployment Status**: Ready for production! 🚀
**Last Updated**: 2025-11-16
