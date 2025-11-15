"""Topic-related schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional


class TopicQuery(BaseModel):
    """Topic search query."""
    query: str = Field(..., min_length=3, max_length=200, description="Search query")
    discipline: Optional[str] = Field(None, description="Academic discipline filter")
    limit: Optional[int] = Field(5, ge=1, le=20, description="Number of results")


class TopicResponse(BaseModel):
    """Individual topic response."""
    id: str
    title: str
    description: str
    impact_score: float = Field(..., ge=0)  # No upper limit - can be based on citation counts
    source: str  # 'semantic_scholar' or 'arxiv'
    url: Optional[str] = None
    citation_count: Optional[int] = None
    year: Optional[int] = None


class TopicListResponse(BaseModel):
    """List of topics."""
    topics: List[TopicResponse]
    count: int
