---
date: 2026-04-21
session: Proposals C, D, E — Full Execution
implements: [[analytics-tracking-decomposition]], [[community-subcluster-proposal]]
references: [[2026-04-21_Tier2_Proposals_CD]]
---

# 2026-04-21 — Proposals C, D, E Execution

## What Was Done

Executed all three approved graph restructuring proposals against `tmp_marketingskills`.

---

## Proposal C — analytics-tracking God Node Decomposition

Modifies: [[analytics-tracking]], creates [[analytics-strategy]], [[ga4-setup]], [[gtm-setup]], [[google-ads-tracking]]

**Router rewrite** (`skills/analytics-tracking/SKILL.md` → v2.0.0):
- Stripped all implementation content; kept identical trigger description for backward compatibility
- Added routing table with file-path links to 4 child skills

**New child skills created:**

| Skill | Key Content |
|-------|-------------|
| `analytics-strategy/SKILL.md` | Platform-agnostic tracking plan, event taxonomy, naming conventions |
| `ga4-setup/SKILL.md` | GA4 property setup, custom events, conversions |
| `gtm-setup/SKILL.md` | GTM container, data layer pushes, UTM parameter strategy |
| `google-ads-tracking/SKILL.md` | Paid conversion tags, gclid, GA4 import vs direct tag |

**Reference file created** (IDE hook triggered broken-link warning):
- `skills/google-ads-tracking/references/google-ads-implementation.md` — conversion tag snippet, GA4 import steps, attribution windows, remarketing tag

**Expected graph effect**: analytics-tracking hub drops from 20 edges to ~4 (one per child). Each child skill becomes its own node, distributing the hub load.

---

## Proposal D — Community Sub-Cluster Densification

Modifies: [[revops]], [[sales-enablement]], [[ab-test-setup]], [[page-cro]]

Converted bold-name inferred edges to explicit `[text](path)` extracted edges in Related Skills sections. Also added triangulating cross-references between RevOps reference docs.

**revops/SKILL.md**: Added inter-reference links between `scoring-models.md ↔ routing-rules.md ↔ lifecycle-definitions.md ↔ automation-playbooks.md`

**sales-enablement/SKILL.md**: Added file-path links for `revops`, `customer-research`, `analytics-tracking`

**ab-test-setup/SKILL.md**: Added file-path links for `page-cro`, `analytics-tracking`, `signup-flow-cro`, `form-cro`

**page-cro/SKILL.md**: Added file-path links for `signup-flow-cro`, `form-cro`, `ab-test-setup`, `landing-page-optimization`; added `## Related Concepts` section back-linking to ICE Prioritization and Hypothesis Framework in ab-test-setup

**Expected graph effect**: Community 0 (RevOps/cohesion 0.04) and Community 1 (Tool Integration APIs/cohesion 0.06) gain intra-community extracted edges, raising cohesion scores.

---

## Proposal E — Orphan Skill Integration

Connects: [[signup-flow-cro]], [[site-architecture]], [[customer-feedback]], [[landing-page-optimization]], [[sales-automation]]

All 5 were isolated singleton communities.

**Files edited (added inbound extracted edges):**
- `signup-flow-cro/SKILL.md` — converted all bold-name links to file paths; added `analytics-tracking` and `landing-page-optimization`
- `content-strategy/SKILL.md` — converted `**site-architecture**` to file-path link
- `seo-audit/SKILL.md` — converted `**site-architecture**` to file-path link

**New stub SKILL.md files created (3 orphans had no files):**

| File | Trigger Phrases | Key Links |
|------|----------------|-----------|
| `customer-feedback/SKILL.md` | NPS, CSAT, review analysis, G2 reviews, exit survey | g2.md, trustpilot.md, typeform.md integrations; links to customer-research, churn-prevention, revops, onboarding-cro |
| `landing-page-optimization/SKILL.md` | landing page, PPC landing page, message match | links to page-cro, signup-flow-cro, ab-test-setup, paid-ads, copywriting, analytics-tracking |
| `sales-automation/SKILL.md` | automate sales process, CRM automation, sales sequences | links to revops/references/routing-rules.md, revops/references/automation-playbooks.md; related: revops, email-sequence, analytics-tracking, cold-email |

**Expected graph effect**: 5 singleton communities collapse into surrounding communities via new extracted edges.

---

## Files Touched

**Created (7):**
- `skills/analytics-strategy/SKILL.md`
- `skills/ga4-setup/SKILL.md`
- `skills/gtm-setup/SKILL.md`
- `skills/google-ads-tracking/SKILL.md`
- `skills/google-ads-tracking/references/google-ads-implementation.md`
- `skills/customer-feedback/SKILL.md`
- `skills/landing-page-optimization/SKILL.md`
- `skills/sales-automation/SKILL.md`

**Modified (6):**
- `skills/analytics-tracking/SKILL.md` (router rewrite)
- `skills/revops/SKILL.md` (inter-reference cross-links)
- `skills/sales-enablement/SKILL.md` (expanded Related Skills)
- `skills/ab-test-setup/SKILL.md` (file-path links)
- `skills/page-cro/SKILL.md` (file-path links + Related Concepts)
- `skills/signup-flow-cro/SKILL.md` (converted bold → file-path links)
- `skills/content-strategy/SKILL.md` (site-architecture file-path link)
- `skills/seo-audit/SKILL.md` (site-architecture file-path link)

---

## Open Items

- [ ] Run `graphify --update tmp_marketingskills` to regenerate graph and validate community cohesion improvements
- [ ] Verify analytics-tracking hub degree drops; check if 4 child skills form a new sub-cluster
- [ ] Check if site-architecture, customer-feedback, landing-page-optimization, sales-automation leave singleton status
