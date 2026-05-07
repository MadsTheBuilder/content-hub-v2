## Remediation Log: Code Review Fixes (2026-04-13)

This section details the explicit changes made to resolve the 8 loose ends identified in the Day 3 & Day 4 Code Review audit. These fixes target both Integrity (Must Fix) and Quality (Should Fix) issues, restoring the system's alignment with its technical design specification.

### 1. Expanded Psychology Sections in Content Synthesis

**What & Why:** The `synthesis.py` script was originally loading only 2 psychology sections, missing the planned "Pricing Psychology" and "Design & Delivery Models". Expanding these sections provides the `generate_strategy_document` LLM with deeper behavioral context necessary to build stronger, structurally-sound strategies.

**File:** `backend/intelligence/synthesis.py`

**Before:**
```python
    psychology_skill = load_skill_sections("psychology", [
        "Understanding Buyers & Human Psychology",
        "Influencing Behavior & Persuasion",
    ])
```

**After:**
```python
    psychology_skill = load_skill_sections("psychology", [
        "Understanding Buyers & Human Psychology",
        "Influencing Behavior & Persuasion",
        "Pricing Psychology",
        "Design & Delivery Models",
    ])
```

### 2. Wired Static Brand Voice Adaptation

**What & Why:** `scripting.py` bypassed the platform rules, injecting raw `brand_voice` instead of adapting it. We added a static voice adaptation that injects platform tone and script style. We explicitly chose the *static* composition route (no Gemini API call) to prevent double LLM latency during the already heavy content generation sequence.

**File:** `backend/content/scripting.py`

**Before:**
```python
    if brand_voice:
        sections.append(f"\n## Brand Voice\n{brand_voice}")
```

**After:**
```python
    if brand_voice:
        # Adapt brand voice to platform conventions using static composition.
        # Intentionally NOT using a Gemini call here to avoid double LLM
        # latency — the scripting LLM receives the adapted voice and does
        # the heavy lifting. This mirrors adapt_voice_to_platform()'s
        # no-API-key path (see code review item 2A-4b / 2A-3).
        from backend.content.platform_adapter import get_platform_rules as _get_voice_rules
        _voice_rules = _get_voice_rules(platform)
        _voice_parts = []
        if _voice_rules.get("tone"):
            _voice_parts.append(f"Tone for {platform}: {_voice_rules['tone']}.")
        if _voice_rules.get("script_style"):
            _voice_parts.append(f"Script style: {_voice_rules['script_style']}")
        adapted_voice = (
            f"{brand_voice}\n\n{' '.join(_voice_parts)}"
            if _voice_parts else brand_voice
        )
        sections.append(f"\n## Brand Voice (adapted for {platform})\n{adapted_voice}")
```

### 3. Removed Redundant Platform Label

**What & Why:** `_build_prompt` previously appended `## Target Platform\n{platform}`, which unnecessarily bloated the prompt since the complete `Platform Strategy Rules` context section was injected immediately afterward (which itself includes platform-specific awareness).

**File:** `backend/content/scripting.py`

**Before:**
```python
    sections.append(f"\n## Target Platform\n{platform}")
```

**After:**
```python
    # NOTE: Redundant bare platform label removed (code review item 2A-4).
    # The structured Platform Strategy Rules section below provides platform
    # name plus detailed rules, making a standalone label unnecessary bloat.
```

### 4. Optimized Copywriting Token Spend

**What & Why:** The prompt generator was loading the *entire* `copywriting.md` (~7.8KB token payload). The plan specified loading 3 targeted sections to manage LLM context size and preserve token limits.

**File:** `backend/content/scripting.py`

**Before:**
```python
    # 1. Core copywriting principles — applied to ALL content types
    copywriting_text = load_skill("copywriting")
    if copywriting_text:
        sections.append(f"\n## Core Copywriting Principles\n{copywriting_text}")
```

**After:**
```python
    # 1. Core copywriting principles — applied to ALL content types.
    #    Targeted sections only (~2KB) instead of full file (~7.8KB) to
    #    manage prompt token spend (code review item 2C-3).
    copywriting_text = load_skill_sections("copywriting", [
        "Copywriting Principles",
        "Writing Style Rules",
        "CTA Copy Guidelines",
    ])
    if copywriting_text:
        sections.append(f"\n## Core Copywriting Principles\n{copywriting_text}")
```

### 5. Documented Gemini Design Decision

**What & Why:** Because the platform voice adaptation was built using Gemini (contrary to the Day 2 static plan), a future developer might be confused. We added docstring rationale noting the tradeoff (Gemini gets higher quality results during setup; fallback static path preserves latency during script generation).

**File:** `backend/content/platform_adapter.py`

**Before:**
```python
    """Use Gemini to adapt a brand voice for a specific platform's conventions.

    Returns an adapted voice description string, or the original on failure.
    If *google_ai_studio_key* is not provided, returns a rule-appended string.
    """
```

**After:**
```python
    """Use Gemini to adapt a brand voice for a specific platform's conventions.

    Returns an adapted voice description string, or the original on failure.
    If *google_ai_studio_key* is not provided, returns a rule-appended string.

    **Design Note (2A-3):** The original plan specified static string composition
    to avoid double LLM latency. The Gemini path was added because it produces
    noticeably higher-quality platform-native voice descriptions, especially for
    platforms with very different conventions (e.g., TikTok vs LinkedIn).
    However, ``_build_prompt()`` in ``scripting.py`` intentionally uses the
    **static path** (no API key) to avoid the latency hit during script
    generation. The Gemini path is available for standalone pre-computation
    (e.g., in a brand setup flow where latency is acceptable).
    """
```

### 6. Corrected False System Logistics Claims

**What & Why:** The `Day3_Frontend_Polish_E2E_Verification.md` log contained two factually manipulated claims referencing frontend router removal and phantom validation artifacts. These were resolved to maintain accurate knowledge base integrity.

**File(s):**
- `Content-Hub-Vault/00-Management/Sessions/2026-04-12_Day3_Frontend_Polish_E2E_Verification.md` (Notated corrections inplace regarding `useRouter` and ephemeral sessions).
- `Content-Hub-Vault/00-Management/Tasks/MVP_Completion_Tasks.md` (Fixed function mapping issue for `generate_strategy_document`).