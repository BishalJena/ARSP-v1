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
    Check text, file, or website for plagiarism.

    **Winston AI (Recommended - use_winston=true)**:
    - Internet-wide plagiarism detection
    - 45+ language support with auto-detection
    - Supports text, file URLs, and websites
    - Attack detection (zero-width spaces, homoglyphs)
    - Detailed source attribution with snippets
    - Citation detection

    **Legacy (use_winston=false)**:
    - Academic paper comparison via Semantic Scholar
    - Sentence Transformers semantic similarity
    - Limited language support

    **Priority**: website > file_url > text

    **Limits**:
    - Text: 100-120,000 characters
    - Files: PDF, DOC, DOCX (must be publicly accessible)
    """
    try:
        # Validate that at least one input is provided
        if not request.text and not request.file_url and not request.website:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one of text, file_url, or website must be provided"
            )

        # Use Winston AI enhanced detection (recommended)
        if request.use_winston:
            result = await plagiarism_service.check_plagiarism_enhanced(
                text=request.text,
                file_url=request.file_url,
                website=request.website,
                excluded_sources=request.excluded_sources,
                language=request.language or "auto",
                country=request.country or "us",
                use_winston=True
            )

            # Translate Winston AI results to user's language if needed
            if request.language and request.language not in ["en", "auto"]:
                # Translate source titles and snippets
                if result.get("sources"):
                    titles = [s["title"] for s in result["sources"] if s.get("title")]
                    snippets = [s["snippet"] for s in result["sources"] if s.get("snippet")]

                    if titles:
                        translated_titles = await translation_service.translate_batch(
                            titles,
                            target_language=request.language,
                            source_language="en"
                        )
                        # Map back to sources
                        title_idx = 0
                        for source in result["sources"]:
                            if source.get("title"):
                                source["title"] = translated_titles[title_idx]
                                title_idx += 1

                    if snippets:
                        translated_snippets = await translation_service.translate_batch(
                            snippets,
                            target_language=request.language,
                            source_language="en"
                        )
                        # Map back to sources
                        snippet_idx = 0
                        for source in result["sources"]:
                            if source.get("snippet"):
                                source["snippet"] = translated_snippets[snippet_idx]
                                snippet_idx += 1

                # Translate flagged section texts and snippets
                if result.get("flagged_sections"):
                    texts = [s["text"] for s in result["flagged_sections"] if s.get("text")]
                    sources = [s["source"] for s in result["flagged_sections"] if s.get("source")]
                    snippets = [s["snippet"] for s in result["flagged_sections"] if s.get("snippet")]

                    if texts:
                        translated_texts = await translation_service.translate_batch(
                            texts,
                            target_language=request.language,
                            source_language="en"
                        )
                        text_idx = 0
                        for section in result["flagged_sections"]:
                            if section.get("text"):
                                section["text"] = translated_texts[text_idx]
                                text_idx += 1

                    if sources:
                        translated_sources = await translation_service.translate_batch(
                            sources,
                            target_language=request.language,
                            source_language="en"
                        )
                        source_idx = 0
                        for section in result["flagged_sections"]:
                            if section.get("source"):
                                section["source"] = translated_sources[source_idx]
                                source_idx += 1

                    if snippets:
                        translated_snippets = await translation_service.translate_batch(
                            snippets,
                            target_language=request.language,
                            source_language="en"
                        )
                        snippet_idx = 0
                        for section in result["flagged_sections"]:
                            if section.get("snippet"):
                                section["snippet"] = translated_snippets[snippet_idx]
                                snippet_idx += 1
        else:
            # Legacy method - requires text
            if not request.text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Text is required when use_winston=false"
                )

            # Translate text to English if needed (for accurate plagiarism detection)
            text_to_check = request.text
            if request.language and request.language not in ["en", "auto"]:
                text_to_check = await translation_service.translate_text(
                    request.text,
                    target_language="en",
                    source_language=request.language
                )

            # Use legacy Semantic Scholar hybrid detection
            result = await semantic_scholar_service.detect_plagiarism_hybrid(
                text=text_to_check,
                check_online=request.check_online if request.check_online is not None else True
            )

            # Translate flagged sections back to user's language if needed
            if request.language and request.language not in ["en", "auto"] and result.get("flagged_sections"):
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
        if current_user and request.text:  # Only store text checks (not file/website)
            user_id = current_user["user_id"]

            # Check if draft exists, update or create
            draft_result = supabase.table("drafts").select("id").eq("user_id", user_id).limit(1).execute()

            draft_data = {
                "user_id": user_id,
                "content": request.text[:50000],  # Limit stored content
                "plagiarism_score": result.get("originality_score", 0),
                "last_checked_at": result["checked_at"]
            }

            if draft_result.data:
                # Update existing draft
                supabase.table("drafts").update(draft_data).eq("id", draft_result.data[0]["id"]).execute()
            else:
                # Create new draft
                supabase.table("drafts").insert(draft_data).execute()

        return PlagiarismCheckResponse(**result)

    except HTTPException:
        raise  # Re-raise HTTP exceptions
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
