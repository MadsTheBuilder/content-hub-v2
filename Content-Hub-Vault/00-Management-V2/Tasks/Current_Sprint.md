---
status: Active
sprint: "V2 Phase 0 — Cleanup + Foundation"
created: "2026-04-28"
description: "Live task list for Content Hub V2 — local-first skill engine."
---

# Current Sprint: Content Hub V2 — Build Local-First Engine

> Started 2026-04-28 after V2 fork decision. See [[2026-04-28_V2_Pivot_Local_First_Engine]] for context. Full build spec: [[Local_First_Skill_Engine_Plan]].

## Current Status

- **Phase 0 (Cleanup):** ✅ Complete
- **Phase 1 (Infrastructure):** 🟡 Not started
- **Phase 2 (Callaway Masterclass):** 🟡 Blocked on user-provided URLs
- **Phase 3 (Distribution Multipliers):** 🟡 Queued
- **Phase 4 (New-Piece Creation):** 🟡 Queued
- **Phase 5 (Verification):** 🟡 Queued

**Status legend:** `[ ]` not started · `[~]` in progress · `[x]` complete · `[!]` blocked

---

## Open Inputs Required (from user)

- [ ] Callaway YouTube channel link + 10 specific video URLs (blocks Phase 2 + `/hook` + `/outline`)
- [ ] Voice profile seed — first version of `Content-Hub-Vault/01-Knowledge/voice_profile.md` (10–20 lines on tone/voice/banned phrases)
- [ ] Ollama model preference (default `llama3.2` or `mistral` — confirm what's pulled locally)
- [ ] ComfyUI — confirmed deferred to v2 of V2

---

## Phase 0 — Cleanup (~1 afternoon)

Strip SaaS layers from V2 only. V1 is never touched.

- [x] Verify V2 git state — confirm clean working tree before destructive ops
- [x] `git rm -rf frontend/ remotion-service/ supabase/` *(skipped — files already absent)*
- [x] `git rm backend/content/renderer_video.py backend/content/renderer_slides.py backend/content/renderer_talking_head.py backend/content/storyboard.py`
- [x] `git rm -rf backend/experiments/` (or `mv` to `archive/` for prompt patterns) *(skipped — directory already absent)*
- [x] `mv tmp/ archive/` (preserve bug report for reference)
- [x] Update V2 `CLAUDE.md` — replace SaaS/B2B language with local-first creator-engine framing
- [x] Create new folders: `prompts/`, `skills/`, `Content-Hub-Vault/01-Knowledge/`, `05-Hooks/`, `06-Outlines/`, `07-Titles/`, `08-Distribution/`, `09-Shorts/`, `10-Research/`
- [x] Initial cleanup commit: "Strip SaaS layers; restructure as local-first skill engine"

## Phase 1 — Infrastructure (~1 day)

- [ ] Build `skills/__init__.py` (Python package)
- [ ] Build `skills/runner.py` — shared async runner
  - [ ] Async Ollama client
  - [ ] Async Claude client (Anthropic SDK)
  - [ ] Prompt loader (reads `prompts/<name>.md`)
  - [ ] Vault writer (writes to `Content-Hub-Vault/<folder>/`)
  - [ ] Logger that emits Obsidian-compatible session-log entries

## Phase 2 — Callaway Masterclass (one-time, ~2 hr after URLs)

- [!] **BLOCKED** on user-provided Callaway URLs
- [ ] Fork `extract_video_knowledge.py` → `extract_callaway_masterclass.py`
- [ ] Replace `DRIVE_URL`/`DRIVE_FILE_ID` with multi-YouTube source loader
- [ ] Replace bug-triage `QUESTIONS` with masterclass extraction questions:
  - [ ] `Hook_Patterns`
  - [ ] `Pacing_Rules`
  - [ ] `Psychological_Formulas`
  - [ ] `Title_Patterns`
  - [ ] `Voice_Markers`
  - [ ] `Visual_Style`
- [ ] Run script → `Content-Hub-Vault/01-Knowledge/callaway_masterclass.md`
- [ ] Manual review pass (user edits the AI extraction)

## Phase 3 — Distribution Multipliers (~2 days, highest ROI — build first)

### `/cascade` (long-form transcript → blog + thread + LinkedIn)
- [ ] `prompts/cascade.md`
- [ ] `skills/cascade.py`
- [ ] `.claude/skills/cascade/SKILL.md`
- [ ] Smoke test: pick any existing transcript → 3 deliverable files in `vault/08-Distribution/`

### `/short-form` (long-form → 3× vertical scripts)
- [ ] `prompts/short_form.md`
- [ ] `skills/short_form.py`
- [ ] `.claude/skills/short-form/SKILL.md`
- [ ] Smoke test: 3 scripts at 30/60/90s in `vault/09-Shorts/`

### `/voice-cleanup` (de-AI'ify; lifts from `backend/prompts/skills/copy-editing.md`)
- [ ] `prompts/voice_cleanup.md` (extract relevant sections from `copy-editing.md`)
- [ ] `skills/voice_cleanup.py`
- [ ] `.claude/skills/voice-cleanup/SKILL.md`
- [ ] Smoke test: cleaned file exists, no "Let's dive in"

## Phase 4 — New-Piece Creation (~2 days)

### `/researcher` (trending → 5 video ideas)
- [ ] `prompts/researcher.md`
- [ ] `skills/researcher.py` — reads `vault/04-Trends/trends.md`
- [ ] `.claude/skills/researcher/SKILL.md`
- [ ] Smoke test: 5 ideas with rationale in `vault/10-Research/`

### `/hook` (Callaway-injected hook generation) — depends on Phase 2
- [ ] `prompts/hook.md`
- [ ] `skills/hook.py` — Ollama draft → Claude polish
- [ ] `.claude/skills/hook/SKILL.md`
- [ ] Smoke test: 3 hooks in `vault/05-Hooks/`

### `/outline` (structural plan)
- [ ] `prompts/outline.md` (base from `backend/prompts/skills/content-strategy.md`)
- [ ] `skills/outline.py`
- [ ] `.claude/skills/outline/SKILL.md`
- [ ] Smoke test: outline with sections + durations + B-roll cues in `vault/06-Outlines/`

### `/title` (5 Tier-1 + 5 Tier-2)
- [ ] `prompts/title.md`
- [ ] `skills/title.py` — pure Claude
- [ ] `.claude/skills/title/SKILL.md`
- [ ] Smoke test: 10 titles in `vault/07-Titles/`

## Phase 5 — Verification (~0.5 day)

- [ ] All 7 slash-commands work from Claude Code
- [ ] All 7 Python helpers run standalone via `python -m skills.<name>`
- [ ] End-to-end run: pick trending topic → skills 1–4 → use existing transcript for 5–7 → 9 deliverable files
- [ ] Total skill compute time < 10 min
- [ ] Callaway masterclass is 5K+ words and reviewed
- [ ] Acceptance commit + V2 README updated

---

## Build Order Summary (~6 working days)

| Day | Phase | Output |
|---|---|---|
| 0.5 | Phase 0 | V2 stripped, folders created |
| 1 | Phase 1 | `skills/runner.py` working |
| 0.25 | Phase 2 (after URLs) | Masterclass extracted + reviewed |
| 1 | Phase 3 (`/cascade`) | First 3 deliverables shipping |
| 0.5 | Phase 3 (`/short-form`) | +3 deliverables |
| 0.5 | Phase 3 (`/voice-cleanup`) | Polished outputs |
| 0.5 | Phase 4 (`/researcher`) | New-topic discovery online |
| 0.5 | Phase 4 (`/hook`) | Hook engine online |
| 0.5 | Phase 4 (`/outline`) | Outline engine online |
| 0.5 | Phase 4 (`/title`) | Full creation pipeline |
| 0.5 | Phase 5 | Verification + sign-off |

---

## Cross-References

Implements: [[Local_First_Skill_Engine_Plan]]
References: [[2026-04-28_V2_Pivot_Local_First_Engine]] | [[context]] | [[CLAUDE]]
V1 (parked) sprint: `00-Management/Tasks/Current_Sprint.md`

---
[[context]] | [[Local_First_Skill_Engine_Plan]] | [[README]]
