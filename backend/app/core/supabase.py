"""Supabase client initialization."""
from supabase import create_client, Client
from .config import settings


def get_supabase_client() -> Client:
    """Get Supabase client instance."""
    return create_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_KEY
    )


def get_supabase_admin_client() -> Client:
    """Get Supabase admin client with service key."""
    return create_client(
        supabase_url=settings.SUPABASE_URL,
        supabase_key=settings.SUPABASE_SERVICE_KEY
    )


# Global client instance
supabase: Client = get_supabase_client()
supabase_admin: Client = get_supabase_admin_client()
