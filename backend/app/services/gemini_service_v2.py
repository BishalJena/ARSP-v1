"""
Enhanced Gemini service for research paper analysis.
Uses optimized prompts and structured JSON output.
"""

import json
import base64
import io
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
import asyncio
from PyPDF2 import PdfReader

from ..core.config import settings
from ..prompts.paper_analysis_prompt import (
    get_analysis_prompt,
    get_translation_prompt,
    PAPER_ANALYSIS_SCHEMA
)


def get_pdf_page_count(pdf_bytes: bytes) -> int:
    """
    Count the number of pages in a PDF.

    Args:
        pdf_bytes: PDF file as bytes

    Returns:
        Number of pages
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        return len(reader.pages)
    except Exception as e:
        print(f"⚠️  Could not count PDF pages: {str(e)}")
        return 10  # Default fallback


def calculate_max_tokens(page_count: int) -> int:
    """
    Calculate max_tokens based on PDF page count.

    Args:
        page_count: Number of pages in PDF

    Returns:
        Appropriate max_tokens value
    """
    # Allocation: ~800 tokens per page for comprehensive analysis
    tokens_per_page = 800
    calculated_tokens = page_count * tokens_per_page

    # Set reasonable bounds
    min_tokens = 4000   # At least 4k for any paper
    max_tokens = 16000  # Cap at 16k (Gemini 2.5 Flash supports up to 8192 output tokens, but we'll be safe)

    # Clamp to bounds
    tokens = max(min_tokens, min(calculated_tokens, max_tokens))

    print(f"📄 PDF has {page_count} pages → allocating {tokens} max_tokens")

    return tokens


class EnhancedGeminiService:
    """
    Service for analyzing research papers using Gemini 2.5 Flash Lite.
    PDFs are sent directly to Gemini for parsing and analysis (no text extraction needed).
    Optimized for speed, accuracy, and multilingual support.
    """

    def __init__(self):
        """Initialize the service with OpenRouter client."""
        # Get API key from settings with fallback to allow server to start
        api_key = settings.OPENROUTER_API_KEY
        if not api_key:
            api_key = "placeholder-key-not-set"

        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.api_key_configured = bool(settings.OPENROUTER_API_KEY)

        # Model selection
        self.analysis_model = "google/gemini-2.5-flash-lite"
        self.translation_model = "google/gemini-2.5-flash-lite"  # Same model, very fast

        # Performance tuning
        self.analysis_temperature = 0.3  # Lower for consistency
        self.translation_temperature = 0.2  # Even lower for accuracy

        # Timeout settings (comprehensive analysis takes longer)
        self.analysis_timeout = 90  # 90 seconds for comprehensive analysis
        self.translation_timeout = 20  # 20 seconds max

    async def analyze_paper(
        self,
        pdf_bytes: bytes,
        paper_type: str = "research",
        extract_length: str = "full"
    ) -> Dict[str, Any]:
        """
        Analyze a research paper PDF using Gemini 2.5 Flash Lite.
        PDF is sent directly to Gemini for parsing and analysis.

        Args:
            pdf_bytes: PDF file as bytes
            paper_type: Type of paper (research, review, clinical, ml)
            extract_length: "full" or "short" analysis

        Returns:
            Structured analysis as JSON dict

        Raises:
            Exception: If API call fails or timeout occurs
        """
        # Check if API key is configured
        if not self.api_key_configured:
            raise Exception(
                "OPENROUTER_API_KEY not configured. "
                "Please set it in your .env file to use the enhanced papers API."
            )

        try:
            # Count PDF pages for dynamic token allocation
            page_count = get_pdf_page_count(pdf_bytes)
            max_tokens = calculate_max_tokens(page_count)

            # Convert PDF to base64 for data URL
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

            # Get appropriate prompt
            system_prompt = get_analysis_prompt(paper_type, extract_length)

            # Send PDF directly to Gemini 2.5 Flash Lite via OpenRouter
            # Use the correct "file" content type with pdf-text engine (free)
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.analysis_model,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Please analyze this research paper PDF following the structured format."
                                },
                                {
                                    "type": "file",
                                    "file": {
                                        "filename": "paper.pdf",
                                        "file_data": f"data:application/pdf;base64,{pdf_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=self.analysis_temperature,
                    response_format={"type": "json_object"},
                    max_tokens=max_tokens,  # Dynamic allocation based on page count
                    extra_body={
                        "plugins": [
                            {
                                "id": "file-parser",
                                "pdf": {
                                    "engine": "pdf-text"  # Free text extraction
                                }
                            }
                        ]
                    }
                ),
                timeout=self.analysis_timeout
            )

            # Check if response was truncated
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "length":
                print("⚠️  Response was truncated due to max_tokens limit!")
                raise Exception(
                    "Response truncated. The analysis is too long. "
                    "Try using a shorter paper or increase max_tokens."
                )

            # Parse JSON response with error handling
            content = response.choices[0].message.content

            try:
                analysis = json.loads(content)
            except json.JSONDecodeError as e:
                # Try to fix common JSON issues
                print(f"⚠️  JSON parsing failed: {str(e)}")
                print(f"📊 Response length: {len(content)} chars")
                print(f"🏁 Finish reason: {finish_reason}")
                print("🔧 Attempting to repair JSON...")

                # Remove markdown code blocks if present
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                # Try parsing again
                try:
                    analysis = json.loads(content)
                    print("✅ JSON repaired successfully!")
                except json.JSONDecodeError:
                    # If still fails, provide partial response
                    print("❌ Could not repair JSON. Returning minimal response.")
                    print(f"Response preview:\n{content[:1000]}...")
                    raise Exception(
                        f"Gemini returned invalid JSON. "
                        f"Error: {str(e)}. "
                        f"This may be due to the PDF being too complex. "
                        f"Try a shorter or simpler PDF."
                    )

            # Add metadata
            analysis["_metadata"] = {
                "model": self.analysis_model,
                "paper_type": paper_type,
                "extract_length": extract_length,
                "page_count": page_count,
                "max_tokens_allocated": max_tokens,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "processing_time": "~1-3 seconds",
                "pdf_processing": "direct_to_gemini"
            }

            return analysis

        except asyncio.TimeoutError:
            raise Exception(f"Analysis timeout after {self.analysis_timeout} seconds")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response from Gemini: {str(e)}")
        except Exception as e:
            raise Exception(f"Paper analysis failed: {str(e)}")

    async def translate_analysis(
        self,
        analysis: Dict[str, Any],
        target_language: str,
        cache_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate paper analysis to target language.

        Args:
            analysis: Original analysis dict (usually in English)
            target_language: Target language name (e.g., "Hindi", "Spanish", "中文")
            cache_key: Optional cache key for storing translation

        Returns:
            Translated analysis dict with same structure

        Raises:
            Exception: If translation fails
        """
        try:
            # Prepare analysis for translation (remove metadata)
            analysis_copy = analysis.copy()
            analysis_copy.pop("_metadata", None)

            # Get translation prompt
            prompt = get_translation_prompt(
                json.dumps(analysis_copy, indent=2, ensure_ascii=False),
                target_language
            )

            # Call Gemini for translation
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.translation_model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=self.translation_temperature,
                    response_format={"type": "json_object"},
                    max_tokens=4000
                ),
                timeout=self.translation_timeout
            )

            # Parse translated response
            content = response.choices[0].message.content
            translated = json.loads(content)

            # Add translation metadata
            translated["_metadata"] = {
                "original_language": analysis.get("_metadata", {}).get("language", "en"),
                "translated_to": target_language,
                "translation_model": self.translation_model,
                "cache_key": cache_key
            }

            return translated

        except asyncio.TimeoutError:
            raise Exception(f"Translation timeout after {self.translation_timeout} seconds")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in translation: {str(e)}")
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")

    async def analyze_and_translate(
        self,
        pdf_bytes: bytes,
        target_language: str = "en",
        paper_type: str = "research"
    ) -> Dict[str, Any]:
        """
        Analyze paper and optionally translate in one go.

        Args:
            pdf_bytes: PDF file bytes
            target_language: Language for final output (default: English)
            paper_type: Type of paper

        Returns:
            Analysis in target language
        """
        # First, analyze in English (fastest)
        analysis = await self.analyze_paper(pdf_bytes, paper_type)

        # If not English, translate
        if target_language.lower() not in ["en", "english"]:
            analysis = await self.translate_analysis(analysis, target_language)

        return analysis

    async def batch_translate(
        self,
        analysis: Dict[str, Any],
        languages: list[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Translate analysis to multiple languages in parallel.

        Args:
            analysis: Original analysis
            languages: List of target languages

        Returns:
            Dict mapping language -> translated analysis
        """
        tasks = [
            self.translate_analysis(analysis, lang)
            for lang in languages
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        translations = {}
        for lang, result in zip(languages, results):
            if isinstance(result, Exception):
                translations[lang] = {"error": str(result)}
            else:
                translations[lang] = result

        return translations


# Singleton instance
enhanced_gemini_service = EnhancedGeminiService()
