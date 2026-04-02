"""
End-to-end smoke test for NGT-AI.

This script exercises the critical backend flows:
1. Register & login a fresh user.
2. Fetch workspace snapshot (projects/tasks should be empty for the new user).
3. Create a project and a task.
4. Submit a decision job wired to that task.
5. Poll status until completion and then fetch the final report.

Usage:
    python tests/system_flow_test.py

Environment variables:
    NGTAI_API_BASE_URL  Base URL for the FastAPI backend (default: http://localhost:8000/api)
    NGTAI_POLL_TIMEOUT  Seconds to wait for a decision run to finish (default: 120)
    NGTAI_POLL_INTERVAL Seconds between status polls (default: 4)
"""

from __future__ import annotations

import os
import sys
import time
import uuid
from dataclasses import dataclass

import requests


DEFAULT_BASE_URL = "http://localhost:8000/api"
BASE_URL = os.getenv("NGTAI_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
POLL_TIMEOUT = int(os.getenv("NGTAI_POLL_TIMEOUT", "120"))
POLL_INTERVAL = float(os.getenv("NGTAI_POLL_INTERVAL", "4"))


def api_url(path: str) -> str:
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{BASE_URL}{path}"


def pretty_print(title: str, payload: dict | list | str | None) -> None:
    print(f"\n[{title}]")
    if payload is None:
        print("  (no payload)")
        return
    if isinstance(payload, (dict, list)):
        import json

        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(payload)


@dataclass
class ApiContext:
    session: requests.Session
    token: str | None = None

    def set_token(self, token: str) -> None:
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})


class SystemSmokeTest:
    def __init__(self) -> None:
        self.ctx = ApiContext(session=requests.Session())
        self.slug = uuid.uuid4().hex[:10]
        self.email = f"demo_{self.slug}@example.com"
        self.password = "TempPass!123"
        self.nickname = f"demo-{self.slug[:5]}"
        self.project_id: str | None = None
        self.task_id: str | None = None
        self.run_id: str | None = None

    # ----------------------------- helpers ----------------------------- #
    def _post(self, path: str, json=None, expected: int = 200):
        response = self.ctx.session.post(api_url(path), json=json)
        pretty_print(f"POST {path}", response.json() if response.content else response.text)
        if response.status_code != expected:
            raise AssertionError(f"POST {path} expected {expected} got {response.status_code}")
        return response.json()

    def _get(self, path: str, expected: int = 200):
        response = self.ctx.session.get(api_url(path))
        pretty_print(f"GET {path}", response.json() if response.content else response.text)
        if response.status_code != expected:
            raise AssertionError(f"GET {path} expected {expected} got {response.status_code}")
        return response.json()

    # ----------------------------- steps ----------------------------- #
    def register_user(self) -> None:
        payload = {
            "email": self.email,
            "password": self.password,
            "nickname": self.nickname,
        }
        data = self._post("/auth/register", json=payload, expected=201)
        token = data["access_token"]
        self.ctx.set_token(token)
        print(f"✅ Registered user {self.email}")

    def login_user(self) -> None:
        payload = {"email": self.email, "password": self.password}
        data = self._post("/auth/login", json=payload, expected=200)
        token = data["access_token"]
        self.ctx.set_token(token)
        print(f"✅ Logged in user {self.email}")

    def fetch_workspace(self) -> None:
        data = self._get("/workspace", expected=200)
        assert "projects" in data
        print(f"Workspace has {len(data['projects'])} projects")

    def create_project(self) -> None:
        payload = {"name": f"System Flow {self.slug}"}
        data = self._post("/workspace/projects", json=payload, expected=201)
        self.project_id = data["id"]
        print(f"✅ Created project {self.project_id}")

    def create_task(self) -> None:
        assert self.project_id
        payload = {"title": f"Smoke Task {self.slug}"}
        data = self._post(f"/workspace/projects/{self.project_id}/tasks", json=payload, expected=201)
        self.task_id = data["id"]
        print(f"✅ Created task {self.task_id}")

    def submit_decision(self) -> None:
        assert self.project_id and self.task_id
        payload = {
            "project_id": self.project_id,
            "task_id": self.task_id,
            "question": "系统集成测试：是否扩容 NGTAI 集群？",
            "context": "目标：在 2025 年 Q4 支撑 5 倍用户增长。",
            "options": ["立即扩容", "按需扩容", "暂缓"],
            "criteria": ["成本", "风险", "体验"],
            "agents": [
                {
                    "id": "AI-OPS",
                    "type": "discussant",
                    "model": "mock-ops",
                    "prompt": "扮演运维负责人，关注稳定与SLA。",
                },
                {
                    "id": "AI-FIN",
                    "type": "discussant",
                    "model": "mock-fin",
                    "prompt": "扮演财务负责人，关注ROI与现金流。",
                },
                {
                    "id": "AI-PM",
                    "type": "discussant",
                    "model": "mock-pm",
                    "prompt": "扮演产品负责人，关注用户体验与增长。",
                },
                {
                    "id": "AI-REF",
                    "type": "referee",
                    "model": "mock-referee",
                    "prompt": "总结观点并给出仲裁决策。",
                },
            ],
        }
        data = self._post("/decision/analyze", json=payload, expected=202)
        self.run_id = data["run_id"]
        print(f"✅ Decision run queued: {self.run_id}")

    def wait_for_completion(self) -> None:
        assert self.run_id
        deadline = time.time() + POLL_TIMEOUT
        last_status = None
        while time.time() < deadline:
            data = self._get(f"/decision/status/{self.run_id}", expected=200)
            last_status = data["status"]
            print(
                f"  -> status={last_status} stage={data.get('stage')} progress={data.get('progress')}%"
            )
            if last_status in {"completed", "failed", "cancelled"}:
                if last_status != "completed":
                    raise AssertionError(f"Decision run ended with status {last_status}")
                print("✅ Decision run completed")
                return
            time.sleep(POLL_INTERVAL)
        raise TimeoutError(f"Decision run did not finish within {POLL_TIMEOUT}s (last status {last_status})")

    def fetch_result(self) -> None:
        assert self.run_id
        data = self._get(f"/decision/result/{self.run_id}", expected=200)
        assert data.get("result_json"), "result_json missing"
        assert data.get("result_markdown"), "result_markdown missing"
        print("✅ Retrieved final decision report")

    # ----------------------------- orchestrator ----------------------------- #
    def run(self) -> None:
        steps = [
            ("register", self.register_user),
            ("login", self.login_user),
            ("workspace", self.fetch_workspace),
            ("create_project", self.create_project),
            ("create_task", self.create_task),
            ("submit_decision", self.submit_decision),
            ("wait_finish", self.wait_for_completion),
            ("fetch_result", self.fetch_result),
        ]

        for name, func in steps:
            print(f"\n=== Step: {name} ===")
            func()


def main() -> None:
    print(f"NGT-AI system smoke test using base URL: {BASE_URL}")
    tester = SystemSmokeTest()
    try:
        tester.run()
    except Exception as exc:  # pragma: no cover - CLI entry point
        print(f"❌ Test failed: {exc}")
        sys.exit(1)
    print("\n🎉 All system checks passed.")


if __name__ == "__main__":
    main()
