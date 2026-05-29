---
name: voice-cleanup
description: >-
  Strip AI-isms, corporate language, and robotic phrasing from any skill output — rewrites content in the
  creator's authentic human voice using a detailed voice profile and banned-phrase list. Use this whenever
  the user types /voice-cleanup, says "de-AI this", "humanize this", "make this sound like me", "strip the
  AI language", "clean up the robot speak", or "voice cleanup". Also trigger automatically when the user
  just finished /short-form or /cascade and mentions the output sounds too formal, stiff, polished,
  corporate, or AI-generated — voice-cleanup is the mandatory final step before publishing anything.
  Supports single files, pasted text, and batch cleanup of an entire folder.
---

# /voice-cleanup

The final polish step in the content pipeline. Runs **after** `/short-form` or `/cascade` to strip AI-isms
and rewrite outputs in the creator's authentic voice. Uses Claude-first routing (`polish()` — premium model)
and the banned-phrase / positive-marker patterns embedded in `prompts/voice_cleanup.md`.

## Pipeline Position

```
/researcher → /ideation → /hook → /outline → /title → /short-form → [/voice-cleanup] → publish
/researcher → /ideation → /hook → /outline → /title → /cascade    → [/voice-cleanup] → publish
```

This is **step 8 of 8** — the gate before anything goes public.

---

## Execution

### No file path provided

Don't just ask "paste text or give a path." Be smart: look at context for what was just produced.

1. If the user just ran `/short-form`, the output is likely at:
   `Content-Hub-Vault-V2/07-Short-Form/<date>_<slug>/<format>.md`
2. If the user just ran `/cascade`, look in:
   `Content-Hub-Vault-V2/08-Distribution/<date>_<slug>/`

Propose the most likely file: "Looks like your last /short-form produced `instagram_caption.md` — clean that one?"
If context is ambiguous, ask: "Paste the text you want cleaned, or give me a file path."

### File path provided

1. Confirm: "Running voice cleanup on: `[path]` — confirm?"
2. Wait for confirmation.
3. Run: `python -m skills.voice_cleanup "<file_path>"`
4. Report:
   - Output file path (always `{stem}_cleaned.md` beside the original)
   - First 300 characters of cleaned output as preview
   - Which AI provider handled it (claude / gemini / ollama)

### Pasted text

Write to a temp file and run:
```
python -m skills.voice_cleanup "<temp_file>"
```
Print the cleaned output directly in chat.

### Batch: clean an entire folder

When the user says "clean all scripts in [folder]" or "voice cleanup everything in [path]":

1. List `.md` files: `Get-ChildItem "<folder>" -Filter *.md`
2. Confirm the list: "Found N files — clean all?\n- [list them]"
3. Run cleanup on each: `python -m skills.voice_cleanup "<file>"` in sequence
4. Report: N files cleaned, output paths listed.

---

## Output Modes

| Mode | Command | Saves to |
|------|---------|----------|
| File (default) | `python -m skills.voice_cleanup "<file>"` | `{stem}_cleaned.md` beside original |
| In-place (destructive) | `python -m skills.voice_cleanup "<file>" --inplace` | Overwrites original — **always ask first** |
| Stdin | `python -m skills.voice_cleanup` (no arg) | Prints to terminal |

---

## Common Workflows

**After /short-form (single script):**
```
/voice-cleanup Content-Hub-Vault-V2/07-Short-Form/2026-05-15_<slug>/instagram_caption.md
```

**After /cascade (three files):**
```
/voice-cleanup Content-Hub-Vault-V2/08-Distribution/2026-05-15_<slug>/blog_post.md
/voice-cleanup Content-Hub-Vault-V2/08-Distribution/2026-05-15_<slug>/twitter_thread.md
/voice-cleanup Content-Hub-Vault-V2/08-Distribution/2026-05-15_<slug>/linkedin_post.md
```

**Or batch-clean an entire distribution folder:**
```
/voice-cleanup all files in Content-Hub-Vault-V2/08-Distribution/2026-05-15_<slug>/
```

---

## Notes

- **Prompt source of truth**: `prompts/voice_cleanup.md` — banned phrases + positive voice markers live here.
- **Voice profile**: `Content-Hub-Vault-V2/01-Knowledge/voice_profile.md` — patterns embedded in prompt, not read at runtime.
- **Model**: Claude-first (`polish()` function) — this is premium polish, never route to Ollama.
- **No auto-publishing.** Always review `_cleaned.md` before posting.
