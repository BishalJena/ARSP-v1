"""Pydantic schemas for request/response validation."""
from .topics import TopicQuery, TopicResponse, TopicListResponse
from .papers import PaperUploadResponse, PaperProcessRequest, LiteratureReviewResponse
from .plagiarism import PlagiarismCheckRequest, PlagiarismCheckResponse
from .journals import JournalRecommendRequest, JournalResponse, JournalListResponse

__all__ = [
    "TopicQuery",
    "TopicResponse",
    "TopicListResponse",
    "PaperUploadResponse",
    "PaperProcessRequest",
    "LiteratureReviewResponse",
    "PlagiarismCheckRequest",
    "PlagiarismCheckResponse",
    "JournalRecommendRequest",
    "JournalResponse",
    "JournalListResponse",
]
