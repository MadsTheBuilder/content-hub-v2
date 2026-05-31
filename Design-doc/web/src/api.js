// Single module that owns all fetch calls. No other file in web/src/ may call fetch directly.

export class ConflictError extends Error {
  constructor(message) {
    super(message);
    this.status = 409;
  }
}

const STAGE_ENDPOINTS = {
  trends: "/api/pipeline/trends",
  research: "/api/pipeline/researcher",
  ideation: "/api/pipeline/ideation",
  hooks: "/api/pipeline/hook",
  outline: "/api/pipeline/outline",
  title: "/api/pipeline/title",
  cascade: "/api/pipeline/cascade",
  "short-form": "/api/pipeline/short-form",
  "voice-cleanup": "/api/pipeline/voice-cleanup",
};

export async function runStage(stage, body) {
  const endpoint = STAGE_ENDPOINTS[stage];
  if (!endpoint) throw new Error(`No endpoint mapped for stage: ${stage}`);
  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    if (res.status === 409) throw new ConflictError(`${stage} already running`);
    throw new Error(`${stage} failed (${res.status}): ${text}`);
  }
  return res.json(); // { job_id }
}

export async function getRecent(folder, limit = 10, subfoldersOnly = false) {
  let url = `/api/vault/recent?folder=${encodeURIComponent(folder)}&limit=${limit}`;
  if (subfoldersOnly) url += "&subfolders_only=true";
  const res = await fetch(url);
  if (!res.ok) return [];
  return res.json(); // [{ name, path, modified }]
}

export async function readVaultFile(path) {
  const res = await fetch(`/api/vault/file?path=${encodeURIComponent(path)}`);
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(`File not found (${res.status}): ${text}`);
  }
  return res.json(); // { path, content }
}

export async function listOutputs(path) {
  const res = await fetch(`/api/vault/outputs?path=${encodeURIComponent(path)}`);
  if (!res.ok) return [];
  return res.json(); // [{ name, path }]
}

export async function runBrainAnalysis(content) {
  const res = await fetch("/api/brain/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    if (res.status === 409) throw new ConflictError("Brain analysis already running");
    throw new Error(`Brain analyze failed (${res.status}): ${text}`);
  }
  return res.json(); // { job_id }
}

export async function getJobStatus(jobId) {
  const res = await fetch(`/api/jobs/${encodeURIComponent(jobId)}`);
  if (!res.ok) throw new Error(`Job not found: ${res.status}`);
  return res.json(); // { job_id, stage, status, result, error, ... }
}

export async function getHealth() {
  const res = await fetch("/api/health");
  if (!res.ok) return { status: "error" };
  return res.json(); // { status, backend, capabilities }
}
