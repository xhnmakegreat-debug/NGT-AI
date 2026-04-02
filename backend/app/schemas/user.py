"""
Pydantic schemas for user APIs.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class UserCreateRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    nickname: str | None = Field(default=None, max_length=120)


class UserLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str


class UserPublicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str | None = None
    nickname: str | None = None
    avatar_url: str | None = None
    tier: str
    status: str
    last_login_at: datetime | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublicResponse
