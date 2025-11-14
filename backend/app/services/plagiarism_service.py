"""Plagiarism detection service using Sentence Transformers."""
import httpx
import numpy as np
import re
from typing import List, Dict, Any, Tuple
from datetime import datetime
import time
from ..core.config import settings


class PlagiarismService:
    """Service for detecting plagiarism using semantic similarity."""

    def __init__(self):
        self.hf_api_url = "https://api-inference.huggingface.co/models"
        self.model = "sentence-transformers/all-mpnet-base-v2"
        self.crossref_url = "https://api.crossref.org/works"

        self.hf_headers = {}
        if settings.HF_API_KEY:
            self.hf_headers["Authorization"] = f"Bearer {settings.HF_API_KEY}"

    async def check_plagiarism(
        self,
        text: str,
        language: str = "en",
        check_online: bool = True
    ) -> Dict[str, Any]:
        """
        Check text for plagiarism using semantic similarity.

        Returns originality score, flagged sections, and citation suggestions.
        """
        start_time = time.time()

        try:
            # Step 1: Chunk text into sentences/paragraphs
            chunks = self._chunk_text(text)

            # Step 2: Generate embeddings for all chunks
            chunk_embeddings = await self._generate_embeddings(chunks)

            # Step 3: Search for similar content online (using Semantic Scholar)
            similar_sources = []
            if check_online:
                similar_sources = await self._search_similar_content(text[:500])  # Use first 500 chars

            # Step 4: Compare embeddings and detect plagiarism
            flagged_sections = []
            if similar_sources:
                source_texts = [s.get("abstract", s.get("title", "")) for s in similar_sources]
                source_embeddings = await self._generate_embeddings(source_texts)

                # Compare each chunk against each source
                for i, chunk in enumerate(chunks):
                    if chunk_embeddings and i < len(chunk_embeddings):
                        chunk_emb = chunk_embeddings[i]

                        for j, source in enumerate(similar_sources):
                            if source_embeddings and j < len(source_embeddings):
                                source_emb = source_embeddings[j]

                                # Calculate cosine similarity
                                similarity = self._cosine_similarity(chunk_emb, source_emb)

                                # Flag if similarity > 80%
                                if similarity > 0.8:
                                    # Find chunk position in original text
                                    start_idx = text.find(chunk)

                                    flagged_sections.append({
                                        "text": chunk,
                                        "start_index": start_idx if start_idx >= 0 else 0,
                                        "end_index": start_idx + len(chunk) if start_idx >= 0 else len(chunk),
                                        "similarity": similarity * 100,
                                        "source": source.get("title", "Unknown source"),
                                        "source_url": source.get("url")
                                    })

            # Step 5: Calculate originality score
            if flagged_sections:
                max_similarity = max(section["similarity"] for section in flagged_sections)
                originality_score = max(0, 100 - max_similarity)
            else:
                originality_score = 100.0

            # Step 6: Get citation suggestions
            citations = await self._get_citation_suggestions(text)

            processing_time = time.time() - start_time

            return {
                "originality_score": round(originality_score, 2),
                "flagged_sections": flagged_sections[:10],  # Limit to top 10
                "citations": citations[:10],  # Limit to top 10
                "checked_at": datetime.utcnow().isoformat(),
                "processing_time_seconds": round(processing_time, 2)
            }

        except Exception as e:
            raise Exception(f"Plagiarism check failed: {str(e)}")

    def _chunk_text(self, text: str, max_chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks (sentences/paragraphs).

        Each chunk should be meaningful for comparison.
        """
        # Split by sentences
        import re
        sentences = re.split(r'[.!?]+\s+', text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # If adding this sentence exceeds max size, save current chunk
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence

        # Add last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())

        return [c for c in chunks if len(c) > 50]  # Filter out very short chunks

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

    async def _search_similar_content(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for similar content using Semantic Scholar API.

        Returns list of potentially plagiarized sources.
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = "https://api.semanticscholar.org/graph/v1/paper/search"
                params = {
                    "query": query,
                    "limit": 10,
                    "fields": "title,abstract,url,year,authors"
                }

                headers = {}
                if settings.SEMANTIC_SCHOLAR_API_KEY:
                    headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY

                response = await client.get(url, params=params, headers=headers)

                if response.status_code == 200:
                    data = response.json()
                    return data.get("data", [])

                return []

        except Exception as e:
            print(f"Error searching similar content: {e}")
            return []

    async def _get_citation_suggestions(self, text: str) -> List[Dict[str, Any]]:
        """
        Get citation suggestions using CrossRef API.

        Suggests relevant papers to cite based on content.
        """
        # Extract keywords from text
        keywords = self._extract_keywords(text)

        if not keywords:
            return []

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Search CrossRef
                params = {
                    "query": " ".join(keywords[:5]),  # Use top 5 keywords
                    "rows": 10,
                    "sort": "relevance"
                }

                # Add polite pool access if email configured
                if settings.CROSSREF_EMAIL:
                    params["mailto"] = settings.CROSSREF_EMAIL

                response = await client.get(self.crossref_url, params=params)

                if response.status_code != 200:
                    return []

                data = response.json()
                citations = []

                for item in data.get("message", {}).get("items", []):
                    # Format author names
                    authors = []
                    for author in item.get("author", [])[:3]:  # First 3 authors
                        given = author.get("given", "")
                        family = author.get("family", "")
                        if family:
                            authors.append(f"{given} {family}".strip())

                    # Get publication year
                    year = None
                    if "published" in item:
                        date_parts = item["published"].get("date-parts", [[]])[0]
                        if date_parts:
                            year = date_parts[0]

                    # Get journal name
                    journal = None
                    if "container-title" in item and item["container-title"]:
                        journal = item["container-title"][0]

                    citations.append({
                        "doi": item.get("DOI", ""),
                        "title": item.get("title", [""])[0] if isinstance(item.get("title"), list) else item.get("title", ""),
                        "authors": ", ".join(authors) if authors else None,
                        "year": year,
                        "journal": journal,
                        "relevance": 0.8  # Placeholder - would calculate based on text similarity
                    })

                return citations

        except Exception as e:
            print(f"Error getting citations: {e}")
            return []

    def _extract_keywords(self, text: str, num_keywords: int = 10) -> List[str]:
        """
        Extract keywords from text.

        Simple implementation using word frequency.
        For production, use NLP models like RAKE or KeyBERT.
        """
        import re
        from collections import Counter

        # Remove special characters and convert to lowercase
        text = re.sub(r'[^\w\s]', ' ', text.lower())

        # Common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
            'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        # Split into words and filter
        words = text.split()
        words = [w for w in words if len(w) > 3 and w not in stop_words]

        # Count frequencies
        word_counts = Counter(words)

        # Return most common
        return [word for word, count in word_counts.most_common(num_keywords)]


# Global service instance
plagiarism_service = PlagiarismService()
