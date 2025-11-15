"""Topics discovery endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from ...schemas.topics import TopicQuery, TopicListResponse, TopicResponse
from ...services.topics_service import topics_service
from ...services.semantic_scholar_service import semantic_scholar_service
from ...services.translation_service import translation_service
from ...core.auth import get_current_user, get_current_user_optional

router = APIRouter()


class TopicEvolutionRequest(BaseModel):
    """Topic evolution request."""
    topic: str
    years: Optional[int] = 5


@router.get("/trending", response_model=TopicListResponse)
async def get_trending_topics(
    query: str = "",
    discipline: Optional[str] = None,
    limit: Optional[int] = 10,
    language: Optional[str] = "en"
):
    """
    Get trending research topics based on search query.

    Uses Semantic Scholar and arXiv APIs to find relevant topics.
    Supports translation to user's preferred language.
    """
    try:
        # Translate discipline to English if needed
        if language != "en" and discipline:
            discipline = await translation_service.translate_query(discipline, target_language="en", source_language=language)

        # Use Semantic Scholar citation velocity for trending topics
        papers = await semantic_scholar_service.get_trending_topics(
            field=discipline,
            limit=limit or 10,
            days_back=90
        )

        # Format response - convert papers to topics
        topic_responses = [
            TopicResponse(
                id=paper.get("paperId", str(i)),
                title=paper.get("title", ""),
                description=paper.get("abstract", "")[:200] if paper.get("abstract") else "",
                impact_score=paper.get("impact_score", 0.0),
                source="Semantic Scholar",
                url=paper.get("url"),
                citation_count=paper.get("citationCount"),
                year=paper.get("year")
            )
            for i, paper in enumerate(papers)
        ]

        # Translate results if needed
        if language != "en":
            topics_dict = [topic.model_dump() for topic in topic_responses]
            translated_topics = await translation_service.translate_results(
                topics_dict,
                target_language=language,
                fields=["title", "description"]
            )
            topic_responses = [TopicResponse(**topic) for topic in translated_topics]

        return TopicListResponse(
            topics=topic_responses,
            count=len(topic_responses)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch topics: {str(e)}")


@router.post("/personalized")
async def get_personalized_topics(
    interests: list[str],
    research_area: Optional[str] = None,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get personalized topic recommendations based on user interests.

    Combines multiple interest queries and ranks by relevance.
    """
    try:
        all_topics = []

        # Search for each interest
        for interest in interests[:3]:  # Limit to 3 interests
            topics = await topics_service.search_topics(
                query=interest,
                discipline=research_area,
                limit=5
            )
            all_topics.extend(topics)

        # Remove duplicates and sort by impact score
        seen_ids = set()
        unique_topics = []
        for topic in all_topics:
            if topic["id"] not in seen_ids:
                seen_ids.add(topic["id"])
                unique_topics.append(topic)

        unique_topics = sorted(unique_topics, key=lambda x: x["impact_score"], reverse=True)[:10]

        # Format response
        topic_responses = [
            TopicResponse(
                id=topic["id"],
                title=topic["title"],
                description=topic["description"],
                impact_score=topic["impact_score"],
                source=topic["source"],
                url=topic.get("url"),
                citation_count=topic.get("citation_count"),
                year=topic.get("year")
            )
            for topic in unique_topics
        ]

        return TopicListResponse(
            topics=topic_responses,
            count=len(topic_responses)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get personalized topics: {str(e)}")


@router.post("/evolution")
async def get_topic_evolution(
    request: TopicEvolutionRequest,
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get topic evolution over time.

    Shows publication trends and citation growth.
    """
    try:
        evolution = await topics_service.get_topic_evolution(
            topic=request.topic,
            years=request.years
        )

        return evolution

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get topic evolution: {str(e)}")
