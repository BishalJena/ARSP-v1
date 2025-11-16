"""Services layer for business logic."""
from .topics_service import topics_service
# Legacy papers_service removed - using papers_service_v2 with Gemini instead
from .plagiarism_service import plagiarism_service
from .journals_service import journals_service
from .translation_service import translation_service

__all__ = [
    "topics_service",
    "papers_service",
    "plagiarism_service",
    "journals_service",
    "translation_service",
]
