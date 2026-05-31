---
date: 2026-05-29
type: session_log
status: open
description: "16 open UI issues found during Phase 7 browser-facing E2E acceptance run. No code changes — findings log only. Deferred post-sprint."
tags: [session, webapp-sprint, bugs, polish, deferred]
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
  - "[[2026-05-29_Design_Doc_Web_App_Wired]]"
  - "[[2026-05-29_phase7-launch-e2e-acceptance]]"
---

# Session: Minor Fixes Left Over — Post-Sprint Open Issues

References: [[2026-05-29_Design_Doc_Web_App_Wired]] (Phase 7 acceptance session)
Found during: browser-facing E2E acceptance run, 2026-05-29

No code changes made this session. All items below are deferred post-sprint.

---

## Trends

**1. Left panel is blank**
The workspace left panel shows nothing. The original [[Design_Doc_Web_App_Plan]] claude.ai design mockup showed a content preview area here.
- File: `Design-doc/web/src/StageWorkspace.jsx` — Trends `InputZone` renders a read-only notice only; no content preview wired.

**2. No "Run Trends" button**
There is no way to trigger a new GitHub trends scrape from the UI. The stage is read-only with no action button.
- File: `Design-doc/web/src/StageWorkspace.jsx` — `handleRun` returns early for `stageId === "trends"`.
- Backend: no `/api/pipeline/trends` endpoint exists in `Design-doc/server/main.py`.

---

## Research

**3. Single-pass synthesis mode does not work**
The mode toggle exists in the UI but the single-pass path does not produce output.
- File: `Design-doc/web/src/StageWorkspace.jsx` — mode value passed in body; suspect `pipeline.py` or `researcher.py` does not handle this mode correctly.

**4. Research does not accept URLs**
User tested a YouTube URL and a GitHub URL as additional context inputs. Neither was processed.
- Root cause (confirmed): `skills/researcher.py` only accepts repos that appear in the GitHub trending file. Arbitrary URLs are not supported by the backend design — this is a skill-layer constraint, not a frontend bug.
- The `urlDraft` flush fix (applied in [[2026-05-29_Design_Doc_Web_App_Wired]]) ensures URLs reach the server, but the skill rejects them if they're not in the trending list.

---

## Ideation

**5. OutputBrowser not scrollable — output cuts off**
The output box clips at the bottom. Long ideation results (e.g. 12 ranked ideas) are not fully readable.
- File: `Design-doc/web/src/OutputBrowser.jsx` — likely missing `overflow-y: auto` or a max-height constraint.

**6. Left panel text box styling is off-theme**
The text input area (below the research file picker) does not match the app's dark theme.
- File: `Design-doc/web/src/StageWorkspace.jsx` — Ideation `InputZone` textarea style.

---

## Hooks

**7. Only 1 research file in dropdown (needs re-test)**
During the session only 1 file appeared in the research file picker. The `vault.py` subdirectory fix was applied and verified via API (5 files returned). The dropdown needs a re-test in a live browser session to confirm the fix took effect end-to-end.
- Fix applied: `Design-doc/server/vault.py` `recent()` — now walks one level of subdirs.
- Modifies: [[VaultPicker]] → `getRecent("10-Research")`.

---

## Distribution — All Tabs (Outline, Title, Cascade, Short-form, Voice-cleanup)

**8. OutputBrowser not scrollable — output cuts off**
Same issue as Ideation (#5). All 5 Distribution tabs clip long output at the bottom of the box.
- File: `Design-doc/web/src/OutputBrowser.jsx` — same fix needed.

**9. No vault sources tab**
Trends, Research, Ideation, and Hooks all have a vault sources tab (showing recent files from their folder). None of the 5 Distribution tabs have this.
- Files: `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`, `TitleTab.jsx`, `CascadeTab.jsx`, `ShortFormTab.jsx`, `VoiceCleanupTab.jsx`.
- Reference component: [[SourcesPanel]] / `LiveSourcesPanel` wired in `StageWorkspace.jsx`.

**10. Button styling does not match app theme**
Buttons on Distribution tabs use a different visual style from the rest of the app (Trends, Research, Ideation, Hooks).
- Files: all 5 Distribution tab files.

---

## Distribution — Title

**11. No outline file picker**
Title tab has only a plain text box for "video concept." There is no `VaultPicker` to select an existing outline file from `06-Outlines/`.
- File: `Design-doc/web/src/DistributionTabs/TitleTab.jsx`.

---

## Distribution — Cascade

**12. Output bundle not confirmed voice-cleaned**
The Cascade bundle was generated but it's unclear whether voice cleanup ran on the output. Raw file suspected. The bundle at `08-Distribution/2026-05-29_your-coding-agent-already-has-a-ui-desig/` contains `README_cleaned.md` — needs manual inspection to confirm voice-cleaned vs raw.
- Skill: [[cascade]] (`skills/cascade.py`) — check whether voice-cleanup step runs automatically or requires manual invocation.

---

## Distribution — Short-form

**13. YouTube URL toggle does not fully highlight**
When toggled to YouTube URL mode, the toggle button does not fully light up/change appearance. Visual feedback is incomplete.
- File: `Design-doc/web/src/DistributionTabs/ShortFormTab.jsx` — toggle state style.

---

## Brain

**14. Layout deviates from original design mockup**
The current Brain implementation uses: text paste area + separate URL input + Analyze button + score chips + collapsible accordion (01–06).

The original [[Design_Doc_Web_App_Plan]] claude.ai mockup showed: single full-width input with URL/file/text tabs, score gauges in a row, scrolling analysis panel below.

This is a cosmetic/layout deviation. All 5 required analysis fields render correctly (confirmed in [[2026-05-29_phase7-launch-e2e-acceptance]]).
- File: `Design-doc/web/src/Brain.jsx`.

---

## Dashboard

**15. Recent activity panel not confirmed**
Sidebar status dots were confirmed working. The Dashboard "recent activity" list was not explicitly tested during the acceptance run. Unknown whether it reflects new vault artifacts.
- File: `Design-doc/web/src/Dashboard.jsx` — `usePipelineSnapshot` hook drives recent activity.

---

## Priority Grouping (suggested fix order)

| Priority | Items | Rationale |
|---|---|---|
| High | #5, #8 | OutputBrowser scrolling affects every stage — single CSS fix likely resolves both |
| High | #9 | Missing vault sources tab on all 5 Distribution tabs — high discoverability impact |
| Medium | #10 | Button theme mismatch — visual coherence across Distribution |
| Medium | #11 | Title has no outline picker — usability gap |
| Medium | #2 | No Trends run button — stage is dead without it |
| Low | #1, #6, #13, #14 | Cosmetic/polish |
| Investigate | #3, #4, #12 | Require backend or skill-layer changes |
| Re-test | #7 | Fix applied — needs browser verification |
| Confirm | #15 | Dashboard activity — quick manual check |
