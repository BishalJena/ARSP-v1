"""Plagiarism detection schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PlagiarismCheckRequest(BaseModel):
    """Plagiarism check request."""
    text: Optional[str] = Field(None, min_length=100, max_length=120000, description="Text to check (100-120,000 chars)")
    file_url: Optional[str] = Field(None, description="URL to publicly accessible PDF/DOC/DOCX file")
    website: Optional[str] = Field(None, description="Website URL to scan")
    excluded_sources: Optional[List[str]] = Field(None, description="Domains/URLs to exclude from scan")
    language: Optional[str] = Field("auto", description="2-letter language code or 'auto'")
    country: Optional[str] = Field("us", description="Country code")
    check_online: Optional[bool] = Field(True, description="Check against online sources (legacy)")
    use_winston: Optional[bool] = Field(True, description="Use Winston AI (recommended) vs legacy Sentence Transformers")


class FlaggedSection(BaseModel):
    """Flagged plagiarized section."""
    text: str
    start_index: int
    end_index: int
    similarity: float = Field(..., ge=0, le=100)
    source: Optional[str] = None
    source_url: Optional[str] = None
    snippet: Optional[str] = None  # Winston AI: matching snippet from source


class CitationSuggestion(BaseModel):
    """Citation suggestion."""
    doi: str
    title: str
    authors: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    relevance: float = Field(..., ge=0, le=1)


class DetailedSource(BaseModel):
    """Detailed plagiarism source information (Winston AI)."""
    url: str
    title: str
    snippet: str
    plagiarism_score: float = Field(..., ge=0, le=100)
    word_count: int
    matched_words: int


class SimilarWord(BaseModel):
    """Similar word found in multiple sources (Winston AI)."""
    word: str
    frequency: int
    sources: List[str] = Field(default_factory=list)


class PlagiarismIndex(BaseModel):
    """Exact plagiarism match index (Winston AI)."""
    text: str
    start_index: int
    end_index: int
    url: str
    plagiarism_score: float = Field(..., ge=0, le=100)


class AttackDetection(BaseModel):
    """Attack detection results (Winston AI)."""
    zero_width_spaces: bool = False
    homoglyph_attack: bool = False


class ScanInfo(BaseModel):
    """Scan information (Winston AI)."""
    word_count: int
    character_count: int
    language_detected: str
    sources_checked: int


class PlagiarismCheckResponse(BaseModel):
    """Plagiarism check result."""
    # Core metrics
    originality_score: float = Field(..., ge=0, le=100)
    plagiarism_score: Optional[float] = Field(None, ge=0, le=100)

    # Flagged content
    flagged_sections: List[FlaggedSection] = Field(default_factory=list)

    # Citations (legacy)
    citations: List[CitationSuggestion] = Field(default_factory=list)

    # Winston AI enhanced fields
    sources: Optional[List[DetailedSource]] = Field(None, description="Detailed source information")
    similar_words: Optional[List[SimilarWord]] = Field(None, description="Similar words analysis")
    indexes: Optional[List[PlagiarismIndex]] = Field(None, description="Exact match indexes")
    attack_detected: Optional[AttackDetection] = Field(None, description="Attack detection results")
    scan_info: Optional[ScanInfo] = Field(None, description="Scan metadata")

    # Word count analysis
    total_word_count: Optional[int] = None
    plagiarized_word_count: Optional[int] = None
    total_text_score: Optional[float] = None

    # Credits (Winston AI)
    credits_used: Optional[int] = None
    credits_remaining: Optional[int] = None

    # Metadata
    checked_at: datetime
    processing_time_seconds: float
    provider: Optional[str] = Field(None, description="Detection provider: winston_ai or legacy")
