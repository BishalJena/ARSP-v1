"""Pydantic schemas for request/response validation."""
from .topics import TopicQuery, TopicResponse, TopicListResponse
# Legacy paper schemas removed - using papers_v2 schemas with Gemini instead
from .plagiarism import PlagiarismCheckRequest, PlagiarismCheckResponse
from .journals import JournalRecommendRequest, JournalResponse, JournalListResponse

__all__ = [
    "TopicQuery",
    "TopicResponse",
    "TopicListResponse",
    "PlagiarismCheckRequest",
    "PlagiarismCheckResponse",
    "JournalRecommendRequest",
    "JournalResponse",
    "JournalListResponse",
]
