"""FastAPI orchestration service — port 8765.

Start from repo root:
    .venv\\Scripts\\python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload

All skill subprocess invocations use the same repo .venv (see runtime.md).
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# Ensure sibling modules (jobs, pipeline, vault, brain) are importable
sys.path.insert(0, str(Path(__file__).parent))

import brain as brain_module
import jobs
import pipeline
import vault

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {"status": "ok", "backend": "up", "capabilities": None}


# ---------------------------------------------------------------------------
# Vault
# ---------------------------------------------------------------------------

@app.get("/api/vault/recent")
async def vault_recent(folder: str = "10-Research", limit: int = 10, subfolders_only: bool = False):
    return vault.recent(folder, min(limit, 50), subfolders_only)


@app.get("/api/vault/file")
async def vault_file(path: str):
    content = vault.read_file(path)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found or path outside vault")
    return {"path": path, "content": content}


@app.get("/api/vault/outputs")
async def vault_outputs(path: str):
    return vault.outputs(path)


# ---------------------------------------------------------------------------
# Job status + SSE stream
# ---------------------------------------------------------------------------

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "job_id": job.job_id,
        "stage": job.stage,
        "status": job.status,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "result": (
            {
                "result_type": job.result.result_type,
                "primary_path": job.result.primary_path,
                "outputs": job.result.outputs,
                "data": job.result.data,
            }
            if job.result
            else None
        ),
        "error": job.error,
    }


@app.get("/api/jobs/{job_id}/stream")
async def stream_job(job_id: str):
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    async def _events():
        # Drain already-buffered events (handles race where job finishes before
        # the client connects to the SSE endpoint)
        while not job.queue.empty():
            event = job.queue.get_nowait()
            yield f"data: {json.dumps(event)}\n\n"

        if job.status in ("completed", "failed"):
            return

        while True:
            try:
                event = await asyncio.wait_for(job.queue.get(), timeout=30.0)
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("type") in ("done", "error"):
                    break
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'type': 'ping'})}\n\n"

    return StreamingResponse(
        _events(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ---------------------------------------------------------------------------
# Conflict guard
# ---------------------------------------------------------------------------

def _check_conflict():
    current = jobs.get_current_job_id()
    if current:
        raise HTTPException(status_code=409, detail=f"Job {current} is already running")


# ---------------------------------------------------------------------------
# Request body models
# ---------------------------------------------------------------------------

class TrendsBody(BaseModel):
    space: str = ""


class ResearcherBody(BaseModel):
    niche: str
    repos: list[str] = []
    mode: str = "deep"
    trend_repo: Optional[str] = ""
    target_length: Optional[int] = None
    tone: Optional[str] = ""
    audience: Optional[str] = ""
    banned_phrases: list[str] = []


class IdeationBody(BaseModel):
    topic: str
    research_file: Optional[str] = ""
    no_trends: bool = False


class HookBody(BaseModel):
    topic: str
    platform: str = "yt-long"
    audience: str = ""
    format: str = "medium"
    research_file: Optional[str] = ""
    no_polish: bool = False


class OutlineBody(BaseModel):
    topic: str
    hook_path: Optional[str] = ""
    length: int = 8
    platform: str = "yt-long"
    no_polish: bool = False


class TitleBody(BaseModel):
    concept: str = ""
    outline_file: Optional[str] = ""


class CascadeBody(BaseModel):
    research_file: Optional[str] = ""
    outline_file: Optional[str] = ""
    title: Optional[str] = ""
    youtube_url: Optional[str] = ""


class ShortFormBody(BaseModel):
    research_file: Optional[str] = ""
    outline_file: Optional[str] = ""
    title: Optional[str] = ""
    youtube_url: Optional[str] = ""


class VoiceCleanupBody(BaseModel):
    file_path: str
    inplace: bool = False


class BrainBody(BaseModel):
    content: str


# ---------------------------------------------------------------------------
# Pipeline endpoints
# ---------------------------------------------------------------------------

@app.post("/api/pipeline/researcher")
async def run_researcher(body: ResearcherBody):
    _check_conflict()
    job_id = await pipeline.run_researcher(
        body.niche, body.repos, body.mode, body.trend_repo or "",
        body.target_length, body.tone or "", body.audience or "", body.banned_phrases,
    )
    return {"job_id": job_id}


@app.post("/api/pipeline/trends")
async def run_trends(body: TrendsBody = None):
    _check_conflict()
    job_id = await pipeline.run_trends(body.space if body else "")
    return {"job_id": job_id}


@app.post("/api/pipeline/ideation")
async def run_ideation(body: IdeationBody):
    _check_conflict()
    job_id = await pipeline.run_ideation(body.topic, body.research_file or "", body.no_trends)
    return {"job_id": job_id}


@app.post("/api/pipeline/hook")
async def run_hook(body: HookBody):
    _check_conflict()
    job_id = await pipeline.run_hook(
        body.topic, body.platform, body.audience,
        body.format, body.research_file or "", body.no_polish,
    )
    return {"job_id": job_id}


@app.post("/api/pipeline/outline")
async def run_outline(body: OutlineBody):
    _check_conflict()
    job_id = await pipeline.run_outline(
        body.topic, body.hook_path or "", body.length,
        body.platform, body.no_polish,
    )
    return {"job_id": job_id}


@app.post("/api/pipeline/title")
async def run_title(body: TitleBody):
    if not body.concept.strip() and not (body.outline_file or "").strip():
        raise HTTPException(status_code=422, detail="Provide a concept or outline_file")
    _check_conflict()
    job_id = await pipeline.run_title(body.concept.strip(), body.outline_file or "")
    return {"job_id": job_id}


@app.post("/api/pipeline/cascade")
async def run_cascade(body: CascadeBody):
    _check_conflict()
    job_id = await pipeline.run_cascade(
        body.research_file or "", body.outline_file or "",
        body.title or "", body.youtube_url or "",
    )
    return {"job_id": job_id}


@app.post("/api/pipeline/short-form")
async def run_short_form(body: ShortFormBody):
    _check_conflict()
    job_id = await pipeline.run_short_form(
        body.research_file or "", body.outline_file or "",
        body.title or "", body.youtube_url or "",
    )
    return {"job_id": job_id}


@app.post("/api/pipeline/voice-cleanup")
async def run_voice_cleanup(body: VoiceCleanupBody):
    _check_conflict()
    job_id = await pipeline.run_voice_cleanup(body.file_path, body.inplace)
    return {"job_id": job_id}


# ---------------------------------------------------------------------------
# Brain endpoint
# ---------------------------------------------------------------------------

@app.post("/api/brain/analyze")
async def analyze_brain(body: BrainBody):
    _check_conflict()
    job = jobs.create_job("brain")

    async def _run():
        try:
            data = await brain_module.analyze(body.content)
            result = jobs.JobResult(result_type="brain_result", primary_path="", outputs=[], data=data)
            jobs.complete_job(job.job_id, result)
        except Exception as exc:
            jobs.fail_job(job.job_id, str(exc))

    asyncio.create_task(_run())
    return {"job_id": job.job_id}
