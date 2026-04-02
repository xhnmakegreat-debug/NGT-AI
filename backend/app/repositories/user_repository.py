"""
Database helpers for user entities.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core import security
from backend.app.models import (
    AuthIdentityStatus,
    AuthProvider,
    User,
    UserAuthIdentity,
    UserSettings,
    UserStatus,
    UserTier,
)


class UserRepository:
    """Encapsulates CRUD logic for user accounts."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalars().first()

    def create_with_email(
        self,
        *,
        email: str,
        password: str,
        nickname: Optional[str] = None,
    ) -> User:
        now = datetime.utcnow()
        user = User(
            email=email,
            nickname=nickname,
            status=UserStatus.ACTIVE,
            tier=UserTier.FREE,
            last_login_at=now,
        )
        self.db.add(user)
        self.db.flush()

        password_hash = security.hash_password(password)
        identity = UserAuthIdentity(
            user_id=user.id,
            provider=AuthProvider.EMAIL,
            provider_user_id=email,
            credential_hash=password_hash,
            status=AuthIdentityStatus.ACTIVE,
            last_used_at=now,
        )
        self.db.add(identity)

        if not self.db.get(UserSettings, user.id):
            settings = UserSettings(user_id=user.id)
            self.db.add(settings)

        return user

    def verify_email_credentials(self, email: str, password: str) -> Optional[User]:
        stmt = (
            select(UserAuthIdentity)
            .join(User)
            .where(
                UserAuthIdentity.provider == AuthProvider.EMAIL,
                UserAuthIdentity.provider_user_id == email,
                UserAuthIdentity.status == AuthIdentityStatus.ACTIVE,
            )
        )
        identity = self.db.execute(stmt).scalars().first()
        if identity and identity.credential_hash and security.verify_password(password, identity.credential_hash):
            now = datetime.utcnow()
            identity.last_used_at = now
            identity.user.last_login_at = now
            return identity.user
        return None

    def attach_identity(
        self,
        *,
        user: User,
        provider: AuthProvider,
        provider_user_id: str,
        access_token: str | None = None,
        refresh_token: str | None = None,
        credential_hash: str | None = None,
    ) -> UserAuthIdentity:
        identity = UserAuthIdentity(
            user_id=user.id,
            provider=provider,
            provider_user_id=provider_user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            credential_hash=credential_hash,
            status=AuthIdentityStatus.ACTIVE,
            last_used_at=datetime.utcnow(),
        )
        self.db.add(identity)
        return identity
