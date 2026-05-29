---
date: 2026-05-28
tags: [session, design-doc, frontend, graph]
description: "Fixed graph sizing bug; embedded D3 system graph as slide 11 inside systems-deck.html with lazy initialisation."
---

# Session: Graph Embedded in Systems Deck

Modifies: [[Design-doc/systems-deck.html]]
References: [[2026-05-27_Design_Doc_Theme_And_Graph]]

## What Changed

### Problem

`Design-doc/graph.html` (created previous session) rendered all nodes collapsed in the top-left corner. Root cause: the D3 setup read `svgEl.clientWidth` at script parse time. Because the SVG was hidden inside a `position:absolute; opacity:0` slide, `clientWidth` returned 0, so `W = 0` and all initial node positions + force center were at `(0, 0)`.

### Fix + Integration

Rather than patch the standalone file, the graph was embedded as **slide 11** inside `Design-doc/systems-deck.html`. The lazy-init pattern fixes the sizing issue by construction:

1. **D3 CDN** added to `<head>` (`https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js`)
2. **Slide 11 HTML** — `.slide.s-graph` with a 42px inner header strip, legend, info panel, controls, and `<svg id="gSvg">`
3. **`initGraph()` function** — full D3 v7 force-directed setup (29 nodes, 40 edges, same data as graph.html). Defined at module scope but never called at page load.
4. **Lazy trigger in `go()`** — when navigating to slide 11 for the first time:
   ```js
   if (slides[cur].id === 's11' && !graphInited) { graphInited = true; setTimeout(initGraph, 80); }
   ```
   The 80ms delay ensures the slide has transitioned into the DOM layout so `clientWidth`/`clientHeight` are real values.

### Slide layout

- `.slide.s-graph { padding: 0; overflow: hidden; }` — overrides default slide padding
- `#gSvg { position: absolute; top: 42px; left: 0; right: 0; bottom: 0; }` — fills slide minus header
- All overlays (legend, info panel, controls) use `position: absolute` (not `fixed`) — scoped to the slide
- Counter auto-updates to `01 / 11` because `total = slides.length` is dynamic

### Interactions (same as standalone graph.html)

- Click node → focus mode + info panel
- Hover → glow
- Legend items → toggle type visibility
- Reset zoom / clear focus buttons
- Zoom/pan + drag nodes

## Files Touched

- `Design-doc/systems-deck.html` — 4 edits: D3 script tag in head, graph CSS block, slide 11 HTML, `initGraph()` JS + `go()` hook

## Open Items

- `Design-doc/graph.html` standalone still has the original sizing bug (clientWidth = 0). Can be fixed by reading dimensions inside a `requestAnimationFrame` callback, but it's now superseded by the embedded slide version.
- Vault output folder structure refactor (raw/cleaned subfolders) still pending — [[project_vault_output_folder_structure]]
- Phase 7 (launch + E2E) of [[Webapp_sprint]] still next
