---
status: Active
created: "2026-04-28"
description: "Canonical build plan for V2 — local-first skill engine modeled on Chase AI workflow."
type: implementation_plan
---

# Local-First Skill Engine — Build Plan for Content Hub V2

References: [[2026-04-28_V2_Pivot_Local_First_Engine]] | [[context]] | [[Architecture_Building]]

## Context

V2 lives at `C:\Users\madhu\Claude cowork\Content Hub V2\`. It's a fork of V1, intended as a fully local-first content production engine. V1 stays untouched as the SaaS-path reservation — resumed only when a paying customer demands it.

**The pain solved:** V1 became cluttered (12 frontend routes, 9 backend modules, broken renderers, 0 deliverables). The `_run_generation` pipeline tried to automate the part Chase AI's playbook explicitly says NOT to automate (rendering finished video). Everything between trending discovery and the human's CapCut workflow is missing — that's where 90 outputs/month live.

**The intended outcome:** within 1–2 weeks of focused work, run a sequence of slash-commands that produces — for any chosen trending topic — a research brief, three hook variants, an outline, ten title candidates (5 safe + 5 risky), three short-form scripts, a blog post, a Twitter thread, and three LinkedIn variations. ~9 deliverables per long-form. Daily 1× = ~270 pieces/month theoretical max; practical target ~30 long-form/month → ~270 pieces/month total.

---

## Architecture

**Two-layer skill pattern, repeated 7 times:**

```
.claude/skills/<name>/SKILL.md       ← Claude Code entry point. /<name> trigger.
                                       Tells Claude what inputs to gather + which Python helper to call.
skills/<name>.py                     ← The actual work. Loads prompt, calls model(s), writes to vault.
prompts/<name>.md                    ← Single source of truth for the prompt text.
```

**Why not pure Python or pure SKILL.md:**
- Pure Python loses Claude Code's natural-language argument parsing and vault integration.
- Pure SKILL.md can't easily orchestrate multi-step model calls (Ollama outline → Claude polish), and can't be cron'd later.
- The split is what lets the engine be a SaaS port-target later: when SaaS resumes (in V1), `POST /api/v1/skills/{name}` loads `prompts/{name}.md` and runs the same logic. Prompts are the durable artifact.

**Model routing per skill (cost-aware):**
- **Ollama (local, free)** for first-draft outlines, structural work, anything where mediocre-but-coherent is fine.
- **Claude (paid, premium)** for hooks, titles, voice cleanup, final-30-second polish — the parts that determine engagement.
- **Gemini** — kept available for any tool that already wires it (research_service.py uses it).

**Knowledge layer:**
- `notebooklm-py` (already cloned at V2/`notebooklm-py/`) for the one-shot Callaway masterclass extraction and ad-hoc deep-research notebooks.
- `Content-Hub-Vault/` (this vault, shared with V1) — human-facing workspace and skill output target.
- pgvector RAG (`backend/research/rag.py`) **kept available** but deprioritized for v1 — the vault + Callaway masterclass cover most needs locally.

---

## Repo Shape — What to Strip, What to Keep

### Strip (delete from V2 — they reserve V1 for SaaS)

| Path                                                                                  | Reason                                                        |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `frontend/`                                                                           | Next.js UI is SaaS-only. Local engine is Claude Code + vault. |
| `remotion-service/`                                                                   | Chase's "don't automate" zone. We stop at the script.         |
| `backend/content/renderer_video.py`, `renderer_slides.py`, `renderer_talking_head.py` | Same. These are the broken layer.                             |
| `backend/content/storyboard.py`                                                       | Coupled to the dropped renderers.                             |
| `backend/experiments/` (router + models)                                              | A/B framework is a SaaS feature.                              |
| `supabase/` migrations                                                                | Not running Supabase locally.                                 |
| `frontend/__tests__/`                                                                 | Gone with frontend.                                           |
| `tmp/video-bug-report.md`, `tmp/video-notes.md`                                       | Bug report belongs to V1's pipeline.                          |

### Keep (core dependencies for the local engine)

| Path | Why kept | Used by |
|---|---|---|
| `backend/research/apify_client.py` | Trending discovery | `/researcher` skill |
| `backend/research/research_service.py` | Research brief assembly (Gemini-powered) | `/researcher` skill |
| `backend/research/rag.py` | pgvector embeddings (optional but kept) | `/researcher` (advanced mode) |
| `backend/intelligence/synthesis.py` | Strategy generation reference | `/synthesize` (future skill) |
| `backend/intelligence/memory.py` | Voice-profile learning loop | `/voice-cleanup` reads voice profile |
| `backend/prompts/skills/` (15 files) | Existing marketing prompts — direct reuse | Multiple skills |
| `Content-Hub-Vault/` | Knowledge graph + workspace + skill output target | All skills |
| `Content-Hub-Vault/00-Management/Superpowers/` | Workflow orchestration skills | `/orchestrate` etc. |
| `notebooklm-py/` | Programmatic NotebookLM access | Callaway extraction + deep research |
| `extract_video_knowledge.py` | Working template for the Callaway extractor | Becomes basis of `extract_callaway_masterclass.py` |
| `.claude/skills/` (existing 6) | Workflow infrastructure | Orchestration of skill pipeline |
| `requirements.txt`, `.env`, `pytest.ini` | Python toolchain config | Project-wide |
| `backend/storage/`, `backend/auth/`, `backend/workflows/`, `backend/brand/` | Reusable abstractions | Some skills reference brand config |

### Build New (the actual work of v1)

| Path | Purpose |
|---|---|
| `prompts/` (NEW root-level dir) | Single source of truth for skill prompts |
| `prompts/researcher.md` | Trending → content-gap analysis prompt |
| `prompts/hook.md` | Hook generation (3 variants, modeled on Callaway) |
| `prompts/outline.md` | Structural plan (sections, durations, B-roll cues) |
| `prompts/title.md` | 5 Tier-1 + 5 Tier-2 titles |
| `prompts/cascade.md` | Long-form transcript → blog + thread + LinkedIn |
| `prompts/short_form.md` | Long-form → 3× vertical scripts (30/60/90s) |
| `prompts/voice_cleanup.md` | De-AI'ify; lifts from existing `backend/prompts/skills/copy-editing.md` |
| `skills/__init__.py` | Python package |
| `skills/runner.py` | Shared async runner: load prompt, format inputs, call Ollama/Claude/Gemini, write to vault, log to graph |
| `skills/researcher.py` ... `skills/voice_cleanup.py` | One file per skill — calls `runner.py` |
| `.claude/skills/researcher/SKILL.md` ... `.claude/skills/voice-cleanup/SKILL.md` | Claude Code entry points (7 dirs) |
| `extract_callaway_masterclass.py` | Forked from `extract_video_knowledge.py`. Takes 10 Callaway YouTube URLs → writes `Content-Hub-Vault/01-Knowledge/callaway_masterclass.md` |
| `Content-Hub-Vault/01-Knowledge/callaway_masterclass.md` | Output of Step 1. The "brain" injected into hook + outline prompts. |
| `Content-Hub-Vault/05-Hooks/`, `06-Outlines/`, `07-Titles/`, `08-Distribution/`, `09-Shorts/`, `10-Research/` | New vault folders for skill outputs |

---

## The 7 Skills

### 1. `/researcher` — source enrichment + content-gap analysis
- **Inputs:** `niche` (e.g. "AI agents"), optional `lookback_days`.
- **Pipeline:**
  1. **Read trends** — loads `Content-Hub-Vault/04-Trends/trends.md`. Extracts URLs (GitHub repos, topic links) scraped by the APScheduler job.
  2. **Add sources to NotebookLM** — uses `notebooklm-py` (`add_url`) to add each trend URL as a notebook source. GitHub URLs and web pages are indexed directly; YouTube URLs are auto-detected.
  3. **Web research** — calls `research.start` (fast or deep mode) to discover related credible content: YouTube videos covering the repo/topic, blog posts, articles. Discovered sources are auto-imported into the notebook.
  4. **Content-gap query** — calls `chat.ask` with a structured prompt: "Given these sources, what angles are underserved? What would make a video stand out?" Returns top-5 video ideas with rationale.
  5. **Export** — generates a study guide or report artifact, exports as markdown. Writes to vault.
- **Output:** `Content-Hub-Vault/10-Research/YYYY-MM-DD_<niche>_brief.md` — contains: source list, discovered coverage, 5 video ideas with angle rationale.
- **Auth dependency:** Google OAuth via Playwright (`~/.notebooklm/storage_state.json`). One-time `notebooklm login` required.

### 2. `/hook` — hook generation (Callaway-injected)
- **Inputs:** `topic` (from `/researcher` output), `audience`, `platform` (yt-long | yt-shorts | tiktok | reels).
- **Logic:** Loads `Content-Hub-Vault/01-Knowledge/callaway_masterclass.md` as context. First draft via Ollama. Final polish via Claude.
- **Output:** `Content-Hub-Vault/05-Hooks/YYYY-MM-DD_<slug>.md` — 3 hooks each with `spoken_line`, `visual_cue`, `text_overlay`.

### 3. `/outline` — structural plan
- **Inputs:** `topic`, `target_length_min`, `hook_path`.
- **Logic:** Ollama drafts; Claude polishes. Reuses `backend/prompts/skills/content-strategy.md`.
- **Output:** `Content-Hub-Vault/06-Outlines/YYYY-MM-DD_<slug>.md`.

### 4. `/title` — Tier-1 / Tier-2 titles
- **Inputs:** `topic`, `outline_path`.
- **Logic:** Pure Claude. 5 safe + 5 risky.
- **Output:** `Content-Hub-Vault/07-Titles/YYYY-MM-DD_<slug>.md`.

### 5. `/cascade` — long-form → blog + thread + LinkedIn
- **Inputs:** `transcript_path` OR `video_url` (auto-fetches transcript).
- **Logic:** Ollama drafts each output; Claude polishes hook lines. Three Claude calls (one per platform).
- **Output:** Three files in `Content-Hub-Vault/08-Distribution/YYYY-MM-DD_<slug>/`:
  - `blog.md` — 800–1500 word SEO post
  - `thread.md` — 7-tweet thread
  - `linkedin.md` — 3 LinkedIn variations
- **Highest ROI skill in v1.** Build first along with /short-form.

### 6. `/short-form` — long-form → vertical scripts
- **Inputs:** `transcript_path`, optional `target_durations` (default `[30, 60, 90]`).
- **Logic:** Identifies clip-worthy moments (Claude). Generates one script per duration with hook + B-roll cues + clip timestamp range.
- **Output:** `Content-Hub-Vault/09-Shorts/YYYY-MM-DD_<slug>_<duration>s.md`.

### 7. `/voice-cleanup` — de-AI'ify
- **Inputs:** `text_path`, `voice_profile_path` (defaults to `Content-Hub-Vault/01-Knowledge/voice_profile.md`).
- **Logic:** Single Claude call. Rewrites in user voice. Strips ChatGPT-isms.
- **Output:** Overwrites input file (with `.original.md` backup) OR writes `<input>.cleaned.md`.

---

## Step 1 — The Callaway Masterclass (do this BEFORE any skill)

The hook + outline skills are only as good as the Callaway extraction. One-time, high-leverage.

1. User provides 10 Callaway YouTube URLs.
2. Fork `extract_video_knowledge.py` → `extract_callaway_masterclass.py`. Replace `DRIVE_URL`/`DRIVE_FILE_ID` with logic that adds 10 YouTube sources to one notebook.
3. Replace bug-triage `QUESTIONS` with masterclass extraction questions:
   - `Hook_Patterns` — categorize opening line patterns (question, contrarian, story, statistic) with timestamps.
   - `Pacing_Rules` — average pacing, scene-change cadence, talking-head vs B-roll ratio.
   - `Psychological_Formulas` — persuasion patterns (curiosity gap, authority anchoring, contrarian-then-resolve).
   - `Title_Patterns` — title structures as templates with CTR signals.
   - `Voice_Markers` — distinctive verbal tics, transitions, sign-offs.
   - `Visual_Style` — color grading, fonts, B-roll selection, on-screen text.
4. Run script. Output → `Content-Hub-Vault/01-Knowledge/callaway_masterclass.md`.
5. **Manual review pass.** User reads the output, edits aggressively, adds corrections.

---

## End-to-End Workflow (one long-form, ~3 hr filming)

| Step | Command | Time | Output |
|---|---|---|---|
| 0 | (one-time) `python extract_callaway_masterclass.py` | 10 min | masterclass.md |
| 1 | `/researcher niche="AI agents"` | 60 s | 5 video ideas → vault/10-Research/ |
| 2 | `/hook topic="<chosen>"` | 30 s | 3 hooks → vault/05-Hooks/ |
| 3 | `/outline topic="<chosen>" hook_path="<...>"` | 45 s | Structural plan → vault/06-Outlines/ |
| 4 | `/title topic="<chosen>" outline_path="<...>"` | 20 s | 10 titles → vault/07-Titles/ |
| 5 | **User films + edits in CapCut** | ~3 hr | Long-form MP4 + transcript |
| 6 | `/cascade transcript_path="<...>"` | 60 s | blog + thread + linkedin → vault/08-Distribution/ |
| 7 | `/short-form transcript_path="<...>"` | 45 s | 3 vertical scripts → vault/09-Shorts/ |
| 8 | `/voice-cleanup text_path="<...>"` (×9 if all polished) | ~3 min | Cleaned files |
| | **Total skill compute:** ~7 min. **Total deliverables:** **9 per long-form.** | | |

---

## Implementation Order

1. **`skills/runner.py`** — shared infrastructure. ~1 day.
2. **`extract_callaway_masterclass.py`** — runs once, unblocks hook/outline. ~2 hr after URLs provided.
3. **`/cascade`** — biggest output multiplier. ~1 day.
4. **`/short-form`** — same multiplier logic. ~0.5 day.
5. **`/voice-cleanup`** — needed to polish #3 and #4. ~0.5 day.
6. **`/researcher`** — needed for new topic discovery. ~0.5 day.
7. **`/hook`** — needs Callaway masterclass. ~0.5 day.
8. **`/outline`** — depends on /hook. ~0.5 day.
9. **`/title`** — last; pure Claude prompt. ~0.5 day.

**Total: ~6 working days.**

---

## Verification

### Per-skill smoke test
- `/researcher niche="AI agents"` → file appears in `vault/10-Research/`, contains 5 ideas with rationale.
- `/hook topic="LLM evals"` → file appears in `vault/05-Hooks/`, contains 3 hooks.
- (etc., one per skill)

### End-to-end test
1. Pick one trending topic from `vault/04-Trends/trends.md`.
2. Run skills 1–4 in order. Confirm 4 vault files created.
3. (Skip filming for the test) Use a transcript from any existing YouTube video as the input to `/cascade` and `/short-form`.
4. Run `/voice-cleanup` on `cascade/blog.md`.
5. Confirm: 9 deliverable files, all in correct vault folders, all readable, none containing literal "Let's dive in".

### Acceptance bar
- All 7 slash-commands work from Claude Code.
- All 7 Python helpers run standalone via `python -m skills.<name> --topic "X"`.
- Total skill compute time end-to-end (excluding filming) < 10 min.
- Callaway masterclass file is 5K+ words and reviewed by user.

---

## Open Inputs (user provides at execution time)

1. Callaway channel link + 10 specific video URLs
2. Voice profile seed (`vault/01-Knowledge/voice_profile.md`)
3. Ollama model preference (default `llama3.2` or `mistral`)
4. ComfyUI deferred to v2 of V2

## Out of Scope for v1

- ComfyUI image generation (deferred)
- A/B experiments framework (kept available, not wired)
- Frontend / Next.js (lives in V1 for SaaS resume)
- Remotion / Playwright rendering (dropped permanently)
- Auto-publishing to YouTube/Twitter/LinkedIn
- pgvector RAG-driven research (kept available; v1 uses NotebookLM + vault)
- Custom dashboard / GUI (Claude Code IS the UI)

---
[[Architecture_Building]] | [[context]] | [[CLAUDE]] | [[2026-04-28_V2_Pivot_Local_First_Engine]]
