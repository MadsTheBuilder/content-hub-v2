# Graph Report - tmp_marketingskills  (2026-04-22)

## Corpus Check
- 251 files · ~99,999 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 887 nodes · 1147 edges · 0 communities detected
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 80 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## God Nodes (most connected - your core abstractions)
1. `Skill: Analytics Tracking` - 36 edges
2. `Email Sequence Design` - 29 edges
3. `API Integration` - 22 edges
4. `Skill: Content Strategy` - 21 edges
5. `Skill: Referral Program` - 20 edges
6. `Sales Enablement Skill` - 18 edges
7. `Skill: A/B Test Setup` - 17 edges
8. `SEO Audit Skill` - 17 edges
9. `Skill: Revenue Operations` - 16 edges
10. `CLI Integration` - 16 edges

## Surprising Connections (you probably didn't know these)
- `api() (dataforseo_api)` --conceptually_related_to--> `Integration Category: SEO Tools (integration_category_seo)`  [EXTRACTED]
  tmp_marketingskills\tools\clis\dataforseo.js → tmp_marketingskills/tools/integrations/ahrefs.md
- `api() (zoominfo_api)` --references--> `Contact Search (zoominfo_contact_search)`  [EXTRACTED]
  tmp_marketingskills\tools\clis\zoominfo.js → tmp_marketingskills/tools/integrations/zoominfo.md
- `api() (zoominfo_api)` --references--> `Company Search (zoominfo_company_search)`  [EXTRACTED]
  tmp_marketingskills\tools\clis\zoominfo.js → tmp_marketingskills/tools/integrations/zoominfo.md
- `api() (zoominfo_api)` --references--> `Company Enrichment (zoominfo_company_enrichment)`  [EXTRACTED]
  tmp_marketingskills\tools\clis\zoominfo.js → tmp_marketingskills/tools/integrations/zoominfo.md
- `api() (zoominfo_api)` --references--> `Scoops Lookup (zoominfo_scoops)`  [EXTRACTED]
  tmp_marketingskills\tools\clis\zoominfo.js → tmp_marketingskills/tools/integrations/zoominfo.md

## Communities

## Knowledge Gaps
- **283 isolated node(s):** `Marketing Skills Repository`, `Contributing Guidelines`, `Versions and Change History`, `Sample Size Guide`, `A/B Test Templates` (+278 more)
  These have ≤1 connection - possible missing edges or undocumented components.