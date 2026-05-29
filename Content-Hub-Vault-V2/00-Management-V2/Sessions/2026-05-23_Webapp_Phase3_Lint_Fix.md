---
date: 2026-05-23
tags: [session, webapp, lint, phase3]
description: "Phase 3 verification fix — resolved all 7 build/lint blockers that were missed in the original phase session."
---

# 2026-05-23 — Webapp Phase 3 Lint Fix

References: [[2026-05-23_Webapp_Phase3_Frontend_Port]] (original session)
Modifies: [[Design_Doc_Web_App_Plan]] Phase 3 status

## What Happened

The original Phase 3 session marked itself complete, but real verification found the frontend had 7 blocking issues. This session fixed every one and confirmed clean build + lint.

## Files Changed

| File | Change |
|---|---|
| `Design-doc/web/src/Brain.jsx` | Removed import of non-existent `./StackedPanel`; both `StackedPanel` and `SourcesPanel` now come from `./SourcesPanel.jsx` (named exports) |
| `Design-doc/web/src/TweaksPanel.jsx` | `TweakSection` prop renamed `label` → `title` to match App.jsx call sites; removed unused `handleOpen` function; added `react-refresh/only-export-components` disable on `useTweaks`; added `react-hooks/refs` disable narrowly on `offsetRef.current` render-read and `valueRef.current` render-write |
| `Design-doc/web/src/SourcesPanel.jsx` | Resolved duplicate `"outline-rag"` key in `FILE_CONTENT`; distribution entry renamed to `"dist-outline-rag"`, matching tree row `kind` updated |
| `Design-doc/web/src/StageWorkspace.jsx` | Suppressed `react-hooks/set-state-in-effect` + `react-hooks/exhaustive-deps` on the stage-reset `useEffect` (intentionally keyed on `stageId` only — initialState is a hardcoded prop per stage) |
| `Design-doc/web/src/particles.js` | Removed `let t` accumulator (declared, incremented, never read); `catch (e)` → `catch {}` (optional catch binding, no binding needed) |
| `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md` | Phase 3 marked complete with fix details; Phase 4 set as next |

## Verification

- `npm run build` → ✅ clean (25 modules, 147ms)
- `npm run lint` → ✅ clean (0 errors, 0 warnings)

## Suppression Rationale

Three ESLint suppressions were added narrowly:

1. **`react-refresh/only-export-components` on `useTweaks`**: Hook is co-located with the panel for cohesion; moving it to a separate file would be premature for a Phase 3 demo port.
2. **`react-hooks/refs` on `offsetRef.current` in render**: Panel position is managed via direct DOM manipulation during drag for performance; reading the ref at initial render is the intended initialization path.
3. **`react-hooks/refs` on `valueRef.current = value`**: Standard "latest-value ref" pattern for avoiding stale closure in pointer-drag handlers; `useEffect` would introduce a timing gap.
4. **`react-hooks/set-state-in-effect` + `exhaustive-deps` on stage-reset effect**: Reset fires only on `stageId` change; `initialState` is intentionally excluded from deps because it's a new object literal every render and must not trigger the reset on every view.

## Open Items

- Phase 4: Wire the 5 stage inputs to FastAPI `/api/jobs/run/{stage}` + SSE streaming
- No behavior changes in this session — Phase 3 is a hardcoded demo port
