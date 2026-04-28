# Graph Report - backend  (2026-04-20)

## Corpus Check
- Corpus is ~44,782 words - fits in a single context window. You may not need a graph.

## Summary
- 506 nodes · 1129 edges · 36 communities detected
- Extraction: 48% EXTRACTED · 52% INFERRED · 0% AMBIGUOUS · INFERRED: 590 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_API Routers|API Routers]]
- [[_COMMUNITY_Synthesis & Tests|Synthesis & Tests]]
- [[_COMMUNITY_Auth & Database|Auth & Database]]
- [[_COMMUNITY_Platform & Skills|Platform & Skills]]
- [[_COMMUNITY_Voice Service|Voice Service]]
- [[_COMMUNITY_Storyboard|Storyboard]]
- [[_COMMUNITY_Data Models|Data Models]]
- [[_COMMUNITY_Memory System|Memory System]]
- [[_COMMUNITY_Backend Module 8|Backend Module 8]]
- [[_COMMUNITY_Backend Module 9|Backend Module 9]]
- [[_COMMUNITY_Backend Module 10|Backend Module 10]]
- [[_COMMUNITY_Backend Module 11|Backend Module 11]]
- [[_COMMUNITY_Backend Module 12|Backend Module 12]]
- [[_COMMUNITY_Backend Module 13|Backend Module 13]]
- [[_COMMUNITY_Backend Module 14|Backend Module 14]]
- [[_COMMUNITY_Backend Module 15|Backend Module 15]]
- [[_COMMUNITY_Backend Module 16|Backend Module 16]]
- [[_COMMUNITY_Backend Module 17|Backend Module 17]]
- [[_COMMUNITY_Backend Module 18|Backend Module 18]]
- [[_COMMUNITY_Backend Module 19|Backend Module 19]]
- [[_COMMUNITY_Backend Module 20|Backend Module 20]]
- [[_COMMUNITY_Backend Module 21|Backend Module 21]]
- [[_COMMUNITY_Backend Module 22|Backend Module 22]]
- [[_COMMUNITY_Backend Module 23|Backend Module 23]]
- [[_COMMUNITY_Backend Module 24|Backend Module 24]]
- [[_COMMUNITY_Backend Module 25|Backend Module 25]]
- [[_COMMUNITY_Backend Module 26|Backend Module 26]]
- [[_COMMUNITY_Backend Module 27|Backend Module 27]]
- [[_COMMUNITY_Backend Module 28|Backend Module 28]]
- [[_COMMUNITY_Backend Module 29|Backend Module 29]]
- [[_COMMUNITY_Backend Module 30|Backend Module 30]]
- [[_COMMUNITY_Backend Module 31|Backend Module 31]]
- [[_COMMUNITY_Backend Module 32|Backend Module 32]]
- [[_COMMUNITY_Backend Module 33|Backend Module 33]]
- [[_COMMUNITY_Backend Module 34|Backend Module 34]]
- [[_COMMUNITY_Backend Module 35|Backend Module 35]]

## God Nodes (most connected - your core abstractions)
1. `get_supabase()` - 62 edges
2. `script_to_storyboard()` - 25 edges
3. `MockQueryBuilder` - 20 edges
4. `StrategyDocument` - 19 edges
5. `_build_prompt()` - 18 edges
6. `_run_generation()` - 16 edges
7. `embed_trending_batch()` - 15 edges
8. `_detect_hook_style()` - 14 edges
9. `generate_strategy_document()` - 14 edges
10. `generate_suggestions()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `_run_generation()` --calls--> `render_video()`  [INFERRED]
  backend\content\router.py → backend\content\renderer_video.py
- `Shared test fixtures — forces mock mode, no real API calls.` --uses--> `MockSupabaseClient`  [INFERRED]
  backend\tests\conftest.py → backend\database.py
- `Every test gets a fresh MockSupabaseClient — no real DB calls.` --uses--> `MockSupabaseClient`  [INFERRED]
  backend\tests\conftest.py → backend\database.py
- `Reset all lazy-init Gemini singletons so no real API keys are used.` --uses--> `MockSupabaseClient`  [INFERRED]
  backend\tests\conftest.py → backend\database.py
- `Realistic enriched trending posts with content_analysis.` --uses--> `MockSupabaseClient`  [INFERRED]
  backend\tests\conftest.py → backend\database.py

## Communities

### Community 0 - "API Routers"
Cohesion: 0.11
Nodes (57): get_supabase(), MockQueryBuilder, Fluent builder that absorbs any chained call and returns safe empty data     on, job_general_trending(), Weekly platform-wide trending scrape — not keyword filtered., check_topic_overlap(), Record learning signals from the user's strategy review modifications.      Ca, Record learning signals when a user edits a generated script.      Captures: (+49 more)

### Community 1 - "Synthesis & Tests"
Cohesion: 0.06
Nodes (35): generate_script(), Generate a content script using Gemini with Anthropic fallback.      *research_c, compute_relevance_score(), enrich_trending_posts(), extract_common_patterns(), _gemini_json(), _generate_alternatives(), generate_strategy_document() (+27 more)

### Community 2 - "Auth & Database"
Cohesion: 0.06
Nodes (30): mock_supabase(), Shared test fixtures — forces mock mode, no real API calls., Realistic brand profile dict., Realistic publication memory dict., Reset all lazy-init Gemini singletons so no real API keys are used., Realistic enriched trending posts with content_analysis., Every test gets a fresh MockSupabaseClient — no real DB calls., reset_genai_clients() (+22 more)

### Community 3 - "Platform & Skills"
Cohesion: 0.07
Nodes (26): adapt_voice_to_platform(), get_platform_group(), get_platform_rules(), get_secondary_platforms(), Platform Adapter — platform rules knowledge base + voice adaptation.  Provides:, Return platform-specific best practices and content rules.      Keys in the retu, Use Gemini to adapt a brand voice for a specific platform's conventions.      Re, _build_prompt() (+18 more)

### Community 4 - "Voice Service"
Cohesion: 0.1
Nodes (22): create_workflow_endpoint(), build_apify_config_from_questionnaire(), create_workflow(), Tests for backend.intelligence.voice — competitor parsing + data structures., TestDataStructures, TestParseCompetitors, BrandProfile, build_voice_config() (+14 more)

### Community 5 - "Storyboard"
Cohesion: 0.1
Nodes (13): Normalise a section label line: strip **, *, (#...), timing markers, and trailin, script_to_storyboard(), _slides_storyboard(), _strip_label(), _talking_head_storyboard(), _video_storyboard(), Tests for backend.content.storyboard — script to frame conversion., Verify AGENTS.md contract: every frame has bg_gradient, accent_color, headline, (+5 more)

### Community 6 - "Data Models"
Cohesion: 0.17
Nodes (25): BaseModel, BrandUpdate, ContentEditRequest, ContentGenerateRequest, ExperimentCreate, ExperimentResponse, ExperimentResult, ExperimentUpdate (+17 more)

### Community 7 - "Memory System"
Cohesion: 0.14
Nodes (5): _detect_hook_style(), _topics_similar(), Tests for backend.intelligence.memory — pure helper functions., TestDetectHookStyle, TestTopicsSimilar

### Community 8 - "Backend Module 8"
Cohesion: 0.16
Nodes (19): _content_hash(), embed_and_store(), embed_image(), embed_text(), embed_texts_batch(), embed_trending_batch(), _get_genai_client(), RAG module for Content Hub.  Handles embedding generation, vector storage, simil (+11 more)

### Community 9 - "Backend Module 9"
Cohesion: 0.1
Nodes (21): Content Pillars and Topic Clusters, Searchable vs Shareable Content, Content Strategy, Quick Copy Editing for Social Scripts, Seven Sweeps Framework, Copy Editing, Clarity Sweep, So What Sweep (+13 more)

### Community 10 - "Backend Module 10"
Cohesion: 0.19
Nodes (17): _build_actor_input(), _build_general_trending_input(), _build_profile_input(), _mock_general_results(), _mock_results(), _normalize_post(), Scrape platform-wide trending content without keyword/competitor filter.      Re, Build Apify actor input for general trending (no keyword filter). (+9 more)

### Community 11 - "Backend Module 11"
Cohesion: 0.19
Nodes (16): _build_brief_user_prompt(), _fallback_brief(), generate_research_brief(), get_full_research_context(), _get_genai_client(), _get_memory(), _get_raw_trending(), _get_recent_published() (+8 more)

### Community 12 - "Backend Module 12"
Cohesion: 0.12
Nodes (16): Hard Gate - Design Before Implementation, Brainstorming Process, Brainstorming Ideas Into Designs, Rationale: Hard gate on design before implementation, Rationale: Why test-first matters, Subagent-Driven Development, Two-Stage Review Process, Four Phases of Debugging (+8 more)

### Community 13 - "Backend Module 13"
Cohesion: 0.23
Nodes (10): _get_active_workflows(), job_detect_trends(), job_flag_rejections(), job_generate_suggestions(), job_scrape_organic(), job_weekly_embed_refresh(), start_scheduler(), lifespan() (+2 more)

### Community 14 - "Backend Module 14"
Cohesion: 0.22
Nodes (6): _placeholder_script(), Return a minimal placeholder when no LLM is available., Tests for backend.content.scripting — prompt construction + placeholder fallback, Placeholder output must be parseable by storyboard.py., Placeholder output must be parseable by storyboard.py., TestPlaceholderScript

### Community 15 - "Backend Module 15"
Cohesion: 0.25
Nodes (5): delete_files(), Delete a list of Supabase Storage files by their public URLs.      Extracts the, upload_file(), render_slides(), package_talking_head()

### Community 16 - "Backend Module 16"
Cohesion: 0.29
Nodes (7): Growth Experimentation Program, Hypothesis Framework, ICE Prioritization, Metrics Selection, A/B Test Setup, Statistical Rigor, Rationale: Why use hypothesis framework

### Community 17 - "Backend Module 17"
Cohesion: 0.67
Nodes (2): BaseSettings, Settings

### Community 18 - "Backend Module 18"
Cohesion: 0.67
Nodes (2): fetch_video(), Fetches video metadata and optionally downloads the actual video file.     Use d

### Community 19 - "Backend Module 19"
Cohesion: 1.0
Nodes (1): render_video()

### Community 20 - "Backend Module 20"
Cohesion: 1.0
Nodes (1): Daily Suggestions — generates ranked content suggestions enriched with user memo

### Community 21 - "Backend Module 21"
Cohesion: 1.0
Nodes (2): Context Document Sections, Product Marketing Context

### Community 22 - "Backend Module 22"
Cohesion: 1.0
Nodes (2): Verification Before Completion, Gate Function: Evidence Before Claims

### Community 23 - "Backend Module 23"
Cohesion: 1.0
Nodes (0): 

### Community 24 - "Backend Module 24"
Cohesion: 1.0
Nodes (0): 

### Community 25 - "Backend Module 25"
Cohesion: 1.0
Nodes (0): 

### Community 26 - "Backend Module 26"
Cohesion: 1.0
Nodes (0): 

### Community 27 - "Backend Module 27"
Cohesion: 1.0
Nodes (0): 

### Community 28 - "Backend Module 28"
Cohesion: 1.0
Nodes (0): 

### Community 29 - "Backend Module 29"
Cohesion: 1.0
Nodes (0): 

### Community 30 - "Backend Module 30"
Cohesion: 1.0
Nodes (0): 

### Community 31 - "Backend Module 31"
Cohesion: 1.0
Nodes (0): 

### Community 32 - "Backend Module 32"
Cohesion: 1.0
Nodes (0): 

### Community 33 - "Backend Module 33"
Cohesion: 1.0
Nodes (0): 

### Community 34 - "Backend Module 34"
Cohesion: 1.0
Nodes (0): 

### Community 35 - "Backend Module 35"
Cohesion: 1.0
Nodes (1): Dispatching Parallel Agents

## Knowledge Gaps
- **114 isolated node(s):** `Mimics supabase-py's APIResponse.`, `Fluent builder that absorbs any chained call and returns safe empty data     on`, `Raises so auth/router.py fallback is always triggered.`, `Mock RPC — always returns empty result.`, `Abort startup when running in production with any required secret unset.      Se` (+109 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Backend Module 19`** (2 nodes): `renderer_video.py`, `render_video()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 20`** (2 nodes): `suggestions.py`, `Daily Suggestions — generates ranked content suggestions enriched with user memo`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 21`** (2 nodes): `Context Document Sections`, `Product Marketing Context`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 22`** (2 nodes): `Verification Before Completion`, `Gate Function: Evidence Before Claims`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 23`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 24`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 25`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 26`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 27`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 28`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 29`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 30`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 31`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 32`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 33`** (1 nodes): `templates.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 34`** (1 nodes): `__init__.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Backend Module 35`** (1 nodes): `Dispatching Parallel Agents`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_supabase()` connect `API Routers` to `Synthesis & Tests`, `Auth & Database`, `Voice Service`, `Backend Module 8`, `Backend Module 10`, `Backend Module 11`, `Backend Module 13`, `Backend Module 15`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Why does `_run_generation()` connect `API Routers` to `Synthesis & Tests`, `Platform & Skills`, `Storyboard`, `Backend Module 11`, `Backend Module 15`, `Backend Module 19`?**
  _High betweenness centrality (0.176) - this node is a cross-community bridge._
- **Why does `script_to_storyboard()` connect `Storyboard` to `API Routers`, `Synthesis & Tests`, `Backend Module 14`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Are the 59 inferred relationships involving `get_supabase()` (e.g. with `signup()` and `login()`) actually correct?**
  _`get_supabase()` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `script_to_storyboard()` (e.g. with `_run_generation()` and `test_full_pipeline_slides()`) actually correct?**
  _`script_to_storyboard()` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `StrategyDocument` (e.g. with `TestHappyPathPipeline` and `Integration test: Happy-path E2E pipeline.  Exercises: Workflow fetch -> Synthes`) actually correct?**
  _`StrategyDocument` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `_build_prompt()` (e.g. with `get_platform_rules()` and `load_skill_sections()`) actually correct?**
  _`_build_prompt()` has 15 INFERRED edges - model-reasoned connections that need verification._