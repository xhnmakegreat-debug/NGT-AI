"""
用户与账号体系 ORM 模型
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Dict

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db import Base, TimestampMixin, UUIDPrimaryKeyMixin
from backend.app.models.common import JSONType, enum_type





class UserStatus(enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class UserTier(enum.Enum):
    FREE = "free"
    VIP = "vip"
    PRO = "pro"


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """核心用户实体"""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("phone", name="uq_users_phone"),
    )

    nickname: Mapped[str | None] = mapped_column(String(120), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)

    status: Mapped[UserStatus] = mapped_column(
        enum_type(UserStatus, name="user_status"),
        nullable=False,
        default=UserStatus.ACTIVE,
    )
    tier: Mapped[UserTier] = mapped_column(
        enum_type(UserTier, name="user_tier"),
        nullable=False,
        default=UserTier.FREE,
    )

    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    profile_metadata: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    identities: Mapped[list["UserAuthIdentity"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    memberships: Mapped[list["UserMembership"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    payments: Mapped[list["UserPayment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    settings: Mapped["UserSettings"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )


class AuthProvider(enum.Enum):
    EMAIL = "email"
    PHONE = "phone"
    GOOGLE = "google"
    WECHAT = "wechat"
    APPLE = "apple"
    GITHUB = "github"
    MICROSOFT = "microsoft"
    CUSTOM = "custom"


class AuthIdentityStatus(enum.Enum):
    ACTIVE = "active"
    REVOKED = "revoked"
    PENDING = "pending"


class UserAuthIdentity(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """登录方式与第三方凭证"""

    __tablename__ = "user_auth_identities"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_user_id",
            name="uq_user_auth_provider_user",
        ),
    )

    user_id: Mapped[Any] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    provider: Mapped[AuthProvider] = mapped_column(
        enum_type(AuthProvider, name="auth_provider"),
        nullable=False,
    )

    provider_user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    provider_union_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # 用于邮箱/手机号登录的凭证（如密码哈希、短信校验值等）
    credential_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)

    access_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    token_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[AuthIdentityStatus] = mapped_column(
        enum_type(AuthIdentityStatus, name="auth_identity_status"),
        nullable=False,
        default=AuthIdentityStatus.ACTIVE,
    )
    extra_data: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    user: Mapped[User] = relationship(back_populates="identities")


class MembershipPlanType(enum.Enum):
    FREE = "free"
    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"


class BillingCycle(enum.Enum):
    NONE = "none"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"


class MembershipPlan(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """会员/订阅计划定义"""

    __tablename__ = "membership_plans"

    code: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    plan_type: Mapped[MembershipPlanType] = mapped_column(
        enum_type(MembershipPlanType, name="membership_plan_type"),
        nullable=False,
        default=MembershipPlanType.SUBSCRIPTION,
    )
    billing_cycle: Mapped[BillingCycle] = mapped_column(
        enum_type(BillingCycle, name="membership_billing_cycle"),
        nullable=False,
        default=BillingCycle.MONTHLY,
    )

    price_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    features: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    memberships: Mapped[list["UserMembership"]] = relationship(
        back_populates="plan",
        cascade="all, delete",
    )


class MembershipStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    PENDING = "pending"


class UserMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """用户订阅关系"""

    __tablename__ = "user_memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "plan_id", name="uq_user_plan"),
    )

    user_id: Mapped[Any] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    plan_id: Mapped[Any] = mapped_column(
        ForeignKey("membership_plans.id", ondelete="CASCADE"),
        nullable=False,
    )

    status: Mapped[MembershipStatus] = mapped_column(
        enum_type(MembershipStatus, name="membership_status"),
        nullable=False,
        default=MembershipStatus.PENDING,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    extra_data: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    user: Mapped[User] = relationship(back_populates="memberships")
    plan: Mapped[MembershipPlan] = relationship(back_populates="memberships")


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentProvider(enum.Enum):
    STRIPE = "stripe"
    WECHAT_PAY = "wechat_pay"
    ALIPAY = "alipay"
    PAYPAL = "paypal"
    MANUAL = "manual"


class UserPayment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """付费/充值记录"""

    __tablename__ = "user_payments"

    user_id: Mapped[Any] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    plan_id: Mapped[Any | None] = mapped_column(
        ForeignKey("membership_plans.id", ondelete="SET NULL"),
        nullable=True,
    )

    provider: Mapped[PaymentProvider] = mapped_column(
        enum_type(PaymentProvider, name="payment_provider"),
        nullable=False,
        default=PaymentProvider.MANUAL,
    )
    status: Mapped[PaymentStatus] = mapped_column(
        enum_type(PaymentStatus, name="payment_status"),
        nullable=False,
        default=PaymentStatus.PENDING,
    )

    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")

    transaction_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    raw_response: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    user: Mapped[User] = relationship(back_populates="payments")
    plan: Mapped[MembershipPlan | None] = relationship()


class UserSettings(Base, TimestampMixin):
    """用户偏好设置"""

    __tablename__ = "user_settings"

    user_id: Mapped[Any] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    theme: Mapped[str | None] = mapped_column(String(32), nullable=True, default="system")
    locale: Mapped[str | None] = mapped_column(String(16), nullable=True, default="zh")
    preferred_model: Mapped[str | None] = mapped_column(String(64), nullable=True)

    notifications: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    workspace_config: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    user: Mapped[User] = relationship(back_populates="settings")


class OrganizationStatus(enum.Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """预留组织账户结构"""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_user_id: Mapped[Any] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[OrganizationStatus] = mapped_column(
        enum_type(OrganizationStatus, name="organization_status"),
        nullable=False,
        default=OrganizationStatus.ACTIVE,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_data: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    members: Mapped[list["OrganizationMember"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan",
    )


class OrganizationRole(enum.Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class OrganizationMemberStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class OrganizationMember(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """组织成员关系（当前可不启用，但为未来扩展预留）"""

    __tablename__ = "organization_members"
    __table_args__ = (
        UniqueConstraint("organization_id", "user_id", name="uq_org_member"),
    )

    organization_id: Mapped[Any] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[Any] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[OrganizationRole] = mapped_column(
        enum_type(OrganizationRole, name="organization_role"),
        nullable=False,
        default=OrganizationRole.MEMBER,
    )
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[OrganizationMemberStatus] = mapped_column(
        enum_type(OrganizationMemberStatus, name="organization_member_status"),
        nullable=False,
        default=OrganizationMemberStatus.ACTIVE,
    )

    organization: Mapped[Organization] = relationship(back_populates="members")
