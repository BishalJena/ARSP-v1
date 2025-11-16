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
        Translate multiple texts using Google Translate (smart chunking).

        Chunks texts into batches under 4500 chars each to stay within
        Google Translate's 5000 character limit while minimizing API calls.

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

        if not texts:
            return texts

        try:
            # Map language codes
            source = self.lang_map.get(source_language, source_language)
            target = self.lang_map.get(target_language, target_language)

            # Use a unique delimiter that won't appear in the text
            DELIMITER = "\n\n\n"
            MAX_CHARS = 4500  # Leave buffer below 5000 limit

            # Filter out empty texts and track their positions
            non_empty_texts = []
            non_empty_indices = []
            for i, text in enumerate(texts):
                if text and text.strip():
                    non_empty_texts.append(text)
                    non_empty_indices.append(i)

            if not non_empty_texts:
                return texts

            # Create chunks that fit within character limit
            chunks = []
            current_chunk = []
            current_length = 0

            for text in non_empty_texts:
                text_length = len(text) + len(DELIMITER)

                # If adding this text exceeds limit, start new chunk
                if current_length + text_length > MAX_CHARS and current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = [text]
                    current_length = len(text)
                else:
                    current_chunk.append(text)
                    current_length += text_length

            # Add the last chunk
            if current_chunk:
                chunks.append(current_chunk)

            print(f"📝 Translating {len(non_empty_texts)} segments in {len(chunks)} batch(es)...")

            # Translate each chunk
            translator = GoogleTranslator(source=source, target=target)
            all_translated = []

            for i, chunk in enumerate(chunks):
                # Combine chunk texts
                combined_text = DELIMITER.join(chunk)

                # Translate the chunk
                try:
                    translated_combined = translator.translate(combined_text)

                    if not translated_combined:
                        # If translation fails, use originals
                        all_translated.extend(chunk)
                        continue

                    # Split the translated chunk
                    translated_parts = translated_combined.split(DELIMITER)

                    # Validate split
                    if len(translated_parts) != len(chunk):
                        print(f"⚠️  Chunk {i+1} split mismatch: expected {len(chunk)}, got {len(translated_parts)}")
                        # Use original texts for this chunk
                        all_translated.extend(chunk)
                    else:
                        all_translated.extend(translated_parts)

                except Exception as e:
                    print(f"⚠️  Chunk {i+1} translation failed: {str(e)}")
                    # Use original texts for this chunk
                    all_translated.extend(chunk)

            # Build result list with translated texts in correct positions
            result = list(texts)  # Copy original list
            for idx, translated_text in zip(non_empty_indices, all_translated):
                result[idx] = translated_text

            print(f"✅ Translated {len(non_empty_texts)} segments in {len(chunks)} batch(es)!")
            return result

        except Exception as e:
            print(f"❌ Batch translation failed: {str(e)}")
            print("⚠️  Falling back to individual translation...")

            # Fallback to individual translation
            translated = []
            translator = GoogleTranslator(source=source, target=target)
            for text in texts:
                if not text or text.strip() == "":
                    translated.append(text)
                else:
                    try:
                        result = translator.translate(text)
                        translated.append(result if result else text)
                    except Exception as e:
                        print(f"⚠️  Individual translation failed: {str(e)}")
                        translated.append(text)
            return translated

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
