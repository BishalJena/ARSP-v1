"""Authentication endpoints - Email/Password."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import uuid
from datetime import datetime, timezone
from ...core.auth import (
    get_current_user,
    get_current_user_profile,
    get_password_hash,
    verify_password,
    create_access_token,
)
from ...core.supabase import supabase

router = APIRouter()


class RegisterRequest(BaseModel):
    """User registration request."""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str = Field(..., min_length=1, description="Full name is required")


class LoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    """User profile response."""
    id: str
    email: str
    full_name: str
    created_at: str


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user.

    Creates a new user account with email and password.
    Passwords are hashed using bcrypt before storage.

    Returns:
        - access_token: JWT token for authentication
        - user: User profile information
    """
    # Check if user already exists
    existing_user = supabase.table("users").select("id").eq("email", request.email).execute()

    if existing_user.data and len(existing_user.data) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = get_password_hash(request.password)

    # Create user in database
    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "email": request.email,
        "full_name": request.full_name,
        "password_hash": hashed_password,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        result = supabase.table("users").insert(user_data).execute()

        if not result.data:
            raise Exception("Failed to create user")

        created_user = result.data[0]

        # Create JWT token
        access_token = create_access_token(
            data={
                "sub": user_id,
                "email": request.email,
                "full_name": request.full_name,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": created_user["id"],
                "email": created_user["email"],
                "full_name": created_user["full_name"],
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login user with email and password.

    Validates credentials and returns JWT token.

    Returns:
        - access_token: JWT token for authentication
        - user: User profile information
    """
    # Get user from database
    result = supabase.table("users").select("*").eq("email", request.email).execute()

    if not result.data or len(result.data) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    user = result.data[0]

    # Verify password
    if not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(profile: dict = Depends(get_current_user_profile)):
    """
    Get current authenticated user profile.

    Requires valid JWT token in Authorization header.
    """
    return {
        "id": profile["id"],
        "email": profile["email"],
        "full_name": profile["full_name"],
        "created_at": profile.get("created_at", ""),
    }


@router.put("/me")
async def update_profile(
    updates: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Update current user profile.

    Allows updating: full_name, institution, research_interests, etc.
    Cannot update: email, password (use separate endpoints for those)
    """
    user_id = current_user["user_id"]

    # Don't allow updating sensitive fields
    forbidden_fields = ["id", "email", "password_hash", "created_at"]
    for field in forbidden_fields:
        if field in updates:
            del updates[field]

    # Update profile in Supabase
    result = supabase.table("users").update(updates).eq("id", user_id).execute()

    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return result.data[0]


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout user.

    Note: With JWT, logout is handled client-side by removing the token.
    This endpoint exists for consistency and can be used for logging/analytics.
    """
    return {
        "message": "Successfully logged out",
        "user_id": current_user["user_id"]
    }
