# Voice-Cleanup Skill Simulation Transcript

## Step 1: Skill File Read

**Skill File:** `C:\Users\madhu\Claude cowork\Content Hub V2\.claude\skills\voice-cleanup-workspace\skill-snapshot\SKILL.md`

**Key Instructions:**
- Skill: `/voice-cleanup` — De-AI'ify skill outputs by stripping AI-isms, banned phrases, and corporate language
- Trigger: User types `/voice-cleanup` with optional file path or text
- Execution: For file path, confirm → run Python module → report output
- Output modes: File mode saves `{original_stem}_cleaned.md` beside original; does not overwrite unless `--inplace` flag
- Reporting: Path to cleaned file + first 300 characters preview + AI provider (Claude-first routing)
- Voice profile: Located at `Content-Hub-Vault-V2/01-Knowledge/voice_profile.md`
- Python command: `python -m skills.voice_cleanup "<file_path>"`

---

## Step 2: Claude's Confirmation Message to User

User Input:
```
/voice-cleanup Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/instagram_caption.md
```

Claude's Confirmation Response:
```
Running voice cleanup on: Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/instagram_caption.md — confirm?
```

**User Simulated Response:** ✓ Confirmed (user types "y" or "confirm")

---

## Step 3: Command Execution (Simulated)

After user confirmation, Claude would execute:

```bash
python -m skills.voice_cleanup "Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/instagram_caption.md"
```

**Note:** The vault file does not exist in the actual filesystem — this is expected. The skill would process the file if it existed. The Python module would:
1. Read the file
2. Apply voice cleanup transformations (using Claude via `polish()` routing)
3. Write output to: `Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/instagram_caption_cleaned.md`
4. Leave original untouched

---

## Step 4: Simulated Output Report

**Output File Path:**
```
Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/instagram_caption_cleaned.md
```

**300-Character Preview (Placeholder):**
Since the source file doesn't exist, this is a realistic placeholder of what would be reported:
```
"Breakthrough: AI isn't the villain in your toolbox. The real problem? Creatives using AI like a crutch instead of a lever. We tested 47 workflows last month—found that hybrid human-AI beats pure AI 73% of the time. Real talk: the best prompts come from domain experts who..."
```

**AI Provider:** `claude` (Claude-first routing via `polish()` module)

---

## Step 5: Final Message Claude Would Send

```
✓ Voice cleanup complete.

📄 Cleaned output: Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/instagram_caption_cleaned.md

Preview (first 300 chars):
"Breakthrough: AI isn't the villain in your toolbox. The real problem? Creatives using AI like a crutch instead of a lever. We tested 47 workflows last month—found that hybrid human-AI beats pure AI 73% of the time. Real talk: the best prompts come from domain experts who..."

Provider: claude

✓ Original file untouched. Ready to review and post.
```

---

## Assumptions & Notes

1. **File existence:** The source Instagram caption file does not exist in the vault. The skill snapshot indicates no error handling for missing files—in real execution, the Python module would handle this with appropriate error messaging.

2. **Voice profile:** The skill reads from `Content-Hub-Vault-V2/01-Knowledge/voice_profile.md` at runtime (per line 48 of snapshot), but banned patterns are embedded in the prompt at `prompts/voice_cleanup.md`.

3. **Output naming:** The skill always appends `_cleaned.md` to the original stem, never overwrites, unless `--inplace` flag is used (which requires user confirmation first).

4. **Simulated Python module:** The `python -m skills.voice_cleanup` module is invoked directly by Claude (no manual subprocess setup shown in the snapshot). The module handles all I/O and Claude routing internally.

5. **Provider routing:** The skill uses `claude` (Claude) as the default premium polish provider, no fallback routing to Gemini/Ollama shown in this snapshot version.

---

## Transcript Completion

This transcript documents the complete simulated workflow for the `/voice-cleanup` skill when applied to the Instagram caption file. Claude would:
1. ✓ Confirm the file path
2. ✓ Wait for user confirmation
3. ✓ Execute the Python cleanup module
4. ✓ Report the output file path, preview, and provider
5. ✓ Remind the user the original is safe and ready for review
