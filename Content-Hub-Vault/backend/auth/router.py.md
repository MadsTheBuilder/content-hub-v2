---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/auth/router.py"
category: "Content Hub Source Code"
---

# router.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from backend.database import get_supabase

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
async def signup(req: SignupRequest):
    sb = get_supabase()
    try:
        auth_response = sb.auth.sign_up({"email": req.email, "password": req.password})
        return {"user_id": str(auth_response.user.id), "session": auth_response.session}
    except Exception as e:
        # MVP bypass: return dummy user if Supabase integration fails
        from backend.auth.dependencies import DummyUser
        return {
            "user_id": DummyUser.id,
            "session": {
                "access_token": "local-session-token",
                "refresh_token": "local-refresh-token",
                "user": {"id": DummyUser.id, "email": DummyUser.email}
            }
        }


@router.post("/login")
async def login(req: LoginRequest):
    sb = get_supabase()
    try:
        auth_response = sb.auth.sign_in_with_password({"email": req.email, "password": req.password})
        return {"user_id": str(auth_response.user.id), "session": auth_response.session}
    except Exception as e:
        # MVP bypass: return dummy user if Supabase integration fails
        from backend.auth.dependencies import DummyUser
        return {
            "user_id": DummyUser.id,
            "session": {
                "access_token": "local-session-token",
                "refresh_token": "local-refresh-token",
                "user": {"id": DummyUser.id, "email": DummyUser.email}
            }
        }


@router.post("/logout")
async def logout():
    return {"message": "Logged out"}


@router.get("/me")
async def me(authorization: str = Header(...)):
    from backend.auth.dependencies import get_current_user
    user = await get_current_user(authorization)
    return {"id": str(user.id), "email": user.email}

```
