---
date: 2026-05-08
type: session
status: complete
---

# Artifact Generation Test — Slide Deck + Infographic via --artifacts

Implements: [[Local_First_Skill_Engine_Plan]]
References: [[2026-05-08_YT_Pipeline_Friction_Repair]]
Modifies: [[skills/yt_pipeline.py]]

## Context

Follow-up to [[2026-05-08_YT_Pipeline_Friction_Repair]], which added the `--artifacts` flag and `ARTIFACT_QUEUE`. This session tested slide-deck and infographic generation against the existing OpenMythos notebook (`4546d265-0860-451a-b904-055b39d25c51`).

## Findings

**infographic is a supported generate subcommand.** `python -m notebooklm generate --help` lists: `audio`, `video`, `slide-deck`, `quiz`, `flashcards`, `infographic`, `data-table`, `mind-map`, `report`. Infographic downloads as `.png`.

**Infographic generation succeeded.** Queued async, completed in ~160s. Downloaded to `Content-Hub-Vault-V2/10-Research/2026-05-07_openmythos/infographic.png` — 4.9MB PNG titled "OpenMythos: Innovation or Fan Fiction?".

**Slide-deck generation failed.** Returns `GENERATION_FAILED` after >3 minutes. All 5 notebook sources are `SourceType.YOUTUBE` (no text/PDF sources). Hypothesis: NotebookLM's slide-deck backend requires at least one document-type source and silently fails on all-YouTube notebooks. The error is a backend failure, not a timeout. The `_generate_artifact` 180s timeout also fires before the backend returns its failure — upgraded to 360s.

## Changes applied

- [skills/yt_pipeline.py](../../../skills/yt_pipeline.py): Added `("infographic", "infographic", "png")` to `ARTIFACT_QUEUE` (line 30). Increased `_generate_artifact` timeout from 180s to 360s.

## Files touched

- `skills/yt_pipeline.py` — ARTIFACT_QUEUE + timeout
- `Content-Hub-Vault-V2/10-Research/2026-05-07_openmythos/infographic.png` — generated artifact

## Open items

- Slide-deck failure on all-YouTube notebooks: untested against a mixed (YouTube + document) notebook. If confirmed, `_generate_artifact` could skip `slide-deck` when `source list` shows only YOUTUBE-type sources.
- Consider testing `quiz` and `flashcards` generation — not in ARTIFACT_QUEUE yet but could be useful for educational content.
