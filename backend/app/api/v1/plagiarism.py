"""Plagiarism detection endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from ...schemas.plagiarism import (
    PlagiarismCheckRequest,
    PlagiarismCheckResponse,
    CitationSuggestion
)
from ...services.plagiarism_service import plagiarism_service
from ...services.semantic_scholar_service import semantic_scholar_service
from ...services.translation_service import translation_service
from ...core.auth import get_current_user_optional
from ...core.supabase import supabase

router = APIRouter()


class CitationSuggestRequest(BaseModel):
    """Citation suggestion request."""
    claims: List[str]


@router.post("/check", response_model=PlagiarismCheckResponse)
async def check_plagiarism(
    request: PlagiarismCheckRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Check text for plagiarism using semantic similarity.

    Uses Sentence Transformers to detect paraphrased content.
    Returns originality score, flagged sections, and citation suggestions.
    """
    try:
        # Translate text to English if needed (for accurate plagiarism detection)
        text_to_check = request.text
        if request.language and request.language != "en":
            text_to_check = await translation_service.translate_text(
                request.text,
                target_language="en",
                source_language=request.language
            )

        # Use Semantic Scholar hybrid detection for better accuracy
        result = await semantic_scholar_service.detect_plagiarism_hybrid(
            text=text_to_check,
            check_online=request.check_online if request.check_online is not None else True
        )

        # Translate flagged sections back to user's language if needed
        if request.language and request.language != "en" and result.get("flagged_sections"):
            sections_text = [section["text"] for section in result["flagged_sections"]]
            if sections_text:
                translated_sections = await translation_service.translate_batch(
                    sections_text,
                    target_language=request.language,
                    source_language="en"
                )
                for i, section in enumerate(result["flagged_sections"]):
                    if i < len(translated_sections):
                        section["text"] = translated_sections[i]

        # Store result in database (for history) - only if user is logged in
        if current_user:
            user_id = current_user["user_id"]

            # Check if draft exists, update or create
            draft_result = supabase.table("drafts").select("id").eq("user_id", user_id).limit(1).execute()

            draft_data = {
                "user_id": user_id,
                "content": request.text,
                "plagiarism_score": result["originality_score"],
                "last_checked_at": result["checked_at"]
            }

            if draft_result.data:
                # Update existing draft
                supabase.table("drafts").update(draft_data).eq("id", draft_result.data[0]["id"]).execute()
            else:
                # Create new draft
                supabase.table("drafts").insert(draft_data).execute()

        return PlagiarismCheckResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Plagiarism check failed: {str(e)}"
        )


@router.get("/report/{report_id}")
async def get_plagiarism_report(
    report_id: str,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get a plagiarism report by ID."""
    user_id = current_user["user_id"] if current_user else "demo_user"

    result = supabase.table("drafts").select("*").eq("id", report_id).eq("user_id", user_id).single().execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return result.data


@router.get("/history")
async def get_plagiarism_history(
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get plagiarism check history for current user."""
    user_id = current_user["user_id"] if current_user else "demo_user"

    result = supabase.table("drafts").select("*").eq("user_id", user_id).order("last_checked_at", desc=True).execute()

    return {"history": result.data or [], "count": len(result.data or [])}


@router.post("/citations/suggest", response_model=List[CitationSuggestion])
async def suggest_citations(
    request: CitationSuggestRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get citation suggestions for claims.

    Uses CrossRef API to find relevant papers.
    """
    try:
        # Combine all claims into one text
        combined_text = " ".join(request.claims)

        # Get citations
        citations = await plagiarism_service._get_citation_suggestions(combined_text)

        return [CitationSuggestion(**citation) for citation in citations]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get citation suggestions: {str(e)}"
        )
