"""
Decision persistence helpers (decisions, runs, agents, artifacts).
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from backend.app.models import (
    ArtifactType,
    Decision,
    DecisionAgent,
    DecisionArtifact,
    DecisionRecordStatus,
    DecisionRun,
    DecisionRunStatus,
    ProjectTask,
    TaskStatus,
)


class DecisionRepository:
    """CRUD helpers for decision submissions."""

    def __init__(self, db: Session):
        self.db = db

    # ------------------------------------------------------------------ #
    # Decision creation
    # ------------------------------------------------------------------ #
    def create_decision(
        self,
        *,
        user_id: UUID,
        project_id: UUID,
        task_id: UUID,
        title: str,
        question: str,
        context: str | None,
        options: list[str] | None,
        criteria: list[str] | None,
    ) -> Decision:
        decision = Decision(
            user_id=user_id,
            project_id=project_id,
            task_id=task_id,
            title=title,
            question=question,
            context=context,
            options=options or None,
            criteria=criteria or None,
            status=DecisionRecordStatus.DRAFT,
        )
        self.db.add(decision)
        self.db.flush()
        return decision

    def create_run(
        self,
        *,
        decision: Decision,
        project_id: UUID,
        task_id: UUID,
        user_id: UUID,
        question: str,
        context: str | None,
        options: list[str] | None,
        criteria: list[str] | None,
        agents_snapshot: list[dict] | None,
    ) -> DecisionRun:
        run = DecisionRun(
            decision_id=decision.id,
            project_id=project_id,
            task_id=task_id,
            user_id=user_id,
            status=DecisionRunStatus.PENDING,
            stage="queued",
            progress=0,
            question_snapshot=question,
            context_snapshot=context,
            options_snapshot=options or None,
            criteria_snapshot=criteria or None,
            agents_snapshot=agents_snapshot,
        )
        self.db.add(run)
        self.db.flush()

        decision.run_count += 1
        decision.latest_run_id = run.id
        decision.status = DecisionRecordStatus.RUNNING

        task = self.db.get(ProjectTask, task_id)
        if task:
            task.current_decision_id = decision.id
            task.latest_run_id = run.id
            task.status = TaskStatus.RUNNING

        return run

    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #
    def get_run_for_user(self, *, run_id: UUID, user_id: UUID) -> Optional[DecisionRun]:
        stmt: Select[DecisionRun] = (
            select(DecisionRun)
            .join(Decision, DecisionRun.decision_id == Decision.id)
            .where(DecisionRun.id == run_id, DecisionRun.user_id == user_id)
            .options(
                selectinload(DecisionRun.decision),
                selectinload(DecisionRun.artifacts),
                selectinload(DecisionRun.agents),
            )
        )
        return self.db.execute(stmt).scalars().first()

    def get_run(self, run_id: UUID) -> Optional[DecisionRun]:
        stmt = select(DecisionRun).where(DecisionRun.id == run_id)
        return self.db.execute(stmt).scalars().first()

    # ------------------------------------------------------------------ #
    # Status transitions
    # ------------------------------------------------------------------ #
    def mark_run_started(self, run: DecisionRun, *, message: str | None = None) -> DecisionRun:
        run.status = DecisionRunStatus.RUNNING
        run.started_at = datetime.utcnow()
        run.stage = "initializing"
        run.progress = max(run.progress, 5)
        if message:
            run.message = message

        decision = run.decision
        decision.status = DecisionRecordStatus.RUNNING

        task = self.db.get(ProjectTask, run.task_id)
        if task:
            task.status = TaskStatus.RUNNING

        return run

    def update_run_progress(self, run: DecisionRun, *, stage: str, progress: int, message: str) -> DecisionRun:
        run.stage = stage
        run.progress = progress
        run.message = message
        return run

    def mark_run_completed(
        self,
        run: DecisionRun,
        *,
        status: DecisionRunStatus,
        result_markdown: str | None,
        result_json: dict | None,
        error: str | None = None,
        error_count: int = 0,
    ) -> DecisionRun:
        run.status = status
        run.completed_at = datetime.utcnow()
        run.result_markdown = result_markdown
        run.result_json = result_json
        run.error = error
        run.error_count = error_count
        run.progress = 100 if status == DecisionRunStatus.COMPLETED else run.progress
        run.stage = "completed" if status == DecisionRunStatus.COMPLETED else "failed"

        decision = run.decision
        decision.latest_run_id = run.id
        if status == DecisionRunStatus.COMPLETED:
            decision.status = DecisionRecordStatus.COMPLETED
        elif status == DecisionRunStatus.CANCELLED:
            decision.status = DecisionRecordStatus.CANCELLED
        else:
            decision.status = DecisionRecordStatus.FAILED
        decision.last_error = error

        task = self.db.get(ProjectTask, run.task_id)
        if task:
            task.latest_run_id = run.id
            if status == DecisionRunStatus.COMPLETED:
                task.status = TaskStatus.COMPLETED
            elif status == DecisionRunStatus.CANCELLED:
                task.status = TaskStatus.ACTIVE
            else:
                task.status = TaskStatus.FAILED

        return run

    # ------------------------------------------------------------------ #
    # Agent & artifact helpers
    # ------------------------------------------------------------------ #
    def persist_agents(self, run: DecisionRun, agents: Iterable[dict]) -> list[DecisionAgent]:
        records: list[DecisionAgent] = []
        for payload in agents:
            record = DecisionAgent(
                run_id=run.id,
                agent_key=payload.get("id") or payload.get("agent_key") or "unknown",
                role=payload.get("type") or payload.get("role") or "discussant",
                model=payload.get("model"),
                prompt=payload.get("prompt"),
                parameters=payload.get("parameters"),
            )
            self.db.add(record)
            records.append(record)
        self.db.flush()
        return records

    def persist_artifacts(
        self,
        run: DecisionRun,
        *,
        artifacts: Iterable[dict],
    ) -> list[DecisionArtifact]:
        records: list[DecisionArtifact] = []
        for item in artifacts:
            artifact_type = item.get("artifact_type")
            if isinstance(artifact_type, str):
                try:
                    artifact_type = ArtifactType(artifact_type)
                except ValueError:
                    artifact_type = ArtifactType.RAW
            elif artifact_type is None:
                artifact_type = ArtifactType.RAW

            record = DecisionArtifact(
                run_id=run.id,
                agent_id=item.get("agent_id"),
                stage=item.get("stage") or "stage1",
                artifact_type=artifact_type,
                label=item.get("label"),
                content=item.get("content"),
                markdown=item.get("markdown"),
                scores=item.get("scores"),
                raw_payload=item.get("raw_payload"),
            )
            self.db.add(record)
            records.append(record)
        self.db.flush()
        return records


__all__ = ["DecisionRepository"]
