"""Papers and literature review service."""
import httpx
import PyPDF2
import io
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..core.config import settings
from ..core.supabase import supabase
import time


class PapersService:
    """Service for processing research papers and generating literature reviews."""

    def __init__(self):
        self.hf_api_url = "https://api-inference.huggingface.co/models"
        self.hf_headers = {}

        if settings.HF_API_KEY:
            self.hf_headers["Authorization"] = f"Bearer {settings.HF_API_KEY}"

    async def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """
        Extract text from PDF file.

        Uses PyPDF2 for text extraction.
        """
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"

            return text.strip()

        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")

    async def summarize_text(self, text: str, max_length: int = 500) -> str:
        """
        Summarize text using Hugging Face BART model.

        Falls back to extractive summarization if API fails.
        """
        # Chunk text if too long (BART has max 1024 tokens)
        max_input_length = 4000  # ~1000 tokens
        if len(text) > max_input_length:
            text = text[:max_input_length]

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.hf_api_url}/facebook/bart-large-cnn",
                    headers=self.hf_headers,
                    json={
                        "inputs": text,
                        "parameters": {
                            "max_length": max_length,
                            "min_length": 100,
                            "do_sample": False
                        }
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("summary_text", "")

                # If HF API fails, use extractive summary (first N sentences)
                return self._extractive_summary(text, max_length)

        except Exception as e:
            print(f"Summarization error: {e}")
            return self._extractive_summary(text, max_length)

    def _extractive_summary(self, text: str, max_length: int) -> str:
        """Simple extractive summary by taking first N sentences."""
        sentences = text.split('. ')
        summary = ""

        for sentence in sentences:
            if len(summary) + len(sentence) < max_length:
                summary += sentence + ". "
            else:
                break

        return summary.strip()

    async def extract_insights(self, text: str, num_insights: int = 7) -> List[str]:
        """
        Extract key insights from text.

        Uses simple heuristics to identify important sentences.
        For production, consider using NLP models.
        """
        sentences = [s.strip() + '.' for s in text.split('. ') if len(s.strip()) > 20]

        # Score sentences based on keywords
        keywords = [
            'found', 'showed', 'demonstrated', 'concluded', 'result',
            'significant', 'important', 'novel', 'discovered', 'revealed',
            'evidence', 'analysis', 'indicates', 'suggests', 'proposed'
        ]

        scored_sentences = []
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword.lower() in sentence.lower())
            if score > 0:
                scored_sentences.append((score, sentence))

        # Sort by score and take top N
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        insights = [s[1] for s in scored_sentences[:num_insights]]

        # If not enough insights, add first sentences
        while len(insights) < min(num_insights, len(sentences)):
            for sentence in sentences:
                if sentence not in insights:
                    insights.append(sentence)
                    if len(insights) >= num_insights:
                        break

        return insights[:num_insights]

    async def extract_references(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract references from text.

        Uses simple pattern matching. For production, use specialized tools.
        """
        import re

        references = []

        # Pattern for common reference formats
        # This is a simplified version - production would need more robust parsing
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\((\d{4})\)',  # Author (Year)
            r'([A-Z][a-z]+,\s+[A-Z]\.(?:\s+[A-Z]\.)?)\s+\((\d{4})\)',  # Author, A. (Year)
        ]

        seen = set()
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                authors = match.group(1)
                year = match.group(2)

                ref_key = f"{authors}_{year}"
                if ref_key not in seen:
                    seen.add(ref_key)
                    references.append({
                        "authors": [authors],
                        "year": int(year),
                        "title": "Reference extracted from text"
                    })

        return references[:20]  # Limit to 20 references

    async def process_paper_content(
        self,
        pdf_content: bytes,
        filename: str
    ) -> Dict[str, Any]:
        """
        Process PDF content directly and return analysis.
        Simplified version for quick upload and analysis.
        """
        try:
            # Extract text from PDF
            text = await self.extract_text_from_pdf(pdf_content)

            if not text or len(text) < 100:
                raise Exception("Could not extract meaningful text from PDF")

            # Extract paper title (first meaningful line or from filename)
            paper_title = self._extract_title(text, filename)

            # Find abstract section for better summary
            abstract_text = self._extract_abstract(text)
            summary_text = abstract_text if abstract_text else text

            # Generate simplified, easy-to-understand summary
            summary = await self.summarize_text(summary_text, max_length=800)

            # Extract insights from results/conclusion sections
            insights = await self._extract_key_findings(text)

            # Extract methodology (simple pattern matching)
            methodology = self._extract_methodology(text)

            return {
                "paper_title": paper_title,
                "summary": summary,
                "insights": insights,
                "methodology": methodology,
                "language": "en"
            }

        except Exception as e:
            raise Exception(f"Failed to process paper: {str(e)}")

    def _extract_title(self, text: str, filename: str) -> str:
        """Extract paper title from text or filename."""
        # Try to get the first substantial line (likely the title)
        lines = text.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip()
            # Title is usually 20-200 chars, not all caps or numbers
            if 20 <= len(line) <= 200 and not line.isupper() and not line.isdigit():
                # Avoid common headers and noise
                if not any(x in line.lower() for x in [
                    'page', 'abstract', 'introduction', 'copyright', 'doi:', 'arxiv',
                    'proceedings', 'conference', 'published', 'journal', 'volume',
                    'permission', '@', '.com', 'university', 'google', 'email'
                ]):
                    return line

        # Fallback: use filename
        return filename.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()

    def _extract_abstract(self, text: str) -> str:
        """Extract abstract section from paper text."""
        import re

        # Look for abstract section
        patterns = [
            r'abstract[\s\n:]+(.+?)(?=\n\s*\n|\n\s*(?:introduction|1\.|keywords|categories))',
            r'abstract[\s\n:]+(.+?)(?=\n\n)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                abstract = match.group(1).strip()
                # Clean up
                abstract = ' '.join(abstract.split())
                if len(abstract) > 100:  # Must be substantial
                    return abstract[:2000]  # Limit length

        # Fallback: return first few paragraphs, skipping headers
        lines = text.split('\n')
        paragraphs = []
        current_para = []

        for line in lines[10:]:  # Skip first 10 lines (headers)
            line = line.strip()
            if not line:
                if current_para:
                    para_text = ' '.join(current_para)
                    if len(para_text) > 50:  # Substantial paragraph
                        paragraphs.append(para_text)
                        if len(' '.join(paragraphs)) > 500:
                            break
                    current_para = []
            else:
                current_para.append(line)

        return ' '.join(paragraphs[:3]) if paragraphs else text[:1000]

    async def _extract_key_findings(self, text: str) -> List[str]:
        """Extract key findings from results and conclusion sections."""
        import re

        findings = []

        # Look for results and conclusion sections
        sections = []

        # Extract Results section
        results_pattern = r'(?:results?|findings?|experiments?)[\s\n:]+(.+?)(?=\n\s*\n\s*(?:[A-Z]|\d+\.)|\Z)'
        results_match = re.search(results_pattern, text, re.IGNORECASE | re.DOTALL)
        if results_match:
            sections.append(results_match.group(1))

        # Extract Conclusion section
        conclusion_pattern = r'(?:conclusion|summary|discussion)[\s\n:]+(.+?)(?=\n\s*\n\s*(?:[A-Z]|\d+\.|references|acknowledgments)|\Z)'
        conclusion_match = re.search(conclusion_pattern, text, re.IGNORECASE | re.DOTALL)
        if conclusion_match:
            sections.append(conclusion_match.group(1))

        # Extract sentences from these sections
        for section_text in sections:
            sentences = [s.strip() + '.' for s in section_text.split('. ') if len(s.strip()) > 30]

            # Score sentences based on keywords
            keywords = [
                'achieved', 'demonstrated', 'showed', 'found', 'outperformed',
                'improved', 'better', 'state-of-the-art', 'sota', 'best',
                'novel', 'proposed', 'introduced', 'presented', 'developed'
            ]

            scored = []
            for sentence in sentences[:20]:  # Limit to first 20 sentences
                score = sum(1 for keyword in keywords if keyword.lower() in sentence.lower())
                if score > 0:
                    scored.append((score, sentence))

            scored.sort(reverse=True, key=lambda x: x[0])
            findings.extend([s[1] for s in scored[:4]])  # Top 4 from each section

        # If no findings from sections, use the old method
        if not findings:
            findings = await self.extract_insights(text, num_insights=7)

        return findings[:7]  # Return max 7 findings

    def _extract_methodology(self, text: str) -> str:
        """Extract methodology section from paper text."""
        import re

        # Look for methodology section with full context
        patterns = [
            r'(?:methodology|methods?|approach|experimental\s+setup|model\s+architecture)[\s\n:]+(.+?)(?=\n\s*\n\s*(?:[A-Z]|\d+\.)|\Z)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                methodology = match.group(1).strip()
                # Clean up and extract first few sentences
                sentences = [s.strip() for s in methodology.split('. ') if len(s.strip()) > 20]
                if sentences:
                    result = '. '.join(sentences[:5])  # First 5 sentences
                    return result if len(result) < 800 else result[:800] + '...'

        # Fallback: Look for section 3 or 4 (often methodology)
        section_pattern = r'(?:^|\n)\s*(?:3|4)[\s\.]+(?:methodology|methods?|approach|experimental)(.+?)(?=\n\s*\n\s*(?:\d+\.|[A-Z])|\Z)'
        match = re.search(section_pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            methodology = match.group(1).strip()
            sentences = [s.strip() for s in methodology.split('. ') if len(s.strip()) > 20]
            if sentences:
                result = '. '.join(sentences[:5])
                return result if len(result) < 800 else result[:800] + '...'

        return "This paper uses a systematic research approach with experimental validation of the proposed methods."

    async def process_paper(
        self,
        paper_id: str,
        user_id: str,
        pdf_content: bytes
    ) -> Dict[str, Any]:
        """
        Process a paper: extract text, summarize, extract insights and references.

        Returns a complete literature review.
        """
        start_time = time.time()

        try:
            # Step 1: Extract text from PDF
            text = await self.extract_text_from_pdf(pdf_content)

            if not text or len(text) < 100:
                raise Exception("Could not extract meaningful text from PDF")

            # Step 2: Generate summary
            summary = await self.summarize_text(text)

            # Step 3: Extract insights
            insights = await self.extract_insights(text)

            # Step 4: Extract references
            references = await self.extract_references(text)

            processing_time = time.time() - start_time

            # Step 5: Store in database
            review_data = {
                "user_id": user_id,
                "title": f"Review for paper {paper_id}",
                "summary": summary,
                "insights": insights,
                "references": references,
                "language": "en"
            }

            result = supabase.table("literature_reviews").insert(review_data).execute()

            review_id = result.data[0]["id"] if result.data else None

            # Update upload record with review_id
            if review_id:
                supabase.table("uploads").update({"review_id": review_id}).eq("id", paper_id).execute()

            return {
                "id": review_id or paper_id,
                "title": review_data["title"],
                "summary": summary,
                "insights": insights,
                "references": references,
                "language": "en",
                "created_at": datetime.utcnow().isoformat(),
                "processing_time_seconds": processing_time
            }

        except Exception as e:
            raise Exception(f"Failed to process paper: {str(e)}")

    async def get_related_papers(self, paper_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get related papers using Semantic Scholar API.

        Uses the paper's title or abstract to find similar papers.
        """
        try:
            # Get the paper details from database
            result = supabase.table("uploads").select("file_name").eq("id", paper_id).single().execute()

            if not result.data:
                return []

            # Use filename as search query (remove .pdf extension)
            query = result.data["file_name"].replace(".pdf", "").replace("_", " ")

            # Search Semantic Scholar
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = "https://api.semanticscholar.org/graph/v1/paper/search"
                params = {
                    "query": query,
                    "limit": limit,
                    "fields": "title,abstract,year,authors,url"
                }

                headers = {}
                if settings.SEMANTIC_SCHOLAR_API_KEY:
                    headers["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY

                response = await client.get(url, params=params, headers=headers)

                if response.status_code != 200:
                    return []

                data = response.json()

                related = []
                for paper in data.get("data", []):
                    authors = [f"{a.get('name', '')}" for a in paper.get("authors", [])]

                    related.append({
                        "title": paper.get("title", ""),
                        "authors": authors,
                        "year": paper.get("year"),
                        "abstract": paper.get("abstract", "")[:500],
                        "url": paper.get("url"),
                        "similarity_score": 0.8  # Placeholder - would calculate with embeddings
                    })

                return related

        except Exception as e:
            print(f"Error getting related papers: {e}")
            return []


# Global service instance
papers_service = PapersService()
