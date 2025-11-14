# 🚀 Quick Start Guide

Environment files have been created with your API keys!

## ⚠️ Missing Keys (Required)

You need to get these two keys from Clerk dashboard:

### 1. Clerk Secret Key
1. Go to https://dashboard.clerk.com
2. Select your application
3. Navigate to **API Keys** in the left sidebar
4. Copy the **Secret Key** (starts with `sk_test_...`)
5. Replace `NEEDS_CLERK_SECRET_KEY_FROM_DASHBOARD` in:
   - `backend/.env`
   - `frontend/.env.local`

### 2. Supabase Service Role Key
1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **API**
4. Copy the **service_role** key (under "Project API keys")
5. Replace `NEEDS_SERVICE_ROLE_KEY_FROM_SUPABASE_DASHBOARD` in `backend/.env`

## ✅ Keys Already Configured

- ✅ Clerk Publishable Key
- ✅ Supabase URL & Anon Key
- ✅ Lingo.dev API Key

## 🧪 Testing Steps

### 1. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Start Backend

```bash
cd backend
python -m app.main
```

Backend should start at: http://localhost:8000
API docs at: http://localhost:8000/api/docs

### 3. Start Frontend (in new terminal)

```bash
cd frontend
npm run dev
```

Frontend should start at: http://localhost:3000

### 4. Test the Application

1. **Open** http://localhost:3000
2. **Sign In** using Clerk (email or Google)
3. **Test Language Selector** - Switch between 12+ languages
4. **Test DPDP Consent** - Should appear on first visit
5. **Test All Modules**:
   - Topic Discovery
   - Paper Analysis (upload a PDF)
   - Plagiarism Check
   - Journal Recommendations
   - Government Alignment
   - Impact Prediction

## 🐛 Troubleshooting

### Backend won't start
- Make sure you filled in `CLERK_SECRET_KEY` in `backend/.env`
- Make sure you filled in `SUPABASE_SERVICE_KEY` in `backend/.env`
- Check if port 8000 is already in use

### Frontend won't start
- Make sure you filled in `CLERK_SECRET_KEY` in `frontend/.env.local`
- Run `npm install` to install dependencies
- Check if port 3000 is already in use

### Authentication not working
- Verify Clerk keys are correct (both publishable and secret)
- Check Clerk dashboard for application settings
- Make sure both backend and frontend are running

### Translations not working
- Run `cd frontend && npx lingo translate` to generate translation files
- Verify Lingo.dev API key is correct
- Check browser console for errors

## 📊 Expected Results

| Feature | Status After Setup |
|---------|-------------------|
| User Login | ✅ Should work with Clerk |
| Language Switching | ✅ Should work (13 languages) |
| DPDP Consent | ✅ Should display on first visit |
| API Endpoints | ✅ Should respond (check /api/docs) |
| Translations | ⏳ Run `lingo translate` first |
| File Upload | ⏳ Upload PDFs to test |

## 🎯 Next Steps

After testing:
1. Apply database migrations (see `arsp-app-backup/supabase/migrations/`)
2. Seed journals table
3. Run `npx lingo translate` to generate all translation files
4. Test end-to-end workflows
5. Deploy to production

## 📝 Notes

- **Hugging Face API Key** is optional but recommended for faster AI processing
- **OpenRouter API Key** in your list is not used by this project
- All external APIs (Semantic Scholar, arXiv, CrossRef) work without keys

## 🆘 Need Help?

- Backend API docs: http://localhost:8000/api/docs
- See `SETUP_GUIDE.md` for detailed setup instructions
- See `COMPLETION_SUMMARY.md` for full project overview
- Check `tasks.md` for implementation status
