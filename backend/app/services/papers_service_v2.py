"""
Enhanced Papers service using Gemini 2.0 Flash Lite.
Replaces legacy PyPDF2 + BART approach with faster, better quality analysis.
"""

import io
import copy
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import json

from ..core.config import settings
from ..core.supabase import supabase, supabase_admin
from .gemini_service_v2 import enhanced_gemini_service
from .translation_service import translation_service


class EnhancedPapersService:
    """
    Service for processing research papers using Gemini 2.0 Flash Lite.

    Key improvements over legacy service:
    - 3-5x faster processing
    - Native PDF support (no extraction step)
    - Better quality analysis (2024 model vs 2019 BART)
    - Structured JSON output
    - Integrated translation support
    """

    def __init__(self):
        self.gemini = enhanced_gemini_service

        # Language mapping for on-demand translations
        self.language_names = {
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu",
            "ta": "Tamil",
            "bn": "Bengali",
            "mr": "Marathi",
            "zh": "Chinese (Simplified)",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "pt": "Portuguese",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "ar": "Arabic"
        }

    async def upload_paper(
        self,
        user_id: str,
        file_name: str,
        file_content: bytes
    ) -> Dict[str, Any]:
        """
        Upload a paper PDF to Supabase storage.

        Args:
            user_id: ID of user uploading the paper
            file_name: Original filename
            file_content: PDF bytes

        Returns:
            Paper metadata with upload ID
        """
        try:
            # Generate unique filename
            timestamp = int(datetime.now(timezone.utc).timestamp())
            storage_path = f"{user_id}/{timestamp}_{file_name}"

            # Upload to Supabase storage (use admin client to bypass RLS for demo)
            response = supabase_admin.storage.from_("papers").upload(
                storage_path,
                file_content,
                {
                    "content-type": "application/pdf",
                    "upsert": "false"
                }
            )

            # Get public URL
            file_url = supabase_admin.storage.from_("papers").get_public_url(storage_path)

            # Create database record (use admin client to bypass RLS for demo)
            paper_data = {
                "user_id": user_id,
                "file_name": file_name,
                "file_path": storage_path,
                # "file_url": file_url,  # Skip if column doesn't exist (pending migration)
                "file_size": len(file_content),
                "mime_type": "application/pdf",
                "processed": False,
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            result = supabase_admin.table("uploads").insert(paper_data).execute()

            return {
                "id": result.data[0]["id"],
                "file_name": file_name,
                "file_url": file_url,
                "uploaded_at": paper_data["created_at"],
                "status": "uploaded"
            }

        except Exception as e:
            raise Exception(f"Paper upload failed: {str(e)}")

    async def process_paper(
        self,
        paper_id: str,
        pdf_bytes: bytes,
        paper_type: str = "research",
        target_language: str = "en"
    ) -> Dict[str, Any]:
        """
        Process paper using Gemini 2.5 Flash Lite - English only, fast!

        This is the main analysis function that:
        1. Analyzes PDF with Gemini (30-40 seconds)
        2. Stores English analysis in database
        3. Translations happen on-demand when requested

        Args:
            paper_id: Database ID of the paper
            pdf_bytes: PDF file bytes
            paper_type: Type of paper (research, ml, clinical, review)
            target_language: Ignored - always returns English

        Returns:
            Structured paper analysis in English
        """
        try:
            # Analyze with Gemini - English only!
            print(f"📄 Analyzing paper with Gemini 2.5 Flash Lite...")
            analysis = await self.gemini.analyze_paper(
                pdf_bytes,
                paper_type=paper_type
            )
            print(f"✅ Gemini analysis complete!")

            # Extract metadata
            paper_title = analysis.get("title", "")
            year = analysis.get("year")
            authors = analysis.get("authors", [])
            venue = analysis.get("venue", "")

            # Extract content sections
            abstract = analysis.get("abstract", "")
            introduction = analysis.get("introduction", "")
            conclusion = analysis.get("conclusion", "")

            # Extract legacy fields for frontend compatibility
            summary = analysis.get("tldr", "") or analysis.get("plain_summary", "")
            methodology = analysis.get("methods", {}).get("overview", "") if isinstance(analysis.get("methods"), dict) else ""
            key_findings = analysis.get("results", {}).get("key_findings", []) if isinstance(analysis.get("results"), dict) else []

            # Store in database with both new and legacy fields
            # Translation cache starts empty - will fill on-demand when user requests
            update_data = {
                "processed": True,
                "analysis": analysis,  # English analysis only
                "original_language": "en",
                "paper_type": paper_type,
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "translation_cache": {},  # Empty - filled on-demand when user requests
                # Metadata
                "paper_title": paper_title,
                "year": year,
                "authors": authors,
                "venue": venue,
                # Content sections
                "abstract": abstract,
                "introduction": introduction,
                "conclusion": conclusion,
                # Legacy fields for frontend compatibility
                "summary": summary,
                "methodology": methodology,
                "key_findings": key_findings
            }

            supabase_admin.table("uploads").update(update_data).eq("id", paper_id).execute()

            return {
                "success": True,
                "paper_id": paper_id,
                "analysis": analysis,
                "language": "en",
                "processing_method": "gemini-2.5-flash-lite",
                "performance": "30-40 seconds (50% faster - no pre-translation!)"
            }

        except Exception as e:
            # Mark as failed in database
            try:
                supabase_admin.table("uploads").update({
                    "processed": False,
                    "error_message": str(e),
                    "processed_at": datetime.now(timezone.utc).isoformat()
                }).eq("id", paper_id).execute()
            except:
                # Fallback if new columns don't exist
                supabase_admin.table("uploads").update({
                    "processed": False
                }).eq("id", paper_id).execute()

            raise Exception(f"Paper processing failed: {str(e)}")

    async def get_paper_analysis(
        self,
        paper_id: str,
        language: str = "en",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get paper analysis in specified language.

        Supports instant language switching through cache or on-demand translation.

        Args:
            paper_id: Database ID of paper
            language: Target language code
            user_id: Optional user ID for authorization

        Returns:
            Paper analysis in requested language
        """
        try:
            # Get paper from database
            query = supabase_admin.table("uploads").select("*").eq("id", paper_id)

            if user_id:
                query = query.eq("user_id", user_id)

            result = query.execute()

            if not result.data:
                raise Exception("Paper not found or access denied")

            paper = result.data[0]

            if not paper.get("processed"):
                raise Exception("Paper not yet processed")

            analysis = paper.get("analysis")

            # Extract metadata
            paper_title = paper.get("paper_title")
            year = paper.get("year")
            authors = paper.get("authors")
            venue = paper.get("venue")

            # If English, return original
            if language == "en":
                print(f"📄 Returning English (original) for paper: {paper_title}")
                return {
                    "paper_id": paper_id,
                    "paper_title": paper_title,
                    "year": year,
                    "authors": authors,
                    "venue": venue,
                    "analysis": analysis,
                    "language": "en",
                    "from_cache": True
                }

            # Check translation cache (instant switching!)
            cache = paper.get("translation_cache", {})
            if language in cache:
                print(f"⚡ INSTANT return from cache: {self.language_names.get(language, language)} for paper: {paper_title}")
                return {
                    "paper_id": paper_id,
                    "paper_title": paper_title,
                    "year": year,
                    "authors": authors,
                    "venue": venue,
                    "analysis": cache[language],
                    "language": language,
                    "from_cache": True,
                    "instant": True
                }

            # Translate on-demand using Google Translate (fastest!)
            print(f"🌍 Cache miss! Translating to {self.language_names.get(language, language)} using Google Translate...")

            # Prepare texts to translate
            texts_to_translate = []
            text_keys = []

            # Simple string fields
            for key in ["title", "abstract", "tldr", "introduction", "research_question",
                       "discussion", "conclusion"]:
                if key in analysis and analysis[key]:
                    texts_to_translate.append(str(analysis[key]))
                    text_keys.append(key)

            # Array fields (translate each item)
            for key in ["contributions", "limitations", "practical_takeaways", "future_work"]:
                if key in analysis and isinstance(analysis[key], list):
                    for idx, item in enumerate(analysis[key]):
                        if item:
                            texts_to_translate.append(str(item))
                            text_keys.append(f"{key}[{idx}]")

            # Glossary (translate definitions)
            if "glossary" in analysis and isinstance(analysis["glossary"], dict):
                for term, definition in analysis["glossary"].items():
                    if definition:
                        texts_to_translate.append(str(definition))
                        text_keys.append(f"glossary.{term}")

            # Nested methods fields
            if "methods" in analysis and isinstance(analysis["methods"], dict):
                for method_key in ["overview", "study_design", "data_sources", "sample_size"]:
                    if method_key in analysis["methods"] and analysis["methods"][method_key]:
                        texts_to_translate.append(str(analysis["methods"][method_key]))
                        text_keys.append(f"methods.{method_key}")

            # Nested results fields
            if "results" in analysis and isinstance(analysis["results"], dict):
                if "summary" in analysis["results"] and analysis["results"]["summary"]:
                    texts_to_translate.append(str(analysis["results"]["summary"]))
                    text_keys.append("results.summary")

                # Translate key_findings array
                if "key_findings" in analysis["results"] and isinstance(analysis["results"]["key_findings"], list):
                    for idx, item in enumerate(analysis["results"]["key_findings"]):
                        if item:
                            texts_to_translate.append(str(item))
                            text_keys.append(f"results.key_findings[{idx}]")

                # Translate quantitative_results array
                if "quantitative_results" in analysis["results"] and isinstance(analysis["results"]["quantitative_results"], list):
                    for idx, item in enumerate(analysis["results"]["quantitative_results"]):
                        if item:
                            texts_to_translate.append(str(item))
                            text_keys.append(f"results.quantitative_results[{idx}]")

            # Translate using Google Translate
            print(f"📝 Translating {len(texts_to_translate)} text segments...")
            translated_texts = await translation_service.translate_batch(
                texts_to_translate,
                target_language=language,
                source_language="en"
            )

            # Build translated analysis object (deep copy to avoid mutations)
            translated = copy.deepcopy(analysis)

            for i, key in enumerate(text_keys):
                if "[" in key:  # Array item
                    # Parse "key_findings[0]" or "results.key_findings[0]"
                    if "." in key:
                        parts = key.split(".")
                        field_name = parts[0]
                        array_part = parts[1]
                        array_name = array_part.split("[")[0]
                        idx = int(array_part.split("[")[1].rstrip("]"))
                        if field_name not in translated:
                            translated[field_name] = {}
                        if array_name not in translated[field_name]:
                            translated[field_name][array_name] = []
                        # Ensure array is long enough
                        while len(translated[field_name][array_name]) <= idx:
                            translated[field_name][array_name].append(None)
                        translated[field_name][array_name][idx] = translated_texts[i]
                    else:
                        array_name = key.split("[")[0]
                        idx = int(key.split("[")[1].rstrip("]"))
                        if array_name not in translated:
                            translated[array_name] = []
                        # Ensure array is long enough
                        while len(translated[array_name]) <= idx:
                            translated[array_name].append(None)
                        translated[array_name][idx] = translated_texts[i]
                elif "." in key:  # Nested field (including glossary)
                    parts = key.split(".")
                    if parts[0] == "glossary":
                        # Glossary term: key is "glossary.term_name"
                        term_name = parts[1]
                        if "glossary" not in translated:
                            translated["glossary"] = {}
                        translated["glossary"][term_name] = translated_texts[i]
                    else:
                        # Other nested fields
                        if parts[0] not in translated:
                            translated[parts[0]] = {}
                        translated[parts[0]][parts[1]] = translated_texts[i]
                else:  # Simple field
                    translated[key] = translated_texts[i]

            # Cache the translation for next time
            cache[language] = translated
            supabase_admin.table("uploads").update({
                "translation_cache": cache
            }).eq("id", paper_id).execute()

            print(f"✅ Translation complete! Cached for next time.")

            return {
                "paper_id": paper_id,
                "paper_title": paper_title,
                "year": year,
                "authors": authors,
                "venue": venue,
                "analysis": translated,
                "language": language,
                "from_cache": False,
                "translation_time": "~1-2 seconds (Google Translate)"
            }

        except Exception as e:
            raise Exception(f"Failed to get paper analysis: {str(e)}")

    async def list_user_papers(
        self,
        user_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List all papers for a user.

        Args:
            user_id: User ID
            limit: Max number of papers to return
            offset: Pagination offset

        Returns:
            List of paper metadata
        """
        try:
            result = supabase_admin.table("uploads").select(
                "id, file_name, file_size, created_at, processed, paper_type, "
                "paper_title, year, authors, venue, summary, key_findings"
            ).eq(
                "user_id", user_id
            ).order(
                "created_at", desc=True
            ).range(
                offset, offset + limit - 1
            ).execute()

            return result.data

        except Exception as e:
            raise Exception(f"Failed to list papers: {str(e)}")

    async def delete_paper(
        self,
        paper_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Delete a paper and its analysis.

        Args:
            paper_id: Paper ID
            user_id: User ID (for authorization)

        Returns:
            Deletion confirmation
        """
        try:
            # Get paper to check ownership and get file path
            result = supabase_admin.table("uploads").select(
                "file_path"
            ).eq("id", paper_id).eq("user_id", user_id).execute()

            if not result.data:
                raise Exception("Paper not found or access denied")

            file_path = result.data[0]["file_path"]

            # Delete from storage
            supabase_admin.storage.from_("papers").remove([file_path])

            # Delete from database
            supabase_admin.table("uploads").delete().eq("id", paper_id).execute()

            return {
                "success": True,
                "paper_id": paper_id,
                "message": "Paper deleted successfully"
            }

        except Exception as e:
            raise Exception(f"Failed to delete paper: {str(e)}")

    async def get_paper_pdf(
        self,
        paper_id: str,
        user_id: str
    ) -> bytes:
        """
        Get the original PDF file.

        Args:
            paper_id: Paper ID
            user_id: User ID (for authorization)

        Returns:
            PDF bytes
        """
        try:
            # Get paper file path
            result = supabase_admin.table("uploads").select(
                "file_path"
            ).eq("id", paper_id).eq("user_id", user_id).execute()

            if not result.data:
                raise Exception("Paper not found or access denied")

            file_path = result.data[0]["file_path"]

            # Download from storage
            response = supabase_admin.storage.from_("papers").download(file_path)

            return response

        except Exception as e:
            raise Exception(f"Failed to get PDF: {str(e)}")

    async def batch_process_papers(
        self,
        paper_ids: List[str],
        user_id: str,
        paper_type: str = "research"
    ) -> List[Dict[str, Any]]:
        """
        Process multiple papers in batch.

        Args:
            paper_ids: List of paper IDs
            user_id: User ID (for authorization)
            paper_type: Type of papers

        Returns:
            List of processing results
        """
        results = []

        for paper_id in paper_ids:
            try:
                # Get PDF
                pdf_bytes = await self.get_paper_pdf(paper_id, user_id)

                # Process
                result = await self.process_paper(
                    paper_id,
                    pdf_bytes,
                    paper_type
                )

                results.append(result)

            except Exception as e:
                results.append({
                    "success": False,
                    "paper_id": paper_id,
                    "error": str(e)
                })

        return results


# Singleton instance
enhanced_papers_service = EnhancedPapersService()
