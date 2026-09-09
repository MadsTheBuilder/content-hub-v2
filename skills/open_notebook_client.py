"""Thin async HTTP client for open-notebook REST API.

Default base URL: http://localhost:5055
Override with env var: OPEN_NOTEBOOK_BASE_URL
"""

import asyncio
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

OPEN_NOTEBOOK_BASE_URL = os.environ.get("OPEN_NOTEBOOK_BASE_URL", "http://localhost:5055")
OPEN_NOTEBOOK_MODEL = os.environ.get("OPEN_NOTEBOOK_MODEL", "model:8owfiukkrpbq6uxgm7t3")  # google/gemma-4-31b-it:free


class OpenNotebookClient:
    def __init__(self, base_url: str = OPEN_NOTEBOOK_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "OpenNotebookClient":
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(connect=10.0, read=600.0, write=30.0, pool=10.0),
        )
        return self

    async def __aexit__(self, *_: Any) -> None:
        if self._client:
            await self._client.aclose()

    @property
    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            raise RuntimeError("Use OpenNotebookClient as an async context manager")
        return self._client

    async def health_check(self) -> bool:
        """Return True if open-notebook API is reachable."""
        try:
            resp = await self._http.get("/api/notebooks", timeout=5.0)
            return resp.status_code < 500
        except Exception:
            return False

    # --- Notebooks ---

    async def create_notebook(self, name: str) -> dict[str, Any]:
        resp = await self._http.post("/api/notebooks", json={"name": name})
        resp.raise_for_status()
        return resp.json()

    async def delete_notebook(self, notebook_id: str) -> None:
        await self._http.delete(f"/api/notebooks/{notebook_id}")

    # --- Sources ---

    async def add_source(self, notebook_id: str, url: str, wait: bool = True) -> dict[str, Any]:
        """Add a URL source to a notebook. If wait=True, poll until indexing completes."""
        resp = await self._http.post(
            "/api/sources",
            data={
                "notebook_id": notebook_id,
                "type": "link",
                "url": url,
                "embed": "true",
                "async_processing": "true",
            },
        )
        resp.raise_for_status()
        result = resp.json()
        if wait:
            source_id = (
                result.get("id")
                or (result.get("source") or {}).get("id")
                or (result.get("data") or {}).get("id")
            )
            if source_id:
                await self._wait_for_source(source_id)
        return result

    async def _wait_for_source(
        self, source_id: str, max_polls: int = 30, interval: float = 10.0
    ) -> None:
        terminal = {"completed", "ready", "done", "success", "failed", "error"}
        for _ in range(max_polls):
            try:
                resp = await self._http.get(f"/api/sources/{source_id}/status")
                if resp.status_code == 200:
                    data = resp.json()
                    status = (data.get("status") or "").lower()
                    if status in terminal:
                        if status in {"failed", "error"}:
                            logger.warning("Source %s indexing failed", source_id)
                        return
            except Exception as e:
                logger.debug("Source status poll error: %s", e)
            await asyncio.sleep(interval)

    async def list_sources(self, notebook_id: str) -> list[dict[str, Any]]:
        resp = await self._http.get("/api/sources", params={"notebook_id": notebook_id})
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else data.get("sources", [])

    # --- Chat ---

    async def get_notebook_context(self, notebook_id: str) -> dict[str, Any]:
        """Build context config for a notebook (used in chat/execute)."""
        try:
            resp = await self._http.post(
                "/api/chat/context",
                json={"notebook_id": notebook_id, "context_config": {}},
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("context", data)
        except Exception as e:
            logger.debug("get_notebook_context failed: %s", e)
        return {}

    async def create_chat_session(
        self, notebook_id: str, model: str = OPEN_NOTEBOOK_MODEL
    ) -> str:
        """Create a new chat session. Returns session_id."""
        resp = await self._http.post(
            "/api/chat/sessions",
            json={"notebook_id": notebook_id, "model_override": model},
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("id") or data.get("session_id") or ""

    async def ask(
        self,
        session_id: str,
        question: str,
        context: dict[str, Any] | None = None,
        model: str = OPEN_NOTEBOOK_MODEL,
    ) -> str:
        """Send a question to a chat session. Returns the answer text."""
        resp = await self._http.post(
            "/api/chat/execute",
            json={
                "session_id": session_id,
                "message": question,
                "context": context or {},
                "model_override": model,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        # ExecuteChatResponse shape: {"session_id": ..., "messages": [{"type": "ai", "content": ...}]}
        messages = data.get("messages", [])
        ai_msgs = [m for m in messages if m.get("type") == "ai"]
        if ai_msgs:
            return ai_msgs[-1].get("content", "")
        return (
            data.get("answer")
            or data.get("response")
            or data.get("content")
            or str(data)
        )
