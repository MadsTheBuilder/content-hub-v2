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
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------------

_genai_client = None
_genai_failed = False


def _get_gemini():
    global _genai_client, _genai_failed
    if _genai_client is not None:
        return _genai_client
    if _genai_failed:
        return None
    api_key = os.getenv("GOOGLE_AI_STUDIO_KEY", "")
    if not api_key:
        logger.warning("GOOGLE_AI_STUDIO_KEY not set — Gemini unavailable.")
        _genai_failed = True
        return None
    try:
        from google import genai
        _genai_client = genai.Client(api_key=api_key)
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


async def _openrouter_generate(prompt: str, model: str | None = None) -> dict:
    """Call OpenRouter API (OpenAI-compatible, free model tier)."""
    api_key = os.getenv("OPENROUTER_API_KEY", "")
    if not api_key:
        return {"text": "", "success": False, "provider": "openrouter", "error": "OPENROUTER_API_KEY not set"}
    _model = model or os.getenv("OPENROUTER_DEFAULT_MODEL", "deepseek/deepseek-v4-flash:free")
    try:
        import httpx
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/content-hub-v2",
                    "X-Title": "Content Hub V2",
                },
                json={"model": _model, "messages": [{"role": "user", "content": prompt}]},
            )
            if response.status_code == 200:
                text = response.json()["choices"][0]["message"]["content"]
                return {"text": text, "success": True, "provider": f"openrouter/{_model}"}
            return {
                "text": "", "success": False, "provider": f"openrouter/{_model}",
                "error": f"HTTP {response.status_code}: {response.text[:300]}",
            }
    except Exception as e:
        logger.warning("OpenRouter %s failed: %s", _model, e)
        return {"text": "", "success": False, "provider": f"openrouter/{_model}", "error": str(e)}


async def _nim_generate(prompt: str, model: str = "meta/llama-3.1-70b-instruct") -> dict:
    """Call NVIDIA NIM API (OpenAI-compatible)."""
    api_key = os.getenv("NVIDIA_NIM_API_KEY", "")
    if not api_key:
        return {"text": "", "success": False, "provider": f"nim/{model}", "error": "NVIDIA_NIM_API_KEY not set"}
    try:
        import httpx
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://integrate.api.nvidia.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": model, "messages": [{"role": "user", "content": prompt}], "max_tokens": 4096},
            )
            if response.status_code == 200:
                data = response.json()
                text = data["choices"][0]["message"]["content"]
                return {"text": text, "success": True, "provider": f"nim/{model}"}
            error_preview = response.text[:500] if response.text else "[no response body]"
            logger.warning("NIM %s failed with HTTP %s: %s", model, response.status_code, error_preview)
            return {"text": "", "success": False, "provider": f"nim/{model}", "error": f"HTTP {response.status_code}: {error_preview}"}
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)[:500]}"
        logger.warning("NIM %s failed: %s", model, error_msg)
        time.sleep(1)
        return {"text": "", "success": False, "provider": f"nim/{model}", "error": error_msg}


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


def _find_claude_exe() -> str:
    """Return the claude executable name, accounting for Windows .cmd wrappers."""
    import shutil, sys
    if sys.platform == "win32":
        found = shutil.which("claude.cmd") or shutil.which("claude")
        return found or "claude.cmd"
    return shutil.which("claude") or "claude"


async def _claude_generate(prompt: str, model: str = "claude-sonnet-4-6") -> dict:
    """Call Claude via CLI subprocess (works with Claude Pro, no API key needed)."""
    import sys
    exe = _find_claude_exe()
    _env = {**__import__("os").environ, "PYTHONIOENCODING": "utf-8"}
    try:
        if sys.platform == "win32":
            proc = await asyncio.create_subprocess_shell(
                f'"{exe}" -p -',
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=_env,
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                exe, "-p", "-",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=_env,
            )
        prompt_bytes = prompt.encode("utf-8")
        stdout, stderr = await asyncio.wait_for(proc.communicate(input=prompt_bytes), timeout=180)
        text = stdout.decode("utf-8", errors="replace").strip()
        if proc.returncode == 0 and text:
            return {"text": text, "success": True, "provider": "claude/cli"}
        err_text = stderr.decode("utf-8", errors="replace").strip()
        err = err_text or f"exit code {proc.returncode}"
        logger.warning("Claude CLI failed (rc=%s): %s", proc.returncode, err[:500])
        return {"text": "", "success": False, "provider": "claude/cli", "error": err[:500]}
    except asyncio.TimeoutError:
        return {"text": "", "success": False, "provider": "claude/cli", "error": "Timeout after 180s"}
    except FileNotFoundError:
        return {"text": "", "success": False, "provider": "claude/cli", "error": f"claude CLI not found: {exe}"}
    except Exception as e:
        logger.warning("Claude CLI failed: %s", e)
        return {"text": "", "success": False, "provider": "claude/cli", "error": str(e)}


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

_ollama_up: bool | None = None

async def _ollama_available() -> bool:
    global _ollama_up
    if _ollama_up is not None:
        return _ollama_up
    try:
        import httpx
        async with httpx.AsyncClient(timeout=2) as client:
            r = await client.get("http://localhost:11434/api/tags")
            _ollama_up = r.status_code == 200
    except Exception:
        _ollama_up = False
    if not _ollama_up:
        logger.info("Ollama not available at localhost:11434 — will skip in cascade")
    return _ollama_up


PROVIDER_MAP = {
    "openrouter": _openrouter_generate,
    "nim": _nim_generate,
    "gemini": _gemini_generate,
    "ollama": _ollama_generate,
    "claude": _claude_generate,
}

# Default cascade: OpenRouter free tier first, Claude CLI as fallback, then NIM/Ollama.
# Gemini dropped 2026-05-19 — hitting 503 UNAVAILABLE consistently.
DEFAULT_CASCADE = ["openrouter", "claude", "nim", "ollama"]


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
        if prov_name == "ollama" and not await _ollama_available():
            last_error = "Ollama not running"
            continue
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
    """Quick draft — OpenRouter free tier first, Claude CLI fallback."""
    return await generate(prompt, cascade=["openrouter", "claude", "nim", "ollama"])


async def polish(prompt: str) -> dict:
    """Premium polish — OpenRouter free tier first, Claude CLI fallback."""
    return await generate(prompt, cascade=["openrouter", "claude", "nim", "ollama"])
