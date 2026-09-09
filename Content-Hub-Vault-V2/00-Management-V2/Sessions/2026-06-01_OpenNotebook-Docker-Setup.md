---
date: 2026-06-01
type: session-log
description: "Docker setup for open-notebook — wiring the open-notebook REST backend into the researcher pipeline. Setup in progress, API not yet responding."
tags: [open-notebook, docker, researcher, backend, setup]
---

# Session — Open-Notebook Docker Setup

References: [[researcher.py]], [[open_notebook_client.py]], [[open_notebook_seed.py]], [[Local_First_Skill_Engine_Plan]]

---

## What Was Done

Wired `open-notebook` (open-source NotebookLM alternative) as an optional backend in [[researcher.py]]. The system now supports `--backend auto` (tries open-notebook first, falls back to notebooklm), `--backend open-notebook`, and `--backend notebooklm`.

### Files Created/Modified
- `skills/open_notebook_client.py` — async HTTP client for open-notebook REST API (port 5055)
- `skills/helpers/open_notebook_seed.py` — seed question generator using Claude CLI instead of NLM
- `skills/researcher.py` — added `research_one_open_notebook()` and `--backend` arg

### Docker Setup Progress

Created `C:\Users\madhu\open-notebook\docker-compose.yml` with two services:
- `surrealdb` — database backend (port 8000)
- `opennotebook` — open-notebook app (ports 8502 UI, 5055 API)

Image: `lfnovo/open_notebook:v1-latest`

---

## Current Status — BLOCKED

The open-notebook container starts but the API on port 5055 is not responding.

**Root cause identified:** The container's real startup command is:
```
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
```

The app reads `SURREAL_URL` env var to connect to SurrealDB. All env vars are confirmed set correctly inside the container. The API crashes at startup trying to run database migrations before SurrealDB is fully ready.

**Last attempted fix:** Added `sleep 5` before supervisord startup via `command:` override in docker-compose.yml. Not yet confirmed working — session handed over before retest.

---

## Handover State

### docker-compose.yml location
`C:\Users\madhu\open-notebook\docker-compose.yml`

### Last command run
```powershell
docker compose down --remove-orphans
docker compose up -d
```

### Next step to verify
```powershell
curl http://localhost:5055/notebooks
```
Expected: `[]` — if still failing, check logs:
```powershell
docker logs open-notebook-opennotebook-1 2>&1 | Select-String "error|ERROR|started|ready" -CaseSensitive:$false
```

### If still failing — try this
The `sleep 5` may not be enough. Increase to `sleep 10` in docker-compose.yml or add a proper healthcheck on surrealdb:
```yaml
  surrealdb:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 5s
      timeout: 3s
      retries: 5

  opennotebook:
    depends_on:
      surrealdb:
        condition: service_healthy
```
Then remove the `sleep 5` command override.

### Also check
- Open UI at http://localhost:8502 — if that loads, the app is up and only the API port is the issue
- `ANTHROPIC_API_KEY` is set in docker-compose.yml (key was added by user during session)

---

## Open Items
- [ ] Confirm `curl http://localhost:5055/notebooks` returns `[]`
- [ ] Open http://localhost:8502 and configure API key in Settings UI
- [ ] Add `OPEN_NOTEBOOK_BASE_URL` to `.env` if using non-default port
- [ ] Test end-to-end: `python -m skills.researcher --backend open-notebook`
