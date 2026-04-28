---
status: Proposed
date: 2026-04-21
type: proposal
---

# Proposal D — Community Sub-cluster Proposal

References: [[tmp_marketingskills Knowledge Graph]], [[RevOps and Lead Lifecycle Community]], [[Tool Integration APIs Community]]

## Problem

Two large communities have critically low cohesion scores, meaning the graph algorithm dumped unrelated nodes into them by proximity rather than true relatedness:

| Community | Nodes | Cohesion | Issue |
|-----------|-------|----------|-------|
| Community 0 — RevOps and Lead Lifecycle | 51 | 0.04 | Grab-bag: lead management, sales tools, objection handling, REST API all in one cluster |
| Community 1 — Tool Integration APIs | 42 | 0.06 | Grab-bag: API auth patterns and CRO frameworks in the same cluster |

Cohesion below 0.10 means the community name is misleading — navigation breaks down.

## Proposed Sub-clusters

### Community 0 — RevOps and Lead Lifecycle → 3 sub-clusters

The 51 nodes appear to span three distinct domains. Target sub-clusters:

**Sub-cluster 0A — Lead Intelligence**
Concept: scoring and routing leads before they reach sales
Target nodes: Lead Scoring System, MQL Definition, Lead Routing Rules, Lead Lifecycle Framework, Intent Scoring, Visitor Identification, RB2B
How to create: Add explicit cross-references between `revops/SKILL.md` and any reference docs covering lead scoring/MQL. The tighter reference set gives graphify a basis to split.

**Sub-cluster 0B — Sales Process & Enablement**
Concept: what happens once a lead is qualified — objection handling, demo scripts, ROI props
Target nodes: Objection Handling Framework, ROI Calculator and Value Props, Demo Scripts Reference, Discovery Call Pattern, Authority/Competitor/Price/Status Quo/Timing Objection Handling
How to create: `sales-enablement/SKILL.md` already exists — add `## Related Skills` cross-references to revops + the objection handling reference docs.

**Sub-cluster 0C — CRM & Revenue Tool Integrations**
Concept: the API/tool layer underneath RevOps (Salesforce, Close, Outreach, HubSpot)
Target nodes: REST API, OAuth 2.0 Authentication, CRM Management, platform_salesforce, close_api, outreach_api
How to create: Add a `## CRM Integrations` section to `revops/SKILL.md` with explicit links to the relevant integration docs. This pulls those API nodes closer to RevOps in the graph.

### Community 1 — Tool Integration APIs → 2 sub-clusters

**Sub-cluster 1A — API & MCP Integration Layer**
Concept: how tools connect (auth, API patterns, MCP wrappers)
Target nodes: API Integration, MCP Integration, OAuth Authentication, Basic Authentication, API Key Authentication, Bearer Token Authentication
How to create: These nodes likely already have mutual edges — they may split naturally once Community 0 CRM nodes are pulled away. No source-doc edits needed; re-run graphify after Community 0 changes.

**Sub-cluster 1B — CRO Analysis Framework**
Concept: the testing and optimization framework nodes — separate domain from API tooling
Target nodes: CRO Analysis Framework, CTA Placement and Hierarchy, Headline Effectiveness, Hypothesis Framework, ICE Prioritization Scoring, A/B Test Setup Skill references
How to create: `ab-test-setup/SKILL.md` and `page-cro/SKILL.md` — add explicit `## Related Concepts` or `## Related Skills` cross-references to the ICE, Hypothesis, and CTA reference docs. This creates direct edges that graphify can cluster.

## Implementation Approach

Sub-clustering is achieved by **adding explicit cross-reference links in source SKILL.md and reference files** — not by editing the graph directly. Graphify re-extracts edges on `--update`.

Each change is a `## Related Skills` or `## Related References` addition to an existing file. No new files needed.

## Execution Steps (after approval)

**Phase 1 — Community 0 splits:**
1. `revops/SKILL.md` — add `## CRM Integrations` section with links to Salesforce, Close, Outreach integration docs
2. `sales-enablement/SKILL.md` — add `## Related Skills` pointing to `revops`, `cold-email`, and objection-handling reference docs
3. Verify cross-references are explicit (not just names, but `[text](path)` links that graphify can extract)

**Phase 2 — Community 1 splits:**
4. `ab-test-setup/SKILL.md` — add `## Related Concepts` linking to ICE Prioritization reference and Hypothesis Framework reference
5. `page-cro/SKILL.md` — add `## Related Concepts` linking to CTA Placement and Headline Effectiveness reference docs

**Phase 3 — Validate:**
6. Run `graphify --update tmp_marketingskills`
7. Check GRAPH_REPORT: Community 0 should split into 2–3 clusters, Community 1 cohesion should rise above 0.10

**Estimated impact**: ~5 file edits (existing SKILL.md files only), all additive changes.

## Risks

| Risk | Mitigation |
|------|-----------|
| Adding links doesn't move nodes if reference docs don't exist | Verify each target reference doc exists before adding the link |
| Sub-clusters form but with wrong names | Graphify names communities from node labels — rename is cosmetic, not a risk to structure |
| Cohesion doesn't improve after one update | May need 2 rounds — add more cross-refs if first update doesn't sub-cluster |
