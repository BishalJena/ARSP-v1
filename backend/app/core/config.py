"""Application configuration."""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Environment
    ENVIRONMENT: str = "development"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str

    # JWT Authentication
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"

    # Lingo.dev
    LINGO_API_KEY: str

    # Hugging Face (Legacy - optional after Gemini migration)
    HF_API_KEY: str = ""

    # OpenRouter (for Gemini 2.0 Flash Lite)
    OPENROUTER_API_KEY: str = ""

    # External APIs
    SEMANTIC_SCHOLAR_API_KEY: str = ""
    CROSSREF_EMAIL: str = ""
    WINSTON_API_KEY: str = ""  # Winston AI plagiarism detection

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "ARSP API"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # Ignore extra env variables not defined in schema
    )


settings = Settings()
