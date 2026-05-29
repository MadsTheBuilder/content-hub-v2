---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 09-dashboard-link-agent
task: Point Dashboard Outline card click and CTA to #distribution/outline.
description: "Dashboard: Outline card click and CTA button now set window.location.hash=distribution/outline before calling onNavigate('distribution')."
tags: [phase5, dashboard, distribution, webapp-sprint]
owned_files:
  - Design-doc/web/src/Dashboard.jsx
verification:
  - Outline card click and CTA both land on Outline tab
  - Non-Outline cards keep their current behaviour
  - No Phase 6 recent-activity work slips in
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 09-DashboardLink

## Self-Verification

- [x] Card `onClick`: Outline branch sets `window.location.hash = "distribution/outline"` then calls `handleNavigate("distribution")`.
- [x] CTA button `onClick`: same pattern with `e.stopPropagation()`.
- [x] Non-Outline cards (`trends`, `research`, `ideation`) unaffected — still call `handleNavigate(card.id)`.
- [x] No activity-list or recent-vault wiring added (Phase 6).
- [x] Build ✅.

## Open Items

None.
