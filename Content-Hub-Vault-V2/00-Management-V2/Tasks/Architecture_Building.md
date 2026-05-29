---
status: Active
sprint: "Architecture Building"
created: "2026-04-29"
description: "Task list derived from [[Chase_AI_System_Breakdown]]. This is the canonical plan. Ignore any older task lists in V1 vault."
---

# Current Sprint: Architecture Building

> Source of truth: [[Chase_AI_System_Breakdown]] (`00-Management-V2/Plans/Chase_AI_System_Breakdown.md`).
> All phases and order come from that document. Do not reconcile with V1 task lists.

---

## Status Overview

| # | Phase | Status |
|---|-------|--------|
| 1 | Phase 0b — GitHub Trending Script | ✅ Done |
| 2 | Phase 1 — YT Pipeline Skill | ✅ Done — [[2026-04-29_YT_Pipeline_Skill]] |
| 2 | Callaway Ingestion (via YT Pipeline) | ✅ Done — marketing_brain.md written |
| 3 | Phase 4a — Content Cascade (`/cascade`) | ✅ Done — [[2026-04-29_Phase4a_Cascade_Skill]] |
| 3 | Phase 4b — Short Form (`/short-form`) | ✅ Done — [[2026-04-29_Phase4b_ShortForm_Skill]] |
| 3 | Phase 4c — Voice Cleanup (`/voice-cleanup`) | ✅ Done — [[2026-04-30_Phase4c_VoiceCleanup_Skill]] |
| 4 | Phase 2 — Ideation Skill (`/ideation`) | ✅ Done — [[2026-04-30_Phase2_Ideation_Skill]] |
| 5 | Phase 3a — Hook Skill (`/hook`) | ✅ Done — [[2026-05-06_Phase3a_3b_Hook_Outline_Skills]] |
| 5 | Phase 3b — Outline Skill (`/outline`) | ✅ Done — [[2026-05-06_Phase3a_3b_Hook_Outline_Skills]] |
| 5 | Phase 3c — Title Skill (`/title`) | ✅ Done — [[2026-05-07_Phase3c_Title_Skill]] |
| 6 | OpenMythos Dogfood Run | 🟡 Active — see section below |

**Status legend:** `[ ]` not started · `[~]` in progress · `[x]` complete · `[!]` blocked

---

## Inputs Needed From You

- [x] Callaway YouTube channel link + ~10 specific video URLs → unblocks Callaway Ingestion, `/hook`, `/outline`
  - Channel: https://www.youtube.com/@kallawaymarketing
  - Top 10 by views (fetched 2026-04-29):
    1. 921,838 views — [Social Media Isn't Hard. It's Misunderstood.](https://www.youtube.com/watch?v=h_yQswsXwhY) (2025-04-23)
    2. 659,779 views — [Give me 15 mins, and I'll make your hooks impossible to skip](https://www.youtube.com/watch?v=2byPP_9F0-Q) (2025-07-03)
    3. 440,302 views — [How to Become a Storytelling Genius (Dopamine Ladders)](https://www.youtube.com/watch?v=jtmstMt4WLc) (2025-11-20)
    4. 374,510 views — [Social Media Is About to Change Forever](https://www.youtube.com/watch?v=Vcqgw5zWtDQ) (2025-06-26)
    5. 270,751 views — [How Social Media Algorithms Actually Work (And How to Beat Them)](https://www.youtube.com/watch?v=8cQidXgtGmU) (2026-03-25)
    6. 244,699 views — [You're Not Ready for the Next Phase of Social Media](https://www.youtube.com/watch?v=XxzV82GNolg) (2025-10-09)
    7. 198,456 views — [Game Theory Is The Cheat Code to Social Media](https://www.youtube.com/watch?v=o2nP0lfIsso) (2025-08-21)
    8. 172,419 views — [The ONLY 6 Words You Need to Hook ANY Viewer](https://www.youtube.com/watch?v=S9FlxFv9dxg) (2025-10-01)
    9. 128,207 views — [How to Build a Cult-Like Personal Brand on Social Media](https://www.youtube.com/watch?v=auPtvaoibgk) (2025-08-13)
   10. 105,267 views — [How to Create Irresistible Thumbnails](https://www.youtube.com/watch?v=Iqy644uOOqM) (2025-05-21)
- [x] Your historical title + view count data → unblocked via competitor channel scrape (@nateherk + @Chase-H-AI, 40 titles in `skills/data/competitor_titles.json`)
- [x] Voice profile seed: 10–20 lines on your tone, phrases to avoid → unblocks `/voice-cleanup`
- [ ] Apify API key + Telegram bot token + Grok API key + Twitter API credentials → unblocks Phase 0a

---

## Phase 0b — GitHub Trending Script ✅ DONE

Fountainhead #2. Daily script → top 10 trending AI repos + Claude's pick → written to Obsidian vault.

- [x] Script written: `github_trending.py`
- [x] Pulls top 10 trending repos (last 7 days) + top 5 for month
- [x] Claude's daily pick with reasoning
- [x] Output written to `Content-Hub-Vault/04-Trends/`
- [x] Scheduling: set up via Windows Task Scheduler or run manually each morning

Session log: [[2026-04-29_GitHub_Trending_Script]]

---

## Phase 1 — YT Pipeline Skill (Priority 2 — build next)

Core research primitive. One slash command: topic → NotebookLM analysis → Obsidian vault.

### Setup: `notebooklm-py`
- [x] Clone `notebooklm-py` repo (CLI wrapper for NotebookLM API)
- [x] Install and confirm `notebooklm-py` works: pass a YouTube URL, get analysis back

### Skill: `/yt-pipeline`
- [x] `prompts/yt_pipeline.md` — sourcing + analysis prompt
- [x] `skills/yt_pipeline.py` — calls `notebooklm-py` as subprocess, writes to vault
- [x] `.claude/skills/yt-pipeline/SKILL.md` — slash command entry
- [x] Smoke test: search mode confirmed working (yt-dlp → numbered results)

---

## Callaway Ingestion — One-Time Setup (Priority 2, runs after YT Pipeline)

Feeds Callaway's craft into Obsidian so `/hook`, `/outline`, `/title` can reference it.

- [x] URLs provided — top 10 by view count, fetched 2026-04-29 (see Inputs section above)
- [x] Run `/yt-pipeline` on ~10 Callaway URLs
- [x] NotebookLM extracts: hook patterns, pacing rules, title formulas, outline logic, voice markers
- [x] Output lands in vault as `Content-Hub-Vault/01-Knowledge/callaway_hooks.md`, `callaway_titles.md`, etc.
- [x] Manual review pass (you edit the extraction)

---

## Phase 4a — Content Cascade `/cascade` (Priority 3) ✅ DONE

YouTube video → blog post + Twitter thread + LinkedIn. One command, three platforms.

- [x] `prompts/cascade.md` — voice-tuned, 3 sections (blog / Twitter / LinkedIn), banned phrases embedded
- [x] `skills/cascade.py` — YouTube URL → yt_dlp transcript → AI router → 3 platform outputs
- [x] `.claude/skills/cascade/SKILL.md` — slash command entry
- [x] Smoke test: Kallaway top video → 4 files in `Content-Hub-Vault-V2/08-Distribution/2026-04-29_social-media-isnt-hard-its-misunderstood/`

Session log: [[2026-04-29_Phase4a_Cascade_Skill]]

---

## Phase 4b — Short Form `/short-form` (Priority 3) ✅ DONE

Long-form transcript → 3 vertical scripts (30 / 60 / 90 sec). Re-scripted for format, not clipped.

- [x] `prompts/short_form.md`
- [x] `skills/short_form.py` — reads transcript/outline from vault
- [x] `.claude/skills/short-form/SKILL.md`
- [x] Smoke test: 3 scripts at 30/60/90s in `Content-Hub-Vault-V2/09-Shorts/`

Session log: [[2026-04-29_Phase4b_ShortForm_Skill]]

---

## Phase 4c — Voice Cleanup `/voice-cleanup` (Priority 3) ✅ DONE

De-AI'ify any skill output. Run after any other skill.

- [x] `prompts/voice_cleanup.md` — consolidated banned patterns + positive voice markers
- [x] `skills/voice_cleanup.py` — file or stdin mode, Claude-first, saves `_cleaned.md`
- [x] `.claude/skills/voice-cleanup/SKILL.md` — covers file/stdin/post-cascade workflows
- [x] Smoke test: paste AI text in → clean human-sounding version out, no "Let's dive in" or "it's not X it's Y"

Session log: [[2026-04-30_Phase4c_VoiceCleanup_Skill]]

---

## Phase 2 — Ideation Skill `/ideation` (Priority 4)

Reads Obsidian research → returns ~9 ranked video ideas with competitive reasoning.

- [x] `prompts/ideation.md` — gap analysis, performance outliers, audience desire map
- [x] `skills/ideation.py` — reads vault research notes for the topic
- [x] `.claude/skills/ideation/SKILL.md`
- [x] `Content-Hub-Vault-V2/02-Ideas/` — vault output directory created
- [x] Live smoke test: invoke after a YT Pipeline run → 9 ranked ideas written to vault

Session log: [[2026-04-30_Phase2_Ideation_Skill]]

---

## Phase 3a — Hook Skill `/hook` (Priority 5) ✅ DONE

Drafts the first ~30 seconds. 5 variations, each with spoken hook + visual hook + text overlay.

- [x] `prompts/hook.md` — all 10 Kallaway patterns + Dopamine Ladder opening stages + 5-variation format
- [x] `skills/hook.py` — reads marketing_brain from V2 vault, draft() → polish() cascade, writes to `05-Hooks/`
- [x] `.claude/skills/hook/SKILL.md`
- [x] Smoke test: 5 hook variations (spoken + visual + overlay) written to `Content-Hub-Vault-V2/05-Hooks/`

Session log: [[2026-05-06_Phase3a_3b_Hook_Outline_Skills]]

---

## Phase 3b — Outline Skill `/outline` (Priority 5) ✅ DONE

Structural skeleton: sections, talking points, visual aids, source references, related vault docs.

- [x] `prompts/outline.md` — Dopamine Ladder 6-stage backbone + pacing rules + visual markers
- [x] `skills/outline.py` — reads marketing_brain from V2 vault, --hook-path input, draft() → polish()
- [x] `.claude/skills/outline/SKILL.md`
- [x] Smoke test: outline with per-section durations + B-roll cues in `Content-Hub-Vault-V2/06-Outlines/`

Session log: [[2026-05-06_Phase3a_3b_Hook_Outline_Skills]]

---

## Phase 3c — Title Skill `/title` (Priority 5) ✅ DONE

5 Tier-1 titles (safe, proven patterns) + 5 Tier-2 titles (calculated risks, A/B flag) + thumbnail text. Competitor data used in place of personal history.

- [x] `scripts/scrape_competitor_titles.py` — scrapes @nateherk + @Chase-H-AI via Apify; writes 40 titles to `skills/data/competitor_titles.json`
- [x] `prompts/title.md` — tier system prompt with `{competitor_titles}` + `{concept}` placeholders
- [x] `skills/title.py` — reads JSON top-30, calls `claude -p -` via subprocess, writes to vault
- [x] `.claude/skills/title/SKILL.md`
- [x] Smoke test: `/title "how I built a RAG pipeline that actually works"` → 10 titles with competitor pattern citations in `Content-Hub-Vault-V2/07-Titles/`

Session log: [[2026-05-07_Phase3c_Title_Skill]]

---

## OpenMythos Dogfood Run — Active

End-to-end validation of the V2 production engine on a real topic: [kyegomez/OpenMythos](https://github.com/kyegomez/OpenMythos) (11,100 stars, "theoretical reconstruction of the Claude Mythos architecture" — surfaced via [[github_trending]]).

Goal: push one real topic through every skill, capture every gap into a friction log, then brainstorm fixes together. No new code or prompt edits during the run — only observation.

Friction log: [[2026-05-07_OpenMythos_Dogfood_Run]]

- [x] Step 1 — `/yt-pipeline kyegomez/OpenMythos`: ingested 3 videos; research brief written → [[2026-05-07_OpenMythos_Dogfood_Run]]
- [x] Step 2 — `/ideation`: Rank 6 chosen — "What Anthropic Actually Published vs. What OpenMythos Claims to Reconstruct"
- [x] Step 3 — `/hook "<idea>"`: Hook 1 (Speed to Value) approved → [[2026-05-07_what-anthropic-actually-published-vs-what]] (05-Hooks)
- [x] Step 4 — `/outline --hook-path <hook>`: 12-min Dopamine Ladder approved → [[2026-05-07_what-anthropic-actually-published-vs-what]] (06-Outlines)
- [x] Step 5 — `/title "<idea>"`: Title 9 chosen — "Is OpenMythos Legit? I Checked Every Claim Against Anthropic's Docs" → [[2026-05-07_what-anthropic-actually-published-vs-what-openmyth]] (07-Titles)
- [x] Step 6 — `/cascade`: redesigned to research+outline mode; 3 distribution files written → [[2026-05-07_is-openmythos-legit-i-checked-every-clai]] (08-Distribution)
- [x] Step 7 — `/short-form`: redesigned to research+outline mode; 3 scripts written → [[2026-05-08_is-openmythos-legit-i-checked-every-clai]] (09-Shorts)
- [x] Step 8 — `/voice-cleanup`: 8 `_cleaned.md` files written (hooks, outline, blog, twitter, linkedin, 30s, 60s, 90s)
- [x] Brainstorm: review friction log, produce the next plan → [[2026-05-08_YT_Pipeline_Friction_Repair]]

## Archived Phases

### Phase 0a — Twitter Scraping Web App ⏸ Parked permanently (for now)

Data layer was built; Apify actor never resolved. No active work. Code stays in place (`backend/research/apify_client.py` Twitter section, `skills/twitter_scout.py`, `skills/twitter_scorer.py`, `skills/data/twitter_config.json`, Supabase `tweets` + `tweet_actions` tables) — cheap to leave, expensive to rebuild if it ever returns.

Historical record: [[2026-05-07_Phase0a_Twitter_Data_Layer]] | [[2026-05-07_Phase0a_Twitter_Scout]]

---

## Human Checkpoints (The Collaborator Model)

These are the gates you own — AI does not advance past these automatically:

- [x] After Phase 0b: pick a topic from the daily trending feed
- [x] After YT Pipeline: read the research, decide what angle to explore
- [x] After Ideation: pick one idea from the ranked list, modify as needed
- [x] After Hook: approve or iterate before moving to outline
- [x] After Outline + Title: confirm both before filming
- [x] After Content Cascade: approve Twitter thread before it posts
- [x] After Short Form: review scripts before recording

---

## Ad-hoc Research (outside sprint)

- [x] 2026-05-06 — Ruflo / Claude Code primitives research → [[2026-05-06_Ruflo_Research_Handoff]]. Artifacts in `00-Management-V2/Memory/Research/2026-05-06_ruflo/`.

---

## Cross-References

Implements: [[Chase_AI_System_Breakdown]]
References: [[context]] | [[Local_First_Skill_Engine_Plan]] | [[2026-04-29_GitHub_Trending_Script]] | [[2026-05-06_Ruflo_Research_Handoff]]
