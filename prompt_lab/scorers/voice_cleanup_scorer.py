"""Voice Cleanup Scorer — Programmatic banned-phrase detection.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {banned_phrase_count: int}
This is the most trustworthy metric in the system — exact count, no judge involved.
"""

import re


# Curated banned-phrases list from prompts/voice_cleanup.md
# These are AI clichés that should be removed by the voice-cleanup skill.
BANNED_PHRASES = [
    # Phrases (checked case-insensitive, word-boundary aware)
    r"let\'?s\s+dive\s+(?:in|right\s+in)",
    r"in\s+today\'?s\s+fast-paced\s+(?:world|digital\s+world)",
    r"it\'?s\s+not\s+[^,]+,\s+but\s+[^.]+",
    r"moreover",
    r"furthermore",
    r"additionally",
    r"in\s+conclusion",
    r"remember,",
    r"it\'?s\s+worth\s+noting\s+that",
    r"as\s+we\s+navigate",
    r"paradigm\s+shift",
    r"it\'?s\s+important\s+to",
    r"one\s+thing\s+to\s+keep\s+in\s+mind",
    r"at\s+the\s+end\s+of\s+the\s+day",
    r"this\s+allows\s+us\s+to",
    r"by\s+leveraging",
    r"in\s+order\s+to",
    r"ensure\s+that",
    # Single words (word-boundary to avoid false positives like "delicate" matching "delve")
    r"\bdelve\b",
    r"\bcrucial\b",
    r"\btapestry\b",
    r"\blandscape\b",
    r"\bbeacon\b",
    r"\btestament\b",
    r"\bleverage\b",
    r"\brevolutionize\b",
    r"\bdisrupt\b",
    r"\bstreamline\b",
    r"\boptimize\b",
    r"\bunleash\b",
    r"\bseamless\b",
    r"\brobust\b",
    r"\bcutting-edge\b",
    r"\bgame-changer\b",
    r"\binnovative\b",
]

# Compile regex patterns once
_BANNED_REGEXES = [re.compile(phrase, re.IGNORECASE) for phrase in BANNED_PHRASES]


def score_voice_cleanup_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score voice-cleanup output by counting banned AI-isms.

    Args:
        output: The rewritten/cleaned text from the voice-cleanup skill.
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {banned_phrase_count: int} — exact count of banned phrases found.
        Lower is better (fewer AI-isms = more human).
    """
    if not output:
        return {"banned_phrase_count": 0}

    count = 0
    for regex in _BANNED_REGEXES:
        # Count each match
        matches = regex.findall(output)
        count += len(matches)

    return {"banned_phrase_count": count}
