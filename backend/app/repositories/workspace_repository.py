"""
Persistence helpers for workspace (projects & tasks).
"""

from __future__ import annotations

import math
from typing import Iterable, Optional
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from backend.app.models import (
    Decision,
    Project,
    ProjectTask,
    TaskStatus,
)


class WorkspaceRepository:
    """Encapsulates CRUD logic for user projects and tasks."""

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------ #
    # Project helpers
    # ------------------------------------------------------------------ #
    def list_projects_with_tasks(self, user_id: UUID) -> list[Project]:
        stmt: Select[Project] = (
            select(Project)
            .where(Project.user_id == user_id, Project.is_archived.is_(False))
            .order_by(Project.sort_order, Project.created_at)
            .options(
                selectinload(Project.tasks)
                .options(
                    selectinload(ProjectTask.latest_run),
                    selectinload(ProjectTask.decisions),
                )
            )
        )
        result = self.db.execute(stmt)
        projects = result.scalars().unique().all()
        for project in projects:
            project.tasks = [
                task for task in project.tasks if task.status != TaskStatus.ARCHIVED
            ]
            project.tasks.sort(key=lambda t: (t.sort_order, t.created_at))
        return projects

    def get_project(self, user_id: UUID, project_id: UUID) -> Optional[Project]:
        stmt = select(Project).where(
            Project.id == project_id,
            Project.user_id == user_id,
            Project.is_archived.is_(False),
        )
        return self.db.execute(stmt).scalars().first()

    def create_project(
        self,
        *,
        user_id: UUID,
        name: str,
        summary: str | None = None,
        color: str | None = None,
        path: str | None = None,
    ) -> Project:
        next_order = self._next_project_order(user_id)
        project = Project(
            user_id=user_id,
            name=name,
            summary=summary,
            color=color,
            path=path,
            sort_order=next_order,
        )
        self.db.add(project)
        self.db.flush()
        if not project.path:
            project.path = f"projects/{str(project.id)[:8]}"
        return project

    def rename_project(self, project: Project, *, name: str, summary: str | None = None) -> Project:
        project.name = name
        if summary is not None:
            project.summary = summary
        return project

    def delete_project(self, project: Project) -> None:
        self.db.delete(project)

    # ------------------------------------------------------------------ #
    # Task helpers
    # ------------------------------------------------------------------ #
    def get_task(self, user_id: UUID, task_id: UUID) -> Optional[ProjectTask]:
        stmt = (
            select(ProjectTask)
            .where(
                ProjectTask.id == task_id,
                ProjectTask.user_id == user_id,
                ProjectTask.status != TaskStatus.ARCHIVED,
            )
            .options(selectinload(ProjectTask.project))
        )
        return self.db.execute(stmt).scalars().first()

    def create_task(
        self,
        *,
        project: Project,
        title: str,
        summary: str | None = None,
        status: TaskStatus = TaskStatus.ACTIVE,
    ) -> ProjectTask:
        next_order = self._next_task_order(project.id)
        task = ProjectTask(
            user_id=project.user_id,
            project_id=project.id,
            title=title,
            summary=summary,
            status=status,
            sort_order=next_order,
        )
        self.db.add(task)
        self.db.flush()
        return task

    def update_task_status(self, task: ProjectTask, status: TaskStatus) -> ProjectTask:
        task.status = status
        return task

    def delete_task(self, task: ProjectTask) -> None:
        self.db.delete(task)

    # ------------------------------------------------------------------ #
    # Decision linkage
    # ------------------------------------------------------------------ #
    def attach_decision_to_task(self, task: ProjectTask, decision: Decision) -> None:
        task.current_decision_id = decision.id
        task.latest_run_id = decision.latest_run_id

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _next_project_order(self, user_id: UUID) -> int:
        stmt = select(func.max(Project.sort_order)).where(Project.user_id == user_id)
        current = self.db.execute(stmt).scalar()
        return int(current or 0) + 1

    def _next_task_order(self, project_id: UUID) -> int:
        stmt = select(func.max(ProjectTask.sort_order)).where(ProjectTask.project_id == project_id)
        current = self.db.execute(stmt).scalar()
        return int(current or 0) + 1


__all__ = ["WorkspaceRepository"]
