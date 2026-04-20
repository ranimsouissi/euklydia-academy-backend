from __future__ import annotations

import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.deps import get_current_user
from app.core.limiter import limiter                   # ✅ Amélioration 7
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db

from app.models.user import User
from app.models.role import Role
from app.models.user_profile import UserProfile
from app.models.career_path import CareerPath
from app.models.oauth_account import OAuthAccount
from app.models.oauth_state import OAuthState
from app.models.password_reset_token import PasswordResetToken
from app.services.email_service import send_reset_password_email
from app.schemas.user_update import UpdateMeRequest

from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.token import TokenResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# =========================
# OAuth state — PostgreSQL
# =========================

OAUTH_STATE_TTL_SECONDS = 300


def _remember_state(state: str, db: Session) -> None:
    db.query(OAuthState).filter(
        OAuthState.expires_at < datetime.utcnow()
    ).delete()
    db.commit()

    db.add(OAuthState(
        state=state,
        expires_at=datetime.utcnow() + timedelta(seconds=OAUTH_STATE_TTL_SECONDS),
    ))
    db.commit()


def _is_state_valid(state: str, db: Session) -> bool:
    oauth_state = db.query(OAuthState).filter(
        OAuthState.state == state,
        OAuthState.used == False,
        OAuthState.expires_at > datetime.utcnow(),
    ).first()

    return oauth_state is not None


def _consume_state(state: str, db: Session) -> None:
    db.query(OAuthState).filter(
        OAuthState.state == state
    ).update({"used": True})
    db.commit()


# =========================
# Helper
# =========================

def _get_or_create_default_role(db: Session) -> Role:
    role = db.execute(select(Role).where(Role.name == "learner")).scalar_one_or_none()
    if role:
        return role
    role = Role(name="learner")
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


# =========================
# Email / Password Auth
# =========================

@router.post("/register", status_code=201)
@limiter.limit("3/minute")                             # ✅ Amélioration 7
def register(request: Request, payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.execute(
        select(User).where(User.email == payload.email)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    default_role = _get_or_create_default_role(db)

    user = User(
        full_name=payload.full_name.strip(),
        email=payload.email,
        password_hash=hash_password(payload.password),
        role_id=default_role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    db.add(UserProfile(user_id=user.id))
    db.commit()

    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": default_role.name,
    }


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")                             # ✅ Amélioration 7
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(User.email == payload.email)
    ).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)


# =========================
# Forgot / Reset password
# =========================

@router.post("/forgot-password")
@limiter.limit("3/minute")                             # ✅ Amélioration 7
def forgot_password(request: Request, payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.execute(
        select(User).where(User.email == payload.email)
    ).scalar_one_or_none()

    if not user:
        return {"message": "If the email exists, a reset link has been sent"}

    recent_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.created_at > datetime.utcnow() - timedelta(minutes=5)
    ).first()

    if recent_token:
        logger.warning(
            f"Reset request blocked (rate limit) for user_id={user.id}"
        )
        return {"message": "If the email exists, a reset link has been sent"}

    db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used == False
    ).update({"used": True})
    db.commit()

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode()).hexdigest()

    reset = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=datetime.utcnow() + timedelta(hours=1),
    )
    db.add(reset)
    db.commit()

    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    try:
        send_reset_password_email(user.email, reset_link)
    except Exception as e:
        logger.error(
            f"Email failed for user_id={user.id} email={user.email}: {e}"
        )

    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(payload.token.encode()).hexdigest()

    reset = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used == False,
        )
        .first()
    )

    if not reset:
        raise HTTPException(status_code=400, detail="Invalid token")

    if reset.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    user = db.query(User).filter(User.id == reset.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = hash_password(payload.new_password)
    reset.used = True
    db.commit()

    return {"message": "Password updated"}


# =========================
# Current user
# =========================

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    role_name = current_user.role.name if getattr(current_user, "role", None) else None
    career_path_name = (
        current_user.career_path.name 
        if getattr(current_user, "career_path", None) 
        else None
    )
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": role_name,                       # ← rôle système ("learner")
        "career_path_id": current_user.career_path_id,
        "career_path": career_path_name,         # ← nom du métier ("AI Sales Specialist")
    }
@router.patch("/me")
def update_me(
    payload: UpdateMeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name.strip()

    db.commit()
    db.refresh(current_user)

    role_name = current_user.role.name if getattr(current_user, "role", None) else None
    career_path_name = (
        current_user.career_path.name 
        if getattr(current_user, "career_path", None) 
        else None
    )
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": role_name,
        "career_path_id": current_user.career_path_id,
        "career_path": career_path_name,
    }


@router.patch("/me/career-path/{career_path_id}")
def set_my_career_path(
    career_path_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cp = db.execute(
        select(CareerPath).where(CareerPath.id == career_path_id)
    ).scalar_one_or_none()

    if not cp:
        raise HTTPException(status_code=404, detail="career_path not found")

    current_user.career_path_id = career_path_id
    db.commit()
    db.refresh(current_user)

    return {
        "message": "career_path updated",
        "career_path_id": career_path_id,
    }


# =========================
# Google OAuth
# =========================

@router.get("/google/start")
def google_start(db: Session = Depends(get_db)):
    state = secrets.token_urlsafe(24)
    _remember_state(state, db)

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }

    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

    resp = RedirectResponse(auth_url, status_code=302)
    resp.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        max_age=OAUTH_STATE_TTL_SECONDS,
        samesite="lax",
        secure=False,
        path="/",
    )
    return resp


@router.get("/google/callback")
async def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db),
):
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code/state")

    if not _is_state_valid(state, db):
        raise HTTPException(status_code=400, detail="Invalid state")

    _consume_state(state, db)

    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        token_res = await client.post(token_url, data=data)
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code")

        token_json = token_res.json()
        access_token = token_json.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access_token from Google")

        userinfo_res = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if userinfo_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch userinfo")

        info = userinfo_res.json()

    email = info.get("email")
    google_sub = info.get("sub")
    google_name = info.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Google account has no email")
    if not google_sub:
        raise HTTPException(status_code=400, detail="Google account missing sub")

    user = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if not user:
        default_role = _get_or_create_default_role(db)
        random_pw = secrets.token_urlsafe(32)
        user = User(
            full_name=google_name,
            email=email,
            password_hash=hash_password(random_pw),
            role_id=default_role.id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.add(UserProfile(user_id=user.id))
        db.commit()

    provider = "google"
    existing = db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == provider,
            OAuthAccount.provider_account_id == google_sub,
        )
    ).scalar_one_or_none()

    if not existing:
        db.add(OAuthAccount(
            user_id=user.id,
            provider=provider,
            provider_account_id=google_sub,
            email=email,
        ))
        db.commit()

    jwt_token = create_access_token(subject=str(user.id))

    resp = RedirectResponse(url=f"{settings.FRONTEND_URL}/auth/callback?token={jwt_token}")
    resp.delete_cookie("oauth_state")
    return resp