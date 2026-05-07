---
status: Completed
date: 2026-04-27
type: session_summary
pin: DEFERRED — needs proper fix before production
---

# Session: f-string Brace Escape Bug in _generate_alternatives (Bandaid Applied)

Modifies: [[backend/intelligence/synthesis.py]]
References: [[2026-04-27_Security_Hardening_Phase3_Loose_Ends]], [[2026-04-23_Phase_3_Completion_Orchestration]]

## What Was Done

Applied a **bandaid fix** (brace escaping) to unblock `POST /api/v1/content/synthesize`. The root cause and long-term fix are documented below. **This is NOT a proper resolution — see the Deferred Work section.**

## The Bug

**Symptom**: Frontend shows "Failed to synthesize strategy. Please try again." for every synthesize call.

**Root cause**: `backend/intelligence/synthesis.py:509-520` — the `_generate_alternatives` prompt is an f-string (`f"""..."""`) that embeds a JSON literal example. The JSON example uses unescaped single braces:

```python
prompt = f"""...
Return ONLY a JSON array:
[
  {                              # ← Python parses as f-string expression
    "content_angle": "...",
    "hypothesis": "...",
  },
  ...
]"""
```

Python treats `{"content_angle": "A different compelling angle", ...}` as an f-string expression, sees the `:` after `"content_angle"` as a format spec separator, and raises:

```
ValueError: Invalid format specifier ' "A different compelling angle", ...' for object of type 'str'
```

This fires **every time** `_generate_alternatives` is called, before any Gemini call is made. FastAPI catches the uncaught exception and returns HTTP 500, which the frontend `.catch()` converts to the generic toast.

**Call chain**:
```
Frontend → POST /api/v1/content/synthesize
  router.py:34–53 → generate_strategy_document(...)
    synthesis.py:400 → primary Gemini call (OK)
    synthesis.py:433 → _generate_alternatives(...) ← crashes here
      synthesis.py:487–520 → f-string evaluation → ValueError → 500
```

**Why tests missed it**: The `_generate_alternatives` path was added in the Phase 3 A/B work (commit `7b31ce2`, 2026-04-23). The existing test suite mocks at a layer that bypasses this path, or doesn't exercise the synthesis call chain end-to-end. The primary prompt at `synthesis.py:378–398` correctly uses `{{`/`}}` — so it worked. Only the second prompt (the alternatives generator) had the bug.

## Bandaid Applied

`{ → {{` and `} → }}` on all JSON literal braces in the `_generate_alternatives` f-string prompt (`synthesis.py:509–520`). Matches the pattern already used in the primary prompt in the same file.

**File changed**: `backend/intelligence/synthesis.py` lines 508–520

## ⚠️ Deferred Work — Needs Proper Fix

> **Pin this.** The bandaid works but the underlying trap remains. Any developer adding a third JSON-example prompt to this file will hit the same bug.

Three-layer proper fix:

### 1. Stop using f-strings for prompts with JSON literals (HIGH PRIORITY)
Replace the current pattern with one of:
- **Named `.format()`**: store the prompt as a plain triple-quoted string with `{var}` placeholders for variables only, then call `.format(platform=platform, posts_text=posts_text[:1500], ...)`. JSON examples stay as literal `{` / `}` with no escaping needed.
- **String concatenation**: build the prompt piecemeal — static header + variable injection + static JSON example footer.

Apply to **both** prompts in `synthesis.py` and audit `backend/content/scripting.py` (also modified on this branch — likely has the same structure).

### 2. Add a unit test for `_generate_alternatives` (HIGH PRIORITY)
A single test that calls `_generate_alternatives(primary, platform, posts)` with a stub `_gemini_json` and asserts the prompt string builds without exception would have caught this immediately. Currently the synthesis path is under-covered for the alternatives/experiment-learning integration added in Phase 3.

### 3. Surface server errors to frontend (MEDIUM PRIORITY)
`frontend/app/content/synthesize/page.tsx` — the `.catch()` discards the error and shows a generic message. The same fix as `handleGenerate` (line 94) should be applied to `handleSynthesize` and `handleRevise` (line 117): log `err.message` or show the actual response body. This turns a 30-minute debug into a 5-minute one.

## Files Changed

- `backend/intelligence/synthesis.py` — brace-escape fix on `_generate_alternatives` JSON example (lines 508–520)

## Outstanding

- [ ] Proper f-string refactor for all JSON-literal prompts in `synthesis.py` and `scripting.py`
- [ ] Unit test for `_generate_alternatives` prompt construction
- [ ] Frontend error surfacing in `synthesize/page.tsx` (handleSynthesize + handleRevise)
