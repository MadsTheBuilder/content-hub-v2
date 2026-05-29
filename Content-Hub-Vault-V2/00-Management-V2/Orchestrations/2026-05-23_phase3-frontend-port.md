---
slug: phase3-frontend-port
date: 2026-05-23
created: 2026-05-23
status: complete
current_group: null
groups_complete: [1, 2, 3]
specialists_involved: [frontend-agent]
tags: [orchestration, webapp-sprint, frontend, react, phase3]
description: "6-agent orchestration to complete Phase 3 of [[Webapp_sprint]]: port 4 CDN React components to Vite ES-modules, assemble App.jsx, and verify all 31 criteria before marking tasks 3.2–3.7 done."
---

# Orchestration: Phase 3 Frontend Port — [[Webapp_sprint]]

Implements: [[Webapp_sprint]]
References: [[Design_Doc_Web_App_Plan]], [[Current_Sprint]], [[2026-05-22_Webapp_Phase1_Scaffold]], [[2026-05-22_Webapp_Phase2_Backend]]

## Recon Summary

- **Prototype source**: `Design-doc/Content Hub/` — 8 `.jsx` files + 1 `.html`. All use CDN UMD React globals (`window.React`, destructured `useState`/`useEffect`/`useRef`). No ES module imports. Babel transpiles in-browser.
- **Vite target**: `Design-doc/web/src/` — already has `main.jsx`, `Icons.jsx`, `SourcesPanel.jsx`, `Sidebar.jsx` (all properly ported with explicit imports + `export default`). `App.jsx` is still a Phase 1 stub (9 lines, only mounts particle effect).
- **Missing from `web/src/`**: `Dashboard.jsx`, `StageWorkspace.jsx`, `TweaksPanel.jsx`, `Brain.jsx`.
- **`useTweaks` hook**: Lives in prototype `tweaks-panel.jsx`. Posts/listens via `postMessage` for edit-mode protocol. Must be replaced with `localStorage`-backed equivalent (locked decision §6.6 in [[Webapp_sprint]]).
- **Brain.jsx strip requirement**: Prototype has URL input chips + file-drop controls. Locked decision #8 strips these — pasted-text textarea only.
- **`web/index.html`**: Already clean — no CDN React tags, ESM-only entry via `main.jsx`.
- **Sidebar.jsx**: Exports both named `PIPELINE` and default `Sidebar`.

## Execution Plan

**Tasks:** 6 across 3 groups
**Specialists:** frontend-agent (all tasks — pure frontend port)

### Group 1 (parallel — 4 agents, all independent, no shared files)

- [frontend-agent | EASY] Port `dashboard.jsx` → `Dashboard.jsx`
  Files: CREATE `Design-doc/web/src/Dashboard.jsx`
  Read: `Design-doc/Content Hub/dashboard.jsx`
  Criteria: exists; `export default Dashboard`; no CDN globals; Icon import wired

- [frontend-agent | EASY] Port `stage-workspace.jsx` → `StageWorkspace.jsx`
  Files: CREATE `Design-doc/web/src/StageWorkspace.jsx`
  Read: `Design-doc/Content Hub/stage-workspace.jsx`
  Criteria: exists; `export default StageWorkspace`; no CDN globals; explicit React imports

- [frontend-agent | MEDIUM] Port `tweaks-panel.jsx` → `TweaksPanel.jsx` (localStorage swap)
  Files: CREATE `Design-doc/web/src/TweaksPanel.jsx`
  Read: `Design-doc/Content Hub/tweaks-panel.jsx`
  Criteria: exists; `export default TweaksPanel`; `useTweaks` named export; `localStorage` used (not `postMessage`)

- [frontend-agent | MEDIUM] Port `brain.jsx` → `Brain.jsx` (strip URL/file-drop)
  Files: CREATE `Design-doc/web/src/Brain.jsx`
  Read: `Design-doc/Content Hub/brain.jsx`
  Criteria: exists; `export default Brain`; pasted-text textarea only; NO `type="url"`, `onDrop`, `FileReader`

### Group 2 (sequential — depends on Group 1 exports being known)

- [frontend-agent | MEDIUM] Port `app.jsx` → full `App.jsx` (assemble all components)
  Files: MODIFY `Design-doc/web/src/App.jsx`
  Read: `Design-doc/Content Hub/app.jsx`, all Group 1 outputs
  Criteria: imports all 5 components; `import { useTweaks }` from TweaksPanel; `export default App`; full app rendered (not stub); particle bootstrap preserved

### Group 3 (sequential — final gate, depends on Group 2)

- [verification-agent | HARD] Verify 26 criteria + update sprint docs
  Files: READ all `web/src/` files; MODIFY `Webapp_sprint.md`, `Current_Sprint.md`
  Criteria: All 26 checks pass; sprint tasks 3.2–3.7 → `[x]`; agent context notes exist; if any check fails → NEEDS_RERUN (loop restarts for failing agents only)

## Agent Prompts

### Task: frontend-agent: Dashboard.jsx port

- description: "frontend-agent: Port dashboard.jsx → Dashboard.jsx"
- model: haiku
- prompt: |
    You are the frontend-agent for Content Hub V2. Port CDN React prototype components to Vite + React 19.2.6.

    **Porting pattern:**
    - `const { useState, useEffect } = React;` → `import { useState, useEffect } from 'react'`
    - `Icon.X` (CDN global) → `import Icon from './Icons.jsx'` then use `Icon.X`
    - No `export` in prototype → add `export default Dashboard` at end
    - Never add `window.X = X` globals

    ## Your Task
    Read `Design-doc/Content Hub/dashboard.jsx` fully. Create `Design-doc/web/src/Dashboard.jsx`.

    ## Scope
    Read: `Design-doc/Content Hub/dashboard.jsx`, `Design-doc/web/src/Icons.jsx` (first 20 lines)
    Create: `Design-doc/web/src/Dashboard.jsx`
    IMPORTANT: Only touch the files listed. Other agents work on other files in parallel.

    ## Acceptance Criteria
    1. File exists at `Design-doc/web/src/Dashboard.jsx`
    2. All CDN globals replaced with explicit React imports
    3. `import Icon from './Icons.jsx'` present if icons used
    4. `export default Dashboard` at end of file
    5. No `window.` references, no `const { ... } = React;` patterns
    6. Write context note to `Design-doc/web/src/.agent-context/Dashboard.md`

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT + summary of changes.

### Task: frontend-agent: StageWorkspace.jsx port

- description: "frontend-agent: Port stage-workspace.jsx → StageWorkspace.jsx"
- model: haiku
- prompt: |
    You are the frontend-agent for Content Hub V2. Port CDN React prototype components to Vite + React 19.2.6.

    **Porting pattern:**
    - `const { useState, useEffect, useRef } = React;` → `import { useState, useEffect, useRef } from 'react'`
    - `Icon.X` → `import Icon from './Icons.jsx'` then `Icon.X`
    - Add `export default StageWorkspace` at end

    ## Your Task
    Read `Design-doc/Content Hub/stage-workspace.jsx` fully. Create `Design-doc/web/src/StageWorkspace.jsx`.

    ## Scope
    Read: `Design-doc/Content Hub/stage-workspace.jsx`, `Design-doc/web/src/Sidebar.jsx` (understand PIPELINE shape)
    Create: `Design-doc/web/src/StageWorkspace.jsx`
    IMPORTANT: Only touch the files listed. Other agents work on other files in parallel.

    ## Acceptance Criteria
    1. File exists at `Design-doc/web/src/StageWorkspace.jsx`
    2. All CDN globals replaced with explicit React imports
    3. Icon import wired if icons used
    4. `export default StageWorkspace` at end
    5. No `window.` references, no CDN destructure patterns
    6. Write context note to `Design-doc/web/src/.agent-context/StageWorkspace.md`

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT + summary of changes.

### Task: frontend-agent: TweaksPanel.jsx port (localStorage swap)

- description: "frontend-agent: Port tweaks-panel.jsx → TweaksPanel.jsx with localStorage"
- model: sonnet
- prompt: |
    You are the frontend-agent for Content Hub V2. Port CDN React prototype components to Vite + React 19.2.6.

    ## Critical requirement
    The prototype `tweaks-panel.jsx` uses `postMessage` for persistence (an iframe edit-mode protocol).
    The Vite app MUST use `localStorage` instead. This is locked decision §6.6.

    The `useTweaks(defaults)` hook must:
    - On mount: read each key from localStorage, falling back to defaults
    - On set via `setTweak(key, value)`: write to localStorage immediately
    - Return `[tweakValues, setTweak]`
    - Be exported as a NAMED export: `export { useTweaks }`

    ## Your Task
    Read `Design-doc/Content Hub/tweaks-panel.jsx` fully. Create `Design-doc/web/src/TweaksPanel.jsx`.

    ## Scope
    Read: `Design-doc/Content Hub/tweaks-panel.jsx`
    Create: `Design-doc/web/src/TweaksPanel.jsx`
    IMPORTANT: Only touch the files listed. Other agents work on other files in parallel.

    ## Acceptance Criteria
    1. File exists at `Design-doc/web/src/TweaksPanel.jsx`
    2. `export { useTweaks }` named export present
    3. `useTweaks` reads and writes `localStorage` (NOT `postMessage`)
    4. `export default TweaksPanel` at end
    5. All CDN globals replaced with explicit React imports
    6. No `window.postMessage`, no `window.addEventListener('message', ...)`
    7. Write context note to `Design-doc/web/src/.agent-context/TweaksPanel.md` including the useTweaks hook signature

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT + summary of changes.

### Task: frontend-agent: Brain.jsx port (strip URL/file-drop)

- description: "frontend-agent: Port brain.jsx → Brain.jsx (strip URL + file-drop)"
- model: sonnet
- prompt: |
    You are the frontend-agent for Content Hub V2. Port CDN React prototype components to Vite + React 19.2.6.

    ## Critical requirement — locked decision #8
    The prototype `brain.jsx` has URL input chips and file-drop controls.
    BOTH must be stripped entirely. Brain v1 = pasted-text textarea ONLY.

    Keep: textarea for pasting text, Run Analysis button, results display sections.
    Remove: everything handling `type="url"`, `onDrop`, `FileReader`, youtube_url inputs, URL chip state/JSX.

    ## Your Task
    Read `Design-doc/Content Hub/brain.jsx` fully. Create `Design-doc/web/src/Brain.jsx` — stripped version.

    ## Scope
    Read: `Design-doc/Content Hub/brain.jsx`
    Create: `Design-doc/web/src/Brain.jsx`
    IMPORTANT: Only touch the files listed. Other agents work on other files in parallel.

    ## Acceptance Criteria
    1. File exists at `Design-doc/web/src/Brain.jsx`
    2. `export default Brain` at end
    3. All CDN globals replaced with explicit React imports
    4. Pasted-text textarea present
    5. NO `type="url"` input anywhere
    6. NO `onDrop` handler anywhere
    7. NO `FileReader` anywhere
    8. NO youtube_url or URL chip state/JSX
    9. Write context note to `Design-doc/web/src/.agent-context/Brain.md` listing what was stripped

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT + summary of changes.

### Task: frontend-agent: App.jsx full port (assemble all components)

- description: "frontend-agent: Port app.jsx → full App.jsx assembling all components"
- model: sonnet
- prompt: |
    You are the frontend-agent for Content Hub V2. You are the final assembly step of Phase 3.

    Group 1 agents have already created in `Design-doc/web/src/`:
    - `Dashboard.jsx` (export default Dashboard)
    - `StageWorkspace.jsx` (export default StageWorkspace)
    - `TweaksPanel.jsx` (export default TweaksPanel + named export useTweaks)
    - `Brain.jsx` (export default Brain)

    Previously ported:
    - `Sidebar.jsx` (export default Sidebar, named export PIPELINE)
    - `Icons.jsx` (export default Icon)

    Current `App.jsx` is a Phase 1 stub — replace it entirely.

    ## Critical requirements
    - Import `useTweaks` from `./TweaksPanel.jsx` (NOT a CDN global)
    - Keep particle bootstrap: `useEffect(() => { import('./particles.js') }, [])`
    - `export default App`

    ## Your Task
    1. Read `Design-doc/Content Hub/app.jsx` for full component logic
    2. Read `Design-doc/web/src/TweaksPanel.jsx` to understand useTweaks signature
    3. Read `Design-doc/web/src/Sidebar.jsx` to understand PIPELINE if needed
    4. Rewrite `Design-doc/web/src/App.jsx` as the full assembled Vite app

    ## Scope
    Read: `Design-doc/Content Hub/app.jsx`, `Design-doc/web/src/TweaksPanel.jsx`, `Design-doc/web/src/Sidebar.jsx`
    Modify: `Design-doc/web/src/App.jsx`
    IMPORTANT: Only touch App.jsx. Do NOT modify any other file.

    ## Acceptance Criteria
    1. `import { useState, useEffect } from 'react'` (add useCallback if needed)
    2. `import { useTweaks } from './TweaksPanel.jsx'`
    3. `import Dashboard from './Dashboard.jsx'`
    4. `import Sidebar from './Sidebar.jsx'`
    5. `import StageWorkspace from './StageWorkspace.jsx'`
    6. `import TweaksPanel from './TweaksPanel.jsx'`
    7. `import Brain from './Brain.jsx'`
    8. `export default App` — full assembled app, NOT stub `return <div id="app" />`
    9. No CDN globals, no `window.React`
    10. Particle bootstrap preserved
    11. Write context note to `Design-doc/web/src/.agent-context/App.md`

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT + summary of changes.

### Task: verification-agent: Check all Phase 3 criteria + update sprint docs

- description: "verification-agent: Verify Phase 3 complete + update sprint docs"
- model: sonnet
- prompt: |
    You are the Verification Agent for Webapp Sprint Phase 3. Check all 26 criteria.
    Fail loudly on ANY miss. Do NOT update sprint docs unless ALL checks pass.

    ## Verification Checklist

    File existence (use Glob + Read):
    1. `Design-doc/web/src/App.jsx` exists AND is > 20 lines (not the stub)
    2. `Design-doc/web/src/Dashboard.jsx` exists
    3. `Design-doc/web/src/StageWorkspace.jsx` exists
    4. `Design-doc/web/src/TweaksPanel.jsx` exists
    5. `Design-doc/web/src/Brain.jsx` exists

    Export checks (Grep each file for `export default`):
    6. App.jsx has `export default`
    7. Dashboard.jsx has `export default`
    8. StageWorkspace.jsx has `export default`
    9. TweaksPanel.jsx has `export default`
    10. Brain.jsx has `export default`
    11. TweaksPanel.jsx has `export { useTweaks }` or `export function useTweaks`

    CDN-clean checks (Grep — must find 0 matches across all 5 files):
    12. No `window.React` in any of the 5 files
    13. No `const { useState` destructure pattern in any of the 5 files
    14. No `ReactDOM.render` in any of the 5 files

    App.jsx import checks (Grep App.jsx):
    15. `import Dashboard` present
    16. `import Sidebar` present
    17. `import StageWorkspace` present
    18. `import TweaksPanel` present
    19. `import Brain` present
    20. `import { useTweaks }` or `import { useTweaks, ...` present

    TweaksPanel localStorage check:
    21. TweaksPanel.jsx contains `localStorage`
    22. TweaksPanel.jsx does NOT contain `postMessage`

    Brain strip checks:
    23. Brain.jsx does NOT contain `type="url"`
    24. Brain.jsx does NOT contain `onDrop`
    25. Brain.jsx does NOT contain `FileReader`

    main.jsx unchanged:
    26. `Design-doc/web/src/main.jsx` still contains `import App from './App.jsx'`

    Agent context notes (Glob):
    27. `Design-doc/web/src/.agent-context/Dashboard.md` exists
    28. `Design-doc/web/src/.agent-context/StageWorkspace.md` exists
    29. `Design-doc/web/src/.agent-context/TweaksPanel.md` exists
    30. `Design-doc/web/src/.agent-context/Brain.md` exists
    31. `Design-doc/web/src/.agent-context/App.md` exists

    ## If ALL checks pass:
    Update `Content-Hub-Vault-V2/00-Management-V2/Tasks/Webapp_sprint.md`:
    - Tasks 3.2, 3.3, 3.4, 3.7: `[ ]` → `[x]`
    - Status table row 3: `[~] index/main shell landed; component port pending` → `[x] complete`
    Update `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md`:
    - Phase 3 status → complete; move Phase 4 to **Next**
    Write `Design-doc/web/src/.agent-context/Verification.md` with full pass/fail summary.
    Report: DONE

    ## If ANY check fails:
    Report: NEEDS_RERUN
    List exactly which check numbers failed, what was found vs expected, and which agent is responsible.
    Do NOT update any sprint docs.

    ## When done
    Report: DONE (all 31 checks pass) / NEEDS_RERUN (list failures) / STUCK

## Status Log
- 2026-05-23: created, status=awaiting-approval
- 2026-05-23: approved by user, dispatching Group 1
- 2026-05-23: Group 1 complete (all 4 agents DONE)
- 2026-05-23: Group 2 complete (App-agent DONE)
- 2026-05-23: Verification loop 1 — NEEDS_RERUN (duplicate export in StageWorkspace + TweaksPanel export check)
- 2026-05-23: Targeted fixes dispatched and applied
- 2026-05-23: Verification loop 2 — all 31 checks PASS, status=complete
