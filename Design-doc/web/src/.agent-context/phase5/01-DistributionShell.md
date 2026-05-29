---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 01-distribution-shell-agent
task: Create DistributionWorkspace.jsx shell with tab bar and hash routing.
description: "Distribution workspace shell: tab bar (outline→title→cascade→short-form→voice-cleanup), hash routing #distribution/<tab>, fallback to outline, hashchange listener."
tags: [phase5, distribution, shell, hash-routing, webapp-sprint]
owned_files:
  - Design-doc/web/src/DistributionWorkspace.jsx
  - Design-doc/web/src/styles.css (dist-tab-bar + dist-tab + dist-tab-content appended)
verification:
  - '#distribution/title selects Title tab'
  - '#distribution/not-real falls back to outline'
  - 'No raw fetch in DistributionWorkspace.jsx'
  - 'Shell does not absorb per-tab form or job logic'
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 01-DistributionShell

## Mission

Create `DistributionWorkspace.jsx` with: 5-tab bar in spec order, active tab driven by `#distribution/<tab>`, fallback to `outline` on invalid/missing hash, `hashchange` listener for browser nav.

## Context Read

Read: `App.jsx`, `Sidebar.jsx`, `StageWorkspace.jsx`, `00-Contract.md`.

## Changes Made

- Created `Design-doc/web/src/DistributionWorkspace.jsx`
  - `getTabFromHash()` parses `window.location.hash` via regex `^#distribution/(.+)$`; returns `outline` if slug is missing or not in `VALID_SLUGS`
  - `useState(getTabFromHash)` — initialised from hash so tab persists on refresh and re-entry
  - `useEffect` adds `hashchange` listener to sync state when browser back/forward changes hash
  - `navigate(slug)` writes `window.location.hash = distribution/<slug>` and calls `setActiveTab`
  - Tab bar renders `TABS` in order: `outline → title → cascade → short-form → voice-cleanup`
  - Active tab gets `.is-active` class; inactive tabs get `.dist-tab` only
  - `ActiveTab` is resolved from TABS array and mounted inside `.dist-tab-content`
  - Imports all 5 tab components from `./DistributionTabs/` (created in Group 2)
  - No raw `fetch`; no per-tab form or job logic in this file
- Appended `.dist-tab-bar`, `.dist-tab`, `.dist-tab.is-active`, `.dist-tab-content` to `styles.css`

## Self-Verification

- [x] `#distribution/title` → `getTabFromHash()` returns `'title'` → Title tab selected.
- [x] `#distribution/not-real` → slug not in `VALID_SLUGS` → returns `'outline'` → fallback confirmed.
- [x] `#distribution/` (no slug after slash) → regex match[1] is empty string → not in VALID_SLUGS → `'outline'`.
- [x] No `fetch` call anywhere in `DistributionWorkspace.jsx`.
- [x] Shell only handles tab routing + banner; all form/job logic lives in each `DistributionTabs/*.jsx`.

## Open Items

None. Tab components created in Group 2.
