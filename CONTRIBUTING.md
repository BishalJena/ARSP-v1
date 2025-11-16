# Contributing to ARSP

Thank you for your interest in contributing to ARSP (AI-Enabled Research Support Platform)! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, browser, Node.js version, Python version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why is this enhancement useful?
- **Proposed solution** (optional)
- **Alternatives considered** (optional)

### Pull Requests

We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

### Prerequisites

- Node.js 18+
- Python 3.10+
- Git

### Setup Steps

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ARSP-v1.git
cd ARSP-v1
```

2. **Set up the backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
```

3. **Set up the frontend**

```bash
cd frontend
npm install
cp .env.example .env.local
# Add your API keys to .env.local
```

4. **Run the development servers**

```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

5. **Create a new branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Pull Request Process

1. **Update documentation** - Update README.md or other docs if needed
2. **Add tests** - Include tests for new functionality
3. **Run tests** - Ensure all tests pass
4. **Lint your code** - Run linters before committing
5. **Update CHANGELOG** - Add your changes to the unreleased section (if applicable)
6. **Create PR** - Submit your pull request with a clear description

### PR Title Format

```
type: brief description

Examples:
feat: add journal impact factor filtering
fix: resolve authentication token expiry issue
docs: update setup guide with troubleshooting
refactor: simplify plagiarism detection algorithm
test: add unit tests for topics service
```

### PR Description Template

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
Describe the tests you ran to verify your changes

## Checklist
- [ ] My code follows the code style of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## Coding Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where applicable
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Write docstrings for functions and classes

```python
def calculate_impact_score(
    citation_count: int,
    publication_date: datetime,
    source_credibility: float
) -> float:
    """
    Calculate research topic impact score.

    Args:
        citation_count: Number of citations
        publication_date: Date of publication
        source_credibility: Source credibility score (0-1)

    Returns:
        Impact score between 0 and 100
    """
    # Implementation
    pass
```

**Tools:**
```bash
# Format code
black app/

# Sort imports
isort app/

# Lint
flake8 app/

# Type check (if mypy installed)
mypy app/
```

### TypeScript/React (Frontend)

- Follow [TypeScript best practices](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html)
- Use functional components with hooks
- Use TypeScript strict mode
- Prefer named exports over default exports
- Use meaningful component and variable names

```typescript
interface PaperAnalysisProps {
  paperId: string;
  onComplete: (result: AnalysisResult) => void;
}

export function PaperAnalysis({ paperId, onComplete }: PaperAnalysisProps) {
  // Implementation
}
```

**Tools:**
```bash
# Lint
npm run lint

# Type check
npm run type-check  # if available

# Format (if prettier installed)
npm run format
```

### General Guidelines

- **Keep it simple** - Prefer simple, readable code over clever code
- **Single Responsibility** - Each function/component should do one thing well
- **DRY** - Don't Repeat Yourself
- **Comments** - Write comments for complex logic, not obvious code
- **Error handling** - Always handle errors gracefully
- **Security** - Never commit API keys or secrets

## Commit Messages

Write clear, descriptive commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Changes to build process or auxiliary tools

### Examples

```bash
feat(plagiarism): add semantic similarity threshold configuration

Allow users to configure the similarity threshold for plagiarism detection.
Default remains at 80% but can now be adjusted between 70-95%.

Closes #123

---

fix(auth): resolve token refresh race condition

Fixed issue where multiple simultaneous requests could trigger
multiple token refresh attempts.

---

docs(setup): add troubleshooting section for common errors

Added solutions for:
- Port already in use
- Database connection errors
- Authentication failures
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage  # if available
```

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for technical/architectural changes
- Update API documentation for endpoint changes
- Add inline comments for complex logic
- Update SETUP.md for setup process changes

## Questions?

Feel free to open an issue for:
- Questions about the codebase
- Clarifications on contribution guidelines
- Feature discussions
- Any other concerns

## License

By contributing to ARSP, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes for significant contributions
- README.md (for major contributions)

Thank you for contributing to ARSP! 🎉
