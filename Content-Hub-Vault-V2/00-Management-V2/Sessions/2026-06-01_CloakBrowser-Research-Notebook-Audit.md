---
date: 2026-06-01
type: session-log
description: "Deep post-mortem of CloakBrowser research run — full execution trace through researcher.py, notebooklm-py endpoints, source verification, repo context extraction failure, rate-limit mechanics, and synthesize_brief data-contract breakage."
tags: [audit, researcher, notebooklm, rate-limit, cloakbrowser, synthesize_brief, source-verification]
---

# Session — CloakBrowser Research Run: Deep Audit

References: [[researcher.py]], [[notebooklm-py]], [[_chat.py]], [[_core.py]], [[_notebooks.py]], [[nlm_seed.py]], [[research_plan.py]], [[2026-06-01_browser-cloak_cloakbrowser_brief]], [[2026-06-01_CloakBrowser/research]], [[2026-06-01_ARIS-Research-Notebook-Audit]]

---

## Notebook: `6828efa7-f920-4ae3-ac4d-d85d5e770779`

Repo: `CloakHQ/CloakBrowser` | Stars: 22,845 | Velocity: 705.3/day | Repo age as of 2026-06-01: brand new/viral

---

## Stage-by-Stage Execution Trace

### Stage 1 — Notebook + Source Setup (`researcher.py:229–270`)

```
create("Research: CloakHQ-CloakBrowser — 2026-06-01")
    → batchexecute CCqFvf (CREATE_NOTEBOOK) → success

sources.add_url(nb.id, "https://github.com/CloakHQ/CloakBrowser", wait=True)
    → batchexecute izAoDd (ADD_SOURCE) → success, polled to READY
    → NOT counted in primary_count

sources.add_url(nb.id, "https://raw.githubusercontent.com/CloakHQ/CloakBrowser/main/README.md", wait=False)
    → batchexecute izAoDd → success (main branch confirmed)
    → primary_count = 1 ← this is the "1" in primary_sources_found

discover_primary_docs("CloakHQ/CloakBrowser", max_docs=6)
    → returned 0 candidates
    → No docs/, examples/, or other structured documentation dirs found
    → primary_count stays at 1
```

**Finding 1 — `primary_sources_found` is a misleading metric.** It counts only the README and doc-crawler additions — not the initial GitHub page URL added at line 241. `primary_sources_found: 1` means "2 sources total: GitHub page + README". The metric name implies total primary sources but excludes the most important one.

---

### Stage 2 — Deep Web Research (`researcher.py:274–309`)

```
research.start(nb.id, "CloakBrowser", source="web", mode="deep")
    → batchexecute QA9ei (START_DEEP_RESEARCH) → task_id returned

Polling loop (max 24 × 15s = 6 minutes):
    → research.poll() → batchexecute e3bVqc (POLL_RESEARCH)
    → Eventually: status = "completed"
    → sources_found = [] (zero web sources discovered)
```

**Finding 2 — Deep research returned 0 discoverable web sources.** CloakBrowser was viral on 2026-06-01 (the day it blew up). The web has virtually no content about it yet — no blog posts, no tutorials, no discussions indexed. This is expected for a brand-new repo, but the pipeline has no mechanism to distinguish "0 sources = brand new repo with no web presence" from "0 sources = deep research endpoint failure". Both look identical in the output.

Because `sources_found` is falsy, the `import_sources` call is skipped entirely (`researcher.py:293`). `imported_source_ids` stays empty.

---

### Stage 3 — Source Readiness Poll (`researcher.py:301–308`)

```
Loop (max 18 × 10s = 3 minutes):
    sources.list(nb.id) → batchexecute rLM1Ne (GET_NOTEBOOK)
    → Both sources (GitHub page + README) reached READY (SourceStatus = 2)
    → Loop exited before 3 minutes
```

---

### Stage 4 — Source Verification (`researcher.py:310–387`)

```
imported_id_set = set()  ← empty; no web sources imported
primary_ids = [id_for_github_page, id_for_readme]  ← both sources are "primary"
discovered_sources = []  ← empty; no imported sources
```

Because `discovered_sources` is empty, the entire verification block (`researcher.py:319–387`) is skipped. `observation_log` stays at only the header `["## Verification Decisions\n\n"]`. The observation file at `source-verification/observation/2026-06-01_CloakHQ-CloakBrowser_observation.md` is therefore almost empty — it has only the header and the (empty) repo context block.

**Finding 3 — The empty observation file is a direct artifact of 0 web sources.** This is not a failure of the verification logic; the verification logic was never entered. The observation file being empty is actually correct behavior, but it means there's no record of what sources were considered and no guide-based semantic analysis was captured.

---

### Stage 5 — Repo Context Extraction (`researcher.py:393–414`)

```
primary_source_summaries = []
For each source in all_sources (GitHub page + README):
    sources.get_guide(nb.id, src.id) → batchexecute tr032e (GET_SOURCE_GUIDE)
    → summary = guide.get("summary", "")
    → If non-empty: appended to primary_source_summaries
```

The observation file shows `**Intended Audience:** Developers` — the hardcoded fallback value from both the `except Exception` path AND the `inp.get("audience", "Developers")` path in `extract_repo_context`. All other fields (core_use_cases, key_concepts, common_patterns, anti_patterns) are empty.

**Tracing which path hit "Developers":**

`"Developers"` only appears in two places in the codebase:
1. `extract_repo_context` exception handler: `return RepoContext([], [], [], [], "Developers")`
2. `inp.get("audience", "Developers")` — if Claude parsed JSON but returned no audience key

If `primary_source_summaries` was empty, `extract_repo_context` is never called at all, and `repo_context` would have `audience = ""` (empty string, not "Developers"). The observation shows "Developers" → `extract_repo_context` **was** called → at least one guide returned a non-empty summary.

**Finding 4 — `extract_repo_context` was called but returned the exception-path fallback.** The guide for at least one source returned a non-empty summary (so `primary_source_summaries` was populated), `extract_repo_context` called `claude_cli(prompt, timeout=60)`, and that call either:
- Timed out (the context extraction Claude subprocess took >60s), OR
- Returned non-JSON output that `_parse_json_output` failed to parse
- The exception handler at `researcher.py:209` returned `RepoContext([], [], [], [], "Developers")`

The net result: the custom chat prompt configured in Stage 6 contained an empty repo context — no use cases, no concepts, no patterns, no pitfalls anchored to the actual repo.

---

### Stage 6 — Chat Configuration (`researcher.py:434–445`)

```
chat.configure(nb.id, goal=ChatGoal.CUSTOM, custom_prompt=...)
    → batchexecute s0tc2d (RENAME_NOTEBOOK with chat_settings payload)

The custom_prompt was approximately:
    "## Repo Context\n\n**Core Use Cases:**\n\n**Key Concepts:**\n\n..."
    (all sections empty)
    "You are a technical researcher analysing the GitHub project 'CloakHQ/CloakBrowser'..."
```

The chat was configured with a structurally correct but content-empty context. The project name and URL were present, but no extracted knowledge about the repo was anchored in the system prompt. Any NLM response would have been grounded only in its source indexing of the GitHub page + README.

---

### Stage 7 — Seeding Questions (`researcher.py:447–448`, `nlm_seed.py`)

```
seed_questions_from_nlm(notebook_id):
    # Opens a SEPARATE NotebookLMClient instance
    async with await NotebookLMClient.from_storage(timeout=60) as client:
        desc = await client.notebooks.get_description(notebook_id)
            → batchexecute VfAZjd (SUMMARIZE)
            → result[0][0][0] = summary text
            → result[0][1][0] = topics list

    → Returned 1 suggested topic:
        question: "How do C++ source-level patches improve browser stealth?"
        prompt: (full prompt version of same question)
```

**Finding 5 — `nlm_seed.py` opens a redundant second client.** The seed function creates a fresh `NotebookLMClient` context (new `_reqid_counter = 100000`, new httpx client, new auth session) just to make one batchexecute call. The main `client` in `research_one` is already authenticated and active. This is unnecessary overhead and adds a second login-cookie validation round-trip.

The SUMMARIZE call (`VfAZjd`) uses the batchexecute endpoint — no QUERY_URL consumption. The suggested topic is generated by NotebookLM automatically after source indexing. One suggested topic is unusually few; for a repo with a clear technical differentiator (C++ source-level patching), NLM should have generated 3-5 topics. The low count suggests NLM had limited indexed content to generate from — possibly because the raw README URL (added with `wait=False`) was indexed but thin, and the GitHub HTML page had enough to generate only one question.

---

### Stage 8 — Q&A Loop: The Rate Limit (`researcher.py:454–475`, `_chat.py:61–185`)

```
plan = QuestionPlan([(heading, question)], budget=15)
plan.next_question() → ("How do C++ source-level patches improve browser stealth?", q)

client.chat.ask(nb.id, question, source_ids=verified_source_ids)
    → POST https://notebooklm.google.com/_/LabsTailwindUi/data/
        google.internal.labs.tailwind.orchestration.v1.LabsTailwindOrchestrationService/
        GenerateFreeFormStreamed
    → URL params: bl=boq_labs-tailwind-frontend_20260301.03_p0, hl=en, _reqid=200000, rt=c

Response structure received:
    wrb.fr item where item[2] is None (no inner_json)
    item[5] contains UserDisplayableError payload:
        [8, None, [["type.googleapis.com/.../UserDisplayableError", ...]]]

_raise_if_rate_limited(item[5]):
    → "UserDisplayableError" found in entry[0]
    → raises ChatError("Chat request was rate limited or rejected by the API.")
```

**Finding 6 — The rate limit mechanism traced to `_chat.py:591–613`.** The error is not an HTTP 429 (which would be caught by `_core.rpc_call` and raise `RateLimitError`). It's an HTTP 200 response with an error payload embedded in the body. The QUERY_URL returns 200 even for quota-exceeded scenarios; the error signal is `item[2] is None` combined with a `UserDisplayableError` protobuf type URL in `item[5]`. This is a separate quota surface entirely from the batchexecute endpoint.

**Finding 7 — The `_DEFAULT_BL` value may be stale.** `_chat.py:24`:
```python
_DEFAULT_BL = "boq_labs-tailwind-frontend_20260301.03_p0"
```
This build label (March 1, 2026) is sent as the `bl=` URL parameter to QUERY_URL. If Google has rotated this value server-side since March 1, requests with the stale `bl` value could be rejected or rate-bucketed differently than valid sessions. A stale `bl` is one of the documented "RPC method IDs change" pitfalls in `notebooklm-py/CLAUDE.md`. It cannot be confirmed from logs alone, but it's a potential compounding factor. The environment variable override `NOTEBOOKLM_BL` exists but is not set.

**Finding 8 — The ARIS run pre-exhausted the QUERY_URL quota for the session window.** The ARIS research run occurred earlier in the same session. Its `chat.ask` call also rate-limited immediately. By the time the CloakBrowser run started, the QUERY_URL quota was already at 0. The batchexecute calls (all setup, research, source management) do not share this quota surface and ran fine throughout both runs.

Back in `researcher.py` exception handler:
```python
except Exception as e:
    finding_parts.append(f"### {heading}\n\n[failed: {e}]\n")
    raw_qa.append({"heading": heading, "answer": f"[failed: {e}]"})
    plan.record(question)
    # generate_followups is INSIDE the try block, AFTER chat.ask
    # Exception means generate_followups is never reached
```

`plan.record(question)` → `turns_used = 1`, `budget_remaining = 14`. Queue is now empty. `plan.next_question()` returns `None`. Loop exits with 0 successful answers, 1 failed entry.

---

### Stage 9 — Synthesis: The Data Contract Breakage (`researcher.py:480–486`, `synthesize_brief`)

```
synthesize_brief("CloakHQ/CloakBrowser", repo_context, raw_qa, angle_raw)

Inputs:
    context_text: "Use cases: \nKey concepts: \nPatterns: \nPitfalls: \nAudience: Developers"
    qa_text: "**How do C++ source-level patches improve browser stealth?:**\n[failed: Chat request was rate limited...]"
    angle_text: ""

Prompt sent to claude_cli():
    → synthesis prompt with near-empty inputs + project name "CloakHQ/CloakBrowser"
    → subprocess.run(["claude", "-p", prompt], capture_output=True, timeout=120)
```

**Finding 9 — `synthesize_brief` spawns a full Claude Code agent, not an inference call.** `claude -p <prompt>` does not perform a single inference. It launches a full Claude Code CLI session in print mode. The subprocess has access to all Claude Code tools: Read, Write, Edit, Glob, Grep, WebFetch, WebSearch, and potentially Bash. When the synthesis inputs are near-empty (failed Q&A, empty repo context), the subprocess compensates by using its own tools to research the topic.

The subprocess's stdout (the return value of `synthesize_brief`) was:
```
"Frontmatter updated with `description` (150 chars) and `tags`. Brief is ready at 
`10-Research/2026-06-01_CloakBrowser/research.md`. Run `/ideation` when you're ready 
to generate video ideas from it."
```

This is a status message, not a brief. The subprocess:
1. Researched CloakBrowser using its own tools (WebFetch against the GitHub page and README)
2. Created directory `10-Research/2026-06-01_CloakBrowser/`
3. Wrote the full 148-line `research.md` directly to disk
4. Returned this confirmation text as stdout

**Finding 10 — The data contract is broken.** `synthesize_brief` is typed as `-> str` and is expected to return markdown brief content. Instead it returns a file-path confirmation message. The caller in `researcher.py`:
```python
brief_content = f.get("synthesized_brief", "[Synthesis failed]")
```
... embeds this status message into the meta file's body, producing the stub file at `2026-06-01_browser-cloak_cloakbrowser_brief.md`. The actual detailed brief (`research.md`) is in a subfolder that the pipeline never explicitly created and does not reference in its outputs.

**The output split:**

| File | Source | Content |
|---|---|---|
| `10-Research/2026-06-01_browser-cloak_cloakbrowser_brief.md` | `researcher.py` (pipeline output) | Stub — status message as body, correct frontmatter |
| `10-Research/2026-06-01_CloakBrowser/research.md` | Claude subprocess inside `synthesize_brief` | Full 148-line detailed brief, researched from scratch |

The pipeline code never records the subprocess-written file path. There is no link in the meta file pointing to `research.md`. The only connection is the status message text in the meta body mentioning the path.

---

### Stage 10 — Artifact Generation (`researcher.py:489–543`)

Slides and infographic generation was attempted. Both failed (no slide or infographic in the research dir). Failure likely reasons: NLM artifact generation requires a populated notebook with Q&A history; with 0 successful chat turns, the artifact quality signal is absent. Also possible: QUERY_URL rate limit affects artifact generation as well (unconfirmed — artifacts use `batchexecute R7cb6c`, not QUERY_URL, but NLM may internally require some chat state).

---

## Root Cause Summary

### RC-1: QUERY_URL quota pre-exhausted by ARIS run

The `GenerateFreeFormStreamed` endpoint has a per-account hourly/daily quota separate from batchexecute. The ARIS run (same session, minutes earlier) consumed or further depleted this quota. CloakBrowser inherited a zero-balance QUERY_URL quota. First `chat.ask` immediately returned `UserDisplayableError` in the response body at QUERY_URL even though HTTP status was 200.

**Where in code:** `_chat.py:591–613` (`_raise_if_rate_limited`), triggered at `_chat.py:554–555`.

### RC-2: `extract_repo_context` Claude subprocess failure

`claude_cli(prompt, timeout=60)` for repo context extraction returned either non-JSON output or timed out. The `except Exception` handler at `researcher.py:209` silently swallowed the failure and returned `RepoContext([], [], [], [], "Developers")`. No warning surfaces to stdout about this beyond a `logger.warning` that is never visible in the pipeline's print output. The empty repo context fed into the custom chat prompt and into `synthesize_brief` inputs.

**Where in code:** `researcher.py:199–211`, observable consequence at `source-verification/observation/2026-06-01_CloakHQ-CloakBrowser_observation.md` (all context fields empty).

### RC-3: `synthesize_brief` data contract breakage

`claude -p <prompt>` does not return brief text — it returns a file-write confirmation. The pipeline embeds this confirmation as the brief body in the meta file. The actual brief lives in an untracked subfolder. This is the same behaviour seen in the ARIS run and is not a bug introduced by CloakBrowser's failure specifically — it is structural. Every call to `synthesize_brief` likely produces this split-output pattern.

**Where in code:** `researcher.py:126–172`. The `claude_cli` call at line 172 returns subprocess stdout, which is always a status message when the subprocess writes files to disk.

### RC-4: 0 web sources from deep research

CloakBrowser was newly viral on 2026-06-01. The web has no indexed content about it. Deep research completed but found no importable sources. This is correct behavior, but it means:
- No source verification was run
- No observation log was captured beyond the header
- The notebook contains only 2 sources (GitHub page + raw README)
- The chat was configured with an empty context anchoring prompt

**Where in code:** `researcher.py:293–299` (import block never entered). Observable consequence: `source-verification/observation/2026-06-01_CloakHQ-CloakBrowser_observation.md` contains only the section header.

---

## Structural Problems Revealed

### SP-1: Silent exception handling in `extract_repo_context`

`except Exception as e: logger.warning(...)` makes the failure invisible at the run level. The pipeline prints nothing to stdout. The observation file silently records empty context. No operator knows this step failed unless they read the observation file carefully.

**Fix direction:** Print a `[{slug}] WARNING: repo context extraction failed — {e}` to stdout. Treat an empty `repo_context` as a signal to skip custom chat configuration rather than configuring with empty fields.

### SP-2: `synthesize_brief` is not a synthesis function — it's an agent dispatch

The function name and signature imply LLM-based text synthesis over structured inputs. The implementation spawns a full Claude Code CLI instance with write permissions. When inputs are empty, the subprocess does exploratory research and writes files. The function returns the subprocess's terminal output, not a brief.

The two callers of `synthesize_brief` (`researcher.py` and potentially `yt_pipeline.py`) both do `brief_content = f.get("synthesized_brief")` and embed that string directly into the output file. If the subprocess always returns a status message instead of markdown, the meta file body is always wrong.

**Fix direction:** Either (a) enforce that `synthesize_brief` returns only the generated text by stripping any file-operation output from the subprocess response, or (b) have the subprocess write to a known output path and have the pipeline read from that path, making the two-file pattern explicit and controlled.

### SP-3: No retry on QUERY_URL rate limit

`researcher.py:459–474` catches `Exception` broadly and moves on immediately. A 30–60 second wait before the first `chat.ask` call (or a single retry with exponential backoff) would likely recover at least one answer per session when the rate limit is due to a temporary quota window rather than a session-level exhaustion.

**Fix direction:** Before the Q&A loop, add a configurable pre-chat delay (default 0s, env var override). In the exception handler, detect `ChatError` specifically and retry once with a 45s wait before recording as failed.

### SP-4: `nlm_seed.py` opens a redundant client

Every call to `seed_questions_from_nlm` creates and destroys a complete `NotebookLMClient` — new HTTP client, new auth validation, new session. This is one RPC call (`VfAZjd/SUMMARIZE`) that the main `client` in `research_one` can make directly.

**Fix direction:** Pass the existing `client` into `seed_questions_from_nlm` and remove the `async with` wrapper.

### SP-5: Stale `_DEFAULT_BL` in `_chat.py`

`boq_labs-tailwind-frontend_20260301.03_p0` is the build label sent to QUERY_URL. This is 3 months old as of 2026-06-01. Google typically rotates these values. A stale `bl` may contribute to abnormal QUERY_URL behaviour or misrouting. The env var `NOTEBOOKLM_BL` can override this but is not configured.

**Fix direction:** Capture current `bl` from a live session via network inspection and update. Add `bl` rotation to the NLM authentication/session refresh flow.

---

## Open Items

1. Verify whether the artifact generation failure (slides/infographic) is also caused by QUERY_URL rate limiting or is independent.
2. Capture the actual `UserDisplayableError` payload from the next rate-limited run to confirm the quota window length (hourly? per-session?).
3. Update `_DEFAULT_BL` in `_chat.py` — inspect network traffic from a working NotebookLM session.
4. Decide: should `synthesize_brief` be restructured to return text always, or should the two-file pattern (meta stub + actual brief) be made an explicit, tracked pipeline output?
5. The 705.3 stars/day velocity signal means the CloakBrowser content window is narrow — the detailed brief in `research.md` is ready, `/ideation` can proceed immediately without re-running the pipeline.
