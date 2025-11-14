"""Journal recommendation schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional


class JournalFilters(BaseModel):
    """Journal recommendation filters."""
    open_access_only: Optional[bool] = False
    min_impact_factor: Optional[float] = Field(None, ge=0)
    max_time_to_publish: Optional[int] = Field(None, ge=1)  # months


class JournalRecommendRequest(BaseModel):
    """Journal recommendation request."""
    abstract: str = Field(..., min_length=50, max_length=5000)
    keywords: List[str] = Field(default_factory=list)
    preferences: Optional[JournalFilters] = Field(default_factory=JournalFilters)


class JournalResponse(BaseModel):
    """Individual journal response."""
    id: str
    name: str
    description: Optional[str] = None
    impact_factor: float
    h_index: Optional[int] = None
    is_open_access: bool
    publication_time_months: Optional[int] = None
    domain: str
    url: Optional[str] = None
    fit_score: float = Field(..., ge=0, le=100, description="Content alignment score")


class JournalListResponse(BaseModel):
    """List of journal recommendations."""
    journals: List[JournalResponse]
    count: int
