---
status: complete
session_date: "2026-05-07"
closed: "2026-05-08"
sprint: "OpenMythos Dogfood Run"
topic: "kyegomez/OpenMythos"
description: "End-to-end validation of V2's content production engine on a real topic. Captures every friction point as it surfaces."
---

# OpenMythos Dogfood Run — Friction Log

## Run target

[kyegomez/OpenMythos](https://github.com/kyegomez/OpenMythos) — 11,100 stars, "theoretical reconstruction of the Claude Mythos architecture." Surfaced via [[github_trending]] (`Content-Hub-Vault-V2/04-Trends/github_trending.md`, line 20).

## Friction format

```
### Friction N — <skill>
What: <observation>
Bucket: glue | prompt | missing-skill | infra
Severity: blocker | rough | nice-to-have
```

Buckets:
- **glue** — chaining/handoff between skills, output discovery, file-path ergonomics
- **prompt** — output quality, voice match, craft adherence (edit `prompts/<skill>.md`)
- **missing-skill** — gap in V2's coverage; needs new skill
- **infra** — wiring, env, paths, dependencies

---

## Step 1 — `/yt-pipeline kyegomez/OpenMythos`

**Status:** Complete — research extracted, 4 friction points logged

**Output:** `Content-Hub-Vault-V2/10-Research/2026-05-07_openmythos/research.md`
**Notebook ID:** `4546d265-0860-451a-b904-055b39d25c51`

**Search query used:** "OpenMythos Claude Mythos architecture"

Search mode worked cleanly. 10 results returned in seconds. Mix of high-volume general AI commentary (Fireship, "Awesome") and direct topical breakdowns (mid-tier channels with 100–7K views).

### Search results

| #   | Views     | Title                                                                                   | Channel              |
| --- | --------- | --------------------------------------------------------------------------------------- | -------------------- |
| 1   | 1,059,081 | Claude Mythos is too dangerous for public consumption...                                | Fireship             |
| 2   | 97,044    | Claude Mythos Clone Shocks Anthropic and OpenAI                                         | AI Revolution        |
| 3   | 326       | OpenMythos Explained, The Open Source Claude Mythos Reconstruction                      | TechWealth Hub       |
| 4   | 7,409     | OpenMythos: Open-Source Reconstruction of Anthropic's Mythos                            | Prism Labs           |
| 5   | 412       | OpenMythos - open source Recurrent-Depth Transformer implementation of Anthropic Mythos | AgentOneIntelligence |
| 6   | 229       | OpenMythos: The Bold Theory Behind Claude Mythos                                        | FlashCore            |
| 7   | 874,344   | Claude just got another superpower...                                                   | Fireship             |
| 8   | 12,778    | A 22-Year-Old Just Leaked Anthropic's Biggest Secret (Claude Mythos EXPOSED)            | FutureSketchLab      |
| 9   | 134       | OpenMythos The Architecture of Iteration                                                | AI Application       |
| 10  | 75,549    | The Claude Mythos delusion...                                                           | Awesome              |

### Friction #1 — Search recall is shallow
What: User found 2 highly-relevant OpenMythos videos in 10 seconds of manual YouTube browsing that the `yt_pipeline.py search` query missed entirely:
- https://www.youtube.com/watch?v=60Z0yrrzLdA
- https://www.youtube.com/watch?v=4c9YUnaDxvA

The search likely leans on title-keyword match against a single query. Videos with high topical relevance but different framing words don't surface.

Bucket: prompt | infra (likely a search-strategy issue inside `skills/yt_pipeline.py` — single query vs. multi-query expansion, or relying on yt-dlp's default ranking).
Severity: rough — not a blocker for this run because user can paste URLs directly, but it means *trusting the search blindly will undercut research depth* on every run.

Watch for: NotebookLM ingest reliability when we run the pipeline, especially on the low-view niche videos (3, 9).

### Final URL set (5 videos)

User selection: **3, 4, 9** + 2 manually-added URLs:
1. https://www.youtube.com/watch?v=yGDIbVf-FxQ (TechWealth Hub — OpenMythos Explained)
2. https://www.youtube.com/watch?v=ahhwQ8DLud8 (Prism Labs — Open-Source Reconstruction)
3. https://www.youtube.com/watch?v=15-xELYInks (AI Application — Architecture of Iteration)
4. https://www.youtube.com/watch?v=60Z0yrrzLdA (user-added)
5. https://www.youtube.com/watch?v=4c9YUnaDxvA (user-added)

### Friction #2 — NotebookLM dev/installed version drift + expired session

What: First pipeline attempt failed with `AUTH_REQUIRED` pointing at the legacy path `~/.notebooklm/storage_state.json`, even though a valid `storage_state.json` existed at `~/.notebooklm/profiles/default/storage_state.json`. Two distinct problems compounded:

1. **Version drift.** The site-packages copy of `notebooklm` (v0.3.4) lacked profile-aware path resolution. The local dev tree at `notebooklm-py/` (also v0.3.4) had the profile support. Running `pip install -e ./notebooklm-py` replaced the installed copy with the dev tree — confirmed via `python -c "import notebooklm; print(notebooklm.__file__)"`.
2. **Expired Google session.** Once paths resolved correctly, `python -m notebooklm list` returned `Authentication expired or invalid. Redirected to: accounts.google.com/...`. The stored cookies are stale.

Bucket: infra
Severity: rough — solvable with `pip install -e` + interactive `notebooklm login`, but two failure modes were stacked behind one error message, which made the first failure misleading.

Root-cause notes for the post-run brainstorm:
- Local dev version of `notebooklm-py` is not pinned/installed by any setup script. Anyone refreshing skills or pulling latest can end up with the older site-packages build silently shadowing the dev tree.
- `AUTH_REQUIRED` in the older build only printed the legacy path with no hint that profiles existed. A user without the dev tree open would have no path to diagnose this.
- Session expiry needs an interactive Playwright login; no current way to detect this proactively before kicking off the pipeline.

Workaround applied: `pip install -e notebooklm-py` then user runs `notebooklm login` to refresh session.

### Friction #3 — Q&A structure collapsed into one fused block

What: The pipeline sends all 8 analysis questions as a single prompt to NotebookLM. NotebookLM returned one combined narrative overview instead of answering Q1–Q8 separately. The output file has 8 empty question headers followed by one unstructured block. This breaks downstream skills that expect structured per-question answers (ideation needs "Content Gaps", cascade needs "Strongest Quotes", etc.).

NotebookLM also returned the message "It appears your query was not included in your message" before its fused answer — suggesting the question framing may be confusing the API.

Bucket: prompt | glue
Severity: rough — the fused block still contains useful research (core architecture, controversy, verdict), but the structured format is lost. Ideation can still run by reading the fused block, but the system can't reliably pull specific sections.

Fix direction: Send questions one at a time (sequential `ask` calls), writing each answer under its respective header. Or restructure as numbered questions with explicit `Answer Q1:` prefix instructions.

Output written: `Content-Hub-Vault-V2/10-Research/2026-05-07_openmythos/research.md`
Notebook ID: `4546d265-0860-451a-b904-055b39d25c51`

### Friction #4 — Artifact generation: slide-deck timeout + Windows encoding crash

What: After research extraction, the pipeline attempts to generate a slide-deck and report artifact from NotebookLM. Two failures:
1. **slide-deck timed out** after 300s (task `ee3327c3...` stuck in `in_progress`). Artifact generation is NotebookLM-side and slow — no retry or skip logic.
2. **report download crashed** with `UnicodeEncodeError: 'charmap' codec can't encode character '→'` at `skills/yt_pipeline.py:110`. The `→` arrow in the print statement can't render on Windows CP1252 console.

Bucket: infra (encoding), infra (timeout)
Severity: rough for encoding (trivial fix applied: replaced `→` with `->`); rough for timeout (needs configurable timeout or async polling).

Fix applied: Changed `→` to `->` in `yt_pipeline.py:110`. Artifact timeouts still open.

### Key research findings (from fused NotebookLM block)

- **Architecture:** Recurrent Depth Transformer — 3-stage (Prelude → Recurrent Block → KOD). Loops through layers rather than stacking more. Silent reasoning in latent space (no chain-of-thought tokens). MoE + MLA for efficiency.
- **The controversy:** Performance claim (770M matches 1.3B) was **lifted from the "Parse" paper** published 5 days before OpenMythos appeared — "credential laundering" allegation. No trained weights, no benchmarks, no reproductions. 21% of creator's own test suite fails on main branch including the core stability guarantee.
- **Verdict:** Credible architectural experiment, research playground. Not a production-ready model stack.
- **Author:** kyegomez (Kai Gomez) — prolific but controversial; accused of autogenerated repos and crypto involvement.

---

## Step 2 — `/ideation`

**Status:** Complete — 9 ideas generated, contamination issue logged. Chosen idea: **Rank 6**

**Output:** `Content-Hub-Vault-V2/02-Ideas/2026-05-07_openmythos.md`

### Friction #5 — Ideation auto-detects research file by flat-file scan, misses subdirectories

What: `skills/ideation.py` scans `Content-Hub-Vault-V2/10-Research/` for research files matching the topic. But the yt-pipeline stored the OpenMythos research in a **subdirectory** (`2026-05-07_openmythos/research.md`). The flat scan missed it and picked the most recent flat file instead (`2026-05-06_ruflo_skills_agents_architecture.md`). Result: ideas 2–4, 7–9 are contaminated with ruflo/MemPalace context that has nothing to do with OpenMythos.

Bucket: glue — handoff between yt-pipeline (writes to subdir) and ideation (scans flat) is broken
Severity: blocker — wrong research in = wrong ideas out; the output file is logged as using the wrong source

Fix directions:
1. Ideation scanner should walk subdirectories (glob `**/*.md` not `*.md`)
2. OR yt-pipeline should write research flat to `10-Research/` (no subdirectory)
3. OR yt-pipeline writes a symlink/index file at the flat path pointing into the subdir

Clean ideas (uncontaminated): **Rank 1, 5, 6** are solidly OpenMythos-only.

### Chosen idea: Rank 6

> **"What Anthropic Actually Published vs. What OpenMythos Claims to Reconstruct"**
> Line-by-line comparison: Anthropic's Constitutional AI paper, the model card, and the Claude Character Overview vs. OpenMythos's reconstruction — surfacing exactly where the reconstruction has evidence and where it's speculative.
> Hook: "Before you build anything on OpenMythos, you should know what Anthropic has actually confirmed about Claude's architecture — and what they haven't."
> Format: Long-form 12–15min

---

## Step 3 — `/hook "What Anthropic Actually Published vs. What OpenMythos Claims to Reconstruct"`

**Status:** Complete — 5 hooks generated, no friction. Hook 1 chosen.

**Output:** `Content-Hub-Vault-V2/05-Hooks/2026-05-07_what-anthropic-actually-published-vs-what.md`

### Hooks generated

| # | Pattern | Spoken Line |
|---|---|---|
| 1 ⭐ | Speed to Value | "Stop building on OpenMythos's reconstruction. I pulled the actual Anthropic paper — it's not the same thing." |
| 2 | Stated Contrast | "Most builders are working from OpenMythos's version. Here's what Anthropic's paper actually says." |
| 3 | Pain Point Agitation | "If your product is built on OpenMythos's reconstruction, you have a structural flaw — and it's not in your code." |
| 4 | Curiosity Loop | "Everyone's covering what OpenMythos reconstructed. Nobody's covering what they left out." |
| 5 | Edging Hook | "I thought OpenMythos's reconstruction was close enough. Then I checked the primary source." |

**Chosen: Hook 1** — Speed to Value. Topic clarity in the first two seconds blocks the "what is this about?" drop-off that kills first-30-second retention for technical audiences.

---

## Step 4 — `/outline --hook-path <hook>`

**Status:** Complete — 12-min Dopamine Ladder approved, no friction.

**Output:** `Content-Hub-Vault-V2/06-Outlines/2026-05-07_what-anthropic-actually-published-vs-what.md`

### Dopamine Ladder structure

| Stage | Time | Beat |
|---|---|---|
| 1 Stimulation | 0:00–0:30 | Hook 1 verbatim — split screen visual (OpenMythos clean vs. Anthropic paper annotated in red) |
| 2 Captivation | 0:30–2:00 | "40 pages published. 11 pages reconstructed." Viral spread + architecture diagram B-roll. |
| 3 Anticipation | 2:00–4:30 | **Head Fake 1**: gaps aren't in capability claims — they're in the constraint layer. ToC side-by-side visual. |
| 4 Validation | 4:30–9:30 | 5 gaps in order: memory governance → context boundary → retrieval degradation → token budget → corrigibility dial. **Head Fake 2** before Gap 5. |
| 5 Affection | 9:30–11:00 | "I used the reconstruction for 3 weeks. I told this audience it was flat memory. That was wrong." Talking head only. |
| 6 Revelation | 11:00–12:00 | Every viral AI breakdown is a reconstruction. The habit is checking one layer back. |
| CTA | 12:00–12:30 | Next video: how to read Anthropic's actual papers without an ML background. |

---

## Step 5 — `/title "What Anthropic Actually Published vs. What OpenMythos Claims to Reconstruct"`

**Status:** Complete — 10 titles generated, no friction. Title 9 chosen.

**Output:** `Content-Hub-Vault-V2/07-Titles/2026-05-07_what-anthropic-actually-published-vs-what-openmyth.md`

### Chosen: Title 9 (Tier-2)

> **"Is OpenMythos Legit? I Checked Every Claim Against Anthropic's Docs"**

Rationale: Title 9 openly asks the legitimacy question that the research surfaced — credential laundering, borrowed benchmarks, failing test suite. Stronger match for the video's actual angle than any Tier-1 safe option.

---

## Step 6 — `/cascade`

**Status:** Complete — architecture flaw found and fixed. Cascade re-run on research+outline.

**Initial run:** `python -m skills.cascade https://www.youtube.com/watch?v=ahhwQ8DLud8` (Prism Labs)
**Re-run:** `python -m skills.cascade --research-file ... --outline-file ...`

**Output (final):** `Content-Hub-Vault-V2/08-Distribution/2026-05-07_is-openmythos-legit-i-checked-every-clai/`

### Friction #6 — Cascade blindly repurposes source video, ignores our research and angle

What: Cascade was designed to extract a YouTube transcript and repurpose it into social posts. The Prism Labs video presents OpenMythos positively — so the generated Twitter thread was enthusiastic fan content. It took every architectural claim at face value, mentioned nothing about credential laundering, 21% test failures, or the "Parse" paper. Completely contradicted our research findings.

Root cause: cascade has no awareness of (a) our research files, (b) our outline, or (c) our chosen video angle. It treats the source video as ground truth. When our angle *contradicts* the source video, the cascade output is unusable.

Bucket: missing-skill | glue
Severity: blocker — cascade output actively misleads when our angle contradicts the source video

### Fix applied — cascade.py and short_form.py redesigned

Both `skills/cascade.py` and `skills/short_form.py` now support:
- `--research-file <path>` — load our research markdown
- `--outline-file <path>` — load our approved outline
- `youtube_url` argument made optional (`nargs="?"`)
- `raw_url` used for routing (None-safe); `youtube_url` assigned after branch decision
- Placeholder `[VIDEO_LINK]` used when no URL provided (valid in all output formats)
- YAML frontmatter quotes the URL field: `youtube_url: "[VIDEO_LINK]"` (prevents invalid YAML from unquoted brackets)
- README uses resolved `youtube_url` variable, not `args.youtube_url` (was `None` in research mode)
- Transcript truncation raised from 4,000 to 6,000 chars in both scripts

SKILL.md files updated to set **research+outline as the default mode** after `/outline` is approved. YouTube URL fallback documented separately.

Prompts updated (`prompts/cascade.md`, `prompts/short_form.md`) to say "source content" instead of "transcript" — framing is now mode-agnostic.

### Stop-hook sub-issues caught (Friction #6 sub-entries)

Three stop-hook review cycles caught additional bugs in the cascade fix:

**Sub-issue A** — `youtube_url or "[VIDEO_LINK]"` broke the no-input error path. `"[VIDEO_LINK]"` is truthy, so `elif youtube_url:` always fired and the `else: sys.exit(1)` branch became unreachable. The script would try to extract a transcript from the literal string `"[VIDEO_LINK]"`.
Fix: renamed to `raw_url = args.youtube_url` for routing; `youtube_url` only assigned inside branches after the decision.

**Sub-issue B** — `youtube_url: [VIDEO_LINK]` in YAML frontmatter is invalid YAML (unquoted brackets parsed as a sequence). `**Video:** {args.youtube_url}` in README was `None` (raw arg, not resolved value).
Fix: quoted the YAML value (`"{youtube_url}"`); used resolved `youtube_url` in README.

### Twitter hook (final, research+outline mode)

> "OpenMythos: The idea of a 770M parameter model matching a 1.3B giant with 'recurrent depth' is compelling. But digging into the claims reveals a deep controversy. Is it true innovation or 'credential laundering'? 🧵"

---

## Step 7 — `/short-form`

**Status:** Complete — 3 scripts generated from research+outline. Gemini 503 on one pass (auto-recovered via Ollama fallback).

**Output:** `Content-Hub-Vault-V2/09-Shorts/2026-05-08_is-openmythos-legit-i-checked-every-clai/`

Same `--research-file` / `--outline-file` fix applied to `short_form.py` before running (same root cause as Friction #6 — skill was YouTube-URL-only).

### 30s script hook

> "OpenMythos claims a 770 million parameter model performs like a 1.3 billion parameter giant. But there's a huge catch."

Text overlays: `OpenMythos: 770M vs 1.3B?` · `Recurrent Depth Architecture` · `Loops Same Layers` · `Copied Performance Claims` · `21% Test Suite Fails`

---

## Step 8 — `/voice-cleanup` pass

**Status:** Complete — 8 `_cleaned.md` files written (2026-05-08).

**Files cleaned:**

| File                                                                  | Provider                | Output                      |
| --------------------------------------------------------------------- | ----------------------- | --------------------------- |
| `05-Hooks/2026-05-07_what-anthropic-actually-published-vs-what.md`    | claude/cli              | `_cleaned.md`               |
| `06-Outlines/2026-05-07_what-anthropic-actually-published-vs-what.md` | claude/cli              | `_cleaned.md`               |
| `08-Distribution/.../blog_post.md`                                    | gemini/gemini-2.5-flash | `blog_post_cleaned.md`      |
| `08-Distribution/.../twitter_thread.md`                               | gemini/gemini-2.5-flash | `twitter_thread_cleaned.md` |
| `08-Distribution/.../linkedin_post.md`                                | claude/cli              | `linkedin_post_cleaned.md`  |
| `09-Shorts/.../30s_script.md`                                         | claude/cli              | `30s_script_cleaned.md`     |
| `09-Shorts/.../60s_script.md`                                         | claude/cli              | `60s_script_cleaned.md`     |
| `09-Shorts/.../90s_script.md`                                         | claude/cli              | `90s_script_cleaned.md`     |



**Observation:** Running all 8 in parallel caused 3 initial failures (outline, twitter, 30s) — Claude CLI collision + Gemini 503 simultaneously. Retried sequentially; all recovered within one retry. No data loss.

### 30s hook (cleaned)

> "OpenMythos claims a 770 million parameter model performs like a 1.3 billion parameter giant. But there's a huge catch."

### Blog hook (cleaned)

> "OpenMythos showed up as an open-source PyTorch project. It aimed to rebuild Anthropic's rumored Claude Mythos architecture. It suggested a new way to scale models: 'recurrent depth' instead of just adding layers. But is it real…"

### Twitter hook (cleaned)

> "OpenMythos says a 770M parameter model can match a 1.3B giant. It uses something called 'recurrent depth'. Sounds amazing, but when you look closely, there's a huge fight about it. Is this real innovation or just 'credential laundering'?"

---

## Code changes this session

| File | Change |
|---|---|
| `skills/yt_pipeline.py:110` | `→` → `->` (Windows CP1252 encoding fix) |
| `skills/cascade.py` | Full redesign: optional URL, `--research-file`, `--outline-file`, `raw_url` routing, `[VIDEO_LINK]` placeholder, quoted YAML, 6k char limit |
| `prompts/cascade.md` | "YouTube video transcript" → "source content" in all 3 prompt sections |
| `.claude/skills/cascade/SKILL.md` | Research+outline as default mode; YouTube URL documented as fallback |
| `skills/short_form.py` | Same redesign as cascade.py |
| `prompts/short_form.md` | Same framing update as cascade.md (all 3 script sections) |
| `.claude/skills/short-form/SKILL.md` | Research+outline as default mode; YouTube URL documented as fallback |

---

## Decisions made this session

| Decision | Value |
|---|---|
| Chosen idea | Rank 6 — "What Anthropic Actually Published vs. What OpenMythos Claims to Reconstruct" |
| Chosen hook | Hook 1 — Speed to Value / Rapid Context |
| Chosen title | Title 9 — "Is OpenMythos Legit? I Checked Every Claim Against Anthropic's Docs" |
| Outline approved | Yes — 12-min Dopamine Ladder, 6 stages, 2 head fakes, 5 gaps |
| Cascade source | Switched from YouTube URL to research+outline after Friction #6 |

---

## Brainstorm summary (post-run)

### Friction triage

| # | Friction | Bucket | Severity | Status |
|---|---|---|---|---|
| 1 | Search recall shallow (single query) | prompt / infra | rough | Open |
| 2 | notebooklm version drift + expired session | infra | rough | Open |
| 3 | Q&A structure collapses into fused block | prompt / glue | rough | Open |
| 4 | Slide-deck artifact timeout + Windows encoding | infra | rough | Encoding fixed; timeout open |
| 5 | Ideation flat-scan misses subdirectory research | glue | blocker | Open |
| 6 | Cascade / short-form YouTube-only design | missing-skill / glue | blocker | **Fixed this session** |

### Priority fixes for next session

1. **Friction #5 (blocker):** Fix ideation scanner to walk subdirectories (`glob **/*.md`). Single-line change in `skills/ideation.py`.
2. **Friction #3 (rough):** Send NotebookLM questions one at a time with sequential `ask` calls instead of one fused prompt. Will restore structured Q1–Q8 output.
3. **Friction #1 (rough):** Expand search to 2–3 query variants (e.g., topic name, author + topic, architecture description). More coverage without much extra complexity.
4. **Friction #2 (rough):** Add a `notebooklm ping` check at pipeline start that catches auth failures before the long source-add wait. Surface the dev vs. installed version mismatch in setup docs.
5. **Friction #4 / timeout (rough):** Add configurable artifact timeout + skip-on-timeout flag so a slow NotebookLM doesn't block the whole run.

### What went well

- Hook → Outline → Title chain was frictionless (Steps 3–5): zero blockers, clean outputs, good quality on first pass.
- The "legitimacy question" emerged organically from the research — the credential laundering finding sharpened the video angle without needing a separate research pass.
- AI cascade (Ollama → Gemini → Claude polish) recovered from a Gemini 503 without user intervention.
- The cascade/short-form fix (Friction #6) was caught and fixed within the same session — pipeline integrity restored before Step 8.

---

## Cross-references

Implements: [[Architecture_Building]] (OpenMythos Dogfood Run section)
References: [[voice_profile]] | [[marketing_brain]] | [[github_trending]]
Modifies: `skills/cascade.py` | `skills/short_form.py` | `prompts/cascade.md` | `prompts/short_form.md` | `.claude/skills/cascade/SKILL.md` | `.claude/skills/short-form/SKILL.md`
