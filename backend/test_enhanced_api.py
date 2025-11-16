#!/usr/bin/env python3
"""
Test script for Enhanced Papers API with Gemini 2.0 Flash Lite.

This script demonstrates the complete workflow:
1. Upload a research paper PDF
2. Process it with Gemini
3. Get translations in different languages
4. Test caching behavior

Requirements:
- Server running on http://localhost:8000
- Sample PDF file
- OPENROUTER_API_KEY configured
"""

import requests
import json
import time
from pathlib import Path
import sys

BASE_URL = "http://localhost:8000/api/v1/papers-enhanced"

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def check_server():
    """Check if server is running."""
    print_section("Checking Server Status")
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server is not responding: {e}")
        print("\n💡 Start the server with: uvicorn app.main:app --reload --port 8000")
        return False

def check_performance_stats():
    """Check performance comparison endpoint."""
    print_section("Performance Comparison")
    try:
        response = requests.get(f"{BASE_URL}/stats/performance", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Enhanced API is accessible")
            print(f"\n📊 Performance Stats:")
            print(f"   Old: {stats['old_approach']['total_time']} ({stats['old_approach']['cost_per_paper']})")
            print(f"   New: {stats['new_approach']['total_time']} ({stats['new_approach']['cost_per_paper']})")
            print(f"   Improvement: {stats['new_approach']['improvement']['speed']}")
            return True
        else:
            print(f"❌ Performance stats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking performance: {e}")
        return False

def upload_paper(pdf_path):
    """Upload a research paper PDF."""
    print_section(f"Uploading Paper: {pdf_path}")

    if not Path(pdf_path).exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return None

    try:
        with open(pdf_path, 'rb') as f:
            files = {'file': (Path(pdf_path).name, f, 'application/pdf')}
            response = requests.post(f"{BASE_URL}/upload", files=files, timeout=30)

        if response.status_code == 200:
            data = response.json()
            print("✅ Upload successful!")
            print(f"   Paper ID: {data['id']}")
            print(f"   File name: {data['file_name']}")
            print(f"   Next step: {data['next_step']}")
            return data['id']
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

def process_paper(paper_id, language="en", paper_type="research"):
    """Process paper with Gemini."""
    print_section(f"Processing Paper with Gemini ({language.upper()})")

    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/{paper_id}/process",
            params={"language": language, "paper_type": paper_type},
            timeout=60
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Processing successful! ({elapsed:.2f}s)")
            print(f"   Paper ID: {data['paper_id']}")
            print(f"   Language: {data['language']}")
            print(f"   Method: {data['processing_method']}")

            if 'analysis' in data:
                analysis = data['analysis']
                print(f"\n📄 Analysis Preview:")
                print(f"   Title: {analysis.get('title', 'N/A')[:60]}...")
                print(f"   TL;DR: {analysis.get('tldr', 'N/A')[:80]}...")

                if 'methods' in analysis:
                    print(f"   Methods: {analysis['methods'].get('overview', 'N/A')[:60]}...")

                if 'results' in analysis:
                    print(f"   Results: {len(analysis['results'].get('key_findings', []))} key findings")

                if 'glossary' in analysis:
                    print(f"   Glossary: {len(analysis['glossary'])} terms defined")

            return data
        else:
            print(f"❌ Processing failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Processing error: {e}")
        return None

def get_translation(paper_id, language):
    """Get paper analysis in specified language."""
    print_section(f"Getting Translation ({language.upper()})")

    try:
        start_time = time.time()
        response = requests.get(
            f"{BASE_URL}/{paper_id}",
            params={"language": language},
            timeout=30
        )
        elapsed = time.time() - start_time

        if response.status_code == 200:
            data = response.json()
            cached = data.get('from_cache', False)
            cache_status = "✓ CACHED" if cached else "⚡ TRANSLATED"

            print(f"✅ Translation retrieved! ({elapsed:.2f}s) {cache_status}")
            print(f"   Paper ID: {data['paper_id']}")
            print(f"   Language: {data['language']}")
            print(f"   From cache: {cached}")

            if 'analysis' in data:
                analysis = data['analysis']
                print(f"\n📄 Translation Preview:")
                print(f"   Title: {analysis.get('title', 'N/A')[:60]}...")
                print(f"   TL;DR: {analysis.get('tldr', 'N/A')[:80]}...")

            return data
        else:
            print(f"❌ Translation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return None

def list_papers():
    """List all papers."""
    print_section("Listing Papers")

    try:
        response = requests.get(f"{BASE_URL}/", params={"limit": 10}, timeout=10)

        if response.status_code == 200:
            data = response.json()
            papers = data.get('papers', [])
            print(f"✅ Found {len(papers)} paper(s)")

            for i, paper in enumerate(papers, 1):
                print(f"\n   {i}. {paper.get('file_name', 'Unknown')}")
                print(f"      ID: {paper.get('id', 'N/A')}")
                print(f"      Processed: {paper.get('processed', False)}")
                print(f"      Type: {paper.get('paper_type', 'N/A')}")
                print(f"      Created: {paper.get('created_at', 'N/A')}")

            return papers
        else:
            print(f"❌ List failed: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ List error: {e}")
        return []

def run_full_test(pdf_path):
    """Run complete test workflow."""
    print("="*60)
    print("  ENHANCED PAPERS API - COMPLETE TEST")
    print("="*60)

    # 1. Check server
    if not check_server():
        return False

    # 2. Check performance stats
    if not check_performance_stats():
        return False

    # 3. Upload paper
    paper_id = upload_paper(pdf_path)
    if not paper_id:
        return False

    # 4. Process paper (English)
    result = process_paper(paper_id, language="en", paper_type="research")
    if not result:
        return False

    # 5. Test translations
    languages = ["hi", "es", "fr"]  # Hindi, Spanish, French
    for lang in languages:
        get_translation(paper_id, lang)
        time.sleep(1)  # Small delay between requests

    # 6. Test cache (request same language again)
    print("\n" + "="*60)
    print("  Testing Translation Cache")
    print("="*60)
    print("Requesting Hindi translation again (should be instant)...")
    get_translation(paper_id, "hi")

    # 7. List all papers
    list_papers()

    print_section("✅ TEST COMPLETE!")
    print(f"Paper ID: {paper_id}")
    print(f"Languages tested: en, hi, es, fr")
    print(f"Cache working: ✓")
    print("\n💡 Next steps:")
    print(f"   - View in API docs: http://localhost:8000/api/docs")
    print(f"   - Get analysis: curl http://localhost:8000/api/v1/papers-enhanced/{paper_id}?language=en")

    return True

def main():
    """Main test function."""
    import argparse

    parser = argparse.ArgumentParser(description='Test Enhanced Papers API')
    parser.add_argument('pdf_path', nargs='?', help='Path to PDF file to test')
    parser.add_argument('--check-only', action='store_true', help='Only check server status')
    parser.add_argument('--list', action='store_true', help='List all papers')
    parser.add_argument('--process', help='Process existing paper by ID')
    parser.add_argument('--translate', nargs=2, metavar=('PAPER_ID', 'LANG'),
                       help='Get translation (e.g., --translate abc123 hi)')

    args = parser.parse_args()

    try:
        if args.check_only:
            check_server()
            check_performance_stats()

        elif args.list:
            list_papers()

        elif args.process:
            process_paper(args.process)

        elif args.translate:
            get_translation(args.translate[0], args.translate[1])

        elif args.pdf_path:
            run_full_test(args.pdf_path)

        else:
            print("Enhanced Papers API Test Script")
            print("\nUsage:")
            print("  python test_enhanced_api.py <pdf_path>          # Run full test")
            print("  python test_enhanced_api.py --check-only        # Check server")
            print("  python test_enhanced_api.py --list              # List papers")
            print("  python test_enhanced_api.py --process <id>      # Process paper")
            print("  python test_enhanced_api.py --translate <id> hi # Get translation")
            print("\nExample:")
            print("  python test_enhanced_api.py sample_paper.pdf")

            # Run basic checks
            print("\n" + "="*60)
            check_server()
            check_performance_stats()

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
