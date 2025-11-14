"""Journal recommendation service."""
import httpx
import numpy as np
from typing import List, Dict, Any, Optional
from ..core.config import settings
from ..core.supabase import supabase


class JournalsService:
    """Service for recommending academic journals based on abstract."""

    def __init__(self):
        self.hf_api_url = "https://api-inference.huggingface.co/models"
        self.model = "sentence-transformers/all-mpnet-base-v2"

        self.hf_headers = {}
        if settings.HF_API_KEY:
            self.hf_headers["Authorization"] = f"Bearer {settings.HF_API_KEY}"

    async def recommend_journals(
        self,
        abstract: str,
        keywords: List[str],
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Recommend journals based on abstract and keywords.

        Uses semantic similarity to match abstract with journal descriptions.
        """
        try:
            # Step 1: Get journals from database with filters
            journals = await self._get_journals_from_db(filters or {})

            if not journals:
                return []

            # Step 2: Generate embedding for abstract
            abstract_embedding = await self._generate_embedding(abstract)

            if not abstract_embedding:
                # Fallback to keyword matching
                return self._keyword_based_matching(abstract, keywords, journals)

            # Step 3: Generate embeddings for all journal descriptions
            journal_descriptions = [j.get("description", j.get("name", "")) for j in journals]
            journal_embeddings = await self._generate_embeddings(journal_descriptions)

            # Step 4: Calculate fit scores
            scored_journals = []
            for i, journal in enumerate(journals):
                if journal_embeddings and i < len(journal_embeddings):
                    journal_emb = journal_embeddings[i]
                    similarity = self._cosine_similarity(abstract_embedding, journal_emb)
                    fit_score = similarity * 100

                    journal_copy = journal.copy()
                    journal_copy["fit_score"] = round(fit_score, 2)
                    scored_journals.append(journal_copy)

            # Sort by fit score
            scored_journals.sort(key=lambda x: x["fit_score"], reverse=True)

            return scored_journals[:10]  # Return top 10

        except Exception as e:
            print(f"Error recommending journals: {e}")
            # Fallback to simple matching
            journals = await self._get_journals_from_db(filters or {})
            return self._keyword_based_matching(abstract, keywords, journals)

    async def _get_journals_from_db(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get journals from database with optional filters.

        Filters:
        - open_access_only: bool
        - min_impact_factor: float
        - max_time_to_publish: int (months)
        """
        query = supabase.table("journals").select("*")

        # Apply filters
        if filters.get("open_access_only"):
            query = query.eq("is_open_access", True)

        if filters.get("min_impact_factor"):
            query = query.gte("impact_factor", filters["min_impact_factor"])

        if filters.get("max_time_to_publish"):
            query = query.lte("publication_time_months", filters["max_time_to_publish"])

        result = query.limit(100).execute()

        return result.data or []

    async def _generate_embedding(self, text: str) -> Optional[List[float]]:
        """Generate embedding for a single text using Sentence Transformers."""
        embeddings = await self._generate_embeddings([text])
        return embeddings[0] if embeddings else None

    async def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using Sentence Transformers via Hugging Face API.

        Returns list of 768-dimensional embeddings.
        """
        if not texts:
            return []

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.hf_api_url}/{self.model}",
                    headers=self.hf_headers,
                    json={"inputs": texts}
                )

                if response.status_code == 200:
                    embeddings = response.json()
                    # HF returns different formats, normalize to list of lists
                    if isinstance(embeddings, list):
                        if embeddings and isinstance(embeddings[0], list):
                            return embeddings
                        elif embeddings and isinstance(embeddings[0], (int, float)):
                            # Single embedding returned as flat list
                            return [embeddings]
                    return []
                else:
                    print(f"Embeddings API error: {response.status_code}")
                    return []

        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            a = np.array(vec_a)
            b = np.array(vec_b)

            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)

            if norm_a == 0 or norm_b == 0:
                return 0.0

            return float(dot_product / (norm_a * norm_b))

        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0

    def _keyword_based_matching(
        self,
        abstract: str,
        keywords: List[str],
        journals: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Fallback: Simple keyword-based matching.

        Counts how many keywords appear in journal name/description.
        """
        scored_journals = []

        for journal in journals:
            score = 0
            name_lower = journal.get("name", "").lower()
            desc_lower = journal.get("description", "").lower()

            # Count keyword matches
            for keyword in keywords:
                keyword_lower = keyword.lower()
                if keyword_lower in name_lower:
                    score += 20
                if keyword_lower in desc_lower:
                    score += 10

            # Boost by impact factor
            impact_factor = journal.get("impact_factor", 0)
            score += min(30, impact_factor * 5)

            journal_copy = journal.copy()
            journal_copy["fit_score"] = min(100, score)
            scored_journals.append(journal_copy)

        # Sort by score
        scored_journals.sort(key=lambda x: x["fit_score"], reverse=True)

        return scored_journals[:10]

    async def get_journal_by_id(self, journal_id: str) -> Optional[Dict[str, Any]]:
        """Get journal details by ID."""
        result = supabase.table("journals").select("*").eq("id", journal_id).single().execute()

        return result.data

    async def search_journals(
        self,
        query: str,
        discipline: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search journals by name or description.

        Uses PostgreSQL full-text search.
        """
        db_query = supabase.table("journals").select("*")

        # Simple text search (Supabase supports ilike for partial matching)
        db_query = db_query.or_(f"name.ilike.%{query}%,description.ilike.%{query}%")

        if discipline:
            db_query = db_query.eq("domain", discipline)

        result = db_query.limit(20).execute()

        return result.data or []


# Global service instance
journals_service = JournalsService()
