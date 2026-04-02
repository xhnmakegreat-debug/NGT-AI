"""
决策任务服务
封装核心 NGT 决策流程、状态同步与持久化。
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from ngt_ai_mvp import NGTDecisionApp

from backend.app.models import (
    ArtifactType,
    AuditEvent,
    AuditEventType,
    DecisionRunStatus,
)
from backend.app.repositories.decision_repository import DecisionRepository

logger = logging.getLogger(__name__)

PROGRESS_TTL_SECONDS = 3600


@dataclass
class DecisionJob:
    """待执行的决策任务上下文"""

    run_id: UUID
    decision_id: UUID
    task_id: UUID
    user_id: UUID
    question: str
    context: str
    options: List[str]
    criteria: List[str]
    agents: List[Dict[str, Any]]


class DecisionService:
    """
    决策任务服务：负责执行 NGT 核心流程、持久化运行状态、写入 Redis 进度。
    """

    def __init__(
        self,
        *,
        session_factory: Callable[[], Session],
        ngt_app: Optional[NGTDecisionApp] = None,
        redis_client: Any | None = None,
    ):
        self._app = ngt_app or NGTDecisionApp()
        self._session_factory = session_factory
        self._redis = redis_client

        self._jobs: dict[UUID, DecisionJob] = {}
        self._tasks: dict[UUID, asyncio.Task] = {}
        self._jobs_lock = asyncio.Lock()
        self._execution_lock = asyncio.Lock()

    async def shutdown(self) -> None:
        """关闭服务时取消未完成任务"""
        async with self._jobs_lock:
            tasks = list(self._tasks.items())
        for run_id, task in tasks:
            if not task.done():
                logger.info("取消未完成任务 %s", run_id)
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

    async def enqueue_run(
        self,
        *,
        run_id: UUID,
        decision_id: UUID,
        task_id: UUID,
        user_id: UUID,
        question: str,
        context: str,
        options: List[str],
        criteria: List[str],
        agents: List[Dict[str, Any]],
    ) -> DecisionJob:
        job = DecisionJob(
            run_id=run_id,
            decision_id=decision_id,
            task_id=task_id,
            user_id=user_id,
            question=question,
            context=context,
            options=options,
            criteria=criteria,
            agents=agents,
        )
        async with self._jobs_lock:
            self._jobs[run_id] = job

        task = asyncio.create_task(self._run_job(job), name=f"decision-{run_id}")
        async with self._jobs_lock:
            self._tasks[run_id] = task
        task.add_done_callback(lambda _t: asyncio.create_task(self._cleanup_task(run_id)))

        await self._write_progress(run_id, stage="queued", progress=0, message="任务已排队")
        return job

    async def _cleanup_task(self, run_id: UUID) -> None:
        async with self._jobs_lock:
            self._tasks.pop(run_id, None)
            self._jobs.pop(run_id, None)

    async def _run_job(self, job: DecisionJob) -> None:
        await self._mark_run_started(job.run_id)
        await self._write_progress(job.run_id, stage="initializing", progress=5, message="正在初始化决策流程...")

        try:
            async with self._execution_lock:
                result = await self._app.process_decision_json_with_agents_and_progress(
                    job.question,
                    job.agents,
                    progress_callback=lambda stage, progress, message: asyncio.create_task(
                        self._handle_progress(job.run_id, stage, progress, message)
                    ),
                )

            markdown_result = self._app.presenter.format_result(result)
            await self._persist_completion(
                job=job,
                status=DecisionRunStatus.COMPLETED,
                markdown=markdown_result,
                payload=result,
                error=None,
            )
            await self._write_progress(job.run_id, stage="completed", progress=100, message="决策分析完成")
            logger.info("决策任务 %s 完成", job.run_id)

        except asyncio.CancelledError:
            await self._persist_completion(job=job, status=DecisionRunStatus.CANCELLED, markdown=None, payload=None, error="任务被取消")
            await self._write_progress(job.run_id, stage="cancelled", progress=0, message="任务已取消")
            logger.warning("决策任务 %s 被取消", job.run_id)
            raise
        except Exception as exc:  # pragma: no cover - orchestrator errors
            logger.exception("决策任务 %s 执行失败: %s", job.run_id, exc)
            await self._persist_completion(
                job=job,
                status=DecisionRunStatus.FAILED,
                markdown=None,
                payload=None,
                error=str(exc),
            )
            await self._write_progress(job.run_id, stage="failed", progress=100, message="决策分析失败")

    async def _handle_progress(self, run_id: UUID, stage: str, progress: int, message: str) -> None:
        await self._write_progress(run_id, stage=stage, progress=progress, message=message)
        await self._persist_progress(run_id, stage=stage, progress=progress, message=message)

    async def _write_progress(self, run_id: UUID, *, stage: str, progress: int, message: str) -> None:
        if not self._redis:
            return
        payload = {
            "stage": stage,
            "progress": progress,
            "message": message,
            "updated_at": datetime.utcnow().isoformat(),
        }
        key = f"decision:progress:{run_id}"
        try:
            await self._redis.set(key, json.dumps(payload), ex=PROGRESS_TTL_SECONDS)
        except Exception as exc:  # pragma: no cover - redis errors
            logger.warning("写入 Redis 进度失败: %s", exc)

    async def _persist_progress(self, run_id: UUID, *, stage: str, progress: int, message: str) -> None:
        def _update() -> None:
            session = self._session_factory()
            try:
                repo = DecisionRepository(session)
                run = repo.get_run(run_id)
                if run:
                    repo.update_run_progress(run, stage=stage, progress=progress, message=message)
                    session.commit()
            finally:
                session.close()

        await asyncio.to_thread(_update)

    async def _mark_run_started(self, run_id: UUID) -> None:
        def _mark() -> None:
            session = self._session_factory()
            try:
                repo = DecisionRepository(session)
                run = repo.get_run(run_id)
                if run:
                    repo.mark_run_started(run, message="正在启动智能体...")
                    session.commit()
            finally:
                session.close()

        await asyncio.to_thread(_mark)

    async def _persist_completion(
        self,
        *,
        job: DecisionJob,
        status: DecisionRunStatus,
        markdown: str | None,
        payload: dict | None,
        error: str | None,
    ) -> None:
        def _persist() -> None:
            session = self._session_factory()
            try:
                repo = DecisionRepository(session)
                run = repo.get_run(job.run_id)
                if not run:
                    return

                error_count = 0
                if payload:
                    error_count = payload.get("process_info", {}).get("error_count", 0)

                repo.mark_run_completed(
                    run,
                    status=status,
                    result_markdown=markdown,
                    result_json=payload,
                    error=error,
                    error_count=error_count,
                )

                if status == DecisionRunStatus.COMPLETED and payload:
                    repo.persist_agents(run, job.agents)
                    artifacts = self._extract_artifacts(payload)
                    repo.persist_artifacts(run, artifacts=artifacts)

                event_type = (
                    AuditEventType.DECISION_COMPLETED if status == DecisionRunStatus.COMPLETED else AuditEventType.DECISION_FAILED
                )
                description = "决策完成" if status == DecisionRunStatus.COMPLETED else "决策失败"
                event = AuditEvent(
                    user_id=job.user_id,
                    decision_id=job.decision_id,
                    run_id=job.run_id,
                    event_type=event_type,
                    description=description,
                    metadata_json={
                        "status": status.value,
                        "error": error,
                    },
                )
                session.add(event)

                session.commit()
            finally:
                session.close()

        await asyncio.to_thread(_persist)

    def _extract_artifacts(self, payload: dict[str, Any]) -> List[dict[str, Any]]:
        artifacts: List[dict[str, Any]] = []
        for idea in payload.get("initial_ideas", []):
            artifacts.append(
                {
                    "stage": "stage1",
                    "artifact_type": ArtifactType.INITIAL_IDEA.value,
                    "label": idea.get("ai_id"),
                    "content": idea,
                    "raw_payload": idea,
                }
            )
        for sheet in payload.get("score_sheets", []):
            artifacts.append(
                {
                    "stage": "stage3",
                    "artifact_type": ArtifactType.SCORE_SHEET.value,
                    "label": sheet.get("scorer_ai_id"),
                    "content": sheet,
                    "raw_payload": sheet,
                }
            )
        for final_decision in payload.get("final_decisions", []):
            artifacts.append(
                {
                    "stage": "stage5",
                    "artifact_type": ArtifactType.FINAL_DECISION.value,
                    "label": final_decision.get("ai_id"),
                    "content": final_decision,
                    "raw_payload": final_decision,
                }
            )
        referee_analysis = payload.get("referee_analysis")
        if referee_analysis:
            artifacts.append(
                {
                    "stage": "stage6",
                    "artifact_type": ArtifactType.REFEREE_ANALYSIS.value,
                    "label": "REFEREE",
                    "content": referee_analysis,
                    "raw_payload": referee_analysis,
                }
            )
        statistics = payload.get("statistics")
        process_info = payload.get("process_info")
        if statistics or process_info:
            artifacts.append(
                {
                    "stage": "summary",
                    "artifact_type": ArtifactType.SUMMARY.value,
                    "label": "Summary",
                    "content": {
                        "statistics": statistics,
                        "process_info": process_info,
                    },
                    "raw_payload": {
                        "statistics": statistics,
                        "process_info": process_info,
                    },
                }
            )
        return artifacts


def create_decision_service(
    *,
    use_real_apis: bool,
    session_factory: Callable[[], Session],
    redis_client: Any | None = None,
) -> DecisionService:
    ngt_app = NGTDecisionApp(use_real_apis=use_real_apis)
    return DecisionService(session_factory=session_factory, ngt_app=ngt_app, redis_client=redis_client)


__all__ = ["DecisionService", "create_decision_service"]
