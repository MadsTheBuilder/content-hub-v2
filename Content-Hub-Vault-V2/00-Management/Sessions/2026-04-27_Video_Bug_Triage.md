# Session: Video Bug Triage — 2026-04-27

**Branch**: `feature/phase3-loose-ends`
**Type**: Investigative / Triage
**Output**: `tmp/video-bug-report.md`

---

## What Changed

No code changes this session — pure analysis. Analyzed a 1:14 screen recording of Content Hub via:
1. Local frame extraction (opencv, 1 frame/4s → 21 PNG frames in `tmp/frames/`)
2. Direct visual frame analysis
3. Code cross-reference: `_run_generation` pipeline, scripting, research service, renderers, storage, mock client

---

## Confirmed Findings

### P0 — [[Content Generation Pipeline]] always fails
`_run_generation` background task in [[backend/content/router.py]] succeeds through DB setup and scripting, then crashes in the renderer. Two-layer failure:
1. Sync `client.models.generate_content()` calls in [[backend/content/scripting.py]] and [[backend/research/research_service.py]] block the uvicorn event loop for ~20-30s, freezing the "Initialising Neural Pipeline" UI state
2. After Gemini completes, renderer crashes: either Playwright browser binaries not installed (`playwright install chromium` missing from setup), or Supabase Storage bucket "content-hub" doesn't exist → `upload_file()` raises → `status="failed"`
- Surfaces as `window.alert("Generation failed: …")` at [[frontend/app/content/synthesize/page.tsx]]:135

### P0 — Auth redirect to deleted `/login` page
`frontend/lib/api.ts`:33 — `window.location.href = "/login"` — auth pages were deleted in Phase 3 (commit `7b31ce2`). Any 401 → hard 404.
- Modifies: [[frontend/lib/api.ts]]

### P1 — Sync Gemini SDK calls block async event loop
`client.models.generate_content()` is synchronous, called from async background task. Fix: switch to `await client.aio.models.generate_content()`.
- Modifies: [[backend/content/scripting.py]], [[backend/research/research_service.py]]

### P1 — 13 `window.alert()` + 1 `window.prompt()` across frontend
Existing [[frontend/components/Toast.tsx]] (`useToast`) is unused in these paths. All 13 call sites should use `toast.error()`.
- Modifies: [[frontend/app/content/synthesize/page.tsx]] (4 alert + 1 prompt) + 5 other files

### P2 — `MockSupabaseClient.storage` not implemented
[[backend/database.py]]:125 — `MockSupabaseClient` has no `.storage` attribute. `upload_file()` raises `AttributeError` in mock mode. Latent; demo ran on real Supabase.

---

## Files Touched by Analysis (read-only)

- `backend/content/router.py`
- `backend/content/scripting.py`
- `backend/content/renderer_slides.py`
- `backend/content/renderer_video.py`
- `backend/content/renderer_talking_head.py`
- `backend/storage/client.py`
- `backend/database.py`
- `backend/research/research_service.py`
- `frontend/app/content/synthesize/page.tsx`
- `frontend/lib/api.ts`
- `requirements.txt`

---

## Open Items

- Implement async Gemini fix in scripting.py + research_service.py
- Run `playwright install chromium` or add to setup docs
- Verify/create "content-hub" Supabase Storage bucket
- Replace 13 `alert()` + 1 `prompt()` with Toast
- Update `api.ts:33` auth redirect target
- Add `MockStorage` stub to `MockSupabaseClient`

References: [[backend/content/router.py]], [[frontend/app/content/synthesize/page.tsx]], [[backend/content/scripting.py]], [[backend/research/research_service.py]], [[backend/database.py]]
