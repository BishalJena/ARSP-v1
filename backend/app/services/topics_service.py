"""Topic discovery service using Semantic Scholar and arXiv APIs."""
import asyncio
import math
import httpx
from typing import List, Optional, Dict, Any
from ..core.config import settings


class TopicsService:
    """Service for discovering research topics."""

    def __init__(self):
        self.semantic_scholar_base = "https://api.semanticscholar.org/graph/v1"
        self.arxiv_base = "https://export.arxiv.org/api"  # Changed to https
        self.headers = {
            "User-Agent": "ARSP-Research-Platform/1.0 (mailto:research@arsp.dev)"
        }

        if settings.SEMANTIC_SCHOLAR_API_KEY:
            self.headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY

    async def search_topics(
        self,
        query: str,
        discipline: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for trending research topics.

        Combines results from Semantic Scholar and arXiv.
        """
        # Search both APIs in parallel
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            tasks = [
                self._search_semantic_scholar(client, query, limit),
                self._search_arxiv(client, query, limit)
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

        topics = []

        # Process Semantic Scholar results
        if not isinstance(results[0], Exception):
            try:
                topics.extend(self._format_semantic_scholar_results(results[0]))
            except Exception as e:
                print(f"Error formatting Semantic Scholar results: {e}")
        else:
            print(f"Semantic Scholar API error: {results[0]}")

        # Process arXiv results
        if not isinstance(results[1], Exception):
            try:
                topics.extend(self._format_arxiv_results(results[1]))
            except Exception as e:
                print(f"Error formatting arXiv results: {e}")
        else:
            print(f"arXiv API error: {results[1]}")

        # Calculate impact scores and sort
        topics = self._calculate_impact_scores(topics)
        topics = sorted(topics, key=lambda x: x["impact_score"], reverse=True)

        return topics[:limit]

    async def _search_semantic_scholar(
        self,
        client: httpx.AsyncClient,
        query: str,
        limit: int
    ) -> Dict[str, Any]:
        """Search Semantic Scholar API using regular search endpoint (no auth required)."""
        # Use regular search endpoint - bulk requires API key
        url = f"{self.semantic_scholar_base}/paper/search"
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": "title,year,citationCount"
        }

        response = await client.get(url, params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    async def _search_arxiv(
        self,
        client: httpx.AsyncClient,
        query: str,
        limit: int
    ) -> str:
        """Search arXiv API."""
        url = f"{self.arxiv_base}/query"
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": limit,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.text

    def _format_semantic_scholar_results(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format Semantic Scholar bulk search results."""
        topics = []

        for paper in data.get("data", []):
            # Build Semantic Scholar URL from paper ID
            paper_id = paper.get("paperId", "")
            paper_url = f"https://www.semanticscholar.org/paper/{paper_id}" if paper_id else None

            topics.append({
                "id": f"s2_{paper_id}",
                "title": paper.get("title", ""),
                "description": "",  # Abstract not available in bulk search
                "source": "semantic_scholar",
                "url": paper_url,
                "citation_count": paper.get("citationCount", 0),
                "year": paper.get("year"),
                "raw_score": paper.get("citationCount", 0)
            })

        return topics

    def _format_arxiv_results(self, xml_data: str) -> List[Dict[str, Any]]:
        """Format arXiv results from XML."""
        import xml.etree.ElementTree as ET

        topics = []

        try:
            root = ET.fromstring(xml_data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace)
                summary = entry.find('atom:summary', namespace)
                published = entry.find('atom:published', namespace)
                link = entry.find('atom:id', namespace)

                if title is not None:
                    # Extract year from published date
                    year = None
                    if published is not None and published.text:
                        year = int(published.text[:4])

                    topics.append({
                        "id": f"arxiv_{link.text.split('/')[-1] if link is not None else ''}",
                        "title": title.text.strip() if title.text else "",
                        "description": summary.text.strip()[:500] if summary is not None and summary.text else "",
                        "source": "arxiv",
                        "url": link.text if link is not None else None,
                        "citation_count": None,
                        "year": year,
                        "raw_score": 0  # arXiv doesn't provide citation counts directly
                    })
        except Exception as e:
            print(f"Error parsing arXiv results: {e}")

        return topics

    def _calculate_impact_scores(self, topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calculate impact scores for topics (0-100).

        Score is based on:
        - Citation count (if available)
        - Recency (newer papers get higher scores)
        - Source credibility
        """
        from datetime import datetime, timezone

        current_year = datetime.now(timezone.utc).year

        for topic in topics:
            score = 0

            # Citation score (0-50 points)
            if topic.get("citation_count"):
                # Normalize citation count (log scale)
                import math
                citation_score = min(50, math.log1p(topic["citation_count"]) * 5)
                score += citation_score

            # Recency score (0-30 points)
            if topic.get("year"):
                years_ago = current_year - topic["year"]
                recency_score = max(0, 30 - (years_ago * 3))
                score += recency_score

            # Source credibility (0-20 points)
            if topic["source"] == "semantic_scholar":
                # Semantic Scholar papers are peer-reviewed
                score += 20
            elif topic["source"] == "arxiv":
                # arXiv papers are preprints
                score += 10

            topic["impact_score"] = min(100, score)

        return topics

    async def get_topic_evolution(
        self,
        topic: str,
        years: int = 5
    ) -> Dict[str, Any]:
        """
        Get topic evolution over time.

        Returns citation trends and publication counts.
        """
        from datetime import datetime, timezone

        current_year = datetime.now(timezone.utc).year
        start_year = current_year - years

        async with httpx.AsyncClient(timeout=30.0) as client:
            url = f"{self.semantic_scholar_base}/paper/search"
            params = {
                "query": topic,
                "year": f"{start_year}-{current_year}",
                "limit": 100,
                "fields": "year,citationCount"
            }

            response = await client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()

        # Aggregate by year
        year_data = {}
        for paper in data.get("data", []):
            year = paper.get("year")
            if year:
                if year not in year_data:
                    year_data[year] = {"count": 0, "citations": 0}
                year_data[year]["count"] += 1
                year_data[year]["citations"] += paper.get("citationCount", 0)

        # Format results
        evolution = []
        for year in range(start_year, current_year + 1):
            evolution.append({
                "year": year,
                "publication_count": year_data.get(year, {}).get("count", 0),
                "total_citations": year_data.get(year, {}).get("citations", 0)
            })

        return {
            "topic": topic,
            "years": years,
            "evolution": evolution
        }


# Import asyncio at module level
import asyncio


# Global service instance
topics_service = TopicsService()
