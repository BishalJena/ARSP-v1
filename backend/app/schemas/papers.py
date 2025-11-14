"""Paper and literature review schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class PaperUploadResponse(BaseModel):
    """Response after paper upload."""
    id: str
    file_name: str
    file_size: int
    upload_url: str
    created_at: datetime


class PaperProcessRequest(BaseModel):
    """Request to process a paper."""
    paper_id: str


class Reference(BaseModel):
    """Citation reference."""
    doi: Optional[str] = None
    title: str
    authors: List[str]
    year: Optional[int] = None
    journal: Optional[str] = None


class LiteratureReviewResponse(BaseModel):
    """Literature review results."""
    id: str
    title: Optional[str] = None
    summary: str
    insights: List[str] = Field(default_factory=list)
    references: List[Reference] = Field(default_factory=list)
    language: str = "en"
    created_at: datetime
    processing_time_seconds: float


class RelatedPaperResponse(BaseModel):
    """Related paper recommendation."""
    title: str
    authors: List[str]
    year: Optional[int]
    abstract: Optional[str]
    url: Optional[str]
    similarity_score: float
