---
created: 2026-05-13
status: Proposed
owner: Madhu
related:
  - "[[researcher-pipeline-comparison]]"
  - "[[2026-05-13_Researcher_Source_Verification_Agent]]"
  - "[[2026-05-08_Researcher_Fix_Verified]]"
---

# Researcher Optimisation

Implements: [[Enhanced Researcher Pipeline]] — the "deep documentation crawler" column from `docs/researcher-pipeline-comparison.html`.
References: [[2026-05-13_Researcher_Source_Verification_Agent]] (already-shipped semantic verification baseline).
Modifies: [[skills/researcher.py]], [[prompts/researcher.md]], [[.claude/skills/researcher/SKILL.md]].

---

## Context

Today's researcher (`skills/researcher.py`, 439 lines) ships the "After" pipeline — semantic Haiku verification with `source_ids=` filtering is live at [skills/researcher.py:184-263](skills/researcher.py#L184-L263). Two real problems remain:

1. **Shallow sources.** Primary source is only the raw README. The LLM answers from marketing copy, not from how the thing actually works. We want a panoramic view of the repo — `/docs`, guides, architecture, examples, tutorials.
2. **Unreadable brief.** Today's brief at [researcher.py:353-400](skills/researcher.py#L353-L400) is a question→answer dump. Reader extracts only 20–30% of the info. Format is flat and lacks narrative.

Scale: 1–5 repos per run, mostly single-repo — we can spend extra time/API budget per repo on quality.

---

## Feasibility — facts only

**Already in place (reusable):**
- All NotebookLM APIs needed exist in `notebooklm-py/`: `sources.add_url`, `sources.add_text`, `sources.list`, `sources.get_guide`, `chat.configure(custom_prompt=)`, `chat.ask(source_ids=)`, `artifacts.generate_slide_deck(instructions=)`, `artifacts.generate_infographic(instructions=)`.
- Anthropic async client + Haiku 4.5 tool-use pattern at [skills/researcher.py:210-262](skills/researcher.py#L210-L262).
- GitHub auth header pattern at [github_trending.py:35-43](github_trending.py#L35-L43) reading `GITHUB_TOKEN`.
- `beautifulsoup4`, `httpx`, `requests`, `anthropic`, `notebooklm-py` all installed.

**Must be built:**
- GitHub Contents API tree-walker for `/docs`, `/documentation`, `examples/`.
- Context-extraction Haiku call (mines primary docs into structured use-cases / concepts / patterns / anti-patterns).
- Brief synthesizer Haiku/Sonnet call that converts raw Q&A into the 5-section format.
- Slide deck + infographic generation calls — currently not invoked anywhere.

**Constraints (factual):**
- GitHub REST: 60 req/hr unauthenticated, 5000/hr with token. At 1–5 repos × ~10 calls, safe even unauthenticated.
- NotebookLM source-per-notebook ceiling: not documented in local client code. Plan caps total notebook sources at ~14 (6 primary + ≤8 discovered) — within range the current code already exercises.
- Indexing sleep is 75s for ≤12 sources. May need bump to ~90–120s for ~14 sources. **Verify empirically.**
- Cost: existing pipeline ≈ 1 Haiku call/repo. New: + 1 context extraction + 1 brief synthesis = 3 Haiku calls/repo, each ~$0.001.

---

## Files to be modified

| File | Change |
|------|--------|
| [skills/researcher.py](skills/researcher.py) | All new orchestration |
| `skills/researcher_crawler.py` *(new)* | GitHub doc-tree discovery + raw fetch helpers |
| [prompts/researcher.md](prompts/researcher.md) | Add `{repo_context}` placeholder in anchor prompt |
| [.claude/skills/researcher/SKILL.md](.claude/skills/researcher/SKILL.md) | Document new pipeline + brief format contract |

---

## Phases & sub-phases

### Phase 1 — Deep documentation crawler
*Goal: replace README-only primary sources with a panoramic snapshot of the repo's docs.*

- [ ] **1.1** Create `skills/researcher_crawler.py` exporting `discover_primary_docs(owner_repo, token) -> list[DocCandidate]`
- [ ] **1.2** Implement GitHub Contents API probe for `docs/`, `docs/`, `examples/` (tolerate 404 per directory) — reuse `_gh_headers()` pattern from [github_trending.py:35-43](github_trending.py#L35-L43)
- [ ] **1.3** Implement priority ranker (confirmed order):
    1. README (existing)
    2. `docs/index.md`, `docs/README.md`, `docs/introduction.md`
    3. `docs/getting-started.md`, `docs/quickstart.md`, `docs/installation.md`, `docs/tutorial*.md`
    4. Root `CONTRIBUTING.md`, `ARCHITECTURE.md`, `DESIGN.md`
    5. Remaining `docs/*.md` (alphabetical)
    6. `examples/*.md` or `examples/README.md`
- [ ] **1.4** Raw fetch via `raw.githubusercontent.com` (mirror existing pattern at [researcher.py:146](skills/researcher.py#L146))
- [ ] **1.5** Hard cap at **6 primary docs** (configurable via `--max-primary-docs`, default 6)
- [ ] **1.6** Wire into `researcher.py` between current README step and web research — capture `primary_source_ids`
- [ ] **1.7** Smoke-test on a doc-rich repo (e.g. an established library with `/docs/`) and a doc-sparse repo (README-only) — both must succeed

### Phase 2 — Audit + improve Haiku verification
*Goal: harden the verification that already exists rather than replace it.*

- [ ] **2.1** Read current verify code at [researcher.py:184-263](skills/researcher.py#L184-L263) end-to-end
- [ ] **2.2** Audit: does the Haiku prompt explicitly call out "wrong entity sharing the name" as primary failure mode? If not, add `mercury-agent ≠ mercury chemistry` example
- [ ] **2.3** Audit: short/empty `get_guide()` summaries — currently dropped silently? Change to "treat as unknown, keep" with warning log
- [ ] **2.4** Audit: fallback on Haiku failure — currently keeps all silently. Add warning log
- [ ] **2.5** Extend tool schema to return `reasons: dict[source_id, str]` for transparency in brief's source appendix
- [ ] **2.6** Verify on `mercury-agent` and `terax-ai` cases — wrong-entity sources must be dropped with a logged reason

### Phase 3 — Context extraction & injection
*Goal: turn primary docs into a structured mental-model block the LLM sees before every question.*

- [ ] **3.1** Add helper `extract_repo_context(primary_source_summaries) -> RepoContext` in `researcher.py`
- [ ] **3.2** One Haiku tool-use call returning structured fields:
    - `core_use_cases: list[str]` (2–4)
    - `key_concepts: list[str]` (3–6)
    - `common_patterns: list[str]` (2–4)
    - `anti_patterns: list[str]` (1–3)
    - `audience: str`
- [ ] **3.3** Render `RepoContext` to markdown context block
- [ ] **3.4** Prepend context block to `custom_prompt` in `chat.configure()` at [researcher.py:268-277](skills/researcher.py#L268-L277)
- [ ] **3.5** Add `{repo_context}` placeholder near top of `prompts/researcher.md` anchor prompt
- [ ] **3.6** Spot-check one Q&A answer to confirm it references context concepts, not just README

### Phase 4 — Brief reformatter *(highest-impact phase for the reader)*
*Goal: replace the Q&A dump with a readable 5-section narrative brief.*

- [ ] **4.1** Collect 11 answers + `RepoContext` + verified sources into one structured payload
- [ ] **4.2** Synthesis call (start with Haiku; upgrade to Sonnet 4.6 if output reads flat) with strict 5-section schema:
    - `## What it does`
    - `## Who it's for`
    - `## How it works`
    - `## When to use`
    - `## Watch out for`
- [ ] **4.3** Each section: prose paragraphs, no question headers, no bullet salad. 2–4 short paragraphs each
- [ ] **4.4** Append `## Sources` (verified sources + one-line guide summaries)
- [ ] **4.5** Append `## Raw findings` inside a collapsed `<details>` block (preserves Q&A pairs for traceability, hidden by default in Obsidian)
- [ ] **4.6** Keep existing frontmatter (`date`, `niche`, `repos_researched`, `primary_sources_found`, `notebook_ids`) — downstream scripts and Obsidian links depend on it
- [ ] **4.7** Output path unchanged: `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md`
- [ ] **4.8** User reads cold and confirms the 5-section structure conveys understanding without expanding raw findings

### Phase 5 — Slides + infographics (HTML Step 10)
*Goal: research-driven artifacts, not generic templates. Independent of brief — failure here does not block the brief.*

- [ ] **5.1** Build artifact instruction string from `RepoContext` + synthesized brief
- [ ] **5.2** Call `client.artifacts.generate_slide_deck(notebook_id, instructions=...)`
- [ ] **5.3** Call `client.artifacts.generate_infographic(notebook_id, instructions=...)`
- [ ] **5.4** Poll via existing `wait_for_completion()` at `notebooklm-py/src/notebooklm/_artifacts.py:1782`
- [ ] **5.5** Log artifact URLs/IDs into brief frontmatter
- [ ] **5.6** Confirm artifacts reflect actual research (not generic templates) by opening in NotebookLM UI

---

## Verification (run after each phase, not just at the end)

| Phase | How to verify |
|-------|---------------|
| 1 | `python skills/researcher.py --repos kyegomez/OpenMythos --mode fast` → open notebook in NotebookLM UI → confirm 5–7 sources present |
| 2 | Run on `mercury-agent` + `terax-ai` → confirm wrong-entity sources are dropped with logged reasons |
| 3 | Print the rendered `custom_prompt` → confirm context block is well-formed → spot-check one answer references context concepts |
| 4 | Open brief in Obsidian → user reads cold → confirms 5-section format conveys understanding |
| 5 | Open generated artifacts in NotebookLM → confirm they reflect actual research, not defaults |

---

## Open items to confirm during execution

- **Indexing sleep length** at ~14 sources: start at 90s; poll `sources.list()` for `status == "ready"` and bump if needed. Don't hardcode 75s.
- **Synthesizer model choice** for Phase 4: Haiku is cheap, but the brief is the user-facing deliverable. If Haiku output is flat, switch to Sonnet 4.6. Cost negligible at 1–5 repos.
- **NotebookLM source ceiling**: if a source ever fails to add past N total, crawler cap drops to N − discovered_count − 2. Catch the error explicitly rather than retrying.
