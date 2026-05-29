---
name: pipeline-harness
description: Manual eval harness for validating the 8-step interactive content pipeline — blocking gates, routing order, and step number consistency
---

# Interactive Pipeline — Manual Eval Harness

Run these checks after any change to:

- `.claude/skills/researcher/SKILL.md`
- `.claude/skills/ideation/SKILL.md`
- `.claude/skills/hook/SKILL.md`
- `.claude/skills/outline/SKILL.md`
- `.claude/skills/title/SKILL.md`
- `.claude/skills/cascade/SKILL.md`
- `.claude/skills/short-form/SKILL.md`
- `.claude/skills/voice-cleanup/SKILL.md`

## What this harness tests

1. **Routing correctness** — `/researcher` hands off to `/ideation`, not `/hook`
2. **Ideation blocking gate** — Claude asks for idea selection BEFORE suggesting `/hook`
3. **Hook blocking gate** — Claude shows all 5 Spoken Lines then asks for hook selection BEFORE suggesting `/outline`
4. **Hook → Outline handoff** — chosen hook number propagates into the `/outline` command
5. **Step number consistency** — all skills report the correct step N of 8

Each run uses a fresh Claude Code session. Start each run with no prior conversation context.

---

## Preconditions

- At least one `.md` file exists in `Content-Hub-Vault-V2/10-Research/` (needed for Run B). If none exists, skip Run B.
- Working tree does not need to be clean — this harness does not modify production files.

---

## Run A: Researcher routes to ideation (not hook)

Purpose: verify the pipeline entry point hands off correctly.

| # | Step | Pass criteria |
|---|------|---------------|
| A1 | Fresh session. Type: `/researcher` | Claude asks for a niche or lists repos — does NOT immediately run anything. |
| A2 | Reply with any niche, e.g. `AI agents`. At the "confirm?" prompt, reply `no` (we just need to see the "After Completion" suggestion — skip actual execution). | Claude's response includes a suggestion to run `/ideation` as the next step. |
| A3 | Check Claude's suggestion. | **PASS**: Claude says something like "Next step: `/ideation AI agents`". **FAIL**: Claude suggests `/hook` or `/outline` as next step. |

---

## Run B: Ideation blocking gate fires before /hook suggestion

Purpose: verify Claude withholds the `/hook` suggestion until the user picks an idea.

Precondition: at least one file exists in `Content-Hub-Vault-V2/10-Research/`.

| # | Step | Pass criteria |
|---|------|---------------|
| B1 | Fresh session. Type: `/ideation AI agents` | Claude finds a research file and asks for confirmation. |
| B2 | Reply `yes` to confirm. Wait for the 9 ideas to appear. | 9 ideas are displayed, numbered 1–9. |
| B3 | Observe Claude's response immediately after showing the 9 ideas — **do not reply yet**. | **PASS**: Claude asks "Which idea do you want to pursue? Reply with a number (1–9)." and does NOT yet show a `/hook` command. **FAIL**: Claude suggests running `/hook` before you reply. |
| B4 | Reply `3`. | Claude confirms: "Got it — going with idea #3: [title]. Next step: `/hook topic=\"...\"`" with the exact idea title. **FAIL**: Claude asks another clarifying question instead of confirming and giving the `/hook` command. |

---

## Run C: Hook blocking gate — shows all 5 lines, blocks before /outline

Purpose: verify the 5-hook display and blocking behavior.

| # | Step | Pass criteria |
|---|------|---------------|
| C1 | Fresh session. Type: `/hook "Why your AI content gets zero traction"` | Claude confirms the topic and flags it will run. |
| C2 | Wait for hooks to complete. If Python execution is available, allow it to finish. If not, tell Claude: "The hooks are done. Please show the results." | Claude displays a numbered list of 5 hook Spoken Lines (1–5), with one marked ⭐. |
| C3 | Count the items in the list. | **PASS**: Exactly 5 items, each labelled with a number. **FAIL**: Claude summarises the hooks without numbering all 5 Spoken Lines. |
| C4 | Observe Claude's next message — **do not reply yet**. | **PASS**: Claude asks "Which hook do you prefer? Reply with a number (1–5)." and does NOT include an `/outline` command. **FAIL**: Claude suggests `/outline` before waiting for your answer. |
| C5 | Reply `2`. | Claude confirms: "Using hook #2. Next step: `/outline topic=\"Why your AI content gets zero traction\" --hook-path \"[path]\"`" — including the actual vault path to the hooks file. **FAIL**: Claude gives `/outline` without the `--hook-path` flag. |

---

## Run D: Outline receives the chosen hook number

Purpose: verify the hook selection propagates — outline does not silently default to ⭐ when the user picked a different one.

Precondition: run after Run C succeeds (a hook file must exist for the topic).

| # | Step | Pass criteria |
|---|------|---------------|
| D1 | Fresh session. Type: `/outline "Why your AI content gets zero traction"` — without specifying a hook path. | Claude scans `Content-Hub-Vault-V2/05-Hooks/` for the most recent matching file. |
| D2 | Claude finds the file. Observe its confirmation message. | **PASS**: Claude says something like "Using the ⭐ recommended hook from [filename]. Say the hook number if you want a different one." **FAIL**: Claude proceeds without mentioning the hook it's using. |
| D3 | Reply: `use hook 2`. | Claude acknowledges "Using hook #2" and updates the outline command to reference hook 2's section — not the ⭐ default. |

---

## Run E: Step number and pipeline string consistency

Purpose: verify all 8 SKILL.md files report the correct step number and include "ideation" in the pipeline string.

This run is a static check — no session needed. Open each file and scan visually.

| Skill | Expected step | Check |
|-------|--------------|-------|
| `.claude/skills/researcher/SKILL.md` | Step 1 of 8 | [ ] |
| `.claude/skills/ideation/SKILL.md` | Step 2 of 8 | [ ] |
| `.claude/skills/hook/SKILL.md` | Step 3 of 8 | [ ] |
| `.claude/skills/outline/SKILL.md` | Step 4 of 8 | [ ] |
| `.claude/skills/title/SKILL.md` | Step 5 of 8 | [ ] |
| `.claude/skills/cascade/SKILL.md` | Step 6 of 8 | [ ] |
| `.claude/skills/short-form/SKILL.md` | Step 7 of 8 | [ ] |
| `.claude/skills/voice-cleanup/SKILL.md` | Step 8 of 8 | [ ] |

For each file, also verify the pipeline string contains `ideation`:

```
researcher → ideation → hook → outline → title → cascade → short-form → voice-cleanup
```

**PASS**: All 8 steps present in every pipeline string.  
**FAIL**: Any file says "Step N of 7" or its pipeline string skips ideation.

---

## Result log (scratch — do not commit)

```
Run A:  [ ]  Date: ____  Notes:
Run B:  [ ]  Date: ____  Notes:
Run C:  [ ]  Date: ____  Notes:
Run D:  [ ]  Date: ____  Notes:
Run E:  [ ]  Date: ____  Notes:
```

Any failed run = diagnose root cause in the relevant SKILL.md, fix, re-run the full harness. The pipeline is not regression-safe until all five runs pass in one sitting.
