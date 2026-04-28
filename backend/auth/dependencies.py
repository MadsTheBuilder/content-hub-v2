from fastapi import Depends, HTTPException, Header
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DummyUser:
    """Dummy user for mock mode (no Supabase JWT secret configured)."""
    id = "00000000-0000-0000-0000-000000000000"
    email = "local@contenthub.dev"


class CurrentUser:
    """User object extracted from JWT token."""
    def __init__(self, user_id: str, email: str):
        self.id = user_id
        self.email = email


async def get_current_user(authorization: Optional[str] = Header(None)) -> CurrentUser | DummyUser:
    """
    Decode and validate JWT token from Authorization header.
    Falls back to DummyUser if SUPABASE_JWT_SECRET is not set (mock mode).
    """
    from backend.config import settings

    # Mock mode: no JWT secret configured
    if not settings.supabase_jwt_secret:
        logger.debug("Mock mode: SUPABASE_JWT_SECRET not set, returning DummyUser")
        return DummyUser()

    # No Authorization header
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    # Parse "Bearer <token>"
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    # Decode JWT
    try:
        import jwt

        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
        )

        user_id: str = payload.get("sub")
        email: str = payload.get("email", "")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing 'sub' claim")

        # Check for dummy UUID (mock mode fallback)
        if user_id == "00000000-0000-0000-0000-000000000000":
            logger.debug("Token decoded to dummy UUID, returning DummyUser")
            return DummyUser()

        return CurrentUser(user_id=user_id, email=email)

    except Exception as e:
        logger.error(f"JWT decode error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")
