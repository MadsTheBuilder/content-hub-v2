---
date: 2026-05-31
type: session-log
tags: [webapp, pipeline, frontend, backend, full-pipeline, research]
description: "Full Pipeline research stage now opens a config gate after trend pick — niche/mode/target-length + collapsed advanced (tone/audience/banned). Fixes the empty-niche crash. Frontend + backend, build/lint clean."
---

# Session — Research Options Config Gate

**Implements:** [[Research Options Config Gate]]
**Modifies:** [[FullPipelinePage]], [[main.py]], [[pipeline.py]], [[styles.css]]
**References:** [[2026-05-31_Full_Pipeline_Page]], [[brief_args]], [[researcher.py]], [[useJobStream]], [[VaultPicker]]

## Problem

On the [[Full Pipeline Page]], picking a trend **auto-ran** research with `niche: seed`. The trends `VaultPicker` was not gated on the niche being filled, so picking a trend with an empty seed launched `--niche ""` → [[researcher.py]] aborts with `--niche is required when running research`. Retry re-sent the same empty niche, looping.

## What changed

- **EDIT** `Design-doc/web/src/FullPipelinePage.jsx`
  - New `research` state (`niche, mode, targetLength, tone, audience, banned`).
  - `pickTrend` **no longer launches** — it sets `trendPath`, prefills `research.niche` from the seed, and advances to the Research step in `review` phase.
  - New `runResearch()` launches with all options threaded; blank advanced fields are omitted (→ `brief.md` defaults).
  - New `ResearchConfig` gate component: niche (editable, prefilled, **required**), mode `fast/deep` segmented toggle, target-length number, collapsed `<details>` Advanced (tone / audience / banned phrases). **Run Research** disabled until niche is non-empty — this is the bug fix.
  - `gateReady("research")` → always `true` (the config form is the gate; `ApproveGate` shows once `briefPath` exists). Retry for research routes to `runResearch`.
- **EDIT** `Design-doc/server/main.py` — `ResearcherBody` gains `target_length`, `tone`, `audience`, `banned_phrases`; route forwards them.
- **EDIT** `Design-doc/server/pipeline.py` — `run_researcher` accepts the new params and appends `--target-length / --tone / --audience / --banned-phrase` **only when set**.
- **EDIT** `Design-doc/web/src/styles.css` — appended `.fp-opt-grid`, `.fp-opt`, `.fp-seg`, `.fp-adv` reusing existing tokens.

**No `researcher.py` change** — it already accepts every flag via [[brief_args]] (`add_brief_args`). Gaps were only the web body model + subprocess wrapper.

## Decisions (confirmed with user)

- **Config gate after trend pick** (chosen over inline-at-top auto-run) — explicit "Run Research" launch, options feel per-stage, confirm before spend.
- **All three advanced fields surfaced, collapsed, optional** — blank ⇒ falls back to `brief.md`; research still runs.
- Niche is editable in the gate (prefilled from seed) so "choose niche" is honored even after the top seed input locks.

## Verification

- `npx eslint src/FullPipelinePage.jsx` → 0 errors (2 pre-existing intentional exhaustive-deps warnings).
- `npx vite build` → clean. `python -c ast.parse` on `main.py` + `pipeline.py` → OK.

## Follow-up fix — trend pick researched stale repos (researcher.py)

After the gate shipped, the first live run failed with `ValueError: No matching GitHub repo URLs found in github_trending.md` ([[researcher.py]] `run()` line ~591).

**Root cause:** `run()` used `--repos` only as a *filter against the aggregate `github_trending.md`* — it never researched a repo directly. The `04-Trends` `VaultPicker` lists all **21 persisted subfolders**, but the aggregate only holds the **13 most-recent** repos. Picking any of the 8 stale subfolders (the user picked `Manavarya09/design-extract`, niche "Design") → no slug match → raise.

**Fix (surgical, in `run()` only):** normalize each `--repos` entry to a full URL (`owner/repo` → `https://github.com/owner/repo`) and research exactly those, dropping the aggregate read + slug filter. Strictly more permissive; aligns with the flag's documented intent ("Repos to research"). `extract_urls` + `TRENDS_FILE` remain — still used by the `--list` path. Verified: all 21 subfolders (incl. the failing `design-extract`) now resolve to valid URLs. **No restart needed** — researcher runs as a fresh subprocess per job.

## Open items

- **Backend restart required** — run `uvicorn` with `--reload` (or restart) so the new `ResearcherBody` fields load; otherwise the extra flags are ignored (same stale-`main.py` gotcha noted in [[2026-05-31_Trends_UI_Fix_404_Resolved]]).
- **Live run still pending** — confirm `--target-length / --tone / --audience / --banned-phrase` actually reach the brief in a real research run.

See [[Current_Sprint]].
