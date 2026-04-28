# -*- coding: utf-8 -*-
"""
Content Hub - E2E Smoke Test
Run with:  python smoke_test.py
"""
import asyncio
import os
import sys
import traceback
from datetime import datetime
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
def ok(msg):   print(f"  {GREEN}[PASS]{RESET} {msg}")
def fail(msg): print(f"  {RED}[FAIL]{RESET} {msg}")
def warn(msg): print(f"  {YELLOW}[WARN]{RESET} {msg}")
def info(msg): print(f"       --> {msg}")
def section(title):
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}  {title}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
results = {}
# -------------------------------------------------------------------
# STEP 1 - ENV & Config
# -------------------------------------------------------------------
section("STEP 1 - ENV & Config")
from dotenv import load_dotenv
load_dotenv()
raw = {
    "SUPABASE_URL":         os.getenv("SUPABASE_URL"),
    "SUPABASE_SERVICE_KEY": os.getenv("SUPABASE_SERVICE_KEY"),
    "SUPABASE_KEY":         os.getenv("SUPABASE_KEY"),
    "GOOGLE_AI_STUDIO_KEY": os.getenv("GOOGLE_AI_STUDIO_KEY"),
    "APIFY_API_TOKEN":      os.getenv("APIFY_API_TOKEN"),
}
for k, v in raw.items():
    if v and not v.startswith("your-"):
        ok(f"{k} = {v[:35]}...")
    else:
        warn(f"{k} is MISSING or placeholder")
try:
    from backend.config import settings
    ok("pydantic settings loaded OK")
    info(f"supabase_url             = {settings.supabase_url[:50] if settings.supabase_url else 'EMPTY'}")
    info(f"supabase_service_role_key= {'SET (' + settings.supabase_service_role_key[:20] + '...)' if settings.supabase_service_role_key else 'EMPTY <-- key name mismatch in .env'}")
    info(f"supabase_anon_key        = {'SET' if settings.supabase_anon_key else 'EMPTY'}")
    info(f"google_ai_studio_key     = {'SET (' + settings.google_ai_studio_key[:20] + '...)' if settings.google_ai_studio_key else 'EMPTY'}")
    info(f"apify_api_key            = {'SET' if settings.apify_api_key else 'EMPTY'}")
    results["env"] = True
except Exception as e:
    fail(f"Config load failed: {e}")
    traceback.print_exc()
    results["env"] = False
# -------------------------------------------------------------------
# STEP 2 - Supabase Connectivity
# -------------------------------------------------------------------
section("STEP 2 - Supabase Connectivity")
try:
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
    if not url or not key:
        fail("SUPABASE_URL or key missing from environment")
        results["supabase"] = False
    else:
        sb = create_client(url, key)
        ok(f"Supabase client connected -> {url}")
        results["_sb"] = sb
        tables = [
            "workflows", "content_items", "trending_content",
            "content_embeddings", "content_publication_memory"
        ]
        all_ok = True
        for table in tables:
            try:
                r = sb.table(table).select("id").limit(1).execute()
                ok(f"Table '{table}' accessible")
            except Exception as e:
                fail(f"Table '{table}': {e}")
                all_ok = False
        # Test match_embeddings RPC (1536-dim — upgraded schema)
        try:
            test_vec = [0.0] * 1536
            r = sb.rpc("match_embeddings", {
                "query_embedding": test_vec,
                "match_workflow_id": "00000000-0000-0000-0000-000000000000",
                "match_count": 1,
            }).execute()
            ok(f"match_embeddings() RPC exists (returned {len(r.data)} rows for dummy workflow)")
        except Exception as e:
            fail(f"match_embeddings RPC: {e}")
            info("Migration 002_multimodal_embeddings.sql may not have been applied to Supabase")
            all_ok = False
        # Grab a real workflow_id
        wf = sb.table("workflows").select("id,name").limit(1).execute()
        if wf.data:
            results["workflow_id"] = wf.data[0]["id"]
            ok(f"Found workflow: '{wf.data[0]['name']}' ({results['workflow_id']})")
        else:
            warn("No workflows in DB yet")
            results["workflow_id"] = None
        results["supabase"] = all_ok
except Exception as e:
    fail(f"Supabase failed: {e}")
    traceback.print_exc()
    results["supabase"] = False
    results["workflow_id"] = None
# -------------------------------------------------------------------
# STEP 3 - Trending Content
# -------------------------------------------------------------------
section("STEP 3 - Trending Content in DB")
try:
    sb = results.get("_sb")
    wf_id = results.get("workflow_id")
    if sb and wf_id:
        r = (
            sb.table("trending_content")
            .select("id,title,platform,organic_score")
            .eq("workflow_id", wf_id)
            .order("organic_score", desc=True)
            .limit(5)
            .execute()
        )
        if r.data:
            ok(f"Found {len(r.data)} trending items")
            for t in r.data:
                info(f"[{t.get('platform','?')}] score={t.get('organic_score','?')} | {str(t.get('title',''))[:70]}")
            results["trending"] = True
        else:
            warn("No trending content yet (Apify hasn't run or no workflow data)")
            results["trending"] = False
    else:
        warn("Skipping - no Supabase connection or no workflow")
        results["trending"] = False
except Exception as e:
    fail(f"Trending read failed: {e}")
    results["trending"] = False
# -------------------------------------------------------------------
# STEP 4 - Gemini Embedding
# -------------------------------------------------------------------
section("STEP 4 - Gemini Embedding (rag.py)")
async def test_embedding():
    try:
        from backend.research.rag import embed_text, EMBEDDING_MODEL, EMBEDDING_DIMENSION
        info(f"Model: {EMBEDDING_MODEL}  Dimension: {EMBEDDING_DIMENSION}")
        vec = await embed_text("The best performing fitness content this week")
        if vec and len(vec) == EMBEDDING_DIMENSION:
            ok(f"embed_text() -> {len(vec)}-dim vector (first val: {vec[0]:.6f})")
            return True
        else:
            fail(f"Unexpected vector length: {len(vec) if vec else 'NONE'}")
            return False
    except RuntimeError as e:
        fail(f"API key issue: {e}")
        return False
    except Exception as e:
        fail(f"Embedding failed: {e}")
        traceback.print_exc()
        return False
results["embedding"] = asyncio.run(test_embedding())
# -------------------------------------------------------------------
# STEP 5 - Vector Search
# -------------------------------------------------------------------
section("STEP 5 - Vector Search (search_similar)")
async def test_vector_search():
    wf_id = results.get("workflow_id")
    if not wf_id:
        warn("No workflow_id - skipping")
        return None
    try:
        from backend.research.rag import search_similar
        hits = await search_similar(wf_id, "fitness motivation", limit=3)
        if hits:
            ok(f"search_similar() returned {len(hits)} hits")
            for h in hits:
                info(f"similarity={h.get('similarity',0):.3f} | {str(h.get('content_text',''))[:70]}")
        else:
            warn("0 results - no embeddings stored yet (run embed_trending_batch first)")
        return True
    except Exception as e:
        fail(f"Vector search failed: {e}")
        traceback.print_exc()
        return False
results["vector_search"] = asyncio.run(test_vector_search())
# -------------------------------------------------------------------
# STEP 6 - Research Brief
# -------------------------------------------------------------------
section("STEP 6 - Research Brief (research_service.py)")
async def test_research_brief():
    wf_id = results.get("workflow_id")
    if not wf_id:
        warn("No workflow_id - skipping")
        return None
    try:
        from backend.research.research_service import get_full_research_context
        ctx = await get_full_research_context(wf_id, "fitness motivation", "short_form")
        brief = ctx.get("research_brief", "")
        if brief and len(brief) > 50:
            ok(f"Research brief generated ({len(brief)} chars)")
            info(brief[:250].strip() + "...")
            return True
        else:
            warn(f"Brief too short or empty: '{brief[:100]}'")
            return False
    except Exception as e:
        fail(f"Research brief failed: {e}")
        traceback.print_exc()
        return False
results["research"] = asyncio.run(test_research_brief())
# -------------------------------------------------------------------
# STEP 7 - Script Generation
# -------------------------------------------------------------------
section("STEP 7 - Script Generation (scripting.py)")
async def test_script():
    try:
        from backend.content.scripting import generate_script
        result = await generate_script(
            content_type="short_form",
            topic="3 morning habits that doubled my energy",
            brand_voice="clear, confident, no-fluff",
            content_pillars=["health", "productivity"],
            research_context={"research_brief": "Focus on actionable morning routines."},
            memory={},
            platform="tiktok",
        )
        script = result.get("script", "")
        model  = result.get("model_used", "?")
        if script and len(script) > 30:
            ok(f"Script generated via '{model}' ({len(script)} chars)")
            info(script[:300].strip())
            return True
        else:
            fail(f"Empty script (model={model})")
            return False
    except Exception as e:
        fail(f"Script generation failed: {e}")
        traceback.print_exc()
        return False
results["scripting"] = asyncio.run(test_script())
# -------------------------------------------------------------------
# SUMMARY
# -------------------------------------------------------------------
section("SMOKE TEST SUMMARY")
checks = [
    ("ENV / Config",          results.get("env")),
    ("Supabase Connectivity", results.get("supabase")),
    ("Trending Data in DB",   results.get("trending")),
    ("Gemini Embedding",      results.get("embedding")),
    ("Vector Search",         results.get("vector_search")),
    ("Research Brief",        results.get("research")),
    ("Script Generation",     results.get("scripting")),
]
passed = failed = skipped = 0
for name, status in checks:
    if status is True:
        ok(name)
        passed += 1
    elif status is False:
        fail(name)
        failed += 1
    else:
        warn(f"{name}  <-- SKIPPED")
        skipped += 1
print(f"\n  Result: {passed} passed | {failed} failed | {skipped} skipped")
print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()
if failed > 0:
    print("  Fix the FAILED steps above before proceeding.")
else:
    print("  Pipeline healthy - multimodal RAG upgrade active!")
print()
sys.exit(0 if failed == 0 else 1)
