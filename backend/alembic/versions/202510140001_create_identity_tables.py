"""create identity and membership tables"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg
from alembic import op

revision = "202510140001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    def ensure_enum(type_name: str, values: list[str]) -> None:
        quoted = ", ".join(f"'{value}'" for value in values)
        op.execute(
            sa.text(
                f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{type_name}') THEN
                        CREATE TYPE {type_name} AS ENUM ({quoted});
                    END IF;
                END$$;
                """
            )
        )

    ensure_enum("user_status", ["active", "suspended", "deleted"])
    ensure_enum("user_tier", ["free", "vip", "pro"])
    ensure_enum(
        "auth_provider",
        ["email", "phone", "google", "wechat", "apple", "github", "microsoft", "custom"],
    )
    ensure_enum("auth_identity_status", ["active", "revoked", "pending"])
    ensure_enum("membership_plan_type", ["free", "subscription", "one_time"])
    ensure_enum(
        "membership_billing_cycle",
        ["none", "monthly", "quarterly", "yearly", "lifetime"],
    )
    ensure_enum("membership_status", ["active", "expired", "cancelled", "pending"])
    ensure_enum("payment_provider", ["stripe", "wechat_pay", "alipay", "paypal", "manual"])
    ensure_enum("payment_status", ["pending", "succeeded", "failed", "refunded"])
    ensure_enum("organization_status", ["active", "disabled"])
    ensure_enum("organization_role", ["owner", "admin", "member"])
    ensure_enum("organization_member_status", ["active", "inactive"])

    user_status = pg.ENUM("active", "suspended", "deleted", name="user_status", create_type=False)
    user_tier = pg.ENUM("free", "vip", "pro", name="user_tier", create_type=False)
    auth_provider = pg.ENUM(
        "email",
        "phone",
        "google",
        "wechat",
        "apple",
        "github",
        "microsoft",
        "custom",
        name="auth_provider",
        create_type=False,
    )
    auth_identity_status = pg.ENUM("active", "revoked", "pending", name="auth_identity_status", create_type=False)
    membership_plan_type = pg.ENUM(
        "free",
        "subscription",
        "one_time",
        name="membership_plan_type",
        create_type=False,
    )
    membership_billing_cycle = pg.ENUM(
        "none",
        "monthly",
        "quarterly",
        "yearly",
        "lifetime",
        name="membership_billing_cycle",
        create_type=False,
    )
    membership_status = pg.ENUM(
        "active",
        "expired",
        "cancelled",
        "pending",
        name="membership_status",
        create_type=False,
    )
    payment_provider = pg.ENUM(
        "stripe",
        "wechat_pay",
        "alipay",
        "paypal",
        "manual",
        name="payment_provider",
        create_type=False,
    )
    payment_status = pg.ENUM(
        "pending",
        "succeeded",
        "failed",
        "refunded",
        name="payment_status",
        create_type=False,
    )
    organization_status = pg.ENUM("active", "disabled", name="organization_status", create_type=False)
    organization_role = pg.ENUM("owner", "admin", "member", name="organization_role", create_type=False)
    organization_member_status = pg.ENUM(
        "active",
        "inactive",
        name="organization_member_status",
        create_type=False,
    )

    op.create_table(
        "users",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("nickname", sa.String(length=120), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("status", user_status, nullable=False, server_default="active"),
        sa.Column("tier", user_tier, nullable=False, server_default="free"),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("profile_metadata", pg.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("phone", name="uq_users_phone"),
    )

    op.create_table(
        "membership_plans",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("plan_type", membership_plan_type, nullable=False, server_default="subscription"),
        sa.Column("billing_cycle", membership_billing_cycle, nullable=False, server_default="monthly"),
        sa.Column("price_cents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("features", pg.JSONB(astext_type=sa.Text()), nullable=True),
        sa.UniqueConstraint("code", name="uq_membership_plans_code"),
    )

    op.create_table(
        "organizations",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("owner_user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL")),
        sa.Column("status", organization_status, nullable=False, server_default="active"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("extra_data", pg.JSONB(astext_type=sa.Text()), nullable=True),
    )

    op.create_table(
        "user_settings",
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("theme", sa.String(length=32), nullable=True, server_default="system"),
        sa.Column("locale", sa.String(length=16), nullable=True, server_default="zh"),
        sa.Column("preferred_model", sa.String(length=64), nullable=True),
        sa.Column("notifications", pg.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("workspace_config", pg.JSONB(astext_type=sa.Text()), nullable=True),
    )

    op.create_table(
        "user_auth_identities",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", auth_provider, nullable=False),
        sa.Column("provider_user_id", sa.String(length=255), nullable=True),
        sa.Column("provider_union_id", sa.String(length=255), nullable=True),
        sa.Column("credential_hash", sa.String(length=255), nullable=True),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", auth_identity_status, nullable=False, server_default="active"),
        sa.Column("extra_data", pg.JSONB(astext_type=sa.Text()), nullable=True),
        sa.UniqueConstraint("provider", "provider_user_id", name="uq_user_auth_provider_user"),
    )

    op.create_table(
        "user_memberships",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "plan_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("membership_plans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("status", membership_status, nullable=False, server_default="pending"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("extra_data", pg.JSONB(astext_type=sa.Text()), nullable=True),
        sa.UniqueConstraint("user_id", "plan_id", name="uq_user_plan"),
    )

    op.create_table(
        "user_payments",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "plan_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("membership_plans.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("provider", payment_provider, nullable=False, server_default="manual"),
        sa.Column("status", payment_status, nullable=False, server_default="pending"),
        sa.Column("amount_cents", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="USD"),
        sa.Column("transaction_reference", sa.String(length=255), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw_response", pg.JSONB(astext_type=sa.Text()), nullable=True),
    )

    op.create_table(
        "organization_members",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "organization_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("organizations.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role", organization_role, nullable=False, server_default="member"),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", organization_member_status, nullable=False, server_default="active"),
        sa.UniqueConstraint("organization_id", "user_id", name="uq_org_member"),
    )


def downgrade() -> None:
    op.drop_table("organization_members")
    op.drop_table("user_payments")
    op.drop_table("user_memberships")
    op.drop_table("user_auth_identities")
    op.drop_table("user_settings")
    op.drop_table("organizations")
    op.drop_table("membership_plans")
    op.drop_table("users")

    for enum_name in [
        "organization_member_status",
        "organization_role",
        "organization_status",
        "payment_status",
        "payment_provider",
        "membership_status",
        "membership_billing_cycle",
        "membership_plan_type",
        "auth_identity_status",
        "auth_provider",
        "user_tier",
        "user_status",
    ]:
        op.execute(sa.text(f"DROP TYPE IF EXISTS {enum_name} CASCADE"))
