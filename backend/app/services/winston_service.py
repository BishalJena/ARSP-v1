"""Winston AI plagiarism detection service."""
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import time
from ..core.config import settings


class WinstonAIService:
    """Service for plagiarism detection using Winston AI API."""

    def __init__(self):
        self.api_url = "https://api.gowinston.ai/v2/plagiarism"
        self.api_key = settings.WINSTON_API_KEY

    def _calculate_word_count(self, text: str) -> int:
        """Calculate word count from text."""
        if not text:
            return 0
        return len([word for word in text.split() if word.strip()])

    async def check_plagiarism(
        self,
        text: Optional[str] = None,
        file_url: Optional[str] = None,
        website: Optional[str] = None,
        excluded_sources: Optional[List[str]] = None,
        language: str = "auto",
        country: str = "us"
    ) -> Dict[str, Any]:
        """
        Check text, file, or website for plagiarism using Winston AI.

        Args:
            text: The text to be scanned (100-120,000 characters)
            file_url: URL to a publicly accessible PDF, DOC, or DOCX file
            website: URL to a website to scan
            excluded_sources: List of domains/URLs to exclude from scan
            language: 2-letter language code or 'auto' for auto-detection
            country: Country code (default: 'us')

        Returns:
            Dictionary containing plagiarism results with sources, indexes, and scores

        Note:
            - Priority: website > file_url > text
            - At least one of text, file_url, or website must be provided
            - Text must be 100-120,000 characters
            - Supports 45 languages
        """
        start_time = time.time()

        if not text and not file_url and not website:
            raise ValueError("At least one of text, file_url, or website must be provided")

        if text and len(text) < 100:
            raise ValueError("Text must be at least 100 characters")

        if text and len(text) > 120000:
            raise ValueError("Text must not exceed 120,000 characters")

        try:
            # Prepare request payload
            payload = {
                "language": language,
                "country": country
            }

            # Priority: website > file > text
            if website:
                payload["website"] = website
            elif file_url:
                payload["file"] = file_url
            elif text:
                payload["text"] = text

            if excluded_sources:
                payload["excluded_sources"] = excluded_sources

            # Make API request
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload
                )

                if response.status_code != 200:
                    error_data = response.json() if response.text else {}
                    raise Exception(
                        f"Winston AI API error (status {response.status_code}): "
                        f"{error_data.get('message', response.text)}"
                    )

                result = response.json()

                # Extract and format the response
                formatted_result = self._format_response(result, start_time, text)

                return formatted_result

        except httpx.TimeoutException:
            raise Exception("Winston AI API request timed out. Please try again.")
        except httpx.RequestError as e:
            raise Exception(f"Winston AI API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Plagiarism check failed: {str(e)}")

    def _format_response(self, raw_response: Dict[str, Any], start_time: float, input_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Format Winston AI response into a standardized structure.

        Args:
            raw_response: Raw response from Winston AI API
            start_time: Request start time for calculating processing time
            input_text: Original input text for calculating word count

        Returns:
            Formatted response with normalized field names
        """
        processing_time = time.time() - start_time

        # Extract main result data
        result = raw_response.get("result", {})
        scan_info = raw_response.get("scanInformation", {})
        sources = raw_response.get("sources", [])
        attack_detected = raw_response.get("attackDetected", {})
        similar_words = raw_response.get("similarWords", [])
        citations = raw_response.get("citations", [])
        indexes = raw_response.get("indexes", [])

        # Calculate word count from input text if available
        calculated_word_count = self._calculate_word_count(input_text) if input_text else 0

        # Calculate originality score
        # Winston gives plagiarism score, we convert to originality
        plagiarism_score = result.get("score", 0)
        originality_score = max(0, 100 - plagiarism_score)

        # Format flagged sections from sources
        flagged_sections = []
        for source in sources:
            source_url = source.get("url", "")
            source_title = source.get("title", source_url)
            similarity = source.get("plagiarismScore", 0)

            # Get matching text from indexes for this source
            for index in indexes:
                if index.get("url") == source_url:
                    flagged_sections.append({
                        "text": index.get("text", ""),
                        "start_index": index.get("startIndex", 0),
                        "end_index": index.get("endIndex", 0),
                        "similarity": similarity,
                        "source": source_title,
                        "source_url": source_url,
                        "snippet": source.get("snippet", "")
                    })

        # Format detailed sources
        detailed_sources = [
            {
                "url": source.get("url", ""),
                "title": source.get("title", ""),
                "snippet": source.get("snippet", ""),
                "plagiarism_score": source.get("plagiarismScore", 0),
                "word_count": source.get("wordCount", 0),
                "matched_words": source.get("matchedWords", 0)
            }
            for source in sources
        ]

        # Format similar words
        formatted_similar_words = [
            {
                "word": word.get("word", ""),
                "frequency": word.get("frequency", 0),
                "sources": word.get("sources", [])
            }
            for word in similar_words
        ]

        # Format plagiarism indexes
        formatted_indexes = [
            {
                "text": idx.get("text", ""),
                "start_index": idx.get("startIndex", 0),
                "end_index": idx.get("endIndex", 0),
                "url": idx.get("url", ""),
                "plagiarism_score": idx.get("score", 0)
            }
            for idx in indexes
        ]

        # Use Winston's word count if available, otherwise use calculated
        total_word_count = result.get("totalWordCount") or scan_info.get("wordCount") or calculated_word_count

        # Calculate plagiarized word count based on plagiarism score
        plagiarized_word_count = result.get("plagiarizedWordCount")
        if plagiarized_word_count is None or plagiarized_word_count == 0:
            # Estimate based on plagiarism score percentage
            plagiarized_word_count = int(total_word_count * (plagiarism_score / 100)) if total_word_count > 0 else 0

        return {
            # Core plagiarism metrics
            "originality_score": round(originality_score, 2),
            "plagiarism_score": round(plagiarism_score, 2),
            "total_word_count": total_word_count,
            "total_text_score": result.get("totalTextScore", 0),
            "plagiarized_word_count": plagiarized_word_count,

            # Flagged sections (compatible with existing frontend)
            "flagged_sections": flagged_sections[:20],  # Limit to top 20

            # Detailed sources
            "sources": detailed_sources[:20],

            # Similar words analysis
            "similar_words": formatted_similar_words[:50],

            # Plagiarism indexes (exact matches)
            "indexes": formatted_indexes[:50],

            # Citations found in text
            "citations": citations[:20],

            # Attack detection
            "attack_detected": {
                "zero_width_spaces": attack_detected.get("zeroWidthSpaces", False),
                "homoglyph_attack": attack_detected.get("homoglyphAttack", False)
            },

            # Scan information
            "scan_info": {
                "word_count": total_word_count,  # Use our calculated/combined word count
                "character_count": scan_info.get("characterCount") or (len(input_text) if input_text else 0),
                "language_detected": scan_info.get("languageDetected", "unknown"),
                "sources_checked": len(sources)
            },

            # Credits usage
            "credits_used": raw_response.get("credits_used", 0),
            "credits_remaining": raw_response.get("credits_remaining", 0),

            # Metadata
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "processing_time_seconds": round(processing_time, 2),
            "provider": "winston_ai"
        }

    async def get_credits_info(self) -> Dict[str, Any]:
        """
        Get remaining credits information.

        Returns:
            Dictionary with credits information
        """
        try:
            # Winston AI doesn't have a dedicated credits endpoint
            # Credits info is returned with each plagiarism check
            # This is a placeholder for future implementation
            return {
                "message": "Credits info is included in each plagiarism check response",
                "cost_per_word": 2  # 2 credits per word
            }
        except Exception as e:
            raise Exception(f"Failed to get credits info: {str(e)}")


# Global service instance
winston_service = WinstonAIService()
