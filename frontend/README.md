# ARSP Frontend

Next.js frontend for the AI-Enabled Research Support Platform.

## Features

- **Next.js 16** with App Router
- **React 19** Server Components
- **TypeScript** for type safety
- **Tailwind CSS 4** for styling
- **shadcn/ui** component library
- **Clerk** authentication
- **Lingo.dev** multilingual support (15 languages)
- **Supabase** client for data access

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env.local
# Edit .env.local and add your API keys
```

Required environment variables:
- `NEXT_PUBLIC_API_URL` - Backend API URL (http://localhost:8000/api/v1)
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anon key
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - Clerk publishable key
- `CLERK_SECRET_KEY` - Clerk secret key
- `NEXT_PUBLIC_LINGO_API_KEY` - Lingo.dev API key

### 3. Run Development Server

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

## Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with providers
│   ├── page.tsx                 # Landing page
│   ├── dashboard/               # Protected routes
│   │   ├── page.tsx            # Dashboard home
│   │   ├── topics/             # Topic discovery
│   │   ├── papers/             # Paper analysis
│   │   ├── plagiarism/         # Plagiarism checker
│   │   ├── journals/           # Journal recommendations
│   │   ├── government/         # Government alignment
│   │   └── impact/             # Impact prediction
│   └── auth/                    # Authentication pages
├── components/                  # React components
│   ├── dashboard-layout.tsx    # Dashboard wrapper
│   ├── language-selector.tsx   # Language switcher
│   ├── consent-dialog.tsx      # DPDP consent
│   └── ui/                     # shadcn/ui components
├── lib/                         # Utilities and hooks
│   ├── api-client.ts           # Unauthenticated API client
│   ├── api-client-auth.ts      # Authenticated API client
│   ├── auth-context.tsx        # Clerk auth wrapper
│   ├── useLingo.tsx            # Translation hook
│   ├── supabase.ts             # Supabase client
│   └── utils.ts                # Helper functions
├── locales/                     # Translation files (15 languages)
│   ├── en.json
│   ├── hi.json, te.json, ta.json, bn.json, mr.json
│   ├── zh.json, es.json, fr.json, de.json, pt.json
│   └── ja.json, ko.json
├── public/                      # Static assets
├── middleware.ts                # Route protection
├── next.config.ts               # Next.js configuration
├── tailwind.config.ts           # Tailwind configuration
├── vercel.json                  # Vercel deployment config
└── package.json
```

## Available Scripts

```bash
# Development
npm run dev              # Start dev server

# Production
npm run build            # Build for production
npm start                # Start production server

# Linting
npm run lint             # Run ESLint
```

## Features Guide

### 1. Topic Discovery (`/dashboard/topics`)
- Search trending research topics
- Filter by field and timeframe
- View impact scores
- Explore topic evolution

### 2. Paper Analysis (`/dashboard/papers`)
- Upload PDF research papers
- AI-powered summarization
- Extract key insights
- Find related papers

### 3. Plagiarism Detection (`/dashboard/plagiarism`)
- Paste or upload text
- Semantic similarity detection
- Originality score
- Citation suggestions

### 4. Journal Recommendations (`/dashboard/journals`)
- Enter research abstract
- Get matched journals
- Filter by impact factor, open access
- View fit scores

### 5. Language Support
- 15 languages supported
- Dynamic language switching
- Context-aware translations
- Persistent language preference

## Multilingual Support

Supported languages:
- English, Hindi, Telugu, Tamil, Bengali, Marathi
- Chinese (Simplified), Japanese, Korean
- Spanish, French, German, Portuguese
- Russian (via Lingo.dev)

Translation files are in `locales/` folder. To generate translations:

```bash
npx lingo translate
```

## Authentication Flow

1. User clicks "Sign In" → Clerk modal
2. User authenticates (email/OAuth)
3. Clerk issues JWT token
4. Token included in API requests
5. Backend verifies token
6. User accesses protected routes

## Deployment

### Deploy to Vercel

1. Push to GitHub
2. Import project in Vercel
3. Set root directory to `frontend`
4. Add environment variables
5. Deploy!

See [DEPLOYMENT.md](../DEPLOYMENT.md) for detailed instructions.

### Environment Variables (Production)

```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_LINGO_API_KEY=lingo_...
```

## Component Library

This project uses **shadcn/ui** components. To add new components:

```bash
npx shadcn-ui@latest add [component-name]
```

Available components are in `components/ui/`.

## API Client Usage

### Unauthenticated Requests

```typescript
import { getAPI } from '@/lib/api-client';

const api = getAPI();
const topics = await api.getTrendingTopics();
```

### Authenticated Requests

```typescript
import { useAuthenticatedAPI } from '@/lib/api-client-auth';

function MyComponent() {
  const api = useAuthenticatedAPI();

  const handleUpload = async () => {
    const result = await api.uploadPaper(file);
  };
}
```

## Troubleshooting

### Build Errors

```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### Authentication Issues

- Verify Clerk keys in `.env.local`
- Check Clerk dashboard for correct domain
- Clear cookies and try again

### API Connection Issues

- Verify `NEXT_PUBLIC_API_URL` is correct
- Ensure backend is running
- Check browser console for CORS errors

### Translation Errors

- Run `npx lingo translate` to generate files
- Verify Lingo.dev API key
- Check `i18n.config.json` configuration

## Tech Stack

- **Next.js 16** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Styling
- **shadcn/ui** - Component library
- **Clerk** - Authentication
- **Lingo.dev** - Translations
- **Supabase** - Database client
- **Radix UI** - Accessible primitives

## Development Tips

- Use React DevTools for debugging
- Check Network tab for API issues
- Use `console.log` sparingly, prefer debugger
- Test in multiple browsers
- Test all language translations
- Verify mobile responsiveness

## License

MIT License - See [LICENSE](../LICENSE) for details.
