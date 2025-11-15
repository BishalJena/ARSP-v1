"""Journal recommendation endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from ...schemas.journals import (
    JournalRecommendRequest,
    JournalResponse,
    JournalListResponse
)
from ...services.journals_service import journals_service
from ...services.semantic_scholar_service import semantic_scholar_service
from ...services.translation_service import translation_service
from ...core.auth import get_current_user_optional, get_current_user

router = APIRouter()


@router.post("/recommend", response_model=JournalListResponse)
async def recommend_journals(
    request: JournalRecommendRequest,
    language: Optional[str] = "en",
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get journal recommendations based on abstract.

    Uses semantic similarity to match abstract with journal descriptions.
    Returns ranked list of journals with fit scores.
    Supports translation to user's preferred language.
    """
    try:
        # Translate abstract and keywords to English if needed
        abstract_to_process = request.abstract
        keywords_to_process = request.keywords

        if language and language != "en":
            # Translate abstract
            abstract_to_process = await translation_service.translate_text(
                request.abstract,
                target_language="en",
                source_language=language
            )

            # Translate keywords
            if request.keywords:
                keywords_to_process = await translation_service.translate_batch(
                    request.keywords,
                    target_language="en",
                    source_language=language
                )

        # Convert preferences to dict
        filters = {}
        if request.preferences:
            filters = {
                "open_access_only": request.preferences.open_access_only,
                "min_impact_factor": request.preferences.min_impact_factor,
                "max_time_to_publish": request.preferences.max_time_to_publish
            }

        # First get journals from database with filters
        journals_db = await journals_service._get_journals_from_db(filters)

        # Then use Semantic Scholar hybrid ranking for better recommendations
        journals = await semantic_scholar_service.recommend_journals_hybrid(
            abstract=abstract_to_process,
            keywords=keywords_to_process,
            journals_db=journals_db
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

        # Translate results if needed
        if language and language != "en":
            journals_dict = [journal.model_dump() for journal in journal_responses]
            translated_journals = await translation_service.translate_results(
                journals_dict,
                target_language=language,
                fields=["name", "description"]
            )
            journal_responses = [JournalResponse(**journal) for journal in translated_journals]

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
    current_user: Optional[dict] = Depends(get_current_user_optional)
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
    language: Optional[str] = "en",
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Search journals by name or description.

    Supports partial text matching and translation.
    """
    try:
        # Translate query and discipline to English if needed
        query_to_search = query
        discipline_to_search = discipline

        if language and language != "en":
            query_to_search = await translation_service.translate_query(
                query,
                target_language="en",
                source_language=language
            )
            if discipline:
                discipline_to_search = await translation_service.translate_query(
                    discipline,
                    target_language="en",
                    source_language=language
                )

        journals = await journals_service.search_journals(
            query=query_to_search,
            discipline=discipline_to_search
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

        # Translate results if needed
        if language and language != "en":
            journals_dict = [journal.model_dump() for journal in journal_responses]
            translated_journals = await translation_service.translate_results(
                journals_dict,
                target_language=language,
                fields=["name", "description"]
            )
            journal_responses = [JournalResponse(**journal) for journal in translated_journals]

        return JournalListResponse(
            journals=journal_responses,
            count=len(journal_responses)
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search journals: {str(e)}"
        )
