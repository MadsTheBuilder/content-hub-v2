---
status: Proposed
date: 2026-04-21
type: proposal
---

# Proposal C — Analytics Tracking Decomposition

References: [[Analytics Tracking Skill]], [[tmp_marketingskills Knowledge Graph]]

## Problem

[[Analytics Tracking Skill]] is God Node #2 with 20 edges. It bridges 6 communities (Tool Integration APIs, SEO and Content Strategy, Referral and Affiliate Programs, Popup and Paywall CRO, Billing and Payment Auth, Product Analytics). This breadth means the skill is loaded for questions ranging from "how do I set up GA4" to "how do I track Google Ads conversions" — very different tasks that share a file.

Current SKILL.md has 7 distinct sections that map cleanly to separate concerns.

## Proposed Structure

Keep `analytics-tracking` as a **router skill** — same trigger description, reads context, then hands off. Create 4 child skills:

| Child Skill | Covers | Sections from Current SKILL.md |
|-------------|--------|-------------------------------|
| `analytics-strategy` | Platform-agnostic tracking plan design — event naming, event library, properties, privacy, debugging | Tracking Plan Framework, Event Naming Conventions, Essential Events, Event Properties, Privacy and Compliance, Debugging and Validation |
| `ga4-setup` | GA4 implementation — property setup, custom events, enhanced measurement, conversions | GA4 Implementation section |
| `gtm-setup` | Google Tag Manager — container structure, data layer pattern, UTM parameter strategy | Google Tag Manager section, UTM Parameter Strategy section |
| `google-ads-tracking` | Google Ads conversion tracking — GA4 import vs direct tag, remarketing audiences, auto-tagging | Google Ads Integration section |

## What Changes

**`analytics-tracking/SKILL.md`** — stripped to a router:
- Keep Initial Assessment (context check) and Core Principles
- Replace the 7 implementation sections with a "When to use which skill" routing table
- Keep Related Skills section + Tool Integrations table
- Keep the trigger description unchanged (users still say "set up analytics" → this skill routes them)

**New files created:**
- `skills/analytics-strategy/SKILL.md`
- `skills/ga4-setup/SKILL.md`
- `skills/gtm-setup/SKILL.md`
- `skills/google-ads-tracking/SKILL.md`

Each child SKILL.md:
- Gets its own frontmatter name + description (specific trigger)
- Contains the extracted sections from the parent
- Has a `Related Skills` block pointing back to `analytics-tracking` and siblings
- References the same `references/` docs (no reference file changes needed)

## What Does NOT Change

- All existing `references/` files stay where they are
- All other SKILL.md files that reference `analytics-tracking` in their Related Skills sections — they stay pointing to `analytics-tracking` (the router still exists)
- Trigger semantics — "set up analytics", "GA4", "GTM" etc. still route through `analytics-tracking` first

## Graph Impact

After `graphify --update`:
- `Analytics Tracking Skill` node keeps its 20 edges (router still referenced)
- 4 new nodes appear with their own targeted edges
- Community 1 (Tool Integration APIs) and Community 2 (Auth and Analytics Integration) gain tighter internal edges → better cohesion scores

## Risks

| Risk | Mitigation |
|------|-----------|
| Router becomes confusing — user gets routing table instead of help | Router should answer "which skill?" + call the right child immediately, not stop at routing |
| Child skills lose context from Core Principles | Copy shared principles into each child's preamble (short — 4 bullet points) |
| 4 new SKILL.md files = 4× maintenance surface | The sections are already written; this is a move, not a rewrite |

## Execution Steps (after approval)

1. Write `skills/analytics-strategy/SKILL.md`
2. Write `skills/ga4-setup/SKILL.md`
3. Write `skills/gtm-setup/SKILL.md`
4. Write `skills/google-ads-tracking/SKILL.md`
5. Rewrite `skills/analytics-tracking/SKILL.md` as router
6. Run `graphify --update tmp_marketingskills` → verify 4 new nodes, check cohesion

**Estimated impact**: ~6 file edits, no reference file changes, no other SKILL.md changes.
