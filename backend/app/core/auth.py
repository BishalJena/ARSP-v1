"""Authentication with Clerk."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWKClient
from .config import settings


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Verify Clerk JWT token and return user info.

    Clerk uses RS256 with JWKs for token verification.
    """
    token = credentials.credentials

    try:
        # Get Clerk's JWKS URL
        clerk_domain = settings.CLERK_PUBLISHABLE_KEY.split("_")[1]  # Extract domain from key
        jwks_url = f"https://{clerk_domain}.clerk.accounts.dev/.well-known/jwks.json"

        # Verify token using Clerk's public key
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_exp": True}
        )

        return {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "full_name": payload.get("name"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )


# Optional: Dependency to get user from Supabase
async def get_current_user_profile(current_user: dict = Depends(get_current_user)) -> dict:
    """Get user profile from Supabase."""
    from .supabase import supabase

    user_id = current_user["user_id"]

    result = supabase.table("profiles").select("*").eq("id", user_id).maybe_single().execute()

    if not result.data:
        # Create profile if doesn't exist
        profile_data = {
            "id": user_id,
            "email": current_user["email"],
            "full_name": current_user.get("full_name"),
        }
        result = supabase.table("profiles").insert(profile_data).execute()
        return result.data[0] if result.data else profile_data

    return result.data
