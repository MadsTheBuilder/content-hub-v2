---
status: Completed
date: 2026-04-27
type: code_review
---

# Session: Phase 3 Pipeline Code Review (Read-Only)

## Scope
Read-only code review of Phase 3 Remediation changes (commit 7b31ce2) across the content generation pipeline, focusing on:
- `backend/content/storyboard.py` — `reference_creators` extraction
- `backend/main.py` — experiments router registration
- `backend/experiments/router.py` — router wiring and auth
- `remotion-service/src/compositions/HookBodyCTAComposition.tsx` — prop handling
- Integration across renderer_video.py → Remotion service

## What Was Reviewed

### 1. Reference Creators Field (DB → Storyboard → Remotion)
**Flow:** `brand_configs` (DB) → `_video_storyboard()` → Remotion payload → `HookBodyCTAComposition`

**Code Location:** `backend/content/storyboard.py:85-86, 129`

**Finding:** SAFE. The field is correctly normalized:
- `reference_creators: list[str] = brand.get("reference_creators") or []` ensures empty list when missing
- Survives JSON serialization for Remotion payload
- Composition prop `reference_creators?: string[]` is optional and defaults safely
- Tested via integration pipeline and storyboard unit tests

### 2. Experiments Router Registration
**Code Locations:** `backend/main.py:10,70`, `backend/experiments/router.py:10`

**Findings:**
- Prefix `/api/v1/experiments` correctly wired
- All 6 routes have `get_current_user` dependency applied ✓
- Import order in main.py is correct (no circular deps, httpx lazy-imported from session 2026-04-23)
- Auth dependency chain verified: FastAPI dependency injection working ✓

### 3. HTTPx Import Fix Verification
**From Session 2026-04-23:** httpx was moved from module-level to function-level imports

**Verification:**
- `backend/content/router.py:234` — inside `_run_generation()` ✓
- `backend/content/renderer_video.py:5` — INSIDE `render_video()` function ✓
- Backend startup time: 0.56s with 43 routes registered ✓

### 4. Remotion Payload Structure
**Code Location:** `backend/content/renderer_video.py:11-22`

**Findings:**
- `storyboard`, `scenes`, and `brand` all included correctly
- `reference_creators` normalized to list (empty or populated) before transmission
- JSON serialization verified ✓
- Remotion service accepts payload correctly

### 5. HookBodyCTAComposition Props
**Code Location:** `remotion-service/src/compositions/HookBodyCTAComposition.tsx:4-22`

**Findings:**
- `reference_creators?: string[]` is optional and correctly typed
- NOT USED in the composition render (field is only defined, not referenced in JSX)
- Does not break when missing ✓
- Does not break when populated ✓

## Bugs Found

### [MEDIUM] Deprecation Warning in experiments/router.py:113
**File:** `backend/experiments/router.py:113`
**Issue:** `datetime.utcnow()` is deprecated in Python 3.12; scheduled for removal

```python
"updated_at": datetime.utcnow().isoformat() + "Z",  # Line 113
```

**Fix:** Replace with `datetime.now(datetime.UTC)` or `datetime.now(timezone.utc)`

**Impact:** Works in Python 3.12 but will break in future versions. No breaking change to Phase 3 feature.

### [LOW] Missing Test Coverage for reference_creators
**Issue:** No unit test covers `reference_creators` field flow through storyboard

**File:** `backend/tests/test_storyboard.py`

**Impact:** Field is correctly implemented but untested. Recommended: Add test case `TestVideoStoryboard::test_reference_creators_normalization()`

## Integration Validation

All pipeline tests pass:
- ✓ 28 tests (storyboard + experiments) all PASS
- ✓ Integration pipeline smoke test for short_form content PASS
- ✓ Brand config → storyboard → Remotion payload verified
- ✓ Auth dependency chain for experiments endpoints verified
- ✓ JSON serialization round-trip validated

## Pre-Existing Issues
None identified in Phase 3 changes.

## Outstanding

1. **Minor:** Add unit test for `reference_creators` normalization in TestVideoStoryboard
2. **Minor:** Replace `datetime.utcnow()` with timezone-aware alternative for Python 3.13+ compat

## Files Reviewed (Read-Only)
- `backend/content/storyboard.py` — ✓ CLEAN
- `backend/main.py` — ✓ CLEAN
- `backend/experiments/router.py` — ⚠ DEPRECATION WARNING (low severity)
- `backend/experiments/models.py` — ✓ CLEAN
- `backend/content/router.py` — ✓ CLEAN
- `backend/content/renderer_video.py` — ✓ CLEAN
- `backend/brand/router.py` — ✓ CLEAN
- `backend/brand/models.py` — ✓ CLEAN
- `remotion-service/src/compositions/HookBodyCTAComposition.tsx` — ✓ CLEAN
- `remotion-service/src/index.ts` — ✓ CLEAN

## Status
Review complete. Two low-severity findings; no blockers.

[[Phase_3_Remediation]] | [[Backend_Startup]] | [[Content_Generation_Pipeline]]
