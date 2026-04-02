"""
Decision, project, and artifact ORM models.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db import Base, TimestampMixin, UUIDPrimaryKeyMixin
from backend.app.models.common import JSONType, enum_type


class ProjectVisibility(enum.Enum):
    PRIVATE = "private"
    SHARED = "shared"


class TaskStatus(enum.Enum):
    ACTIVE = "active"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class DecisionRecordStatus(enum.Enum):
    DRAFT = "draft"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DecisionRunStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ArtifactType(enum.Enum):
    INITIAL_IDEA = "initial_idea"
    SCORE_SHEET = "score_sheet"
    FINAL_DECISION = "final_decision"
    REFEREE_ANALYSIS = "referee_analysis"
    SUMMARY = "summary"
    RAW = "raw"


class AuditEventType(enum.Enum):
    USER_ACTION = "user_action"
    DECISION_SUBMITTED = "decision_submitted"
    DECISION_COMPLETED = "decision_completed"
    DECISION_FAILED = "decision_failed"


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Workspace project grouping tasks by user."""

    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_projects_user_name"),
    )

    user_id: Mapped[Any] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    color: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    visibility: Mapped[ProjectVisibility] = mapped_column(
        enum_type(ProjectVisibility, name="project_visibility"),
        nullable=False,
        default=ProjectVisibility.PRIVATE,
    )
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    metadata_json: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    tasks: Mapped[list["ProjectTask"]] = relationship(
        "ProjectTask",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ProjectTask(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tasks under a project. Each task can own multiple decisions."""

    __tablename__ = "project_tasks"
    __table_args__ = (
        UniqueConstraint("project_id", "title", name="uq_project_tasks_name"),
    )

    user_id: Mapped[Any] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[Any] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        enum_type(TaskStatus, name="project_task_status"),
        nullable=False,
        default=TaskStatus.ACTIVE,
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    metadata_json: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    current_decision_id: Mapped[Any | None] = mapped_column(
        ForeignKey("decisions.id", ondelete="SET NULL"),
        nullable=True,
    )
    latest_run_id: Mapped[Any | None] = mapped_column(
        ForeignKey("decision_runs.id", ondelete="SET NULL"),
        nullable=True,
    )

    project: Mapped[Project] = relationship(
        "Project",
        back_populates="tasks",
    )
    decisions: Mapped[list["Decision"]] = relationship(
        "Decision",
        back_populates="task",
        foreign_keys="[Decision.task_id]",
        cascade="all, delete-orphan",
    )
    current_decision: Mapped[Optional["Decision"]] = relationship(
        "Decision",
        foreign_keys=[current_decision_id],
        post_update=True,
    )
    latest_run: Mapped[Optional["DecisionRun"]] = relationship(
        "DecisionRun",
        foreign_keys=[latest_run_id],
        post_update=True,
    )


class Decision(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User decision definition (question + context)."""

    __tablename__ = "decisions"

    user_id: Mapped[Any] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[Any] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_id: Mapped[Any] = mapped_column(ForeignKey("project_tasks.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    options: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    criteria: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    status: Mapped[DecisionRecordStatus] = mapped_column(
        enum_type(DecisionRecordStatus, name="decision_status"),
        nullable=False,
        default=DecisionRecordStatus.DRAFT,
    )
    last_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    latest_run_id: Mapped[Any | None] = mapped_column(
        ForeignKey("decision_runs.id", ondelete="SET NULL"),
        nullable=True,
    )
    run_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    task: Mapped[ProjectTask] = relationship(
        "ProjectTask",
        back_populates="decisions",
        foreign_keys="[Decision.task_id]",
    )
    project: Mapped[Project] = relationship("Project")
    latest_run: Mapped[Optional["DecisionRun"]] = relationship(
        "DecisionRun",
        foreign_keys=[latest_run_id],
        post_update=True,
    )
    runs: Mapped[list["DecisionRun"]] = relationship(
        "DecisionRun",
        back_populates="decision",
        foreign_keys="[DecisionRun.decision_id]",
        cascade="all, delete-orphan",
    )


class DecisionRun(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Single orchestrator execution for a decision."""

    __tablename__ = "decision_runs"

    decision_id: Mapped[Any] = mapped_column(ForeignKey("decisions.id", ondelete="CASCADE"), nullable=False)
    project_id: Mapped[Any] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    task_id: Mapped[Any] = mapped_column(ForeignKey("project_tasks.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[Any] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[DecisionRunStatus] = mapped_column(
        enum_type(DecisionRunStatus, name="decision_run_status"),
        nullable=False,
        default=DecisionRunStatus.PENDING,
    )
    stage: Mapped[str] = mapped_column(String(64), nullable=False, default="queued")
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    message: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    queued_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    result_markdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    result_json: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    agents_snapshot: Mapped[list[Dict[str, Any]] | None] = mapped_column(JSONType, nullable=True)
    options_snapshot: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    criteria_snapshot: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    context_snapshot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    question_snapshot: Mapped[str] = mapped_column(Text, nullable=False)

    decision: Mapped[Decision] = relationship(
        "Decision",
        back_populates="runs",
        foreign_keys=[decision_id],
    )
    artifacts: Mapped[list["DecisionArtifact"]] = relationship(
        "DecisionArtifact",
        back_populates="run",
        cascade="all, delete-orphan",
    )
    agents: Mapped[list["DecisionAgent"]] = relationship(
        "DecisionAgent",
        back_populates="run",
        cascade="all, delete-orphan",
    )


class DecisionAgent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Metadata about an agent participating in a run."""

    __tablename__ = "decision_agents"

    run_id: Mapped[Any] = mapped_column(ForeignKey("decision_runs.id", ondelete="CASCADE"), nullable=False)
    agent_key: Mapped[str] = mapped_column(String(64), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    model: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parameters: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    metrics: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    run: Mapped[DecisionRun] = relationship(
        "DecisionRun",
        back_populates="agents",
    )


class DecisionArtifact(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Artifacts produced during each stage of a run."""

    __tablename__ = "decision_artifacts"

    run_id: Mapped[Any] = mapped_column(ForeignKey("decision_runs.id", ondelete="CASCADE"), nullable=False)
    agent_id: Mapped[Any | None] = mapped_column(
        ForeignKey("decision_agents.id", ondelete="SET NULL"),
        nullable=True,
    )
    stage: Mapped[str] = mapped_column(String(32), nullable=False)
    artifact_type: Mapped[ArtifactType] = mapped_column(
        enum_type(ArtifactType, name="decision_artifact_type"),
        nullable=False,
    )
    label: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    content: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    markdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scores: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    raw_payload: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)

    run: Mapped[DecisionRun] = relationship(
        "DecisionRun",
        back_populates="artifacts",
    )
    agent: Mapped[Optional[DecisionAgent]] = relationship("DecisionAgent")


class AuditEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Security/audit log for key decision actions."""

    __tablename__ = "audit_events"

    user_id: Mapped[Any | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    decision_id: Mapped[Any | None] = mapped_column(ForeignKey("decisions.id", ondelete="SET NULL"), nullable=True)
    run_id: Mapped[Any | None] = mapped_column(ForeignKey("decision_runs.id", ondelete="SET NULL"), nullable=True)
    event_type: Mapped[AuditEventType] = mapped_column(
        enum_type(AuditEventType, name="audit_event_type"),
        nullable=False,
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[Dict[str, Any] | None] = mapped_column(JSONType, nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)


__all__ = [
    "Project",
    "ProjectVisibility",
    "ProjectTask",
    "TaskStatus",
    "Decision",
    "DecisionRecordStatus",
    "DecisionRun",
    "DecisionRunStatus",
    "DecisionAgent",
    "DecisionArtifact",
    "ArtifactType",
    "AuditEvent",
    "AuditEventType",
]