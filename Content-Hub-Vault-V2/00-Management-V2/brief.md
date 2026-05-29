---
status: Active
type: system_config
date: 2026-05-28
description: "Per-run rulebook for content pipeline (Opportunity 3 of Self-Improvement Loop). Skills read constraints from frontmatter before execution; CLI flags override."
tags: [brief, pipeline-config, prompt-optimization, self-improvement-loop]
---

# Brief — Per-Run Instruction File

This is the per-night rulebook for the [[Local_First_Skill_Engine_Plan|content production pipeline]]. Edit the frontmatter below before each run; the pipeline will read these constraints and shape all 8 skills around them.

Implements [[The-Self-Improvement-Loop]] § 3.4 (Karpathy's `program.md` pattern).

---

## Frontmatter Template

```yaml
tone: "conversational, direct, no filler"
audience: "software developers and technical creators"
banned_phrases:
  - "in today's video"
  - "let's dive in"
  - "without further ado"
  - "in this post"
target_length_minutes: 10
must_include: []
must_avoid: []
optimize_for: "scroll_stop"
```

## How Skills Use This File

When you run `/researcher`, `/ideation`, `/hook`, etc., each skill:
1. Loads this file's frontmatter (YAML above)
2. Reads any CLI flag overrides you passed (e.g., `--tone "deadpan"`)
3. CLI flags override brief.md values if both are present
4. Keys are injected into the prompt template where matching placeholders exist

## Frontmatter Fields

- **tone** — How should the creator's voice sound? (e.g., "sarcastic and irreverent", "pragmatic and grounded", "hype-free and direct")
- **audience** — Who is this for? (e.g., "enterprise AI engineers", "indie hackers building side projects")
- **banned_phrases** — List of exact phrases the voice cleanup should flag and rewrite. Case-sensitive.
- **target_length_minutes** — Target video length (informational only; not enforced, but /outline uses this hint)
- **must_include** — List of required topics/keywords (informational)
- **must_avoid** — List of forbidden topics/keywords (informational)
- **optimize_for** — What should `/prompt-lab` prioritize? (e.g., "scroll_stop", "retention", "watch_time")

## Example: Hook-Focused Run

If you're optimizing hook prompts one night, you might set:

```yaml
tone: "provocative, contrarian"
audience: "cynical founders and CTOs"
banned_phrases:
  - "hey guys"
  - "let's dive in"
  - "in this video"
optimize_for: "scroll_stop"
```

Then run:
```bash
python -m skills.hook "My AI agents framework" --audience "cynical founders and CTOs" --tone "provocative, contrarian"
```

The hook skill loads this brief, applies your CLI overrides, and generates 5 hooks shaped by all of it.

## Example: Full-Pipeline Run

For an end-to-end run, you'd fill in all the fields:

```yaml
tone: "stream-of-consciousness, pragmatic"
audience: "senior engineers tired of hype"
banned_phrases:
  - "game-changer"
  - "leverage"
  - "synergy"
target_length_minutes: 12
must_include:
  - "local-first development"
  - "cost comparison"
must_avoid:
  - "magic" (too vague)
  - "AI will do your job"
optimize_for: "retention"
```

Then the full pipeline uses these constraints across researcher → ideation → hook → outline → title → cascade → short_form → voice_cleanup.

---

## Customize This File Before Each Run

The values above are placeholders. Overwrite the frontmatter with your actual preferences, then run the skills. The file is version-controlled — you can see what constraints each night used by looking at git history.
