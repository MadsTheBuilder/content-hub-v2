---
date: 2026-05-08
type: session
tags: [verification, research-guardrails, researcher-skill]
---

# Guardrails Verification Run — 2026-05-08

Implements: [[Research Guardrails]]  
References: [[2026-05-08_Phase3a_3b_Hook_Outline_Skills]]  
Modifies: [[researcher.py]]

---

## Score Card — 4/5 Guardrails Passed

| # | Criterion | Result | Notes |
|---|---|---|---|
| 1 | Primary sources | PASS | `primary_sources_found: 1` ≥ 1 |
| 2 | No duplicate questions | PASS | No duplicate `## ` headings in brief |
| 3 | Follow-up drilling | PASS | N/A — researcher uses single chat.ask per repo |
| 4 | Competitive Landscape | **FAIL** | `### Competitive Landscape` section absent |
| 5 | Angle battery | PASS | All 3 sub-answers non-empty |

---

## Test Run Details

- Command: `python -m skills.researcher --niche "TypeScript" --repos nexu-io/open-design --mode fast`
- Note: Handoff specified `mattpocock/skills` but that slug was not in the trends file. Substituted `nexu-io/open-design` (TypeScript, present in trends). Guardrail logic is repo-agnostic so the substitution is valid for verification purposes.
- Brief output: `Content-Hub-Vault-V2/10-Research/2026-05-08_typescript_brief.md`

---

## Brief Frontmatter

```yaml
date: 2026-05-08
niche: TypeScript
repos_researched: 1
primary_sources_found: 1
notebook_ids: [76fef6c7-3d81-43fa-8db6-81084060258a]
```

---

## Guardrail 4 Failure — Root Cause

The `### Competitive Landscape` section is defined in `prompts/researcher.md` as part of the output template that the main `chat.ask(nb.id, prompt_text)` call is supposed to produce. That call returned an empty answer silently — `result.answer` was `""` or `None` — so nothing was written for the `finding` slot in the compiled brief.

Evidence: the brief has no content between `### Discovered Sources` and `## Content Angle Battery`. The 4 "No answer extracted from response (6 lines parsed)" warnings in the log fired during pre-pipeline session init, but the same failure mode likely recurred on the main query.

**Why this is a silent failure:** `client.chat.ask` returns an object with `.answer`. The code does not check if `.answer` is empty before writing it to the brief. No exception is raised, no retry is attempted, and no `[no answer]` sentinel is written.

---

## Recommended Fixes

### Fix 1 — Guard empty answers in `research_one` (critical)

In `skills/researcher.py`, after:
```python
result = await client.chat.ask(nb.id, prompt_text)
```
Add a retry and a fallback sentinel:
```python
if not result.answer:
    # retry once
    await asyncio.sleep(10)
    result = await client.chat.ask(nb.id, prompt_text)
if not result.answer:
    result = SimpleNamespace(answer="[no answer — main query failed]")
```
This ensures Guardrail 4 has a visible failure marker rather than silent blank output.

### Fix 2 — Guardrail 4 scoring should treat `[no answer]` as FAIL (not invisible)

The scoring criterion checks for presence of `### Competitive Landscape`. Even if the sentinel is written, the guardrail would still fail — which is correct behavior. No change to scoring logic needed.

### Fix 3 — Trends file slug matching for `--repos`

The handoff assumed `mattpocock/skills` would resolve against the trends file. The `--repos` filter only matches slugs present in the file. Either:
- Document that `--repos` requires the repo to be in the trends file, OR
- Add a bypass mode: if `--repos` is set and the slug is not in the trends file, add the GitHub URL directly rather than erroring.

---

## Files Touched

- `Content-Hub-Vault-V2/10-Research/2026-05-08_typescript_brief.md` (generated)
- `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-08_Guardrails_Verification.md` (this file)
