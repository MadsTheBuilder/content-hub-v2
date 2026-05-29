---
date: 2026-05-15
type: eval-report
topic: Claude Code Has Evolved
video: https://www.youtube.com/watch?v=d86VCtQ_dN8
pipeline_run: 2026-05-15_claude-code-has-evolved
description: "Eval report for the first NIM full-pipeline test run. Three failures found: broken research regex, intermittent NIM rate limiting, and hooks generated without research context."
tags: [eval, nim, pipeline, bug-report, research]
---

# NIM Test Run — Eval Report

References: [[2026-05-15_NIM_Full_Pipeline_Takeover]] | Modifies: [[skills/yt_pipeline.py]], [[skills/utils/ai.py]], [[skills/pipeline.py]]

## Summary

The pipeline ran end-to-end (exit code 0) but produced **unreliable output**. Three distinct failures were found: one critical bug that broke the research layer entirely, one infrastructure issue with [[AI Router]] (NIM) reliability, and one structural gap in how hooks are generated. All downstream content (hooks, outline, shorts, distribution) was built on a broken research foundation.

---

## Failure 1 — Research questions not extracted (CRITICAL)

### What happened

The research file `10-Research/2026-05-15_claude_code_has_evolved/research.md` contains no answers. It holds only the raw question templates (Q1–Q12) followed by a single garbled NotebookLM response that reads:

> "It appears that your query was left blank. I have reviewed the provided source..."

All 12 structured research questions were collapsed into one giant blob and sent to NotebookLM as a single query. NotebookLM saw the multi-paragraph wall of text as a malformed input and responded with a generic overview instead of answering any specific question.

### Root cause — confirmed

**File:** `skills/yt_pipeline.py`, line 28

```python
# BROKEN
SECTION_PATTERN = re.compile(r"## (Q\d+ — .+)\n(.*?)(?=\n## |\Z)", re.DOTALL)
```

The regex is compiled with `re.DOTALL`, which makes `.` match newlines. The heading capture group `(Q\d+ — .+)` uses `.+` — greedy, matches newlines in DOTALL mode. So `.+` consumes not just the heading text but the ENTIRE rest of the file. All 12 question headings and their bodies are swallowed into a single "heading" match. The body group captures nothing.

Verified by running the pattern directly against the prompts file:
- **Current pattern:** 1 match (the whole file as one "heading")
- **Fixed pattern using `[^\n]+`:** 12 matches, all correct

### Fix

```python
# FIXED — [^\n]+ stops at line boundary regardless of DOTALL
SECTION_PATTERN = re.compile(r"## (Q\d+ — [^\n]+)\n(.*?)(?=\n## |\Z)", re.DOTALL)
```

### Impact

Every pipeline step downstream of research was affected:
- **Hooks** — generated with no video-specific insights; content is generic "Claude code architecture" framing that does not match the actual video (which is about the Agentic OS framework)
- **Outline** — generic dopamine-ladder structure with invented claims ("5x more complex agents")
- **Short-form scripts** — partially recovered because the garbled NLM response at the bottom of the research file leaked the terms "Agentic OS", "reusable skills", "deterministic outputs" into the 35k-char context blob
- **Distribution** — same partial recovery

---

## Failure 2 — NIM failing silently and intermittently

### What happened

NIM was called approximately 10 times across steps 2–5. It succeeded 4 times and failed 6 times. Every failure fell back to Gemini 2.5 Flash successfully, so no step errored out. But the NIM failure log showed an empty error message every time:

```
WARNING: NIM meta/llama-3.1-70b-instruct failed: 
```

Nothing after the colon. No HTTP status code, no response body.

### Root cause — confirmed

**File:** `skills/utils/ai.py`, lines 88–96

```python
except Exception as e:
    logger.warning("NIM %s failed: %s", model, e)
    return {"text": "", "success": False, ...}
```

When `httpx` throws a transport-level exception (connection reset, empty response from a rate-limited endpoint), `str(e)` is often an empty string or just an exception class name with no message. This is what produced the blank log line. The actual HTTP status code and response body are never captured or logged.

The intermittent pattern (4 successes, 6 failures across one pipeline run) is consistent with **NIM free tier per-minute rate limiting**, not credit exhaustion. NIM worked on the first call of a step, then failed on subsequent rapid-fire calls within the same step, then recovered in the next step after the natural delay between pipeline steps.

### Fix

Two changes needed in `_nim_generate()`:

1. Log the HTTP status code and response body before the exception path, so failures are diagnosable:
```python
return {"text": "", "success": False, "provider": f"nim/{model}",
        "error": f"HTTP {response.status_code}: {response.text[:200]}"}
```

2. Add a short sleep (1–2s) between cascade attempts so rapid retries don't immediately hit the rate limit again.

### Impact

NIM is effectively acting as an unreliable first attempt. Gemini 2.5 Flash is doing the real work for hooks, outline, and the blog post. NIM only reliably handles the shorter-context calls (short-form scripts, Twitter/LinkedIn). The pipeline still completes, but the NIM integration is not delivering value at its current reliability level.

---

## Failure 3 — Hook step has no research context (STRUCTURAL)

### What happened

The hooks generated for this video are entirely disconnected from the actual video content. They discuss "re-engineered Claude code", "5x more complex agents", and "prompt engineering obsolescence" — none of which the video covers. The video is about building an Agentic OS with a Skill Backbone, Memory Layer, and Dashboard.

### Root cause

**File:** `skills/pipeline.py`, line 64

```python
rc = step("2/5 — Hooks (NIM)", [sys.executable, str(SKILLS / "hook.py"), topic])
```

Only the topic string is passed to `hook.py`. No `--research-file` argument is provided. Compare this to the outline, short-form, and cascade steps, which all receive `--research-file` and `--outline-file` when available. Hooks are generated blind — from the topic title alone.

Even if the research bug were fixed, hooks would still be generic without this argument.

### Fix

Pass the research file to hook.py the same way outline.py receives it:

```python
hook_cmd = [sys.executable, str(SKILLS / "hook.py"), topic]
if research_file.exists():
    hook_cmd += ["--research-file", str(research_file)]
rc = step("2/5 — Hooks (NIM)", hook_cmd)
```

Note: `hook.py` would also need to accept and use `--research-file` if it doesn't already.

### Impact

Hooks are the highest-stakes output — they determine whether the video gets watched. Generating them without research context means the most important step of the pipeline is effectively random.

---

## Additional observations

### Primary sources: 0 found (expected)
The video is a tutorial on the Agentic OS framework — it has no arxiv papers or GitHub repos in its description. The NIM/Gemini backstop for primary source suggestions also returned nothing. This is expected for this content type. Not a bug.

### Stale log text in skill scripts
The hook and outline steps logged "Drafting hooks (Ollama → Gemini)..." and "Polishing with Claude..." — these strings are hardcoded in the skill scripts and were not updated when the NIM routing was added. Not a functional issue, but misleading during debugging.

---

## Fix priority

| # | Issue | File | Severity |
|---|---|---|---|
| 1 | SECTION_PATTERN regex uses `.+` instead of `[^\n]+` | `skills/yt_pipeline.py:28` | Critical |
| 2 | NIM errors not logged with status code + body | `skills/utils/ai.py:88-96` | High |
| 3 | Hook step not passed `--research-file` | `skills/pipeline.py:64` | High |
| 4 | `hook.py` needs to accept + use `--research-file` arg | `skills/hook.py` | High |
| 5 | Stale routing text in skill log output | `skills/hook.py`, `skills/outline.py` | Low |
