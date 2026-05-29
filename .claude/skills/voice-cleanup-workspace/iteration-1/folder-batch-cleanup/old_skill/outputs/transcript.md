# Voice-Cleanup Old Skill Simulation — Folder Batch Request

**Simulation Date:** 2026-05-15  
**User Request:** "clean all the scripts in Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/ please"  
**Skill Version:** Old (snapshot from .claude/skills/voice-cleanup-workspace/skill-snapshot/)

---

## Step 1: Skill File Analysis

**File Read:** C:\Users\madhu\Claude cowork\Content Hub V2\.claude\skills\voice-cleanup-workspace\skill-snapshot\SKILL.md

**Key Instructions Found:**
- **Primary trigger:** `/voice-cleanup` with optional file path or pasted text
- **File path mode:** Confirm file, run `python -m skills.voice_cleanup "<file_path>"`, report output file
- **No file path mode:** Ask user to paste text or provide path
- **Output:** Saves `{original_stem}_cleaned.md` beside original (file mode) or prints to terminal (stdin mode)
- **In-place mode:** Only with explicit `--inplace` flag; requires user confirmation first
- **Common workflow:** Single-file operations shown (blog_post.md, twitter_thread.md, linkedin_post.md treated individually)
- **Report template:** Path to cleaned file(s), first 300 chars preview, AI provider used

**Critical Gap:** The old skill.md contains **no explicit batch or folder-mode instructions**. All examples show single-file workflows. No guidance for handling "all scripts in folder" requests.

---

## Step 2: Old Skill's Response to User Prompt

Given the user request: `"clean all the scripts in Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/ please"`

The old skill would likely respond as follows:

---

### What the Old Skill Would Say

**Claude (simulating old /voice-cleanup):**

> Thanks for reaching out! I see you want to clean scripts in that folder. I can help, but I need a bit more clarity because the voice-cleanup skill is designed for single files at a time.
>
> A couple of options:
>
> 1. **Give me a specific file path** — if you have a particular script file like `Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/script_v1.md`, I can clean that directly.
>
> 2. **Paste the text** — if you want, you can paste the script content here and I'll clean it.
>
> 3. **List the files first** — if the folder exists, I could list what's in there and we clean them one by one or you can pick which ones matter most.
>
> Which approach works for you?

---

## Step 3: Interpretation of "All Scripts in Folder"

**How the old skill interprets this ambiguous request:**

| Aspect | Old Skill Handling |
|--------|-------------------|
| **Batch folder support** | **NOT DOCUMENTED**. No batch mode, no loop instructions, no folder traversal logic in SKILL.md |
| **Implicit assumption** | User probably means "multiple files in a folder" but skill is single-file-oriented |
| **Fallback behavior** | Ask clarifying questions OR require user to provide explicit file paths one at a time |
| **Risk of misunderstanding** | Old skill does NOT automatically discover, list, or iterate over folder contents. |
| **Difference from new skill** | Old skill has no `--batch`, `--folder`, or `--glob` mode mentioned. New skill likely handles this seamlessly. |

**Key question:** Does the old skill even try to detect or list the folder? 
- Looking at the SKILL.md, there's **no indication** it would list files or auto-discover "all scripts."
- It expects explicit paths OR pasted text.
- A user saying "all scripts in folder" is **out of scope** for the documented behavior.

---

## Step 4: What the Old Skill Does / Asks

**Decision point:** The old skill would hit an ambiguity and **ask for clarification** rather than assume.

**What it would NOT do:**
- ❌ Automatically glob `*.md` or `*.txt` files in the folder
- ❌ Run cleanup in a loop over 5+ files
- ❌ Use `--batch` or `--folder` flags (not in SKILL.md)
- ❌ Return multiple `_cleaned.md` files in one output

**What it WOULD do:**
- ✅ Acknowledge the request
- ✅ Note that it's designed for single files
- ✅ Ask: "Can you give me the specific file path, or list which files you want cleaned?"
- ✅ Optionally offer: "Or if you want, paste the content and I'll clean it here"
- ✅ Wait for user to clarify or provide an explicit path

---

## Step 5: Final Response the Old Skill Would Send

```
Running /voice-cleanup on folder request...

I see you want to clean "all the scripts" in:
  Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/

The voice-cleanup skill works best with explicit file paths. I have a few options:

**Option 1: Tell me the specific file(s)**
Give me the exact filename(s) — like:
  /voice-cleanup Content-Hub-Vault-V2/07-Short-Form/2026-05-15_ai-tools-arent-the-problem/script.md

I'll clean each one and save `script_cleaned.md` beside it.

**Option 2: Paste the text**
Copy-paste a script here and I'll clean it directly.

**Option 3: I can help list what's in the folder** (if it exists on disk)
Once we know which files are there, you can pick which to clean.

Which would be easiest for you?
```

---

## Summary: Old vs. New Skill Capability

| Capability | Old Skill | Notes |
|-----------|-----------|-------|
| Single-file cleanup | ✅ Yes | Core documented feature |
| Folder/batch mode | ❌ No | Not mentioned in SKILL.md |
| Auto-glob patterns | ❌ No | No `--batch` or `--folder` flag |
| Loop over multiple files | ❌ No | Asks for clarification instead |
| Pasted text cleanup | ✅ Yes | Fall-back documented |
| In-place overwrite | ✅ Yes | With `--inplace` flag + confirmation |

**Key Finding:** The old skill **does not handle folder batch requests** — it would ask the user for specific file paths and then process them one at a time (or require the user to make multiple calls).

---

## Metadata

- **Skill file analyzed:** `C:\Users\madhu\Claude cowork\Content Hub V2\.claude\skills\voice-cleanup-workspace\skill-snapshot\SKILL.md`
- **User request type:** Folder batch (out of scope for old skill)
- **Old skill response strategy:** Clarifying questions + fallback to single-file or pasted-text workflow
- **Ambiguity level:** HIGH — "all scripts in folder" is not explicitly handled
- **Estimated user experience:** Friction — multiple clarifications needed before cleaning can begin
