"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from ...core.auth import get_current_user, get_current_user_profile
from ...core.supabase import supabase

router = APIRouter()


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str
    full_name: str


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User profile response."""
    id: str
    email: str
    full_name: Optional[str] = None
    discipline: Optional[str] = None
    institution: Optional[str] = None
    publication_count: int = 0
    preferred_language: str = "en"


@router.post("/register")
async def register(request: RegisterRequest):
    """
    Register a new user.

    Note: With Clerk, registration happens on the client side.
    This endpoint is mainly for creating the profile in Supabase after Clerk registration.
    """
    # In a Clerk setup, the user is already registered via Clerk
    # This endpoint would be called after Clerk registration to create the profile
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration is handled by Clerk on the frontend. Use Clerk's SignUp component."
    )


@router.post("/login")
async def login(request: LoginRequest):
    """
    Login user.

    Note: With Clerk, authentication happens on the client side.
    Clerk provides the JWT token which is validated in get_current_user.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login is handled by Clerk on the frontend. Use Clerk's SignIn component."
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(profile: dict = Depends(get_current_user_profile)):
    """Get current user profile."""
    return profile


@router.put("/me", response_model=UserResponse)
async def update_profile(
    updates: dict,
    current_user: dict = Depends(get_current_user)
):
    """Update current user profile."""
    user_id = current_user["user_id"]

    # Update profile in Supabase
    result = supabase.table("profiles").update(updates).eq("id", user_id).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return result.data[0]
