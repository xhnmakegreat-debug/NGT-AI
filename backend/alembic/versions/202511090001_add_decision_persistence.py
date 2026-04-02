"""
add decision workspace persistence
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision = "202511090001"
down_revision = "202510140001"
branch_labels = None
depends_on = None


def _ensure_enum(type_name: str, values: list[str]) -> None:
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


def upgrade() -> None:
    _ensure_enum("project_visibility", ["private", "shared"])
    _ensure_enum("project_task_status", ["active", "running", "completed", "failed", "archived"])
    _ensure_enum("decision_status", ["draft", "running", "completed", "failed", "cancelled"])
    _ensure_enum("decision_run_status", ["pending", "running", "completed", "failed", "cancelled"])
    _ensure_enum(
        "decision_artifact_type",
        ["initial_idea", "score_sheet", "final_decision", "referee_analysis", "summary", "raw"],
    )
    _ensure_enum(
        "audit_event_type",
        ["user_action", "decision_submitted", "decision_completed", "decision_failed"],
    )

    project_visibility = pg.ENUM("private", "shared", name="project_visibility", create_type=False)
    project_task_status = pg.ENUM(
        "active",
        "running",
        "completed",
        "failed",
        "archived",
        name="project_task_status",
        create_type=False,
    )
    decision_status = pg.ENUM(
        "draft",
        "running",
        "completed",
        "failed",
        "cancelled",
        name="decision_status",
        create_type=False,
    )
    decision_run_status = pg.ENUM(
        "pending",
        "running",
        "completed",
        "failed",
        "cancelled",
        name="decision_run_status",
        create_type=False,
    )
    artifact_type = pg.ENUM(
        "initial_idea",
        "score_sheet",
        "final_decision",
        "referee_analysis",
        "summary",
        "raw",
        name="decision_artifact_type",
        create_type=False,
    )
    audit_event_type = pg.ENUM(
        "user_action",
        "decision_submitted",
        "decision_completed",
        "decision_failed",
        name="audit_event_type",
        create_type=False,
    )

    json_type = pg.JSONB(astext_type=sa.Text())

    op.create_table(
        "projects",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("color", sa.String(length=32), nullable=True),
        sa.Column("path", sa.String(length=255), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("visibility", project_visibility, nullable=False, server_default="private"),
        sa.Column("is_archived", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("metadata_json", json_type, nullable=True),
        sa.UniqueConstraint("user_id", "name", name="uq_projects_user_name"),
    )

    op.create_table(
        "project_tasks",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "project_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=True),
        sa.Column("status", project_task_status, nullable=False, server_default="active"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("metadata_json", json_type, nullable=True),
        sa.Column("current_decision_id", pg.UUID(as_uuid=True), nullable=True),
        sa.Column("latest_run_id", pg.UUID(as_uuid=True), nullable=True),
        sa.UniqueConstraint("project_id", "title", name="uq_project_tasks_name"),
    )

    op.create_table(
        "decisions",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "project_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "task_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("project_tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("context", sa.Text(), nullable=True),
        sa.Column("options", json_type, nullable=True),
        sa.Column("criteria", json_type, nullable=True),
        sa.Column("status", decision_status, nullable=False, server_default="draft"),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("metadata_json", json_type, nullable=True),
        sa.Column("latest_run_id", pg.UUID(as_uuid=True), nullable=True),
        sa.Column("run_count", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "decision_runs",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("decision_id", pg.UUID(as_uuid=True), sa.ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("project_id", pg.UUID(as_uuid=True), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column(
            "task_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("project_tasks.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", decision_run_status, nullable=False, server_default="pending"),
        sa.Column("stage", sa.String(length=64), nullable=False, server_default="queued"),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("message", sa.String(length=255), nullable=True),
        sa.Column("queued_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("result_markdown", sa.Text(), nullable=True),
        sa.Column("result_json", json_type, nullable=True),
        sa.Column("agents_snapshot", json_type, nullable=True),
        sa.Column("options_snapshot", json_type, nullable=True),
        sa.Column("criteria_snapshot", json_type, nullable=True),
        sa.Column("context_snapshot", sa.Text(), nullable=True),
        sa.Column("question_snapshot", sa.Text(), nullable=False),
    )

    op.create_table(
        "decision_agents",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "run_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("decision_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("agent_key", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=True),
        sa.Column("prompt", sa.Text(), nullable=True),
        sa.Column("parameters", json_type, nullable=True),
        sa.Column("metrics", json_type, nullable=True),
    )

    op.create_table(
        "decision_artifacts",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column(
            "run_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("decision_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "agent_id",
            pg.UUID(as_uuid=True),
            sa.ForeignKey("decision_agents.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("stage", sa.String(length=32), nullable=False),
        sa.Column("artifact_type", artifact_type, nullable=False),
        sa.Column("label", sa.String(length=255), nullable=True),
        sa.Column("content", json_type, nullable=True),
        sa.Column("markdown", sa.Text(), nullable=True),
        sa.Column("scores", json_type, nullable=True),
        sa.Column("raw_payload", json_type, nullable=True),
    )

    op.create_table(
        "audit_events",
        sa.Column("id", pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("user_id", pg.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("decision_id", pg.UUID(as_uuid=True), sa.ForeignKey("decisions.id", ondelete="SET NULL"), nullable=True),
        sa.Column("run_id", pg.UUID(as_uuid=True), sa.ForeignKey("decision_runs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_type", audit_event_type, nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("metadata_json", json_type, nullable=True),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
    )

    op.create_foreign_key(
        "fk_project_tasks_current_decision",
        "project_tasks",
        "decisions",
        ["current_decision_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_project_tasks_latest_run",
        "project_tasks",
        "decision_runs",
        ["latest_run_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fk_decisions_latest_run",
        "decisions",
        "decision_runs",
        ["latest_run_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_decisions_latest_run", "decisions", type_="foreignkey")
    op.drop_constraint("fk_project_tasks_latest_run", "project_tasks", type_="foreignkey")
    op.drop_constraint("fk_project_tasks_current_decision", "project_tasks", type_="foreignkey")

    op.drop_table("audit_events")
    op.drop_table("decision_artifacts")
    op.drop_table("decision_agents")
    op.drop_table("decision_runs")
    op.drop_table("decisions")
    op.drop_table("project_tasks")
    op.drop_table("projects")

    for enum_name in [
        "audit_event_type",
        "decision_artifact_type",
        "decision_run_status",
        "decision_status",
        "project_task_status",
        "project_visibility",
    ]:
        op.execute(sa.text(f"DROP TYPE IF EXISTS {enum_name}"))
