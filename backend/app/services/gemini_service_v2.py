"""
Enhanced Gemini service for research paper analysis.
Uses optimized prompts and structured JSON output.
"""

import json
import base64
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
import asyncio

from ..core.config import settings
from ..prompts.paper_analysis_prompt import (
    get_analysis_prompt,
    get_translation_prompt,
    PAPER_ANALYSIS_SCHEMA
)


class EnhancedGeminiService:
    """
    Service for analyzing research papers using Gemini 2.0 Flash Lite.
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
        self.analysis_model = "google/gemini-2.0-flash-lite-001"
        self.translation_model = "google/gemini-2.0-flash-lite-001"  # Same model, very fast

        # Performance tuning
        self.analysis_temperature = 0.3  # Lower for consistency
        self.translation_temperature = 0.2  # Even lower for accuracy

        # Timeout settings (Gemini is fast!)
        self.analysis_timeout = 30  # 30 seconds max
        self.translation_timeout = 10  # 10 seconds max

    async def analyze_paper(
        self,
        pdf_bytes: bytes,
        paper_type: str = "research",
        extract_length: str = "full"
    ) -> Dict[str, Any]:
        """
        Analyze a research paper PDF using Gemini 2.0 Flash Lite.

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
            # Convert PDF to base64
            pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

            # Get appropriate prompt
            system_prompt = get_analysis_prompt(paper_type, extract_length)

            # Call Gemini API with structured output
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
                                    "text": "Please analyze this research paper following the structured format."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:application/pdf;base64,{pdf_base64}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=self.analysis_temperature,
                    response_format={"type": "json_object"},
                    max_tokens=4000  # Comprehensive analysis
                ),
                timeout=self.analysis_timeout
            )

            # Parse JSON response
            content = response.choices[0].message.content
            analysis = json.loads(content)

            # Add metadata
            analysis["_metadata"] = {
                "model": self.analysis_model,
                "paper_type": paper_type,
                "extract_length": extract_length,
                "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                "processing_time": "~1-3 seconds"
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
