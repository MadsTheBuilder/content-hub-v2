---
type: reference
date: "2026-05-22"
created: "2026-05-22"
tags: [reference, web-app, server, runtime]
description: "Python runtime notes for the Design-doc FastAPI server — interpreter path and shared-venv constraint."
references:
  - "[[Design_Doc_Web_App_Plan]]"
  - "[[Webapp_sprint]]"
---

# Design-doc Server — Runtime Notes

## Resolved interpreter

The FastAPI server runs in the **repo root `.venv`** (not a separate server venv).

- Interpreter: `C:\Users\madhu\Claude cowork\Content Hub V2\.venv\Scripts\python.exe`
- Confirmed working: Python 3.12.10 as of 2026-05-22
- Dependencies are in the root `requirements.txt`; key web-wrapper packages: `fastapi`, `uvicorn`, `aiofiles`, `anthropic`, `python-dotenv`

## First-time install / sync

From the repo root (`C:\Users\madhu\Claude cowork\Content Hub V2\`), run:

```
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This shared `.venv` must contain both the existing pipeline/backend dependencies and the Design-doc wrapper dependencies before either server is started.

The current pinned requirements were verified against Python 3.12.10. Python 3.14 was the source of the earlier install drift and is not the supported shared runtime for this repo today.

## How to start the server

From the repo root (`C:\Users\madhu\Claude cowork\Content Hub V2\`):

```
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload
```

Or from `Design-doc/server/`:
```
..\..\.venv\Scripts\python.exe -m uvicorn main:app --port 8765 --reload
```

If you are already inside the activated repo `.venv`, `python -m uvicorn ...` is equivalent.

## Locked constraint

**No** `Design-doc/server/.venv` or `Design-doc/server/requirements.txt`. The wrapper inherits the repo environment so skills subprocesses share the same dependency surface.
