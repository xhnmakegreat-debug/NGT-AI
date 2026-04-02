"""
Pydantic schemas for workspace (projects/tasks).
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskSummary(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    status: str
    updated_at: datetime
    stage: str | None = None
    progress: int | None = None
    last_run_status: str | None = None
    last_run_id: UUID | None = None


class ProjectSummary(BaseModel):
    id: UUID
    name: str
    summary: str | None = None
    path: str | None = None
    color: str | None = None
    tasks: list[TaskSummary] = Field(default_factory=list)


class WorkspaceSnapshot(BaseModel):
    projects: list[ProjectSummary]


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    summary: str | None = Field(default=None, max_length=500)
    color: str | None = Field(default=None, max_length=32)


class ProjectUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = Field(default=None, max_length=500)
    color: str | None = Field(default=None, max_length=32)


class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: str | None = Field(default=None, max_length=500)


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    summary: str | None = Field(default=None, max_length=500)


__all__ = [
    "TaskSummary",
    "ProjectSummary",
    "WorkspaceSnapshot",
    "ProjectCreateRequest",
    "ProjectUpdateRequest",
    "TaskCreateRequest",
    "TaskUpdateRequest",
]
