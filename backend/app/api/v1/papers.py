"""Papers and literature review endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List, Optional
from datetime import datetime
from ...schemas.papers import (
    PaperUploadResponse,
    LiteratureReviewResponse,
    RelatedPaperResponse
)
from ...services.papers_service import papers_service
from ...services.translation_service import translation_service
from ...core.auth import get_current_user_optional
from ...core.supabase import supabase

router = APIRouter()


@router.post("/upload", response_model=PaperUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Upload a research paper (PDF).

    Stores the file in Supabase Storage and creates a database record.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )

    # Validate file size (10MB limit)
    content = await file.read()
    file_size = len(content)

    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must be less than 10MB"
        )

    try:
        # Use demo user if not authenticated
        user_id = current_user["user_id"] if current_user else "demo_user"

        # Process the PDF immediately instead of storing
        analysis = await papers_service.process_paper_content(content, file.filename)

        # Create database record with analysis
        upload_data = {
            "user_id": user_id,
            "file_name": file.filename,
            "file_path": f"processed/{file.filename}",  # Virtual path
            "file_size": file_size,
            "mime_type": "application/pdf",
            "processed": True,
            "summary": analysis.get("summary", ""),
            "methodology": analysis.get("methodology", ""),
            "key_findings": analysis.get("insights", [])
        }

        db_result = supabase.table("uploads").insert(upload_data).execute()

        if not db_result.data:
            raise Exception("Failed to create database record")

        upload_record = db_result.data[0]

        return PaperUploadResponse(
            id=upload_record["id"],
            file_name=file.filename,
            file_size=file_size,
            upload_url=f"/api/v1/papers/{upload_record['id']}",
            created_at=upload_record["created_at"]
        )

    except Exception as e:
        import traceback
        print(f"Upload error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload paper: {str(e)}"
        )


@router.post("/{paper_id}/process", response_model=LiteratureReviewResponse)
async def process_paper(
    paper_id: str,
    language: Optional[str] = "en",
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Process a paper to generate literature review.

    Extracts text, generates summary, identifies insights, and extracts references.
    Supports translation to user's preferred language.
    """
    try:
        user_id = current_user["user_id"] if current_user else "demo_user"

        # Get paper details from database
        result = supabase.table("uploads").select("*").eq("id", paper_id).eq("user_id", user_id).single().execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paper not found"
            )

        paper = result.data

        # Download file from storage
        file_content = supabase.storage.from_("papers").download(paper["file_path"])

        # Process the paper (always in English)
        review = await papers_service.process_paper(
            paper_id=paper_id,
            user_id=user_id,
            pdf_content=file_content
        )

        # Translate results if needed
        if language and language != "en":
            # Translate title, summary, and insights
            texts_to_translate = []
            if review.get("title"):
                texts_to_translate.append(review["title"])
            texts_to_translate.append(review["summary"])
            texts_to_translate.extend(review.get("insights", []))

            if texts_to_translate:
                translated_texts = await translation_service.translate_batch(
                    texts_to_translate,
                    target_language=language,
                    source_language="en"
                )

                # Update review with translated texts
                idx = 0
                if review.get("title"):
                    review["title"] = translated_texts[idx]
                    idx += 1
                review["summary"] = translated_texts[idx]
                idx += 1
                if review.get("insights"):
                    review["insights"] = translated_texts[idx:]

            # Translate reference titles
            if review.get("references"):
                ref_titles = [ref["title"] for ref in review["references"]]
                if ref_titles:
                    translated_titles = await translation_service.translate_batch(
                        ref_titles,
                        target_language=language,
                        source_language="en"
                    )
                    for i, ref in enumerate(review["references"]):
                        if i < len(translated_titles):
                            ref["title"] = translated_titles[i]

            # Update language field
            review["language"] = language

        return LiteratureReviewResponse(**review)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process paper: {str(e)}"
        )


@router.get("/{paper_id}")
async def get_paper(
    paper_id: str,
    language: Optional[str] = "en",
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Get paper details with optional translation."""
    user_id = current_user["user_id"] if current_user else "demo_user"

    result = supabase.table("uploads").select("*").eq("id", paper_id).eq("user_id", user_id).single().execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )

    paper = result.data

    # Translate if needed
    if language and language != "en" and paper.get("processed"):
        texts_to_translate = []

        # Add paper title
        if paper.get("paper_title"):
            texts_to_translate.append(paper["paper_title"])

        if paper.get("summary"):
            texts_to_translate.append(paper["summary"])
        if paper.get("methodology"):
            texts_to_translate.append(paper["methodology"])

        # Add insights
        if paper.get("key_findings"):
            texts_to_translate.extend(paper["key_findings"])

        if texts_to_translate:
            translated = await translation_service.translate_batch(
                texts_to_translate,
                target_language=language,
                source_language="en"
            )

            idx = 0
            if paper.get("paper_title"):
                paper["paper_title"] = translated[idx]
                idx += 1
            if paper.get("summary"):
                paper["summary"] = translated[idx]
                idx += 1
            if paper.get("methodology"):
                paper["methodology"] = translated[idx]
                idx += 1
            if paper.get("key_findings"):
                paper["key_findings"] = translated[idx:]

    return paper


@router.get("/")
async def list_papers(
    language: Optional[str] = "en",
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """List all papers for the current user with optional translation."""
    user_id = current_user["user_id"] if current_user else "demo_user"

    result = supabase.table("uploads").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

    papers = result.data or []

    # Translate all papers if needed
    if language and language != "en" and papers:
        for paper in papers:
            if paper.get("processed"):
                texts_to_translate = []

                # Add paper title
                if paper.get("paper_title"):
                    texts_to_translate.append(paper["paper_title"])

                if paper.get("summary"):
                    texts_to_translate.append(paper["summary"])
                if paper.get("methodology"):
                    texts_to_translate.append(paper["methodology"])

                # Add insights
                if paper.get("key_findings"):
                    texts_to_translate.extend(paper["key_findings"])

                if texts_to_translate:
                    translated = await translation_service.translate_batch(
                        texts_to_translate,
                        target_language=language,
                        source_language="en"
                    )

                    idx = 0
                    if paper.get("paper_title"):
                        paper["paper_title"] = translated[idx]
                        idx += 1
                    if paper.get("summary"):
                        paper["summary"] = translated[idx]
                        idx += 1
                    if paper.get("methodology"):
                        paper["methodology"] = translated[idx]
                        idx += 1
                    if paper.get("key_findings"):
                        paper["key_findings"] = translated[idx:]

    return {"papers": papers, "count": len(papers)}


@router.get("/{paper_id}/related", response_model=List[RelatedPaperResponse])
async def get_related_papers(
    paper_id: str,
    limit: int = 10,
    language: Optional[str] = "en",
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get related papers using Semantic Scholar.

    Supports translation to user's preferred language.
    """
    try:
        related = await papers_service.get_related_papers(paper_id, limit)

        # Translate results if needed
        if language and language != "en" and related:
            # Convert to dict for translation
            papers_dict = [paper.dict() if hasattr(paper, 'dict') else paper for paper in related]

            # Translate titles and abstracts
            translated_papers = await translation_service.translate_results(
                papers_dict,
                target_language=language,
                fields=["title", "abstract"]
            )

            # Convert back to RelatedPaperResponse objects
            related = [RelatedPaperResponse(**paper) for paper in translated_papers]

        return related

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get related papers: {str(e)}"
        )


@router.delete("/{paper_id}")
async def delete_paper(
    paper_id: str,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """Delete a paper."""
    user_id = current_user["user_id"] if current_user else "demo_user"

    # Get paper details
    result = supabase.table("uploads").select("*").eq("id", paper_id).eq("user_id", user_id).single().execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )

    paper = result.data

    # Delete from storage
    try:
        supabase.storage.from_("papers").remove([paper["file_path"]])
    except Exception as e:
        print(f"Failed to delete file from storage: {e}")

    # Delete from database
    supabase.table("uploads").delete().eq("id", paper_id).execute()

    return {"message": "Paper deleted successfully"}
