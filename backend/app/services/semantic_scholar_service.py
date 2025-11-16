"""
Semantic Scholar API integration service.

Implements hybrid approaches for:
1. Paper recommendations (bulk search + local re-ranking)
2. Plagiarism detection (API metadata + local embeddings)
3. Trending topics (S2 + arXiv with citation velocity)
"""

import httpx
import asyncio
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
import time
from ..core.config import settings


class SemanticScholarService:
    """Enhanced service using Semantic Scholar Academic Graph API."""

    def __init__(self):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.headers = {}

        if settings.SEMANTIC_SCHOLAR_API_KEY:
            self.headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY

        # HuggingFace for local embeddings
        self.hf_api_url = "https://api-inference.huggingface.co/models"
        self.embedding_model = "sentence-transformers/paraphrase-MiniLM-L6-v2"

        if settings.HF_API_KEY:
            self.hf_headers = {"Authorization": f"Bearer {settings.HF_API_KEY}"}
        else:
            self.hf_headers = {}

    async def search_papers_bulk(
        self,
        query: str,
        limit: int = 100,
        fields: Optional[List[str]] = None,
        year_filter: Optional[str] = None,
        sort: str = "citationCount"
    ) -> List[Dict[str, Any]]:
        """
        Use Academic Graph's paper bulk search with filters and sorting.

        Args:
            query: Search query (supports advanced syntax)
            limit: Max results to fetch
            fields: Fields to return
            year_filter: Year range (e.g., "2023-" for 2023 onwards)
            sort: Sort by citationCount, publicationDate, or paperId
        """
        if not fields:
            fields = [
                "paperId", "title", "abstract", "year", "citationCount",
                "influentialCitationCount", "authors", "url", "publicationDate",
                "openAccessPdf", "fieldsOfStudy"
            ]

        params = {
            "query": query,
            "fields": ",".join(fields),
            "limit": min(limit, 100),  # Max 100 per request
            "sort": sort
        }

        if year_filter:
            params["year"] = year_filter

        papers = []

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = f"{self.base_url}/paper/search/bulk"

                while len(papers) < limit:
                    response = await client.get(url, params=params, headers=self.headers)

                    if response.status_code == 429:
                        # Rate limit - wait and retry
                        await asyncio.sleep(1)
                        continue

                    if response.status_code != 200:
                        print(f"S2 API error: {response.status_code}")
                        break

                    data = response.json()
                    papers.extend(data.get("data", []))

                    # Check for pagination token
                    token = data.get("token")
                    if not token or len(papers) >= limit:
                        break

                    params["token"] = token

                return papers[:limit]

        except Exception as e:
            print(f"Error searching Semantic Scholar: {e}")
            return []

    async def get_paper_recommendations(
        self,
        positive_paper_ids: List[str],
        negative_paper_ids: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get paper recommendations using S2 Recommendations API.

        Args:
            positive_paper_ids: Papers you like (seed papers)
            negative_paper_ids: Papers to exclude from recommendations
            limit: Max recommendations (up to 500)
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = "https://api.semanticscholar.org/recommendations/v1/papers"

                data = {
                    "positivePaperIds": positive_paper_ids,
                    "negativePaperIds": negative_paper_ids or []
                }

                params = {
                    "fields": "paperId,title,abstract,year,citationCount,authors,url",
                    "limit": min(limit, 500)
                }

                response = await client.post(
                    url,
                    json=data,
                    params=params,
                    headers=self.headers
                )

                if response.status_code == 200:
                    return response.json().get("recommendedPapers", [])

                print(f"Recommendations API error: {response.status_code}")
                return []

        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []

    async def get_trending_topics(
        self,
        field: Optional[str] = None,
        limit: int = 20,
        days_back: int = 1095  # 3 years for good balance
    ) -> List[Dict[str, Any]]:
        """
        Find trending topics using papers sorted by citations with citation velocity boost.

        Citation velocity = citations / days_since_publication

        Args:
            field: Field of study filter (e.g., "Computer Science")
            limit: Number of trending papers to return
            days_back: Consider papers from last N days (default 1095 = 3 years)
        """
        # Current date for age calculation (timezone-aware)
        end_date = datetime.now(timezone.utc)

        # Search for papers using regular search (better citation sorting than bulk)
        # Use a default broad query if no field specified
        query = field if field else "computer science"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                url = f"{self.base_url}/paper/search"
                params = {
                    "query": query,
                    "limit": 100,
                    "fields": "paperId,title,abstract,year,citationCount,publicationDate,url,authors"
                }

                response = await client.get(url, params=params, headers=self.headers)
                if response.status_code == 200:
                    data = response.json()
                    papers = data.get("data", [])
                else:
                    print(f"S2 search error: {response.status_code}")
                    papers = []
        except Exception as e:
            print(f"Error searching S2: {e}")
            papers = []

        # Calculate impact scores for papers
        scored_papers = []
        for paper in papers:
            pub_date_str = paper.get("publicationDate")
            citation_count = paper.get("citationCount", 0)
            year = paper.get("year")

            # Use year as fallback for publication date
            if not pub_date_str and year:
                pub_date_str = f"{year}-06-01"

            # Default to medium impact score if no date available
            if not pub_date_str:
                paper["citation_velocity"] = 0
                paper["impact_score"] = float(citation_count * 0.5)
                scored_papers.append(paper)
                continue

            try:
                pub_date = datetime.fromisoformat(pub_date_str.replace("Z", "+00:00"))
                # Ensure pub_date is timezone-aware
                if pub_date.tzinfo is None:
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                days_old = max(1, (end_date - pub_date).days)

                # Citation velocity (citations per day)
                velocity = citation_count / days_old

                # Impact score: citations are base, velocity provides boost for newer papers
                # Recent papers with high velocity get higher scores
                impact_score = citation_count + (velocity * 365 * 0.3)

                paper["citation_velocity"] = round(velocity, 4)
                paper["impact_score"] = round(impact_score, 2)
                scored_papers.append(paper)

            except Exception as e:
                # Use citation count only as fallback
                paper["citation_velocity"] = 0
                paper["impact_score"] = float(citation_count)
                scored_papers.append(paper)

        # Sort by impact score
        scored_papers.sort(key=lambda x: x["impact_score"], reverse=True)

        return scored_papers[:limit]

    async def detect_plagiarism_hybrid(
        self,
        text: str,
        check_online: bool = True
    ) -> Dict[str, Any]:
        """
        Hybrid plagiarism detection: S2 API metadata + local embeddings.

        1. Generate embeddings for text chunks locally
        2. Search S2 for similar papers by keyword
        3. Compare embeddings with paper abstracts
        4. Flag high-similarity sections

        Args:
            text: Text to check
            check_online: Whether to search online sources
        """
        import time
        start_time = time.time()

        # Step 1: Chunk text
        chunks = self._chunk_text(text)

        # Step 2: Generate embeddings for chunks
        chunk_embeddings = await self._generate_embeddings(chunks)

        flagged_sections = []
        similar_sources = []

        if check_online:
            # Step 3: Search S2 for potentially similar papers
            keywords = self._extract_keywords(text)
            query = " ".join(keywords[:5])

            papers = await self.search_papers_bulk(
                query=query,
                limit=20,
                fields=["paperId", "title", "abstract", "url", "year", "authors"]
            )

            # Step 4: Generate embeddings for paper abstracts
            abstracts = [p.get("abstract", "") for p in papers if p.get("abstract")]
            if abstracts:
                abstract_embeddings = await self._generate_embeddings(abstracts)

                # Step 5: Compare chunk embeddings with paper embeddings
                for i, chunk in enumerate(chunks):
                    if not chunk_embeddings or i >= len(chunk_embeddings):
                        continue

                    chunk_emb = chunk_embeddings[i]

                    for j, paper in enumerate(papers):
                        if not abstract_embeddings or j >= len(abstract_embeddings):
                            continue

                        abstract_emb = abstract_embeddings[j]
                        similarity = self._cosine_similarity(chunk_emb, abstract_emb)

                        # Flag if similarity > 75%
                        if similarity > 0.75:
                            start_idx = text.find(chunk)

                            flagged_sections.append({
                                "text": chunk[:200],  # First 200 chars
                                "start_index": start_idx if start_idx >= 0 else 0,
                                "end_index": start_idx + len(chunk) if start_idx >= 0 else len(chunk),
                                "similarity": round(similarity * 100, 2),
                                "source": paper.get("title", "Unknown"),
                                "source_url": paper.get("url"),
                                "source_year": paper.get("year")
                            })

                            if paper not in similar_sources:
                                similar_sources.append(paper)

        # Calculate originality score
        if flagged_sections:
            avg_similarity = sum(s["similarity"] for s in flagged_sections) / len(flagged_sections)
            text_length = len(text)
            flagged_length = sum(len(s["text"]) for s in flagged_sections)
            coverage = (flagged_length / text_length) * 100 if text_length > 0 else 0

            originality_score = max(0, 100 - (avg_similarity * 0.7 + coverage * 0.3))
        else:
            originality_score = 90.0 if similar_sources else 100.0

        processing_time = time.time() - start_time

        return {
            "originality_score": round(originality_score, 2),
            "flagged_sections": flagged_sections[:10],
            "citations": [],  # Will be added by citation suggestions if needed
            "similar_sources_count": len(similar_sources),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "processing_time_seconds": round(processing_time, 2)
        }

    async def recommend_journals_hybrid(
        self,
        abstract: str,
        keywords: List[str],
        journals_db: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Hybrid journal recommendations: local embedding + keyword matching.

        1. Generate embedding for abstract
        2. Generate embeddings for journal descriptions
        3. Calculate semantic similarity scores
        4. Boost scores with keyword matching
        5. Return ranked list
        """
        # Generate embedding for abstract
        abstract_embedding = await self._generate_embedding(abstract)

        if not abstract_embedding:
            # Fallback to pure keyword matching
            return self._keyword_match_journals(abstract, keywords, journals_db)

        # Generate embeddings for journals
        journal_texts = [
            f"{j.get('name', '')} {j.get('description', '')}"
            for j in journals_db
        ]
        journal_embeddings = await self._generate_embeddings(journal_texts)

        scored_journals = []

        for i, journal in enumerate(journals_db):
            score = 0

            # Semantic similarity score (0-50 points)
            if journal_embeddings and i < len(journal_embeddings):
                similarity = self._cosine_similarity(abstract_embedding, journal_embeddings[i])
                score += similarity * 50

            # Keyword matching (0-30 points)
            keyword_score = self._calculate_keyword_score(abstract, keywords, journal)
            score += keyword_score

            # Impact factor boost (0-20 points)
            impact_factor = journal.get("impact_factor", 0)
            if impact_factor > 0:
                import math
                score += min(20, math.log(1 + impact_factor) * 8)

            journal_copy = journal.copy()
            journal_copy["fit_score"] = round(score, 2)
            scored_journals.append(journal_copy)

        # Sort by fit score
        scored_journals.sort(key=lambda x: x["fit_score"], reverse=True)

        return scored_journals

    # Helper methods

    def _chunk_text(self, text: str, max_size: int = 500) -> List[str]:
        """Split text into chunks for comparison."""
        import re
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = []
        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) > max_size and current:
                chunks.append(current.strip())
                current = sentence
            else:
                current += " " + sentence if current else sentence

        if current:
            chunks.append(current.strip())

        return [c for c in chunks if len(c) > 50]

    async def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate single embedding."""
        embeddings = await self._generate_embeddings([text])
        return embeddings[0] if embeddings else None

    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using HuggingFace."""
        if not texts:
            return []

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.hf_api_url}/{self.embedding_model}",
                    headers=self.hf_headers,
                    json={"inputs": texts}
                )

                if response.status_code == 200:
                    embeddings = response.json()
                    if isinstance(embeddings, list):
                        if embeddings and isinstance(embeddings[0], list):
                            return embeddings
                        elif embeddings and isinstance(embeddings[0], (int, float)):
                            return [embeddings]
                    return []
                else:
                    return []

        except Exception as e:
            print(f"Embedding error: {e}")
            return []

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Calculate cosine similarity."""
        try:
            a = np.array(vec_a)
            b = np.array(vec_b)
            return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        except:
            return 0.0

    def _extract_keywords(self, text: str, num: int = 10) -> List[str]:
        """Extract keywords from text."""
        import re
        from collections import Counter

        text = re.sub(r'[^\w\s]', ' ', text.lower())

        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be'
        }

        words = [w for w in text.split() if len(w) > 3 and w not in stop_words]
        return [word for word, _ in Counter(words).most_common(num)]

    def _calculate_keyword_score(
        self,
        abstract: str,
        keywords: List[str],
        journal: Dict[str, Any]
    ) -> float:
        """Calculate keyword matching score (0-30)."""
        score = 0
        name = journal.get("name", "").lower()
        desc = journal.get("description", "").lower()
        domain = journal.get("domain", "").lower()

        for keyword in keywords:
            kw = keyword.lower()
            if kw in name:
                score += 8
            if kw in desc:
                score += 5
            if kw in domain:
                score += 3

        return min(30, score)

    def _keyword_match_journals(
        self,
        abstract: str,
        keywords: List[str],
        journals: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Fallback keyword-only matching."""
        scored = []

        for journal in journals:
            score = self._calculate_keyword_score(abstract, keywords, journal)

            # Add impact factor boost
            impact = journal.get("impact_factor", 0)
            if impact > 0:
                import math
                score += min(20, math.log(1 + impact) * 8)

            journal_copy = journal.copy()
            journal_copy["fit_score"] = round(score, 2)
            scored.append(journal_copy)

        scored.sort(key=lambda x: x["fit_score"], reverse=True)
        return scored


# Global service instance
semantic_scholar_service = SemanticScholarService()
