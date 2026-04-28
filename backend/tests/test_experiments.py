"""
Integration tests for A/B experiments lifecycle.

Exercises the full endpoint lifecycle: create → start → record-result → conclude,
with assertion that update_experiment_learnings is invoked on conclude.
Uses FastAPI TestClient against backend.main.app with mock Supabase (no real DB calls).
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import MockResult
import uuid


class PersistentMockQueryBuilder:
    """Enhanced MockQueryBuilder that persists data in a shared store."""

    def __init__(self, table_name: str, store: dict):
        self._table = table_name
        self._store = store
        self._op = "select"
        self._insert_data: dict | list | None = None
        self._single = False
        self._filters = {}  # Track eq() filters for select/update/delete

    # --- filter / sort / limit ---
    def select(self, *a, **kw):
        return self

    def eq(self, key: str, value):
        self._filters[key] = value
        return self

    def neq(self, *a, **kw):
        return self

    def in_(self, *a, **kw):
        return self

    def gte(self, *a, **kw):
        return self

    def lte(self, *a, **kw):
        return self

    def ilike(self, *a, **kw):
        return self

    def order(self, *a, **kw):
        return self

    def limit(self, *a, **kw):
        return self

    def desc(self, *a, **kw):
        return self

    def single(self):
        self._single = True
        return self

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
        # Initialize table in store if not present
        if self._table not in self._store:
            self._store[self._table] = []

        table_data = self._store[self._table]

        if self._op == "insert" and self._insert_data is not None:
            # Insert a new row with generated id
            base = self._insert_data if isinstance(self._insert_data, dict) else {}
            row = {"id": str(uuid.uuid4()), **base}
            table_data.append(row)
            return MockResult(data=[row])

        if self._op == "update":
            # Update matching rows
            matches = self._filter_rows(table_data)
            for row in matches:
                row.update(self._insert_data or {})
            return MockResult(data=matches if matches else [{}])

        if self._op == "delete":
            # Delete matching rows
            matches = self._filter_rows(table_data)
            for row in matches:
                table_data.remove(row)
            return MockResult(data=[{}])

        # SELECT operations
        matches = self._filter_rows(table_data)

        if self._single:
            # Return single row or None
            if matches:
                return MockResult(data=matches[0])
            return MockResult(data=None)

        # SELECT — list (return matches or empty)
        return MockResult(data=matches)

    def _filter_rows(self, rows: list) -> list:
        """Filter rows based on stored eq() filters."""
        if not self._filters:
            return rows
        filtered = []
        for row in rows:
            if all(row.get(k) == v for k, v in self._filters.items()):
                filtered.append(row)
        return filtered


class PersistentMockSupabaseClient:
    """Mock Supabase client that persists data within a test."""

    def __init__(self):
        self._store = {}  # Table name -> list of rows

    def table(self, name: str) -> PersistentMockQueryBuilder:
        return PersistentMockQueryBuilder(name, self._store)

    def rpc(self, fn_name: str, params: dict | None = None) -> PersistentMockQueryBuilder:
        """Mock RPC — always returns empty result."""
        return PersistentMockQueryBuilder(f"rpc:{fn_name}", self._store)


class TestExperimentsLifecycle:
    """Full-lifecycle A/B experiment flow."""

    @pytest.mark.asyncio
    async def test_experiment_complete_lifecycle(self, monkeypatch):
        """
        Stepwise lifecycle test:
        1. POST /api/v1/experiments → 200, status='draft'
        2. POST /experiments/{id}/start → status='active'
        3. POST /experiments/{id}/record-result (variant a, ctr=0.12) → metrics recorded
        4. POST /experiments/{id}/record-result (variant a, ctr=0.18) → second value appended
        5. POST /experiments/{id}/record-result (variant b, ctr=0.10) → variant b recorded
        6. POST /experiments/{id}/record-result (variant b, ctr=0.15) → second b value
        7. POST /experiments/{id}/conclude with winner='a' → status='concluded', winner='a'
        8. Assert update_experiment_learnings was called with correct experiment_id
        """
        # Replace MockSupabaseClient with persistent version for this test
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        # Spy on update_experiment_learnings
        spy_calls = []

        async def spy_update_experiment_learnings(exp_id: str):
            spy_calls.append(exp_id)

        import backend.experiments.router as router_mod
        monkeypatch.setattr(
            router_mod,
            "update_experiment_learnings",
            spy_update_experiment_learnings,
        )

        client = TestClient(app)

        # Step 1: Create experiment
        create_response = client.post(
            "/api/v1/experiments",
            json={
                "name": "Homepage CTA Test",
                "variant_a": {"button_text": "Start Free Trial", "color": "blue"},
                "variant_b": {"button_text": "Get Started Now", "color": "green"},
            },
        )
        assert create_response.status_code == 200
        exp_data = create_response.json()
        assert "experiment" in exp_data
        experiment = exp_data["experiment"]
        exp_id = experiment["id"]
        assert experiment["status"] == "draft"
        assert experiment["name"] == "Homepage CTA Test"

        # Step 2: Start experiment
        start_response = client.post(f"/api/v1/experiments/{exp_id}/start")
        assert start_response.status_code == 200
        exp_data = start_response.json()
        assert exp_data["experiment"]["status"] == "active"

        # Step 3: Record first result for variant a
        result_response = client.post(
            f"/api/v1/experiments/{exp_id}/record-result",
            json={"variant": "a", "metric_name": "ctr", "metric_value": 0.12},
        )
        assert result_response.status_code == 200
        exp_data = result_response.json()
        metrics = exp_data["experiment"].get("metrics", {})
        assert metrics["a"]["ctr"] == [0.12]

        # Step 4: Record second result for variant a
        result_response = client.post(
            f"/api/v1/experiments/{exp_id}/record-result",
            json={"variant": "a", "metric_name": "ctr", "metric_value": 0.18},
        )
        assert result_response.status_code == 200
        exp_data = result_response.json()
        metrics = exp_data["experiment"].get("metrics", {})
        assert metrics["a"]["ctr"] == [0.12, 0.18]

        # Step 5: Record first result for variant b
        result_response = client.post(
            f"/api/v1/experiments/{exp_id}/record-result",
            json={"variant": "b", "metric_name": "ctr", "metric_value": 0.10},
        )
        assert result_response.status_code == 200
        exp_data = result_response.json()
        metrics = exp_data["experiment"].get("metrics", {})
        assert metrics["b"]["ctr"] == [0.10]

        # Step 6: Record second result for variant b
        result_response = client.post(
            f"/api/v1/experiments/{exp_id}/record-result",
            json={"variant": "b", "metric_name": "ctr", "metric_value": 0.15},
        )
        assert result_response.status_code == 200
        exp_data = result_response.json()
        metrics = exp_data["experiment"].get("metrics", {})
        assert metrics["b"]["ctr"] == [0.10, 0.15]

        # Step 7: Conclude with winner='a'
        conclude_response = client.post(
            f"/api/v1/experiments/{exp_id}/conclude",
            json={"winner": "a"},
        )
        assert conclude_response.status_code == 200
        exp_data = conclude_response.json()
        experiment = exp_data["experiment"]
        assert experiment["status"] == "concluded"
        assert experiment["winner"] == "a"

        # Step 8: Assert spy captured the call to update_experiment_learnings
        assert len(spy_calls) == 1
        assert spy_calls[0] == exp_id

    @pytest.mark.asyncio
    async def test_conclude_invalid_winner(self, monkeypatch):
        """Conclude with invalid winner 'c' → 422 (Pydantic validation)."""
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        client = TestClient(app)

        # Create and start experiment
        create_response = client.post(
            "/api/v1/experiments",
            json={
                "name": "Test Experiment",
                "variant_a": {"option": "a"},
                "variant_b": {"option": "b"},
            },
        )
        exp_id = create_response.json()["experiment"]["id"]

        client.post(f"/api/v1/experiments/{exp_id}/start")

        # Try to conclude with invalid winner
        conclude_response = client.post(
            f"/api/v1/experiments/{exp_id}/conclude",
            json={"winner": "c"},
        )
        assert conclude_response.status_code == 422

    @pytest.mark.asyncio
    async def test_start_already_active_experiment(self, monkeypatch):
        """Start an already-active experiment → 400."""
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        client = TestClient(app)

        # Create and start experiment
        create_response = client.post(
            "/api/v1/experiments",
            json={
                "name": "Test Experiment",
                "variant_a": {"option": "a"},
                "variant_b": {"option": "b"},
            },
        )
        exp_id = create_response.json()["experiment"]["id"]

        client.post(f"/api/v1/experiments/{exp_id}/start")

        # Try to start again
        start_response = client.post(f"/api/v1/experiments/{exp_id}/start")
        assert start_response.status_code == 400
        assert "Only draft experiments can be started" in start_response.json()["detail"]

    @pytest.mark.asyncio
    async def test_get_experiment_not_found(self, monkeypatch):
        """Get unknown experiment ID → 404."""
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        client = TestClient(app)
        response = client.get("/api/v1/experiments/unknown-id-12345")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_record_result_not_found(self, monkeypatch):
        """Record result on unknown experiment → 404."""
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        client = TestClient(app)
        response = client.post(
            "/api/v1/experiments/unknown-id-12345/record-result",
            json={"variant": "a", "metric_name": "ctr", "metric_value": 0.12},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_conclude_not_found(self, monkeypatch):
        """Conclude unknown experiment → 404."""
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        client = TestClient(app)
        response = client.post(
            "/api/v1/experiments/unknown-id-12345/conclude",
            json={"winner": "a"},
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_list_experiments(self, monkeypatch):
        """List experiments returns empty list initially."""
        persistent_mock = PersistentMockSupabaseClient()
        import backend.database as db_mod
        monkeypatch.setattr(db_mod, "_client", persistent_mock)

        client = TestClient(app)
        response = client.get("/api/v1/experiments")
        assert response.status_code == 200
        data = response.json()
        assert "experiments" in data
        # Initially empty (MockSupabaseClient)
        assert isinstance(data["experiments"], list)
