from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr
from backend.database import get_supabase, _is_placeholder

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
        return {
            "user_id": str(auth_response.user.id),
            "access_token": auth_response.session.access_token if auth_response.session else None,
            "refresh_token": auth_response.session.refresh_token if auth_response.session else None,
        }
    except Exception as e:
        if _is_placeholder():
            from backend.auth.dependencies import DummyUser
            return {
                "user_id": DummyUser.id,
                "access_token": "local-session-token",
                "refresh_token": "local-refresh-token",
            }
        raise HTTPException(status_code=400, detail=f"Signup failed: {str(e)}")


@router.post("/login")
async def login(req: LoginRequest):
    sb = get_supabase()
    try:
        auth_response = sb.auth.sign_in_with_password({"email": req.email, "password": req.password})
        return {
            "user_id": str(auth_response.user.id),
            "access_token": auth_response.session.access_token if auth_response.session else None,
            "refresh_token": auth_response.session.refresh_token if auth_response.session else None,
        }
    except Exception as e:
        if _is_placeholder():
            from backend.auth.dependencies import DummyUser
            return {
                "user_id": DummyUser.id,
                "access_token": "local-session-token",
                "refresh_token": "local-refresh-token",
            }
        raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout")
async def logout():
    return {"message": "Logged out"}


@router.get("/me")
async def me(authorization: str = Header(...)):
    from backend.auth.dependencies import get_current_user
    user = await get_current_user(authorization)
    return {"id": str(user.id), "email": user.email}
