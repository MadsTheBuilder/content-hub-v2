---
date: 2026-04-21
type: session-log
---

# Tier 2 Proposals C and D — Written for Review

Implements: [[tmp_marketingskills Knowledge Graph]]
References: [[2026-04-21_Graph_Questions_Followup]], [[Analytics Tracking Skill]], [[RevOps and Lead Lifecycle Community]], [[Tool Integration APIs Community]]
Modifies: [[Plans/analytics-tracking-decomposition]], [[Plans/community-subcluster-proposal]]

## Context

Resumed from [[2026-04-21_Graph_Questions_Followup]]. Tier 1 was complete. This session writes Tier 2 proposals C and D for user review before any structural changes are made.

## Actions Taken

### Proposal C — Analytics Tracking Decomposition
Written to: `Content-Hub-Vault/00-Management/Plans/analytics-tracking-decomposition.md`

Proposes splitting [[Analytics Tracking Skill]] (God Node #2, 20 edges) into a router + 4 child skills:
- `analytics-strategy` — event naming, tracking plan, privacy (platform-agnostic)
- `ga4-setup` — GA4 property setup, custom events, conversions
- `gtm-setup` — GTM container, data layer, UTM strategy
- `google-ads-tracking` — Google Ads conversion tracking, GA4 import vs direct tag

Execution is ~6 file edits. No reference file changes. Parent `analytics-tracking` becomes a router (same trigger, routes to children).

### Proposal D — Community Sub-cluster Proposal
Written to: `Content-Hub-Vault/00-Management/Plans/community-subcluster-proposal.md`

Proposes adding cross-reference links to existing SKILL.md files to push graphify toward tighter sub-clusters in:
- Community 0 (RevOps, 51 nodes, cohesion 0.04) → 3 sub-clusters via `revops/SKILL.md` + `sales-enablement/SKILL.md` edits
- Community 1 (Tool Integration APIs, 42 nodes, cohesion 0.06) → 2 sub-clusters via `ab-test-setup/SKILL.md` + `page-cro/SKILL.md` edits

Execution is ~5 additive edits. No new files. Validate with `graphify --update`.

## Open Items

- [ ] User review and approval of Proposal C (analytics-tracking-decomposition)
- [ ] User review and approval of Proposal D (community-subcluster-proposal)
- [ ] After C approved: execute decomposition (6 file edits + graphify --update)
- [ ] After D approved: execute sub-cluster cross-references (5 file edits + graphify --update)
- [ ] Proposal E (no proposal needed): Add Related Skills to 5 orphan skill SKILL.md files — signup-flow-cro, site-architecture, customer-feedback, landing-page-optimization, sales-automation
- [ ] Create `references/google-ads-implementation.md` stub in analytics-tracking (carried from prior session)
- [ ] Run `graphify --update tmp_marketingskills` after all edits complete
