"""API v1 router."""
from fastapi import APIRouter
from .topics import router as topics_router
from .papers import router as papers_router
from .papers_v2 import router as papers_v2_router
from .plagiarism import router as plagiarism_router
from .journals import router as journals_router
from .auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(topics_router, prefix="/topics", tags=["topics"])
api_router.include_router(papers_router, prefix="/papers", tags=["papers"])
api_router.include_router(papers_v2_router, prefix="/papers-enhanced", tags=["papers-enhanced"])
api_router.include_router(plagiarism_router, prefix="/plagiarism", tags=["plagiarism"])
api_router.include_router(journals_router, prefix="/journals", tags=["journals"])
