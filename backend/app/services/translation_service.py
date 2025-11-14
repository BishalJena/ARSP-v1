"""Translation service using Lingo.dev API."""
import httpx
from typing import Dict, List, Optional, Any
from app.core.config import settings


class TranslationService:
    """Service for translating text using Lingo.dev API."""

    def __init__(self):
        self.api_url = "https://api.lingo.dev/v1"
        self.api_key = settings.LINGO_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.academic_context = [
            "research",
            "paper",
            "journal",
            "citation",
            "plagiarism",
            "academic",
            "scientific",
        ]

    async def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: str = "en",
        context: Optional[List[str]] = None,
    ) -> str:
        """
        Translate text from source to target language.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'hi', 'zh', 'es')
            source_language: Source language code (default: 'en')
            context: Optional context tags for better translation

        Returns:
            Translated text
        """
        # If target is the same as source, return original text
        if target_language == source_language:
            return text

        # If Lingo API key is not set, return original text
        if not self.api_key or self.api_key == "":
            return text

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "text": text,
                    "source_locale": source_language,
                    "target_locale": target_language,
                    "context": context or self.academic_context,
                }

                response = await client.post(
                    f"{self.api_url}/translate", headers=self.headers, json=payload
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("translated_text", text)
                else:
                    # Fallback to original text if translation fails
                    return text

        except Exception as e:
            # Fallback to original text if API call fails
            print(f"Translation failed: {str(e)}")
            return text

    async def translate_batch(
        self,
        texts: List[str],
        target_language: str,
        source_language: str = "en",
        context: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Translate multiple texts in a single request.

        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code (default: 'en')
            context: Optional context tags

        Returns:
            List of translated texts
        """
        if target_language == source_language:
            return texts

        if not self.api_key or self.api_key == "":
            return texts

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "texts": texts,
                    "source_locale": source_language,
                    "target_locale": target_language,
                    "context": context or self.academic_context,
                }

                response = await client.post(
                    f"{self.api_url}/translate/batch",
                    headers=self.headers,
                    json=payload,
                )

                if response.status_code == 200:
                    data = response.json()
                    return data.get("translated_texts", texts)
                else:
                    return texts

        except Exception as e:
            print(f"Batch translation failed: {str(e)}")
            return texts

    async def translate_query(
        self, query: str, target_language: str = "en", source_language: str = "auto"
    ) -> str:
        """
        Translate user query to English for API calls.

        This is used to translate user input from any language to English
        before making API calls to external services.

        Args:
            query: User query in any language
            target_language: Target language (default: 'en')
            source_language: Source language ('auto' for auto-detection)

        Returns:
            Translated query in target language
        """
        if source_language == "auto":
            # Use Lingo's auto-detection
            return await self.translate_text(
                query, target_language, "auto", context=["search", "query"]
            )
        else:
            return await self.translate_text(
                query, target_language, source_language, context=["search", "query"]
            )

    async def translate_results(
        self, results: List[Dict[str, Any]], target_language: str, fields: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Translate specified fields in a list of result dictionaries.

        Args:
            results: List of result dictionaries
            target_language: Target language code
            fields: List of field names to translate

        Returns:
            List of results with translated fields
        """
        if target_language == "en":
            return results

        if not self.api_key or self.api_key == "":
            return results

        try:
            # Collect all texts to translate
            texts_to_translate = []
            for result in results:
                for field in fields:
                    if field in result and result[field]:
                        texts_to_translate.append(str(result[field]))

            # Translate all texts in batch
            translated_texts = await self.translate_batch(
                texts_to_translate, target_language
            )

            # Map translated texts back to results
            text_index = 0
            for result in results:
                for field in fields:
                    if field in result and result[field]:
                        result[field] = translated_texts[text_index]
                        text_index += 1

            return results

        except Exception as e:
            print(f"Result translation failed: {str(e)}")
            return results


# Global translation service instance
translation_service = TranslationService()
