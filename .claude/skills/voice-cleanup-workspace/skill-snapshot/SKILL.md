# /voice-cleanup

De-AI'ify any skill output. Takes a vault file or pasted text and rewrites it in the creator's authentic voice — strips AI-isms, banned phrases, and corporate language. Run this after `/cascade`, `/short-form`, or any other skill output that needs humanising.

## Trigger
User types `/voice-cleanup` with an optional file path or text.

## Execution Steps

### If a file path is provided:
1. Confirm the file: "Running voice cleanup on: [path] — confirm?"
2. Wait for user confirmation.
3. Run: `python -m skills.voice_cleanup "<file_path>"`
4. Report: output file path + first 300 characters preview.

### If no file path is provided:
1. Ask: "Paste the text you want cleaned, or give me a file path from the vault."
2. If they paste text, write it to a temp file and run: `python -m skills.voice_cleanup "<temp_file>"`
3. Or if they give a file path, use the file path flow above.
4. Report: cleaned output printed directly, or saved file path.

## Output

- **File mode:** saves `{original_stem}_cleaned.md` beside the original file. Original is untouched.
- **Stdin mode:** prints cleaned text to terminal.
- **In-place mode (explicit):** `python -m skills.voice_cleanup "<file>" --inplace` — overwrites original. Ask user before using this.

## Common post-cascade workflow

After `/cascade` generates a blog post, thread, and LinkedIn:
```
/voice-cleanup Content-Hub-Vault-V2/08-Distribution/2026-04-29_<slug>/blog_post.md
/voice-cleanup Content-Hub-Vault-V2/08-Distribution/2026-04-29_<slug>/twitter_thread.md
/voice-cleanup Content-Hub-Vault-V2/08-Distribution/2026-04-29_<slug>/linkedin_post.md
```

## After Completion

Report:
- Path to cleaned file(s)
- First 300 characters of the cleaned output as a preview
- Which AI provider handled the cleanup (claude/gemini/ollama)

## Notes

- This skill uses Claude-first routing (`polish()`) — voice cleanup is premium polish work.
- The prompt source of truth is `prompts/voice_cleanup.md`.
- Voice profile source is `Content-Hub-Vault-V2/01-Knowledge/voice_profile.md` — but the banned patterns and positive markers are embedded directly in the prompt, not read at runtime.
- No auto-posting. Review before publishing.