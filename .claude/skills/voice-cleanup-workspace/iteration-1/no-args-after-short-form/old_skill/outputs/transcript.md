# Voice-Cleanup Skill Simulation: /short-form → /voice-cleanup (No Args)

## Step 1: Skill File Read

**File**: `C:\Users\madhu\Claude cowork\Content Hub V2\.claude\skills\voice-cleanup-workspace\skill-snapshot\SKILL.md`

**Key Instructions**:
- Skill purpose: De-AI'ify text — strips AI-isms, corporate language, banned phrases; rewrites in creator's authentic voice
- Trigger: User types `/voice-cleanup` with optional file path or text
- **No file path provided** → Flow: "Paste the text you want cleaned, or give me a file path from the vault"
- Common post-cascade workflow shows multi-file cleanup (blog_post.md, twitter_thread.md, linkedin_post.md) saved as `{original_stem}_cleaned.md`
- After `/short-form` user has Instagram caption script (inline text, not a file reference)
- Output mode for text input: prints cleaned text to terminal OR saves to temp file and reports path
- Report: path to cleaned file(s), first 300 characters preview, which AI provider handled cleanup

## Step 2: Full Response to User

```
Got it — you've got your Instagram caption script from /short-form. Let me clean up the AI-isms and polish it to your voice.

Paste the script here, or if it's already saved in the vault (likely in Content-Hub-Vault-V2/08-Distribution/ or 09-Short-Form/), give me the file path and I'll run the cleanup.

Which would you prefer?
```

## Step 3: Reasoning

**Why this response?**

1. **Acknowledge context**: User explicitly said "just finished /short-form and got my instagram caption script" — indicates the script is fresh, likely not yet saved or in memory.

2. **No explicit file path given**: The SKILL.md flow for "no file path provided" is:
   > "Ask: 'Paste the text you want cleaned, or give me a file path from the vault.'"
   
   This is exactly what I followed.

3. **Proactive vault hint, not command execution**: The old skill does NOT auto-infer vault paths when none is given. Instead, it asks the user to either:
   - Paste the text directly, OR
   - Provide a file path

4. **No tool calls yet**: The skill waits for user confirmation/input before running `python -m skills.voice_cleanup`. Jumping to command execution without text/path would violate the "If no file path is provided" flow.

5. **Tone**: Friendly, action-oriented, acknowledges the prior skill (`/short-form`), gives user clear options.

## Step 4: Commands (Conditional on User Input)

If user pastes text directly:
```bash
python -m skills.voice_cleanup "<temp_file>" 
# (after writing pasted text to a temporary file)
```

If user provides a vault file path (e.g., `Content-Hub-Vault-V2/08-Distribution/2026-05-15_ai_automation/instagram_caption.md`):
```bash
python -m skills.voice_cleanup "Content-Hub-Vault-V2/08-Distribution/2026-05-15_ai_automation/instagram_caption.md"
```

Default output mode: saves as `instagram_caption_cleaned.md` beside the original.

## Step 5: Completion Report (After User Input + Execution)

Once user provides text or path, I would:

1. **If text pasted**:
   - Write text to temp file
   - Run voice cleanup
   - Report:
     ```
     Cleaned output:
     
     [First 300 characters of cleaned text]
     
     (Full cleaned output saved to: [temp_file_path])
     Claude handled the voice cleanup polish.
     ```

2. **If file path given**:
   - Confirm the path
   - Run voice cleanup
   - Report:
     ```
     Cleaned Instagram caption saved to:
     Content-Hub-Vault-V2/08-Distribution/2026-05-15_ai_automation/instagram_caption_cleaned.md
     
     Preview:
     [First 300 characters]
     
     Claude handled the voice cleanup polish. Review before posting.
     ```

---

## Key Discriminator

**Did I proactively suggest a specific vault file path, or just ask generically?**

**ANSWER: Generic ask with vault hint, no specific path inference.**

The old skill snapshot does NOT include logic to auto-infer `Content-Hub-Vault-V2/08-Distribution/<date>_<slug>/instagram_caption.md` or similar paths. It simply asks:

> "Paste the text you want cleaned, or give me a file path from the vault."

This is a **reactive** flow: the skill waits for the user to provide specifics, rather than guessing. The common post-cascade workflow example shows explicit paths because the user has already run `/cascade` and knows where the files live.

In this scenario (post `/short-form`), the output may not yet be saved to a vault file, so the skill correctly defaults to "paste or provide path" rather than attempting inference.

