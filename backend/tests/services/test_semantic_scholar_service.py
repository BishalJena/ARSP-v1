"""Unit tests for Semantic Scholar service."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from app.services.semantic_scholar_service import SemanticScholarService


@pytest.fixture
def s2_service():
    """Create Semantic Scholar service instance."""
    return SemanticScholarService()


@pytest.fixture
def mock_papers():
    """Mock paper data from S2 API."""
    return [
        {
            "paperId": "test123",
            "title": "Test Paper on Deep Learning",
            "abstract": "This is a test abstract about deep learning.",
            "year": 2023,
            "citationCount": 100,
            "publicationDate": "2023-01-15",
            "url": "https://example.com/paper1",
            "authors": [{"name": "John Doe"}]
        },
        {
            "paperId": "test456",
            "title": "Machine Learning Survey",
            "abstract": "A comprehensive survey of machine learning.",
            "year": 2024,
            "citationCount": 50,
            "publicationDate": "2024-06-01",
            "url": "https://example.com/paper2",
            "authors": [{"name": "Jane Smith"}]
        }
    ]


class TestSemanticScholarService:
    """Test Semantic Scholar service methods."""

    def test_chunk_text(self, s2_service):
        """Test text chunking."""
        # Need longer text to create chunks (min 50 chars per chunk)
        text = "This is a longer sentence with enough content to create a valid chunk. " \
               "This is another sentence that will be part of the chunking process. " \
               "And this is a third sentence to ensure we have sufficient text."
        chunks = s2_service._chunk_text(text, max_size=100)

        assert len(chunks) > 0
        # Chunks should be meaningful size (> 50 chars minimum)
        assert all(len(chunk) > 50 for chunk in chunks)

    def test_cosine_similarity(self, s2_service):
        """Test cosine similarity calculation."""
        vec_a = [1.0, 0.0, 0.0]
        vec_b = [1.0, 0.0, 0.0]
        similarity = s2_service._cosine_similarity(vec_a, vec_b)

        assert similarity == pytest.approx(1.0, abs=0.01)

        vec_c = [0.0, 1.0, 0.0]
        similarity2 = s2_service._cosine_similarity(vec_a, vec_c)
        assert similarity2 == pytest.approx(0.0, abs=0.01)

    def test_extract_keywords(self, s2_service):
        """Test keyword extraction."""
        text = "Machine learning is a subset of artificial intelligence. Deep learning uses neural networks."
        keywords = s2_service._extract_keywords(text, num=5)

        assert len(keywords) <= 5
        assert "machine" in keywords or "learning" in keywords

    @pytest.mark.asyncio
    async def test_search_papers_bulk(self, s2_service, mock_papers):
        """Test bulk paper search."""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock the HTTP response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": mock_papers, "token": None}

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

            results = await s2_service.search_papers_bulk(query="deep learning", limit=10)

            assert len(results) == 2
            assert results[0]["title"] == "Test Paper on Deep Learning"

    @pytest.mark.asyncio
    async def test_get_trending_topics(self, s2_service, mock_papers):
        """Test trending topics retrieval."""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock the HTTP response
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"data": mock_papers}

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

            results = await s2_service.get_trending_topics(field="deep learning", limit=5)

            assert len(results) > 0
            assert "impact_score" in results[0]
            assert "citation_velocity" in results[0]

    @pytest.mark.asyncio
    async def test_detect_plagiarism_hybrid(self, s2_service):
        """Test plagiarism detection."""
        test_text = "Deep learning is a subset of machine learning that uses neural networks."

        # Mock both embedding generation and the S2 search
        with patch.object(s2_service, '_generate_embeddings', return_value=[[0.1, 0.2, 0.3]]):
            with patch('httpx.AsyncClient') as mock_client:
                # Mock empty S2 search response
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"data": []}

                mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

                result = await s2_service.detect_plagiarism_hybrid(test_text, check_online=True)

                assert "originality_score" in result
                assert 0 <= result["originality_score"] <= 100
                assert "flagged_sections" in result
                assert "processing_time_seconds" in result

    @pytest.mark.asyncio
    async def test_recommend_journals_hybrid(self, s2_service):
        """Test journal recommendations."""
        abstract = "This paper presents a novel approach to deep learning."
        keywords = ["deep learning", "neural networks"]
        journals_db = [
            {
                "id": "j1",
                "name": "Nature Machine Intelligence",
                "description": "AI and machine learning journal",
                "impact_factor": 25.0,
                "domain": "Computer Science"
            },
            {
                "id": "j2",
                "name": "IEEE TPAMI",
                "description": "Pattern recognition journal",
                "impact_factor": 24.0,
                "domain": "Computer Science"
            }
        ]

        with patch.object(s2_service, '_generate_embedding', return_value=[0.1, 0.2, 0.3]):
            with patch.object(s2_service, '_generate_embeddings', return_value=[[0.1, 0.2, 0.3], [0.2, 0.3, 0.4]]):
                results = await s2_service.recommend_journals_hybrid(abstract, keywords, journals_db)

                assert len(results) == 2
                assert all("fit_score" in j for j in results)
                # Should be sorted by fit_score
                assert results[0]["fit_score"] >= results[1]["fit_score"]

    def test_calculate_keyword_score(self, s2_service):
        """Test keyword score calculation."""
        abstract = "Deep learning and neural networks"
        keywords = ["deep learning", "neural"]
        journal = {
            "name": "Deep Learning Journal",
            "description": "Journal about neural networks",
            "domain": "Computer Science"
        }

        score = s2_service._calculate_keyword_score(abstract, keywords, journal)

        assert score > 0
        assert score <= 30  # Max score is 30


@pytest.mark.asyncio
async def test_service_initialization():
    """Test service initialization."""
    service = SemanticScholarService()

    assert service.base_url == "https://api.semanticscholar.org/graph/v1"
    assert service.embedding_model == "sentence-transformers/paraphrase-MiniLM-L6-v2"
