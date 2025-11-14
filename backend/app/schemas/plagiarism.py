"""Plagiarism detection schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PlagiarismCheckRequest(BaseModel):
    """Plagiarism check request."""
    text: str = Field(..., min_length=10, max_length=50000)
    language: Optional[str] = Field("en", description="Text language code")
    check_online: Optional[bool] = Field(True, description="Check against online sources")


class FlaggedSection(BaseModel):
    """Flagged plagiarized section."""
    text: str
    start_index: int
    end_index: int
    similarity: float = Field(..., ge=0, le=100)
    source: Optional[str] = None
    source_url: Optional[str] = None


class CitationSuggestion(BaseModel):
    """Citation suggestion."""
    doi: str
    title: str
    authors: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    relevance: float = Field(..., ge=0, le=1)


class PlagiarismCheckResponse(BaseModel):
    """Plagiarism check result."""
    originality_score: float = Field(..., ge=0, le=100)
    flagged_sections: List[FlaggedSection] = Field(default_factory=list)
    citations: List[CitationSuggestion] = Field(default_factory=list)
    checked_at: datetime
    processing_time_seconds: float
