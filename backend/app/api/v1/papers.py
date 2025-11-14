"""Papers and literature review endpoints."""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from typing import List
from datetime import datetime
from ...schemas.papers import (
    PaperUploadResponse,
    LiteratureReviewResponse,
    RelatedPaperResponse
)
from ...services.papers_service import papers_service
from ...core.auth import get_current_user
from ...core.supabase import supabase

router = APIRouter()


@router.post("/upload", response_model=PaperUploadResponse)
async def upload_paper(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
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
        user_id = current_user["user_id"]

        # Generate file path: user_id/filename
        file_path = f"{user_id}/{file.filename}"

        # Upload to Supabase Storage
        result = supabase.storage.from_("papers").upload(
            file_path,
            content,
            {"content-type": "application/pdf"}
        )

        # Get public URL (or signed URL for private buckets)
        file_url = supabase.storage.from_("papers").get_public_url(file_path)

        # Create database record
        upload_data = {
            "user_id": user_id,
            "file_name": file.filename,
            "file_path": file_path,
            "file_size": file_size,
            "mime_type": "application/pdf"
        }

        db_result = supabase.table("uploads").insert(upload_data).execute()

        if not db_result.data:
            raise Exception("Failed to create database record")

        upload_record = db_result.data[0]

        return PaperUploadResponse(
            id=upload_record["id"],
            file_name=file.filename,
            file_size=file_size,
            upload_url=file_url,
            created_at=upload_record["created_at"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload paper: {str(e)}"
        )


@router.post("/{paper_id}/process", response_model=LiteratureReviewResponse)
async def process_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Process a paper to generate literature review.

    Extracts text, generates summary, identifies insights, and extracts references.
    """
    try:
        user_id = current_user["user_id"]

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

        # Process the paper
        review = await papers_service.process_paper(
            paper_id=paper_id,
            user_id=user_id,
            pdf_content=file_content
        )

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
    current_user: dict = Depends(get_current_user)
):
    """Get paper details."""
    user_id = current_user["user_id"]

    result = supabase.table("uploads").select("*").eq("id", paper_id).eq("user_id", user_id).single().execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paper not found"
        )

    return result.data


@router.get("/")
async def list_papers(
    current_user: dict = Depends(get_current_user)
):
    """List all papers for the current user."""
    user_id = current_user["user_id"]

    result = supabase.table("uploads").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()

    return {"papers": result.data or [], "count": len(result.data or [])}


@router.get("/{paper_id}/related", response_model=List[RelatedPaperResponse])
async def get_related_papers(
    paper_id: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get related papers using Semantic Scholar."""
    try:
        related = await papers_service.get_related_papers(paper_id, limit)
        return related

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get related papers: {str(e)}"
        )


@router.delete("/{paper_id}")
async def delete_paper(
    paper_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a paper."""
    user_id = current_user["user_id"]

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
