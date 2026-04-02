"""
Authentication API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.security import create_access_token
from backend.app.db import get_db
from backend.app.models import User
from backend.app.repositories.user_repository import UserRepository
from backend.app.schemas import (
    TokenResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserPublicResponse,
)

router = APIRouter(prefix="/auth", tags=["用户认证"])


def _build_user_response(user: User) -> UserPublicResponse:
    return UserPublicResponse.model_validate(user, from_attributes=True)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreateRequest, db: Session = Depends(get_db)) -> TokenResponse:
    repo = UserRepository(db)
    if repo.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = repo.create_with_email(email=payload.email, password=payload.password, nickname=payload.nickname)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(str(user.id))
    return TokenResponse(access_token=access_token, user=_build_user_response(user))


@router.post("/login", response_model=TokenResponse)
def login_user(payload: UserLoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    repo = UserRepository(db)
    user = repo.verify_email_credentials(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    db.commit()

    access_token = create_access_token(str(user.id))
    return TokenResponse(access_token=access_token, user=_build_user_response(user))

