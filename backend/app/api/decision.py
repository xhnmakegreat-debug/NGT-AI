"""
决策分析 API - 负责接收任务、查询进度以及返回结果。
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user
from backend.app.db import get_db
from backend.app.models import (
    AuditEvent,
    AuditEventType,
    DecisionRun,
    DecisionRunStatus,
    Project,
    ProjectTask,
    TaskStatus,
    User,
)
from backend.app.repositories.decision_repository import DecisionRepository
from backend.app.repositories.workspace_repository import WorkspaceRepository
from backend.app.services.decision_service import DecisionService

router = APIRouter()
logger = logging.getLogger(__name__)

STAGE_LABELS = {
    "queued": "阶段 0 · 排队中",
    "initializing": "阶段 0 · 初始化",
    "stage1": "阶段 1 · 独立观点",
    "stage3": "阶段 3 · 交叉评分",
    "stage4": "阶段 4 · 分数聚合",
    "stage5": "阶段 5 · 修正/捍卫",
    "stage6": "阶段 6 · 裁判汇总",
    "completed": "阶段 6 · 裁判汇总",
    "failed": "执行失败",
}


class AgentConfig(BaseModel):
    """AI 智能体配置"""

    id: str = Field(..., description="智能体 ID")
    type: str = Field(..., description="智能体类型 discussant/referee")
    model: str = Field(..., description="模型名称")
    prompt: str = Field(..., description="角色提示词")


class DecisionRequest(BaseModel):
    """提交决策任务的 payload"""

    question: str = Field(..., min_length=5, max_length=4000, description="需要分析的核心问题")
    context: str | None = Field(default=None, max_length=8000, description="补充背景或约束条件")
    options: List[str] = Field(default_factory=list, description="备选方案列表")
    criteria: List[str] = Field(default_factory=list, description="决策评估指标")
    agents: List[AgentConfig] = Field(default_factory=list, description="AI 智能体配置列表")
    project_id: UUID | None = Field(default=None, description="已有项目 ID")
    project_name: str | None = Field(default=None, description="新建项目名称")
    task_id: UUID | None = Field(default=None, description="已有任务 ID")
    task_title: str | None = Field(default=None, description="新建任务标题")


class DecisionAcceptedResponse(BaseModel):
    decision_id: str
    run_id: str
    project_id: str
    task_id: str
    status: str
    message: str
    queued_at: datetime


class DecisionStatusResponse(BaseModel):
    decision_id: str
    run_id: str
    project_id: str
    task_id: str
    question: str
    status: str
    progress: int
    stage: str
    message: str | None
    created_at: datetime
    updated_at: datetime
    queued_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    error: str | None
    error_count: int
    current_stage: str
    stage_progress: Dict[str, Any]


class DecisionResultResponse(DecisionStatusResponse):
    result_markdown: Optional[str] = None
    result_json: Optional[Dict[str, Any]] = None


def get_decision_service(request: Request) -> DecisionService:
    service: Optional[DecisionService] = getattr(request.state, "decision_service", None)
    if not service:
        raise HTTPException(status_code=500, detail="Decision service not initialized")
    return service


def _normalized_stage(stage: str) -> str:
    return STAGE_LABELS.get(stage, stage)


def _generate_project_name(question: str) -> str:
    prefix = question.strip().splitlines()[0][:16]
    timestamp = datetime.utcnow().strftime("%m%d%H%M")
    return f"{prefix or 'Quick'} · {timestamp}"


def _generate_task_title(question: str) -> str:
    headline = question.strip().splitlines()[0][:42]
    return headline or "新建任务"


async def _read_progress_snapshot(request: Request, run_id: UUID) -> dict[str, Any] | None:
    redis_client = getattr(request.app.state, "redis", None)
    if not redis_client:
        return None
    key = f"decision:progress:{run_id}"
    try:
        data = await redis_client.get(key)
    except Exception as exc:  # pragma: no cover - network errors
        logger.warning("读取 Redis 进度失败: %s", exc)
        return None
    if not data:
        return None
    try:
        import json

        return json.loads(data)
    except Exception:  # pragma: no cover - defensive
        return None


def _build_status_response(run: DecisionRun, progress_override: dict[str, Any] | None = None) -> DecisionStatusResponse:
    stage = progress_override.get("stage") if progress_override else run.stage
    progress = progress_override.get("progress") if progress_override else run.progress
    message = progress_override.get("message") if progress_override else run.message
    return DecisionStatusResponse(
        decision_id=str(run.decision_id),
        run_id=str(run.id),
        project_id=str(run.project_id),
        task_id=str(run.task_id),
        question=run.question_snapshot,
        status=run.status.value,
        progress=progress or 0,
        stage=stage,
        message=message,
        created_at=run.created_at,
        updated_at=run.updated_at,
        queued_at=run.queued_at,
        started_at=run.started_at,
        completed_at=run.completed_at,
        error=run.error,
        error_count=run.error_count,
        current_stage=_normalized_stage(stage or "queued"),
        stage_progress={
            "stage": stage,
            "progress": progress,
            "message": message,
        },
    )


def _build_result_response(run: DecisionRun, progress_override: dict[str, Any] | None = None) -> DecisionResultResponse:
    status = _build_status_response(run, progress_override)
    return DecisionResultResponse(**status.model_dump(), result_markdown=run.result_markdown, result_json=run.result_json)


def _record_audit_event(
    db: Session,
    *,
    user: User,
    decision_id: UUID,
    run_id: UUID,
    event_type: AuditEventType,
    description: str,
    metadata: Dict[str, Any] | None = None,
) -> None:
    event = AuditEvent(
        user_id=user.id,
        decision_id=decision_id,
        run_id=run_id,
        event_type=event_type,
        description=description,
        metadata_json=metadata,
    )
    db.add(event)


def _ensure_project_and_task(
    *,
    payload: DecisionRequest,
    current_user: User,
    workspace_repo: WorkspaceRepository,
) -> tuple[Project, ProjectTask]:
    if payload.task_id:
        task = workspace_repo.get_task(current_user.id, payload.task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权访问")
        if task.status == TaskStatus.ARCHIVED:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="任务已归档，无法继续执行")
        project = task.project
        return project, task

    if payload.project_id:
        project = workspace_repo.get_project(current_user.id, payload.project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在或无权访问")
        title = payload.task_title or _generate_task_title(payload.question)
        task = workspace_repo.create_task(project=project, title=title)
        return project, task

    name = payload.project_name or _generate_project_name(payload.question)
    project = workspace_repo.create_project(user_id=current_user.id, name=name, summary=None)
    task_title = payload.task_title or _generate_task_title(payload.question)
    task = workspace_repo.create_task(project=project, title=task_title)
    return project, task


@router.post(
    "/decision/analyze",
    response_model=DecisionAcceptedResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def analyze_decision(
    payload: DecisionRequest,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """提交决策分析任务"""
    question = payload.question.strip()
    if len(question) < 5:
        raise HTTPException(status_code=400, detail="问题内容过短")

    workspace_repo = WorkspaceRepository(db)
    decision_repo = DecisionRepository(db)

    project, task = _ensure_project_and_task(payload=payload, current_user=current_user, workspace_repo=workspace_repo)

    decision = decision_repo.create_decision(
        user_id=current_user.id,
        project_id=project.id,
        task_id=task.id,
        title=task.title,
        question=question,
        context=payload.context.strip() if payload.context else None,
        options=payload.options,
        criteria=payload.criteria,
    )

    run = decision_repo.create_run(
        decision=decision,
        project_id=project.id,
        task_id=task.id,
        user_id=current_user.id,
        question=question,
        context=payload.context.strip() if payload.context else None,
        options=payload.options,
        criteria=payload.criteria,
        agents_snapshot=[agent.model_dump() for agent in payload.agents],
    )

    _record_audit_event(
        db,
        user=current_user,
        decision_id=decision.id,
        run_id=run.id,
        event_type=AuditEventType.DECISION_SUBMITTED,
        description="用户提交新的决策任务",
        metadata={"question": question},
    )

    db.commit()
    db.refresh(run)

    service = get_decision_service(request)
    await service.enqueue_run(
        run_id=run.id,
        decision_id=decision.id,
        task_id=task.id,
        user_id=current_user.id,
        question=question,
        context=payload.context or "",
        options=payload.options,
        criteria=payload.criteria,
        agents=[agent.model_dump() for agent in payload.agents],
    )

    return DecisionAcceptedResponse(
        decision_id=str(decision.id),
        run_id=str(run.id),
        project_id=str(project.id),
        task_id=str(task.id),
        status=run.status.value,
        message="任务已加入队列",
        queued_at=run.queued_at,
    )


@router.get("/decision/status/{run_id}", response_model=DecisionStatusResponse)
async def get_decision_status(
    run_id: UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = DecisionRepository(db)
    run = repo.get_run_for_user(run_id=run_id, user_id=current_user.id)
    if not run:
        raise HTTPException(status_code=404, detail="未找到对应的决策任务")

    progress_override = await _read_progress_snapshot(request, run_id)
    return _build_status_response(run, progress_override)


@router.get("/decision/result/{run_id}", response_model=DecisionResultResponse)
async def get_decision_result(
    run_id: UUID,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    repo = DecisionRepository(db)
    run = repo.get_run_for_user(run_id=run_id, user_id=current_user.id)
    if not run:
        raise HTTPException(status_code=404, detail="未找到对应的决策任务")

    progress_override = await _read_progress_snapshot(request, run_id)
    return _build_result_response(run, progress_override)
