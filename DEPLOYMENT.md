# ARSP-v1 Deployment Guide

Complete step-by-step guide to deploy your ARSP (AI-Enabled Research Support Platform) to production.

---

## ⚠️ CRITICAL: Localhost Problem Explained

**The Problem:** If you deploy without proper setup, your frontend will try to call `http://localhost:8000` from users' browsers (which fails).

**The Solution:** Environment variables! Your code uses `process.env.NEXT_PUBLIC_API_URL` which:
- **Development**: Uses `localhost:8000`
- **Production**: Uses your deployed backend URL (set in Vercel)

**The Fix (Simple):**
1. Deploy backend first → Copy URL (`https://arsp-backend-xyz.onrender.com`)
2. In Vercel, set `NEXT_PUBLIC_API_URL=https://arsp-backend-xyz.onrender.com/api/v1`
3. Deploy frontend → It will call production backend, not localhost ✅

---

## 📝 Deployment Order (FOLLOW THIS!)

```
Step 1: Deploy Backend → https://backend.onrender.com
Step 2: Copy that URL
Step 3: Set NEXT_PUBLIC_API_URL in Vercel = backend URL + /api/v1
Step 4: Deploy Frontend → https://arsp.vercel.app
Step 5: Update Backend CORS to allow frontend URL
✅ Done!
```

---

## 🎯 Deployment Overview

**Stack:**
- **Frontend**: Next.js 16 (React 19) → Deploy to **Vercel**
- **Backend**: FastAPI (Python) → Deploy to **Render** or **Railway**
- **Database**: Supabase (already set up)
- **Authentication**: Clerk (already configured)

---

## 📋 Pre-Deployment Checklist

### 1. Verify Your Services Are Ready

- [x] **Supabase**: Already configured (`rvhngxjkkikzsawplagw.supabase.co`)
- [x] **Clerk**: Already configured
- [ ] **Hugging Face API Key**: Get from https://huggingface.co/settings/tokens
- [ ] **Lingo.dev API Key**: Already have (`api_cevh9pmp5jfz4gjpr8poj1ap`)

---

## 🚀 Part 1: Deploy Backend (FastAPI)

### Option A: Deploy to Render (Recommended - Free Tier Available)

#### Step 1: Prepare Backend for Deployment

1. **Create `render.yaml` in backend folder:**

```bash
cd backend
```

Create file `render.yaml`:
```yaml
services:
  - type: web
    name: arsp-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: ENVIRONMENT
        value: production
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: SUPABASE_SERVICE_KEY
        sync: false
      - key: CLERK_SECRET_KEY
        sync: false
      - key: HF_API_KEY
        sync: false
      - key: LINGO_API_KEY
        sync: false
```

#### Step 2: Deploy to Render

1. Go to https://render.com and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the `ARSP-v1` repository
5. Configure:
   - **Name**: `arsp-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or paid for better performance)

6. **Add Environment Variables** (click "Advanced" → "Add Environment Variable"):
   ```
   ENVIRONMENT=production
   SUPABASE_URL=https://rvhngxjkkikzsawplagw.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2aG5neGpra2lrenNhd3BsYWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxMjg0NjYsImV4cCI6MjA3ODcwNDQ2Nn0.eqYflu69T5Ywo4UJzrp4e3SBq1tWZs5IA1BDHYyJAmI
   SUPABASE_SERVICE_KEY=<get from Supabase dashboard>
   CLERK_SECRET_KEY=sk_test_C3eCN9MiuOymS1CKdeFNaaIB6Qy6Mb4aavA0uzAR1S
   HF_API_KEY=<your-huggingface-api-key>
   LINGO_API_KEY=api_cevh9pmp5jfz4gjpr8poj1ap
   HOST=0.0.0.0
   PORT=10000
   DEBUG=False
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

7. Click **"Create Web Service"**
8. Wait for deployment (5-10 minutes first time)
9. **Note your backend URL**: `https://arsp-backend.onrender.com`

---

### Option B: Deploy to Railway (Alternative)

1. Go to https://railway.app and sign up/login
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway will auto-detect Python
5. Add environment variables (same as Render above)
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Deploy and note your URL

---

## 🎨 Part 2: Deploy Frontend (Next.js)

### Deploy to Vercel (Recommended - Made by Next.js creators)

#### Step 1: Prepare Frontend

1. **Update API URL for production** - Create `frontend/.env.production`:

```bash
cd frontend
```

Create `.env.production` file:
```env
# Backend API URL (update with your Render/Railway URL)
NEXT_PUBLIC_API_URL=https://arsp-backend.onrender.com/api/v1

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://rvhngxjkkikzsawplagw.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ2aG5neGpra2lrenNhd3BsYWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMxMjg0NjYsImV4cCI6MjA3ODcwNDQ2Nn0.eqYflu69T5Ywo4UJzrp4e3SBq1tWZs5IA1BDHYyJAmI

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_aG9seS1odXNreS05Mi5jbGVyay5hY2NvdW50cy5kZXYk
CLERK_SECRET_KEY=sk_test_C3eCN9MiuOymS1CKdeFNaaIB6Qy6Mb4aavA0uzAR1S

# Lingo.dev
NEXT_PUBLIC_LINGO_API_KEY=api_cevh9pmp5jfz4gjpr8poj1ap
```

#### Step 2: Deploy to Vercel

1. Go to https://vercel.com and sign up/login with GitHub
2. Click **"Add New..."** → **"Project"**
3. Import your `ARSP-v1` repository
4. Configure:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)

5. **Add Environment Variables**:
   - Click "Environment Variables"
   - Add all variables from `.env.production` above
   - Make sure to add them for **Production**, **Preview**, and **Development**

6. Click **"Deploy"**
7. Wait 2-5 minutes
8. **Note your frontend URL**: `https://arsp-v1.vercel.app` (or custom domain)

#### Step 3: Update CORS in Backend

1. Go back to Render/Railway backend settings
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://arsp-v1.vercel.app,https://arsp-v1-*.vercel.app
   ```
3. Redeploy backend

---

## 🔧 Part 3: Configure Clerk for Production

1. Go to https://dashboard.clerk.com
2. Select your application
3. Go to **"Domains"** in sidebar
4. Add your production domain: `arsp-v1.vercel.app`
5. Update **Redirect URLs**:
   - Add: `https://arsp-v1.vercel.app/dashboard`
   - Add: `https://arsp-v1.vercel.app/login`

---

## 🗄️ Part 4: Verify Supabase Configuration

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **API**
4. Verify:
   - Project URL matches your env vars
   - Anon key is correct
5. Go to **Authentication** → **URL Configuration**
6. Add your Vercel URL to **Redirect URLs**:
   - `https://arsp-v1.vercel.app/**`

---

## ✅ Part 5: Post-Deployment Testing

### Test Backend

1. Visit: `https://arsp-backend.onrender.com/docs`
2. You should see FastAPI Swagger documentation
3. Test the `/health` endpoint

### Test Frontend

1. Visit: `https://arsp-v1.vercel.app`
2. Try to register/login
3. Test each feature:
   - Topic Discovery
   - Paper Analysis
   - Plagiarism Check
   - Journal Finder

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Backend won't start
- Check logs in Render/Railway dashboard
- Verify all environment variables are set
- Check Python version is 3.11+

**Problem**: CORS errors
- Update `CORS_ORIGINS` to include your Vercel URL
- Redeploy backend

**Problem**: Database connection fails
- Verify Supabase credentials
- Check if Supabase project is active

### Frontend Issues

**Problem**: API calls fail
- Check `NEXT_PUBLIC_API_URL` points to correct backend
- Verify backend is running
- Check browser console for errors

**Problem**: Authentication fails
- Verify Clerk keys are correct
- Check Clerk dashboard for domain configuration
- Ensure redirect URLs are set

**Problem**: Build fails
- Check Node.js version (should be 18+)
- Run `npm install` locally to verify dependencies
- Check Vercel build logs

---

## 🔐 Security Checklist

- [ ] All API keys are in environment variables (not in code)
- [ ] `.env` files are in `.gitignore`
- [ ] Supabase Row Level Security (RLS) is enabled
- [ ] Backend has rate limiting (consider adding)
- [ ] HTTPS is enabled (automatic on Vercel/Render)
- [ ] CORS is properly configured

---

## 💰 Cost Estimate

**Free Tier (Good for testing/MVP):**
- Vercel: Free (Hobby plan)
- Render: Free (with sleep after inactivity)
- Supabase: Free (500MB database, 2GB bandwidth)
- Clerk: Free (10,000 MAU)
- Total: **$0/month**

**Production Tier (Recommended for real users):**
- Vercel Pro: $20/month
- Render Starter: $7/month
- Supabase Pro: $25/month
- Clerk Pro: $25/month
- Total: **~$77/month**

---

## 🚀 Quick Deploy Commands

```bash
# Commit all changes
git add .
git commit -m "Prepare for deployment"
git push origin main

# Backend will auto-deploy on Render/Railway
# Frontend will auto-deploy on Vercel
```

---

## 📝 Next Steps After Deployment

1. **Set up monitoring**: Add error tracking (Sentry)
2. **Configure analytics**: Add Google Analytics or Plausible
3. **Set up custom domain**: Buy domain and configure in Vercel
4. **Enable caching**: Configure Redis for better performance
5. **Add CI/CD**: Set up automated testing before deployment

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Clerk Docs**: https://clerk.com/docs

---

**Good luck with your deployment! 🎉**
