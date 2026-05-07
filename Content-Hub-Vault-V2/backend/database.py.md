---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/database.py"
category: "Content Hub Source Code"
---

# database.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
import uuid
import logging
from backend.config import settings

logger = logging.getLogger(__name__)

_client = None

# ---------------------------------------------------------------------------
# Mock Supabase client — used when .env has placeholder/missing keys
# ---------------------------------------------------------------------------

_MOCK_SINGLE_DEFAULTS: dict = {
    "workflows": {
        "id": "mock-wf-001",
        "user_id": "00000000-0000-0000-0000-000000000000",
        "name": "Demo Workflow",
        "template_type": "custom",
        "brand_voice": "clear, confident, educational",
        "content_pillars": ["education", "tips", "motivation"],
        "platforms": ["tiktok", "instagram"],
        "apify_search_config": {},
        "is_active": True,
        "created_at": "2026-01-01T00:00:00",
    },
    "brand_configs": {
        "workflow_id": "mock-wf-001",
        "primary_color": "#C9A96E",
        "secondary_color": "#1E293B",
        "font_family": "Inter",
        "logo_url": None,
        "style_notes": "",
    },
    "content_publication_memory": {
        "workflow_id": "mock-wf-001",
        "content_type_distribution": {},
        "avg_script_length": {},
        "preferred_hook_styles": {},
        "topics_published": [],
        "platform_content_map": {},
    },
}


class MockResult:
    """Mimics supabase-py's APIResponse."""
    def __init__(self, data):
        self.data = data


class MockQueryBuilder:
    """
    Fluent builder that absorbs any chained call and returns safe empty data
    on .execute() so the app boots without a live Supabase connection.
    """

    def __init__(self, table_name: str):
        self._table = table_name
        self._op = "select"
        self._insert_data: dict | list | None = None
        self._single = False

    # --- filter / sort / limit (all no-ops) ---
    def select(self, *a, **kw): return self
    def eq(self, *a, **kw): return self
    def neq(self, *a, **kw): return self
    def in_(self, *a, **kw): return self
    def gte(self, *a, **kw): return self
    def lte(self, *a, **kw): return self
    def ilike(self, *a, **kw): return self
    def order(self, *a, **kw): return self
    def limit(self, *a, **kw): return self
    def desc(self, *a, **kw): return self
    def single(self): self._single = True; return self

    # --- mutations ---
    def insert(self, data):
        self._op = "insert"
        self._insert_data = data
        return self

    def update(self, data):
        self._op = "update"
        self._insert_data = data
        return self

    def delete(self):
        self._op = "delete"
        return self

    def execute(self) -> MockResult:
        if self._op == "insert" and self._insert_data is not None:
            # Return a row with a generated id so callers can do .data[0]["id"]
            base = self._insert_data if isinstance(self._insert_data, dict) else {}
            row = {"id": str(uuid.uuid4()), **base}
            return MockResult(data=[row])

        if self._op in ("update", "delete"):
            return MockResult(data=[{}])

        # SELECT — single row
        if self._single:
            default = _MOCK_SINGLE_DEFAULTS.get(self._table)
            return MockResult(data=default)

        # SELECT — list (return empty so UI shows the "no items" state)
        return MockResult(data=[])


class MockAuthClient:
    """Raises so auth/router.py fallback is always triggered."""
    def get_user(self, token):
        raise RuntimeError("Mock mode: Supabase not connected")

    def sign_up(self, data):
        raise RuntimeError("Mock mode: Supabase not connected")

    def sign_in_with_password(self, data):
        raise RuntimeError("Mock mode: Supabase not connected")

    def sign_out(self, *a, **kw):
        return None


class MockSupabaseClient:
    def __init__(self):
        self.auth = MockAuthClient()
        logger.warning(
            "\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "  🔧  MOCK MODE  —  Supabase not connected\n"
            "  Data will NOT persist. Set real keys in .env to\n"
            "  enable database, auth, and RAG features.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

    def table(self, name: str) -> MockQueryBuilder:
        return MockQueryBuilder(name)

    def rpc(self, fn_name: str, params: dict | None = None) -> MockQueryBuilder:
        """Mock RPC — always returns empty result."""
        return MockQueryBuilder(f"rpc:{fn_name}")


# ---------------------------------------------------------------------------
# Public accessor
# ---------------------------------------------------------------------------

def _is_placeholder() -> bool:
    url = settings.supabase_url or ""
    key = settings.supabase_service_role_key or ""
    return (
        not url
        or "your-project" in url
        or not key
        or key.startswith("your-")
    )


def get_supabase():
    global _client
    if _client is None:
        if _is_placeholder():
            _client = MockSupabaseClient()
        else:
            try:
                from supabase import create_client
                _client = create_client(
                    settings.supabase_url,
                    settings.supabase_service_role_key,
                )
                logger.info("✅ Supabase client connected to %s", settings.supabase_url)
            except Exception as exc:
                logger.error("Supabase connection failed (%s) — falling back to mock mode.", exc)
                _client = MockSupabaseClient()
    return _client

```
