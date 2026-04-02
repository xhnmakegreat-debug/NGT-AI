"""
Workspace (projects/tasks) API.
"""

from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user
from backend.app.db import get_db
from backend.app.models import ProjectTask, TaskStatus, User
from backend.app.repositories.workspace_repository import WorkspaceRepository
from backend.app.schemas import (
    ProjectCreateRequest,
    ProjectSummary,
    ProjectUpdateRequest,
    TaskCreateRequest,
    TaskSummary,
    TaskUpdateRequest,
    WorkspaceSnapshot,
)

router = APIRouter(prefix="/workspace", tags=["工作区"])


def _task_to_summary(task: ProjectTask) -> TaskSummary:
    run = task.latest_run
    return TaskSummary(
        id=task.id,
        project_id=task.project_id,
        title=task.title,
        status=task.status.value if isinstance(task.status, TaskStatus) else str(task.status),
        updated_at=task.updated_at,
        stage=run.stage if run else None,
        progress=run.progress if run else None,
        last_run_status=run.status.value if run else None,
        last_run_id=run.id if run else None,
    )


def _project_to_summary(project) -> ProjectSummary:
    tasks = [_task_to_summary(task) for task in project.tasks]
    return ProjectSummary(
        id=project.id,
        name=project.name,
        summary=project.summary,
        path=project.path,
        color=project.color,
        tasks=tasks,
    )


@router.get("", response_model=WorkspaceSnapshot)
def list_workspace(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    projects = repo.list_projects_with_tasks(current_user.id)
    return WorkspaceSnapshot(projects=[_project_to_summary(project) for project in projects])


@router.post("/projects", response_model=ProjectSummary, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    project = repo.create_project(
        user_id=current_user.id,
        name=payload.name.strip(),
        summary=payload.summary.strip() if payload.summary else None,
        color=payload.color,
    )
    db.commit()
    db.refresh(project)
    return _project_to_summary(project)


@router.patch("/projects/{project_id}", response_model=ProjectSummary)
def update_project(
    project_id: UUID,
    payload: ProjectUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    project = repo.get_project(current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    name = payload.name.strip() if payload.name else project.name
    summary = payload.summary.strip() if payload.summary else project.summary
    repo.rename_project(project, name=name, summary=summary)
    if payload.color:
        project.color = payload.color
    db.commit()
    db.refresh(project)
    return _project_to_summary(project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    project = repo.get_project(current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    repo.delete_project(project)
    db.commit()
    return None


@router.post("/projects/{project_id}/tasks", response_model=TaskSummary, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: UUID,
    payload: TaskCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    project = repo.get_project(current_user.id, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")

    task = repo.create_task(
        project=project,
        title=payload.title.strip(),
        summary=payload.summary.strip() if payload.summary else None,
    )
    db.commit()
    db.refresh(task)
    return _task_to_summary(task)


@router.patch("/tasks/{task_id}", response_model=TaskSummary)
def update_task(
    task_id: UUID,
    payload: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    task = repo.get_task(current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    if payload.title:
        task.title = payload.title.strip()
    if payload.summary is not None:
        task.summary = payload.summary.strip()
    db.commit()
    db.refresh(task)
    return _task_to_summary(task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = WorkspaceRepository(db)
    task = repo.get_task(current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    repo.delete_task(task)
    db.commit()
    return None
