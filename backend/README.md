# ARSP Backend

FastAPI backend for the AI-Enabled Research Support Platform.

## Features

- **REST API** with FastAPI
- **AI-Powered** services (BART summarization, semantic search)
- **Clerk Authentication** with JWT verification
- **Supabase** PostgreSQL database and storage
- **Pydantic** data validation
- **Async** operations for better performance

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required environment variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `CLERK_SECRET_KEY` - Clerk secret key
- `HF_API_KEY` - Hugging Face API key (optional but recommended)

### 3. Set Up Database

```bash
python setup_db_auto.py
```

This creates all tables and seeds the journals database.

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

Server runs at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── core/                # Core infrastructure
│   │   ├── config.py        # Settings management
│   │   ├── auth.py          # JWT authentication
│   │   └── supabase.py      # Database client
│   ├── api/v1/              # API endpoints
│   │   ├── topics.py        # Topic discovery
│   │   ├── papers.py        # Paper analysis
│   │   ├── plagiarism.py    # Plagiarism detection
│   │   └── journals.py      # Journal recommendations
│   ├── services/            # Business logic
│   │   ├── topics_service.py
│   │   ├── papers_service.py
│   │   ├── plagiarism_service.py
│   │   ├── journals_service.py
│   │   └── translation_service.py
│   └── schemas/             # Pydantic models
│       ├── topics.py
│       ├── papers.py
│       ├── plagiarism.py
│       └── journals.py
├── tests/                   # Unit tests
├── supabase_setup.sql       # Database schema
├── setup_db_auto.py         # Database setup script
├── requirements.txt
├── render.yml               # Render deployment config
└── README.md
```

## API Endpoints

### Topics
- `GET /api/v1/topics/trending` - Get trending research topics
- `POST /api/v1/topics/personalized` - Get personalized recommendations
- `POST /api/v1/topics/evolution` - Track topic evolution

### Papers
- `POST /api/v1/papers/upload` - Upload PDF for analysis
- `POST /api/v1/papers/{id}/process` - Process paper with AI
- `GET /api/v1/papers/{id}` - Get paper details
- `GET /api/v1/papers/{id}/related` - Find related papers
- `DELETE /api/v1/papers/{id}` - Delete paper

### Plagiarism
- `POST /api/v1/plagiarism/check` - Check text for plagiarism
- `GET /api/v1/plagiarism/report/{id}` - Get plagiarism report
- `GET /api/v1/plagiarism/history` - Get check history

### Journals
- `POST /api/v1/journals/recommend` - Get journal recommendations
- `GET /api/v1/journals/{id}` - Get journal details
- `GET /api/v1/journals/search` - Search journals

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black app/

# Sort imports
isort app/

# Type checking (if mypy is installed)
mypy app/
```

## Deployment

See the main [DEPLOYMENT.md](../DEPLOYMENT.md) for deploying to Render or Railway.

Quick deploy to Render:
```bash
# Push to GitHub
git push origin main

# Render will auto-deploy using render.yml
```

## Environment Variables (Production)

Set these in your deployment platform:

```env
ENVIRONMENT=production
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
CLERK_SECRET_KEY=sk_test_...
HF_API_KEY=hf_...
LINGO_API_KEY=lingo_...
HOST=0.0.0.0
PORT=10000
DEBUG=False
CORS_ORIGINS=https://your-frontend.vercel.app
```

## Troubleshooting

### Port already in use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

### Database connection issues
- Verify Supabase credentials in `.env`
- Check if Supabase project is active
- Ensure RLS policies are set correctly

### Import errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Authentication failures
- Verify Clerk secret key is correct
- Check JWT token is being sent in Authorization header
- Ensure Clerk JWKS endpoint is accessible

## Tech Stack

- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Supabase** - PostgreSQL database and storage
- **Sentence Transformers** - Semantic embeddings
- **Hugging Face** - AI model inference
- **PyPDF2 & pdfplumber** - PDF processing

## External APIs

- **Semantic Scholar** - 230M+ academic papers
- **arXiv** - Preprint repository
- **CrossRef** - Citation metadata
- **Lingo.dev** - Translation service

## License

MIT License - See [LICENSE](../LICENSE) for details.
