# Copilot / AI Agent Instructions — NGT AI System

This file gives concise, project-specific guidance so an AI coding agent can be productive editing and extending this repository.

1. Big picture
- Purpose: a minimal AI orchestration demo. Main runtime is `ngt_ai_mvp.py` which constructs an `Orchestrator` from `src/core/orchestrator.py` and runs it with a prompt.
- Major components:
  - `src/core` — orchestrator, parser, and state tracker; implements the runtime flow.
  - `src/providers` — pluggable LLM providers (`MockProvider`, `OpenAIProvider`) implementing `BaseProvider.complete(messages)`.
  - `src/models` — lightweight dataclasses (`Message`, `Conversation`) used to model messages.
  - `src/utils` — small helpers: `logger` and `presenter`.
- Data flow: `Orchestrator.run(prompt)` appends a `user` message to `Conversation`, converts to a list of dicts, calls `provider.complete(messages)`, appends `assistant` message with the response, and returns it.

2. Developer workflows
- Install deps and run (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
python run.py
```

- Run tests:

```powershell
python -m pytest -q
```

- To switch provider to OpenAI, edit `config.yaml` or instantiate `OpenAIProvider(api_key="...")` and ensure `openai` is installed.

3. Project-specific conventions & patterns
- Providers follow the `BaseProvider` interface and accept a list of message dicts with `role` and `content` keys. Example: `[{"role":"user","content":"hi"}]`.
- `Conversation` stores `Message` dataclasses; convert to provider format via `dict(role=m.role, content=m.content)`.
- Tests are simple unit tests using `pytest` and import code under `src` package-style (no package install required).
- Keep provider logic thin: mapping between dataclasses and provider API happens in `Orchestrator` or small adapter functions.

4. Integration points and external deps
- `OpenAIProvider` uses the `openai` package and `OPENAI_API_KEY` env var; it expects ChatCompletion API. If `openai` is missing, instantiate provider only in environments with the SDK.
- `config.yaml` controls the default provider (`provider: mock|openai`) and `openai_api_key`.

5. Files to edit for common tasks
- Add new provider: `src/providers/your_provider.py`, implement `BaseProvider.complete`.
- Extend orchestrator logic: `src/core/orchestrator.py`.
- Add new message parsing: `src/core/parser.py`.

6. Examples from repo
- Creating a conversation and calling provider (see `src/core/orchestrator.py`).
- Mock provider behavior: `src/providers/mock_provider.py` — simple echo for tests.

7. Safety & secrets
- Never commit real API keys to `config.yaml` or source files. Use `OPENAI_API_KEY` env var or CI secrets.

8. When in doubt
- Follow existing simple style: small, explicit functions; avoid heavy dependency additions unless needed.

If any part of the project's real runtime differs from this scaffold (build steps, configs, or external services), tell me and I will update this file accordingly.

9. Windows convenience scripts
- `setup.bat` — creates a virtual environment in `.venv` and installs `requirements.txt` (Windows `cmd`/`bat`).
- `start.bat` — activates the `.venv` (if present) and runs `run.py`.

Example (Windows `cmd`):

```
setup.bat    # run once to prepare env
start.bat    # start the app
```