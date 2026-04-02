"""
Security utilities: password hashing & JWT helpers.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.app.config import settings

pwd_context = CryptContext(
    # pbkdf2_sha256 不受 72 字节限制，避免长密码触发 bcrypt 限制
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    expires_minutes: int | None = None,
    additional_claims: Optional[dict[str, Any]] = None,
) -> str:
    expire_delta = timedelta(
        minutes=expires_minutes if expires_minutes is not None else settings.access_token_expires_minutes
    )
    to_encode: dict[str, Any] = {"sub": subject, "exp": datetime.utcnow() + expire_delta}

    if additional_claims:
        to_encode.update(additional_claims)

    token = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])


class InvalidTokenError(Exception):
    """Raised when token verification fails."""


def get_subject_from_token(token: str) -> str:
    try:
        payload = decode_token(token)
        subject = payload.get("sub")
        if subject is None:
            raise InvalidTokenError("Token missing subject.")
        return subject
    except JWTError as exc:  # pragma: no cover
        raise InvalidTokenError(str(exc)) from exc
