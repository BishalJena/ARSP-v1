"""Journal recommendation endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ...schemas.journals import (
    JournalRecommendRequest,
    JournalResponse,
    JournalListResponse
)
from ...services.journals_service import journals_service
from ...core.auth import get_current_user

router = APIRouter()


@router.post("/recommend", response_model=JournalListResponse)
async def recommend_journals(
    request: JournalRecommendRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get journal recommendations based on abstract.

    Uses semantic similarity to match abstract with journal descriptions.
    Returns ranked list of journals with fit scores.
    """
    try:
        # Convert preferences to dict
        filters = {}
        if request.preferences:
            filters = {
                "open_access_only": request.preferences.open_access_only,
                "min_impact_factor": request.preferences.min_impact_factor,
                "max_time_to_publish": request.preferences.max_time_to_publish
            }

        journals = await journals_service.recommend_journals(
            abstract=request.abstract,
            keywords=request.keywords,
            filters=filters
        )

        # Format response
        journal_responses = [
            JournalResponse(
                id=str(journal["id"]),
                name=journal["name"],
                description=journal.get("description"),
                impact_factor=float(journal["impact_factor"]),
                h_index=journal.get("h_index"),
                is_open_access=journal["is_open_access"],
                publication_time_months=journal.get("publication_time_months"),
                domain=journal["domain"],
                url=journal.get("url"),
                fit_score=journal.get("fit_score", 0.0)
            )
            for journal in journals
        ]

        return JournalListResponse(
            journals=journal_responses,
            count=len(journal_responses)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get journal recommendations: {str(e)}"
        )


@router.get("/{journal_id}", response_model=JournalResponse)
async def get_journal(
    journal_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get journal details by ID."""
    try:
        journal = await journals_service.get_journal_by_id(journal_id)

        if not journal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Journal not found"
            )

        return JournalResponse(
            id=str(journal["id"]),
            name=journal["name"],
            description=journal.get("description"),
            impact_factor=float(journal["impact_factor"]),
            h_index=journal.get("h_index"),
            is_open_access=journal["is_open_access"],
            publication_time_months=journal.get("publication_time_months"),
            domain=journal["domain"],
            url=journal.get("url"),
            fit_score=0.0  # Not applicable for direct lookup
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get journal: {str(e)}"
        )


@router.get("/search", response_model=JournalListResponse)
async def search_journals(
    query: str,
    discipline: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Search journals by name or description.

    Supports partial text matching.
    """
    try:
        journals = await journals_service.search_journals(
            query=query,
            discipline=discipline
        )

        journal_responses = [
            JournalResponse(
                id=str(journal["id"]),
                name=journal["name"],
                description=journal.get("description"),
                impact_factor=float(journal["impact_factor"]),
                h_index=journal.get("h_index"),
                is_open_access=journal["is_open_access"],
                publication_time_months=journal.get("publication_time_months"),
                domain=journal["domain"],
                url=journal.get("url"),
                fit_score=0.0
            )
            for journal in journals
        ]

        return JournalListResponse(
            journals=journal_responses,
            count=len(journal_responses)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search journals: {str(e)}"
        )
