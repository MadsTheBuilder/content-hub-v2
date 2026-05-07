import sys
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from backend.auth.router import router as auth_router
from backend.workflows.router import router as workflows_router
from backend.content.router import router as content_router
from backend.brand.router import router as brand_router
from backend.experiments.router import router as experiments_router
from backend.config import settings

logger = logging.getLogger(__name__)

# Initialize scheduler (will be started in lifespan)
scheduler = BackgroundScheduler()

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


def setup_scheduled_jobs() -> list[dict]:
    """
    Register all scheduled jobs with APScheduler.

    Registers the daily auto-commit job at 6:00 AM.

    Returns:
        List of dicts with job metadata: name, next_run_time, last_run_time
    """
    from daily import run_auto_commit

    def auto_commit_job():
        """Execute auto-commit pipeline with logging."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "scheduler.log"

        try:
            result = run_auto_commit()
            with open(log_file, "a") as f:
                timestamp = datetime.now().isoformat()
                f.write(
                    f"[{timestamp}] daily-auto-commit: "
                    f"success={result['success']}, "
                    f"files_staged={result['files_staged']}, "
                    f"commit_hash={result['commit_hash']}\n"
                )
            logger.info(
                f"Auto-commit job completed: success={result['success']}, "
                f"commit_hash={result['commit_hash']}"
            )
        except Exception as e:
            with open(log_file, "a") as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] daily-auto-commit ERROR: {str(e)}\n")
            logger.error(f"Auto-commit job failed: {str(e)}")

    # Register the daily auto-commit job at 6:00 AM
    scheduler.add_job(
        auto_commit_job,
        "cron",
        hour=6,
        minute=0,
        id="daily-auto-commit",
        name="Daily Auto-Commit (vault sync + quality checks + commit)",
        replace_existing=True,
    )

    # Build job metadata list
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append(
            {
                "name": job.name,
                "id": job.id,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "last_run_time": job.last_run_time.isoformat() if job.last_run_time else None,
            }
        )

    return jobs


@asynccontextmanager
async def lifespan(app: FastAPI):
    _validate_production_secrets()

    # Initialize and start scheduler
    scheduler.start()
    jobs = setup_scheduled_jobs()

    # Log scheduled jobs on startup
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "scheduler.log"

    with open(log_file, "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n[{timestamp}] Scheduler started with jobs:\n")
        for job in jobs:
            next_run = job["next_run_time"] or "N/A"
            f.write(f"  - {job['name']} → next run: {next_run}\n")

    logger.info(f"Scheduler active: {len(jobs)} job(s) scheduled")
    for job in jobs:
        logger.info(f"  {job['name']} at {job['next_run_time']}")

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
