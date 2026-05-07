---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/main.py"
category: "Content Hub Source Code"
---

# main.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.auth.router import router as auth_router
from backend.workflows.router import router as workflows_router
from backend.content.router import router as content_router
from backend.brand.router import router as brand_router
from backend.scheduler.jobs import start_scheduler, scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(title="Content Hub API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(workflows_router)
app.include_router(content_router)
app.include_router(brand_router)


@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}


@app.get("/api/v1/status")
async def status():
    from backend.database import _is_placeholder
    return {
        "status": "ok",
        "mock_mode": _is_placeholder(),
        "version": "2.0.0",
    }

```
