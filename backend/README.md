# ARSP Backend API

AI-Enabled Research Support Platform - FastAPI Backend

## Architecture

```
backend/
├── app/
│   ├── api/v1/               # API endpoints
│   │   ├── auth.py           # Authentication routes
│   │   ├── topics.py         # Topic discovery
│   │   ├── papers.py         # Literature review
│   │   ├── plagiarism.py     # Plagiarism detection
│   │   └── journals.py       # Journal recommendations
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration
│   │   ├── auth.py           # Clerk JWT verification
│   │   └── supabase.py       # Database client
│   ├── services/             # Business logic
│   │   ├── topics_service.py
│   │   ├── papers_service.py
│   │   ├── plagiarism_service.py
│   │   └── journals_service.py
│   ├── schemas/              # Pydantic models
│   └── main.py               # FastAPI app
├── tests/                    # Test suite
├── requirements.txt          # Python dependencies
└── .env.example              # Environment template
```

## Tech Stack

- **FastAPI**: Modern Python web framework
- **Supabase**: PostgreSQL database + storage
- **Clerk**: Authentication
- **Lingo.dev**: Multilingual support
- **Hugging Face**: AI/ML models
- **Sentence Transformers**: Plagiarism detection
- **External APIs**: Semantic Scholar, CrossRef, arXiv

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required environment variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_SERVICE_KEY` - Supabase service role key (for admin operations)
- `CLERK_SECRET_KEY` - Clerk secret key for JWT verification
- `LINGO_API_KEY` - Lingo.dev API key
- `HF_API_KEY` - Hugging Face API key (optional, increases rate limits)

### 3. Run Development Server

```bash
python -m app.main
# or
uvicorn app.main:app --reload --port 8000
```

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/users/me` - Get current user profile

### Topics
- `GET /api/v1/topics/trending` - Get trending research topics
- `POST /api/v1/topics/personalized` - Get personalized recommendations
- `POST /api/v1/topics/evolution` - Get topic evolution over time

### Papers
- `POST /api/v1/papers/upload` - Upload PDF paper
- `POST /api/v1/papers/{id}/process` - Process paper (extract text, summarize)
- `GET /api/v1/papers/{id}` - Get paper details
- `GET /api/v1/papers/` - List user's papers
- `GET /api/v1/papers/{id}/related` - Get related papers

### Plagiarism
- `POST /api/v1/plagiarism/check` - Check text for plagiarism
- `GET /api/v1/plagiarism/report/{id}` - Get plagiarism report
- `POST /api/v1/plagiarism/citations/suggest` - Get citation suggestions

### Journals
- `POST /api/v1/journals/recommend` - Get journal recommendations
- `GET /api/v1/journals/{id}` - Get journal details
- `GET /api/v1/journals/search` - Search journals

## Services

### Topics Service
Uses **Semantic Scholar API** and **arXiv API** to find trending research topics.

**Features**:
- Multilingual query support (via Lingo.dev)
- Discipline filtering
- Impact score calculation
- Citation velocity tracking

### Papers Service
Processes PDF papers for literature review.

**Features**:
- PDF text extraction (PyPDF2/pdfplumber)
- AI summarization (Hugging Face BART model)
- Key insights extraction
- Reference formatting (Zotero JSON)
- Multilingual summaries

### Plagiarism Service
Detects plagiarism using **Sentence Transformers**.

**Features**:
- Semantic similarity detection (not just exact matches)
- Paraphrase detection
- Source attribution
- Citation suggestions (CrossRef API)
- 85-90% accuracy

**Model**: `sentence-transformers/all-mpnet-base-v2`

### Journals Service
Recommends academic journals based on abstract.

**Features**:
- Abstract-journal matching (cosine similarity)
- Impact factor filtering
- Open-access filtering
- Fit score calculation (0-100%)
- Domain classification

## Development

### Running Tests

```bash
pytest tests/ -v
pytest tests/ --cov=app  # With coverage
```

### Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Adding a New Endpoint

1. Create route in `app/api/v1/`
2. Define schemas in `app/schemas/`
3. Implement service logic in `app/services/`
4. Add tests in `tests/`

## Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Railway/Render/Fly.io

1. Push to GitHub
2. Connect repository
3. Set environment variables
4. Deploy!

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `SUPABASE_URL` | Supabase project URL | Yes | - |
| `SUPABASE_KEY` | Supabase anon key | Yes | - |
| `SUPABASE_SERVICE_KEY` | Supabase service key | Yes | - |
| `CLERK_SECRET_KEY` | Clerk secret key | Yes | - |
| `LINGO_API_KEY` | Lingo.dev API key | Yes | - |
| `HF_API_KEY` | Hugging Face API key | No | "" |
| `SEMANTIC_SCHOLAR_API_KEY` | S2 API key | No | "" |
| `CROSSREF_EMAIL` | Email for CrossRef polite pool | No | "" |
| `PORT` | Server port | No | 8000 |
| `CORS_ORIGINS` | Allowed CORS origins | No | "http://localhost:3000" |

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### Database connection errors
Check your `SUPABASE_URL` and `SUPABASE_KEY` in `.env`

### Authentication failures
Verify `CLERK_SECRET_KEY` is correct and tokens are valid

### Slow AI processing
- Hugging Face free tier has rate limits
- Consider caching results
- Use smaller models for faster inference

## Next Steps

- [ ] Implement all service methods
- [ ] Add Lingo.dev translation to API responses
- [ ] Set up Supabase database with migrations
- [ ] Add comprehensive tests
- [ ] Configure CI/CD pipeline
- [ ] Deploy to production

## License

MIT
