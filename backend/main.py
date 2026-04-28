import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.auth.router import router as auth_router
from backend.workflows.router import router as workflows_router
from backend.content.router import router as content_router
from backend.brand.router import router as brand_router
from backend.experiments.router import router as experiments_router
from backend.scheduler.jobs import start_scheduler, scheduler
from backend.config import settings

logger = logging.getLogger(__name__)

_REQUIRED_PRODUCTION_SECRETS = {
    "REMOTION_SECRET": settings.remotion_secret,
    "SUPABASE_JWT_SECRET": settings.supabase_jwt_secret,
}


def _validate_production_secrets() -> None:
    """Abort startup when running in production with any required secret unset.

    Secrets must be non-empty strings.  Empty string, whitespace-only, and the
    literal placeholder values used in .env.example are all treated as unset.
    """
    if settings.environment.lower() != "production":
        return

    _PLACEHOLDER_PREFIXES = ("your-", "change-me", "<", "todo")
    missing: list[str] = []
    for name, value in _REQUIRED_PRODUCTION_SECRETS.items():
        stripped = (value or "").strip()
        is_placeholder = any(stripped.lower().startswith(p) for p in _PLACEHOLDER_PREFIXES)
        if not stripped or is_placeholder:
            missing.append(name)

    if missing:
        logger.critical(
            "STARTUP ABORTED — the following secrets are required in production but are "
            "missing or contain placeholder values: %s",
            ", ".join(missing),
        )
        sys.exit(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    _validate_production_secrets()
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
app.include_router(experiments_router)


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
