"""Knowledge Brain — Claude content analysis.

Uses skills/utils/ai.py generate(provider="claude") so auth flows through
the same Claude CLI session used by all other skills. No separate API key needed.

Returns a dict with keys:
  hook_quality, structure_score, emotional_triggers,
  techniques_to_steal, replication_template
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from skills.utils.ai import generate

_PROMPT = """\
Analyze this YouTube script or content excerpt.

Return ONLY a JSON object with exactly these keys — no markdown fences, no explanation:

{
  "hook_quality": <integer 0-100>,
  "structure_score": <integer 0-100>,
  "emotional_triggers": ["trigger1", "trigger2"],
  "techniques_to_steal": ["technique1", "technique2"],
  "replication_template": "2-3 sentence template capturing the core approach"
}

Content:
---
{content}
---"""


async def analyze(content: str) -> dict:
    prompt = _PROMPT.replace("{content}", content[:8000])
    result = await generate(prompt, provider="claude")
    if not result.get("success"):
        raise RuntimeError(f"Brain analysis failed: {result.get('error', 'empty response')}")
    text = result["text"].strip()
    # Strip markdown code fences if the model wraps its output
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:])
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3].rstrip()
    return json.loads(text)
