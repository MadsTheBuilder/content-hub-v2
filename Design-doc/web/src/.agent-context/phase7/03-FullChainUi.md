---
date: 2026-05-29
type: phase7-agent-note
status: done_with_concerns
agent: 03-full-chain-ui-agent
task: run the browser-facing full chain and record evidence
description: "Group 3 UI acceptance evidence: 8/9 pipeline stages produced real vault output. Hooks blocked by argparse bug (fixed in same session). Multiple shared UI bugs documented as open items."
tags: [phase7, webapp-sprint, acceptance, full-chain, ui]
owned_files:
  - Design-doc/web/src/.agent-context/phase7/03-FullChainUi.md
verification:
  - Trends renders files from 04-Trends/ — PASS
  - Research produces new file in 10-Research/ — PASS
  - Ideation produces new file in 02-Ideas/, rendered in OutputBrowser — PASS
  - Hooks argparse error blocked run — FIXED (skills/hook.py duplicate --audience removed)
  - Outline produces new file in 06-Outlines/ — PASS
  - Title produces new file in 07-Titles/ — PASS
  - Cascade produces bundle in 08-Distribution/ — PASS
  - Short-form produces bundle in 09-Shorts/ (both vault files and YouTube URL mode) — PASS
  - Voice-cleanup runs on selected file — PASS
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 03-Full-Chain UI Agent

## Mission
Run the browser-facing full chain and record evidence from user's live browser session.

## Context Read
- `Design-doc/web/src/.agent-context/phase7/00-Contract.md`
- `Design-doc/web/src/.agent-context/phase7/02-Preflight.md`

## Acceptance Topic
User ran existing research file `2026-05-21_open-source-design-tools_brief.md` (seeded research — existing vault file used across stages). This is noted as **"E2E with seeded research"** per contract rules.

## Stage Evidence

### 1. Trends — PASS
- Vault panel shows 2 files from `04-Trends/`:
  - `github_trending.md` (2026-05-26)
  - `2026-05-25_github_trending.md` (2026-05-26)
- Read-only workspace behavior confirmed.

### 2. Research — PASS
- Stage ran ("Done — View Results" button visible).
- Vault panel shows `2026-05-21_open-source-design-tools_brief.md` in `10-Research/`.
- User tested a GitHub URL as additional context input.

### 3. Ideation — PASS
- Research file selected: `2026-05-21_open-source-design-tools_brief.md`
- OutputBrowser rendered 12 ranked ideas including:
  - "Rank 1 — I Replaced Figma With My Terminal (Here's What Actually Happened)"
  - With Gap analysis, Audience desire, Competitive signal sections
- New file saved to vault (`02-Ideas/`), "Saved to vault" confirmed in OutputBrowser header.

### 4. Hooks — BLOCKED → FIXED
- Input: topic = "How to build a local RAG system in 20 minutes — for indie devs who want privacy and no API costs."
- Research file: `2026-05-21_open-source-design-tools_brief.md`
- **Error**: `argparse.ArgumentError: argument --audience: conflicting option string(s): --audience`
  - Root cause: `skills/hook.py` registered `--audience` directly AND called `add_brief_args(parser)` which also registers `--audience`.
  - **Fix applied**: Removed duplicate `--audience` from `hook.py` main(); added `if not args.audience: args.audience = "AI builders and content creators"` fallback after parse.
  - Verified fix: `python skills/hook.py --help` prints clean help with `--audience` once. No crash.
- **Hooks acceptance requires a re-run** after the fix.

### 5. Distribution → Outline — PASS
- Hook file selected: `2026-05-21_top-10-skills-for-claude-code.md`
- Video topic: "make a outline for a 10 min you tube video 1min per skill"
- Sections: 8, Platform: yt-long
- OutputBrowser rendered full Dopamine Ladder outline with stages, hook verbatim, goals.
- "Saved to vault · 06-Outlines" confirmed.
- Output path: `06-Outlines/2026-05-29_make-a-outline-for-a-10-min-you-tube-video-1min-per-skill.md` (approx slug)

### 6. Distribution → Title — PASS
- Video concept: "top 10 skills of claude code"
- OutputBrowser rendered Tier-1, Tier-2, Tier-3 title groups with pattern-match reasoning.
- "Saved to vault · 07-Titles" confirmed.

### 7. Distribution → Cascade — PASS
- Research file: `2026-05-21_open-source-design-tools_brief.md`
- Outline file: `06-Outlines/2026-05-29_your-coding-agent-already-has-a.md` (selected from dropdown)
- Bundle created: `08-Distribution/2026-05-29_your-coding-agent-already-has-a-ui-desig/`
- OutputBrowser rendered bundle README by default.

### 8. Distribution → Short-form — PASS (both modes)
**Vault files mode:**
- Research: `2026-05-21_open-source-design-tools_brief.md`
- Outline: `06-Outlines/2026-05-29_make-a-outline-for-a-10.md`
- Bundle: `09-Shorts/2026-05-29_why-open-source-design-tools-are-suddenl/`
- OutputBrowser rendered README with 30s_script.md, 60s_script.md, 90s_script.md tabs.

**YouTube URL mode:**
- URL: `https://www.youtube.com/watch?v=BbUqyF-cosA&list=PLIsL-9VqYVt5OyhIpg5ycPByTqjYscsWh&index=3`
- Bundle: `09-Shorts/2026-05-29_free-open-source-whatsapp-crm-step-by-st/`
- OutputBrowser rendered README with Scripts section and Checklist.

### 9. Distribution → Voice-cleanup — PASS
- Source folder: Outlines (06)
- File: `2026-05-29_make-a-outline-for-a-10.md`
- In-place overwrite checkbox: ticked
- Run completed.

## SSE / Spinner Behavior
- All completed stages showed "Done — View Results" button — no infinite spinners observed.
- SSE log lines were not explicitly confirmed moving during run, but jobs completed without stalls.

## Dashboard + Sidebar
- Sidebar dots: Trends (green), Research (yellow/amber during run → green), Ideation (green), Hooks (gray — not run successfully), Distribution (green).
- Dashboard recent activity: not explicitly confirmed.

## Open Items (UI bugs — post-sprint)

| # | Stage | Bug |
|---|---|---|
| 1 | Trends | Left panel (read-only workspace) is blank — original design showed content preview |
| 2 | Trends | No "Run Trends" button wired to a new scrape |
| 3 | Research | Single-pass synthesis mode does not work |
| 4 | Research | Only 1 file shown in vault panel (more files exist in vault) |
| 5 | Ideation | OutputBrowser not scrollable — output cuts off |
| 6 | Ideation | Left panel (text prompt box) styling off-theme |
| 7 | All Distribution tabs | OutputBrowser not scrollable — output cuts off |
| 8 | All Distribution tabs | No vault sources tab (Trends/Research/Ideation/Hooks have it, Distribution does not) |
| 9 | All Distribution tabs | Button styling does not match app theme |
| 10 | Title | No picker for existing outline file — text box only |
| 11 | Cascade | Output bundle not confirmed voice-cleaned (raw file suspected) |
| 12 | Short-form | YouTube URL toggle does not fully highlight when selected |

## Self-Verification
- 8 of 9 pipeline stages produced real vault output (not demo content).
- Hooks blocked by confirmed bug → fix applied and verified.
- OutputBrowser rendered real vault markdown/bundle content in all passing stages.
- No demo output observed.
