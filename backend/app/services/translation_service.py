"""Translation service using Google Translate (via deep-translator)."""
import httpx
from typing import Dict, List, Optional, Any
from app.core.config import settings
from deep_translator import GoogleTranslator


class TranslationService:
    """Service for translating text using Google Translate."""

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
        # Language code mapping for Google Translate
        self.lang_map = {
            'zh': 'zh-CN',  # Chinese simplified
            'te': 'te',     # Telugu
            'ta': 'ta',     # Tamil
            'hi': 'hi',     # Hindi
            'es': 'es',     # Spanish
            'fr': 'fr',     # French
            'de': 'de',     # German
            'ja': 'ja',     # Japanese
            'ko': 'ko',     # Korean
            'pt': 'pt',     # Portuguese
            'bn': 'bn',     # Bengali
            'mr': 'mr',     # Marathi
            'en': 'en'      # English
        }

    async def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: str = "en",
        context: Optional[List[str]] = None,
    ) -> str:
        """
        Translate text from source to target language using Google Translate.

        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'hi', 'zh', 'es')
            source_language: Source language code (default: 'en')
            context: Optional context tags (not used with Google Translate)

        Returns:
            Translated text
        """
        # If target is the same as source, return original text
        if target_language == source_language:
            return text

        # If text is empty, return it
        if not text or text.strip() == "":
            return text

        try:
            # Map language codes
            source = self.lang_map.get(source_language, source_language)
            target = self.lang_map.get(target_language, target_language)

            # Use Google Translate
            translator = GoogleTranslator(source=source, target=target)
            translated = translator.translate(text)
            return translated if translated else text

        except Exception as e:
            # Fallback to original text if translation fails
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
        Translate multiple texts using Google Translate.

        Args:
            texts: List of texts to translate
            target_language: Target language code
            source_language: Source language code (default: 'en')
            context: Optional context tags (not used)

        Returns:
            List of translated texts
        """
        if target_language == source_language:
            return texts

        try:
            # Map language codes
            source = self.lang_map.get(source_language, source_language)
            target = self.lang_map.get(target_language, target_language)

            # Translate each text
            translated = []
            translator = GoogleTranslator(source=source, target=target)

            for text in texts:
                if not text or text.strip() == "":
                    translated.append(text)
                else:
                    try:
                        result = translator.translate(text)
                        translated.append(result if result else text)
                    except:
                        translated.append(text)

            return translated

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
