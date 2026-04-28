"""
AI Router — unified interface for LLM calls across providers.

Routes: Gemini Flash (primary) → Ollama/Gemma (cheap/local) → Claude (premium polish)

Usage:
    from skills.utils.ai import generate
    
    # Auto-route: tries Gemini first, falls back to Ollama, then Claude
    result = await generate("Write me a hook about AI tools")
    
    # Force a specific provider
    result = await generate("Polish this hook", provider="claude")
    result = await generate("Draft an outline", provider="ollama")
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add project root to path so we can import backend modules
PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini client (reuses existing pattern from backend)
# ---------------------------------------------------------------------------

_genai_client = None
_genai_failed = False


def _get_gemini():
    global _genai_client, _genai_failed
    if _genai_client is not None:
        return _genai_client
    if _genai_failed:
        return None
    if not settings.google_ai_studio_key:
        logger.warning("GOOGLE_AI_STUDIO_KEY not set — Gemini unavailable.")
        _genai_failed = True
        return None
    try:
        from google import genai
        _genai_client = genai.Client(api_key=settings.google_ai_studio_key)
        return _genai_client
    except Exception:
        logger.exception("Failed to create Gemini client.")
        _genai_failed = True
        return None


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

async def _gemini_generate(prompt: str, model: str = "gemini-2.5-flash") -> dict:
    """Call Gemini API."""
    client = _get_gemini()
    if client is None:
        return {"text": "", "success": False, "provider": "gemini", "error": "No client"}
    try:
        result = client.models.generate_content(model=model, contents=prompt)
        return {"text": result.text, "success": True, "provider": f"gemini/{model}"}
    except Exception as e:
        logger.warning("Gemini %s failed: %s", model, e)
        return {"text": "", "success": False, "provider": f"gemini/{model}", "error": str(e)}


async def _ollama_generate(prompt: str, model: str = "gemma4:e4b") -> dict:
    """Call local Ollama API."""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
            )
            if response.status_code == 200:
                data = response.json()
                return {"text": data.get("response", ""), "success": True, "provider": f"ollama/{model}"}
            else:
                return {"text": "", "success": False, "provider": f"ollama/{model}", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        logger.warning("Ollama %s failed: %s", model, e)
        return {"text": "", "success": False, "provider": f"ollama/{model}", "error": str(e)}


async def _claude_generate(prompt: str, model: str = "claude-sonnet-4-6") -> dict:
    """Call Claude via CLI subprocess (works with Claude Pro, no API key needed)."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "claude", "-p", prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        text = stdout.decode().strip()
        if proc.returncode == 0 and text:
            return {"text": text, "success": True, "provider": "claude/cli"}
        err = stderr.decode().strip() or f"exit code {proc.returncode}"
        logger.warning("Claude CLI failed: %s", err)
        return {"text": "", "success": False, "provider": "claude/cli", "error": err}
    except asyncio.TimeoutError:
        return {"text": "", "success": False, "provider": "claude/cli", "error": "Timeout after 120s"}
    except FileNotFoundError:
        return {"text": "", "success": False, "provider": "claude/cli", "error": "claude CLI not found in PATH"}
    except Exception as e:
        logger.warning("Claude CLI failed: %s", e)
        return {"text": "", "success": False, "provider": "claude/cli", "error": str(e)}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

PROVIDER_MAP = {
    "gemini": _gemini_generate,
    "ollama": _ollama_generate,
    "claude": _claude_generate,
}

# Default cascade: try each in order until one succeeds
DEFAULT_CASCADE = ["gemini", "ollama", "claude"]


async def generate(
    prompt: str,
    *,
    provider: str | None = None,
    model: str | None = None,
    cascade: list[str] | None = None,
) -> dict:
    """Generate text using the AI cascade.
    
    Args:
        prompt: The text prompt to send
        provider: Force a specific provider ("gemini", "ollama", "claude")
        model: Force a specific model (overrides provider default)
        cascade: Custom cascade order (default: gemini → ollama → claude)
    
    Returns:
        dict with keys: text, success, provider, error (optional)
    """
    if provider:
        # Direct call to a specific provider
        func = PROVIDER_MAP.get(provider)
        if not func:
            return {"text": "", "success": False, "provider": provider, "error": f"Unknown provider: {provider}"}
        kwargs = {"prompt": prompt}
        if model:
            kwargs["model"] = model
        return await func(**kwargs)
    
    # Cascade mode: try each provider in order
    chain = cascade or DEFAULT_CASCADE
    last_error = ""
    for prov_name in chain:
        func = PROVIDER_MAP.get(prov_name)
        if not func:
            continue
        kwargs = {"prompt": prompt}
        if model and prov_name == chain[0]:  # only apply custom model to first in chain
            kwargs["model"] = model
        result = await func(**kwargs)
        if result["success"] and result["text"].strip():
            logger.info("AI generation succeeded via %s", result["provider"])
            return result
        last_error = result.get("error", "Empty response")
        logger.info("Provider %s failed (%s), trying next...", prov_name, last_error)
    
    return {"text": "", "success": False, "provider": "none", "error": f"All providers failed. Last: {last_error}"}


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------

async def draft(prompt: str) -> dict:
    """Quick draft using cheapest available model (Ollama first, then Gemini lite)."""
    return await generate(prompt, cascade=["ollama", "gemini"])


async def polish(prompt: str) -> dict:
    """Premium polish using best available model (Claude first, then Gemini)."""
    return await generate(prompt, cascade=["claude", "gemini"])
