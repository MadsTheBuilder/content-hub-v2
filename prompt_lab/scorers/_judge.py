"""Shared LLM-judge helper for scorer modules.

Encapsulates Claude CLI calls with error handling and result parsing.
All LLM-judge scorers use this to avoid duplication.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Find Claude executable
def _find_claude_exe() -> str:
    """Return the claude executable name, accounting for Windows .cmd wrappers."""
    import shutil
    if sys.platform == "win32":
        found = shutil.which("claude.cmd") or shutil.which("claude")
        return found or "claude.cmd"
    return shutil.which("claude") or "claude"


def call_judge(rubric_prompt: str, timeout_sec: int = 60) -> dict:
    """
    Call Claude via CLI subprocess to score content per a rubric.

    Args:
        rubric_prompt: Full prompt including rubric and content to score.
                      Should instruct the LLM to return JSON.
        timeout_sec: Command timeout in seconds (default: 60).

    Returns:
        dict with keys:
        - success (bool): True if judge call succeeded
        - scores (dict): Parsed JSON result (or empty dict on failure)
        - error (str): Error message if success=False
    """
    exe = _find_claude_exe()
    try:
        result = subprocess.run(
            [exe, "-p", "-"],
            input=rubric_prompt,
            text=True,
            capture_output=True,
            timeout=timeout_sec,
            encoding="utf-8",
        )
        if result.returncode != 0:
            err = result.stderr.strip() or f"exit code {result.returncode}"
            logger.warning("Claude CLI judge failed: %s", err[:200])
            return {"success": False, "scores": {}, "error": err[:200]}

        # Parse JSON from stdout
        stdout = result.stdout.strip()
        if not stdout:
            logger.warning("Claude CLI returned empty response")
            return {"success": False, "scores": {}, "error": "Empty response"}

        # Strip markdown fences if present
        if stdout.startswith("```"):
            lines = stdout.split("\n")
            end = len(lines)
            for i in range(1, len(lines)):
                if lines[i].strip() == "```":
                    end = i
                    break
            stdout = "\n".join(lines[1:end])

        try:
            scores = json.loads(stdout)
            return {"success": True, "scores": scores, "error": ""}
        except json.JSONDecodeError as e:
            logger.warning("Failed to parse judge JSON: %s", str(e)[:100])
            return {"success": False, "scores": {}, "error": f"Invalid JSON: {str(e)[:100]}"}

    except subprocess.TimeoutExpired:
        logger.warning("Claude CLI judge timeout after %d seconds", timeout_sec)
        return {"success": False, "scores": {}, "error": f"Timeout after {timeout_sec}s"}
    except FileNotFoundError:
        logger.warning("Claude CLI not found: %s", exe)
        return {"success": False, "scores": {}, "error": f"Claude CLI not found: {exe}"}
    except Exception as e:
        logger.warning("Claude CLI judge failed: %s", str(e)[:200])
        return {"success": False, "scores": {}, "error": str(e)[:200]}
