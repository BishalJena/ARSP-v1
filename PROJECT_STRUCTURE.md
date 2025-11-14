# ARSP Project Structure

## Overview
AI-Enabled Research Support Platform - A multilingual research assistant for academic workflows.

## Directory Structure

```
ARSP-v1/
├── frontend/              # Next.js 16 Frontend Application
│   ├── app/              # Next.js App Router pages
│   │   ├── dashboard/   # Main application pages
│   │   │   ├── topics/        # Topic discovery
│   │   │   ├── papers/        # Literature review
│   │   │   ├── plagiarism/    # Plagiarism detection
│   │   │   ├── journals/      # Journal recommendations
│   │   │   ├── government/    # AP Govt alignment
│   │   │   └── impact/        # Impact prediction
│   │   ├── login/       # Authentication pages
│   │   └── register/
│   ├── components/      # React components
│   │   └── ui/         # shadcn/ui components
│   ├── lib/            # Utilities and API client
│   │   ├── api-client.ts    # Backend API integration
│   │   ├── auth-context.tsx # Auth state management
│   │   └── utils.ts         # Helper functions
│   └── .env.local      # Environment variables
│
├── backend/              # Backend Services (To Be Built)
│   ├── supabase/        # Supabase Edge Functions
│   │   ├── functions/
│   │   │   ├── lit-review/      # Literature review processing
│   │   │   ├── plagiarism/      # Plagiarism detection
│   │   │   └── journals/        # Journal recommendations
│   │   └── migrations/  # Database migrations
│   └── README.md
│
├── .kiro/                # Project Specifications
│   └── specs/
│       └── arsp-multilingual-research-platform/
│           ├── requirements.md  # System requirements
│           ├── design.md        # Architecture design
│           └── tasks.md         # Implementation tasks
│
├── docs/                 # Documentation
│   ├── API.md           # API documentation
│   ├── SETUP.md         # Setup instructions
│   └── DEPLOYMENT.md    # Deployment guide
│
├── arsp-app-backup/      # Backup of previous React/Vite work
│
└── README.md             # Project overview
```

## Technology Stack

### Frontend
- **Framework**: Next.js 16 with App Router
- **UI**: Tailwind CSS + shadcn/ui components
- **Language**: TypeScript
- **State**: React Context + localStorage
- **API Client**: Custom fetch-based client

### Backend (Pending)
- **Database**: Supabase (PostgreSQL)
- **Functions**: Supabase Edge Functions (Deno)
- **AI/ML**: Hugging Face Inference API
- **APIs**: Semantic Scholar, arXiv, CrossRef
- **i18n**: Lingo.dev SDK

## Current Status

✅ **Completed:**
- Frontend UI (all 6 modules)
- API client structure
- Authentication flow
- Component library

❌ **Pending:**
- Backend Edge Functions
- AI processing services
- Database schema implementation
- Lingo.dev integration
- DPDP consent dialog

## Quick Start

### Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Backend (Coming Soon)
```bash
cd backend
# Setup instructions TBD
```

## Next Steps

1. Build Supabase Edge Functions
2. Implement AI processing services
3. Add Lingo.dev multilingual support
4. Connect frontend to backend
5. Deploy to production
