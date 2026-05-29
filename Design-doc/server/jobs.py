"""In-memory job registry and SSE event bus.

Single-job-at-a-time constraint: while _current_job_id is set, new POST
requests should return 409. Cleared on job completion or failure.
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class JobResult:
    result_type: str        # "file" | "bundle" | "file_set" | "brain_result"
    primary_path: str
    outputs: list           # list[str] paths for file/bundle; empty for brain_result
    data: Optional[dict] = None  # brain_result payload only


@dataclass
class Job:
    job_id: str
    stage: str
    status: str             # "running" | "completed" | "failed"
    started_at: str
    completed_at: Optional[str] = None
    result: Optional[JobResult] = None
    error: Optional[str] = None
    stdout_lines: list = field(default_factory=list)
    stderr_lines: list = field(default_factory=list)
    queue: asyncio.Queue = field(default_factory=asyncio.Queue)


_jobs: dict[str, Job] = {}
_current_job_id: Optional[str] = None


def get_current_job_id() -> Optional[str]:
    return _current_job_id


def create_job(stage: str) -> Job:
    global _current_job_id
    job_id = str(uuid.uuid4())[:8]
    job = Job(
        job_id=job_id,
        stage=stage,
        status="running",
        started_at=datetime.utcnow().isoformat(),
        queue=asyncio.Queue(),
    )
    _jobs[job_id] = job
    _current_job_id = job_id
    return job


def get_job(job_id: str) -> Optional[Job]:
    return _jobs.get(job_id)


def complete_job(job_id: str, result: JobResult) -> None:
    global _current_job_id
    job = _jobs.get(job_id)
    if job:
        job.status = "completed"
        job.completed_at = datetime.utcnow().isoformat()
        job.result = result
        job.queue.put_nowait({
            "type": "done",
            "result": {
                "result_type": result.result_type,
                "primary_path": result.primary_path,
                "outputs": result.outputs,
                "data": result.data,
            },
        })
    if _current_job_id == job_id:
        _current_job_id = None


def fail_job(job_id: str, error: str) -> None:
    global _current_job_id
    job = _jobs.get(job_id)
    if job:
        job.status = "failed"
        job.completed_at = datetime.utcnow().isoformat()
        job.error = error
        job.queue.put_nowait({"type": "error", "error": error})
    if _current_job_id == job_id:
        _current_job_id = None
