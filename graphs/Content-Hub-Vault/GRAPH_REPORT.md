# Graph Report - Content-Hub-Vault  (2026-04-20)

## Corpus Check
- 155 files · ~50,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 298 nodes · 298 edges · 47 communities detected
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 29 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Phase 3 Implementation & Auth|Phase 3 Implementation & Auth]]
- [[_COMMUNITY_Content Types & Frontend Stack|Content Types & Frontend Stack]]
- [[_COMMUNITY_API Routes & DB Schema|API Routes & DB Schema]]
- [[_COMMUNITY_Brand Config System|Brand Config System]]
- [[_COMMUNITY_Frontend Pages & Navigation|Frontend Pages & Navigation]]
- [[_COMMUNITY_CLAUDE.md Refactor & Phase 2 Sessions|CLAUDE.md Refactor & Phase 2 Sessions]]
- [[_COMMUNITY_Content Pillars & Formats|Content Pillars & Formats]]
- [[_COMMUNITY_Backend Intelligence & Synthesis|Backend Intelligence & Synthesis]]
- [[_COMMUNITY_Feature Pattern Extraction|Feature Pattern Extraction]]
- [[_COMMUNITY_UI Sidebar & Auth Components|UI Sidebar & Auth Components]]
- [[_COMMUNITY_Organic Content Filtering|Organic Content Filtering]]
- [[_COMMUNITY_Learning Loop Architecture|Learning Loop Architecture]]
- [[_COMMUNITY_Phase 3 Audit & Remediation|Phase 3 Audit & Remediation]]
- [[_COMMUNITY_Phase 4 AB Testing Sessions|Phase 4 AB Testing Sessions]]
- [[_COMMUNITY_Research & Storage Backend|Research & Storage Backend]]
- [[_COMMUNITY_Orchestrated Execution Sessions|Orchestrated Execution Sessions]]
- [[_COMMUNITY_Skill Brainstorming|Skill Brainstorming]]
- [[_COMMUNITY_Brand Voice & Typography|Brand Voice & Typography]]
- [[_COMMUNITY_Brand Colors|Brand Colors]]
- [[_COMMUNITY_Content Calendar & Library Pages|Content Calendar & Library Pages]]
- [[_COMMUNITY_Session Logs (Apr 16)|Session Logs (Apr 16)]]
- [[_COMMUNITY_Phase 3 Complete Status|Phase 3 Complete Status]]
- [[_COMMUNITY_Tasks & Findings Backlog|Tasks & Findings Backlog]]
- [[_COMMUNITY_Verification Gate Pattern|Verification Gate Pattern]]
- [[_COMMUNITY_Skill Writing Plans|Skill Writing Plans]]
- [[_COMMUNITY_Phase 2 Tasks|Phase 2 Tasks]]
- [[_COMMUNITY_Trend Detection Spikes|Trend Detection Spikes]]
- [[_COMMUNITY_Scrape & Trending Workflows|Scrape & Trending Workflows]]
- [[_COMMUNITY_Orchestrated Execution Skill|Orchestrated Execution Skill]]
- [[_COMMUNITY_Gen Tree Module|Gen Tree Module]]
- [[_COMMUNITY_Resume Orchestration Skill|Resume Orchestration Skill]]
- [[_COMMUNITY_Phase 3 Remediation Logs|Phase 3 Remediation Logs]]
- [[_COMMUNITY_Parallel Dispatch Pattern|Parallel Dispatch Pattern]]
- [[_COMMUNITY_Brand Config Module|Brand Config Module]]
- [[_COMMUNITY_Content Storyboard|Content Storyboard]]
- [[_COMMUNITY_Intelligence Rejection Logic|Intelligence Rejection Logic]]
- [[_COMMUNITY_Content Requests Handler|Content Requests Handler]]
- [[_COMMUNITY_Selection Memory Update|Selection Memory Update]]
- [[_COMMUNITY_Suggestion Generator|Suggestion Generator]]
- [[_COMMUNITY_Skill Section Loader|Skill Section Loader]]
- [[_COMMUNITY_Content Init Module|Content Init Module]]
- [[_COMMUNITY_Intelligence Init|Intelligence Init]]
- [[_COMMUNITY_Storage Client Module|Storage Client Module]]
- [[_COMMUNITY_Workflow API Module|Workflow API Module]]
- [[_COMMUNITY_Dashboard Page|Dashboard Page]]
- [[_COMMUNITY_Workflow Pages|Workflow Pages]]
- [[_COMMUNITY_Shared Types Library|Shared Types Library]]

## God Nodes (most connected - your core abstractions)
1. `Content Hub` - 18 edges
2. `Phase 3 Complete: All 7 Tasks Delivered` - 12 edges
3. `content.router` - 11 edges
4. `Orchestrated Execution` - 9 edges
5. `API Client Library` - 9 edges
6. `Final Implementation Plan (7 tasks)` - 8 edges
7. `T1.2 Multi-User Auth Hardening (Supabase JWT)` - 8 edges
8. `Content Calendar Page` - 8 edges
9. `Workflows Table` - 7 edges
10. `Phase 2 Production Execution (MVP Waves 1-4)` - 6 edges

## Surprising Connections (you probably didn't know these)
- `T1.2 Multi-User Auth Hardening (Supabase JWT)` --implements--> `JWT Authentication System (T1.2)`  [EXTRACTED]
  Content-Hub-Vault/00-Management/Sessions/2026-04-15_T1.2_Multi_User_Auth_Hardening.md → backend/auth/dependencies.py, backend/auth/router.py, frontend/lib/api.ts
- `A/B Testing Experiments System (Phase 4)` --references--> `F-02: conclude_experiment not calling update_experiment_learnings`  [EXTRACTED]
  backend/experiments/models.py, backend/experiments/router.py, backend/intelligence/memory.py, backend/intelligence/synthesis.py → Content-Hub-Vault/00-Management/Sessions/2026-04-20_Phase3_Remediation_Verification_Audit.md
- `A/B Testing Experiments System (Phase 4)` --references--> `F-06: record_result has no status guard`  [EXTRACTED]
  backend/experiments/models.py, backend/experiments/router.py, backend/intelligence/memory.py, backend/intelligence/synthesis.py → Content-Hub-Vault/00-Management/Sessions/2026-04-20_Phase3_Remediation_Verification_Audit.md
- `A/B Testing Experiments System (Phase 4)` --references--> `F-05: ExperimentResult.variant has no validation`  [EXTRACTED]
  backend/experiments/models.py, backend/experiments/router.py, backend/intelligence/memory.py, backend/intelligence/synthesis.py → Content-Hub-Vault/00-Management/Sessions/2026-04-20_Phase3_Remediation_Verification_Audit.md
- `Migration 006 A/B Experiments` --implements--> `A/B Testing Experiments System (Phase 4)`  [EXTRACTED]
  supabase/migrations/006_ab_experiments.sql → backend/experiments/models.py, backend/experiments/router.py, backend/intelligence/memory.py, backend/intelligence/synthesis.py

## Communities

### Community 0 - "Phase 3 Implementation & Auth"
Cohesion: 1.0
Nodes (43): A/B Testing: Advisory Integration via Skill, Frontend Component: AuthProvider, JWT Authentication System (T1.2), Server-Side Content Search (T2.2), Transition Style Markers (T3.1), General Trending Scrape (T3.2), Production Deployment Checklist, Finding: reference_creators Unused in Pipeline (+35 more)

### Community 1 - "Content Types & Frontend Stack"
Cohesion: 1.0
Nodes (34): Brand API, Content API, Workflows API, Brand Color System, Brand Configuration, Brand Typography, Brand Voice Signature, Generating Status (+26 more)

### Community 2 - "API Routes & DB Schema"
Cohesion: 1.0
Nodes (28): Content Generate From Strategy API, Content Synthesize API, Workflows Scrape API, Workflows Trending API, Sidebar Component, API Client Library, Auth Utilities, Multimodal Embeddings Migration (+20 more)

### Community 3 - "Brand Config System"
Cohesion: 1.0
Nodes (27): adapt_for_platform, BrandProfile, check_topic_overlap, content.models, content.platform_adapter, content.renderer_slides, content.renderer_talking_head, content.renderer_video (+19 more)

### Community 4 - "Frontend Pages & Navigation"
Cohesion: 1.0
Nodes (23): brand-agent, db-agent, frontend-agent, intelligence-agent, pipeline-agent, research-agent, Agentic Second Brain (ASB) Framework, Phase 1: The Seed Brain (Current State) (+15 more)

### Community 5 - "CLAUDE.md Refactor & Phase 2 Sessions"
Cohesion: 1.0
Nodes (17): Multi-Agent Dispatch Pattern, Red-Green-Refactor Cycle, Root Cause Investigation, Phase 1: Recon and Exploration, Phase 2: Task Decomposition and Planning, Phase 3: User Approval, Phase 4: Parallel Execution, Phase 5: Result Handling and Stuck Agent Recovery (+9 more)

### Community 6 - "Content Pillars & Formats"
Cohesion: 1.0
Nodes (14): Content Pillars & Topic Clustering, Hook Formulas for Social Content, A/B Test Hypothesis Framework, ICE Prioritization Framework, Mental Models for Marketing, Seven Sweeps Copy Editing Framework, A/B Test Setup Skill, Content Strategy Skill (+6 more)

### Community 7 - "Backend Intelligence & Synthesis"
Cohesion: 1.0
Nodes (12): Workflow Templates, Guided Questionnaire, Life & Business Coaching Niche, Finance & Investing Niche, Fitness & Health Niche, Real Estate Niche, Software Development Niche, Instagram Platform (+4 more)

### Community 8 - "Feature Pattern Extraction"
Cohesion: 1.0
Nodes (10): Pattern Extraction & Performance Estimation, Remotion Rendering Microservice, Storyboard Enrichment with Timing & Transitions, Strategy Revision Loop, CRITICAL: Missing brand-assets Storage Bucket, CRITICAL: Missing HookBodyCTAComposition.tsx, CRITICAL: Port Mismatch (Remotion 3001 vs config 3100), CRITICAL: Regenerate Notes Parameter Mismatch (+2 more)

### Community 9 - "UI Sidebar & Auth Components"
Cohesion: 1.0
Nodes (9): A/B Testing Experiments System (Phase 4), F-02: conclude_experiment not calling update_experiment_learnings, F-05: ExperimentResult.variant has no validation, F-06: record_result has no status guard, F-07: updated_at not set on start and record-result, Migration 006 A/B Experiments, Phase 4 A/B Testing Frontend Recon & Planning, Phase 4 A/B Testing Server-Side (Complete) (+1 more)

### Community 10 - "Organic Content Filtering"
Cohesion: 1.0
Nodes (8): Organic Content Filtering (Non-Sponsored), Research Brief Generation, Apify Web Scraping Client, Organic Content Scoring Engine, RAG (Retrieval-Augmented Generation), Research Service (Orchestration Layer), Scheduler Jobs (APScheduler), Video Downloader (yt-dlp wrapper)

### Community 11 - "Learning Loop Architecture"
Cohesion: 1.0
Nodes (6): Architecture: The Learning Loop (Intelligence), Architecture: Platform Strategy (Setup Phase), Architecture: Script Generation (Creation Phase), Architecture: Content Synthesis (Strategy Review), Architecture: Trending Intelligence (Discovery Phase), Architecture: Voice Configuration (Setup Phase)

### Community 12 - "Phase 3 Audit & Remediation"
Cohesion: 1.0
Nodes (6): Brain in a Jar Structural Gap (Orchestrator Tools Limitation), Claude Code Orchestration Architecture (Advisor + Subagents), Orchestrate Skill Compaction Recovery Fix, Orchestrated Execution Skill Design, Orchestrator Deep Dive & Architecture Audit, State Persistence Fix for Orchestration (Compaction Recovery)

### Community 13 - "Phase 4 AB Testing Sessions"
Cohesion: 1.0
Nodes (5): MVP Completion Plan: 4 Days (Apr 9-13), Session: Day 1 E2E Pipeline Smoke Test, Session: Day 2 MVP Backend (Platform Strategy, Learning Loops, Skills), Session: Day 3 Code Review Audit, Session: Day 3 Frontend Polish & E2E Verification

### Community 14 - "Research & Storage Backend"
Cohesion: 1.0
Nodes (5): Authentication Dependencies, Authentication Router, Backend Configuration Module, Database Client and Mock Mode, FastAPI Main Application

### Community 15 - "Orchestrated Execution Sessions"
Cohesion: 1.0
Nodes (4): Phase 3 Loose Ends - Critical Issues, Current Sprint: Phase 3 Completion, Phase 2 Production Tasks, Phase 3 Remediation Tasks

### Community 16 - "Skill Brainstorming"
Cohesion: 1.0
Nodes (3): Brainstorming Skill (Design Before Implementation), Executing Plans Skill, Finishing Development Branch Skill

### Community 17 - "Brand Voice & Typography"
Cohesion: 1.0
Nodes (3): brand.models, brand.router, BrandUpdate

### Community 18 - "Brand Colors"
Cohesion: 1.0
Nodes (3): build_voice_config, parse_brand_persona, VoiceConfig

### Community 19 - "Content Calendar & Library Pages"
Cohesion: 1.0
Nodes (3): Authentication API, Login Page, Signup Page

### Community 20 - "Session Logs (Apr 16)"
Cohesion: 1.0
Nodes (2): APScheduler Jobs Configuration, 2026-04-13 Day 4 Final Hardening

### Community 21 - "Phase 3 Complete Status"
Cohesion: 1.0
Nodes (2): Test Infrastructure: Offline Wall (Mock Supabase & Gemini), Phase 2.5: Test Infrastructure

### Community 22 - "Tasks & Findings Backlog"
Cohesion: 1.0
Nodes (2): Remotion Shared-Secret Authentication (T2.1), T2.1 Remotion Authentication (Shared-Secret)

### Community 23 - "Verification Gate Pattern"
Cohesion: 1.0
Nodes (2): Verification Gate Function, Verification Before Completion

### Community 24 - "Skill Writing Plans"
Cohesion: 1.0
Nodes (2): Writing Plans, Specification Coverage Self-Review

### Community 25 - "Phase 2 Tasks"
Cohesion: 1.0
Nodes (2): Project Phase Status Tracking, MVP Completion Tasks

### Community 26 - "Trend Detection Spikes"
Cohesion: 1.0
Nodes (2): detect_trend_spikes, intelligence.triggers

### Community 27 - "Scrape & Trending Workflows"
Cohesion: 1.0
Nodes (2): Workflow Pydantic Models, Workflow API Router

### Community 28 - "Orchestrated Execution Skill"
Cohesion: 1.0
Nodes (1): Orchestration Skill

### Community 29 - "Gen Tree Module"
Cohesion: 1.0
Nodes (1): Actual Generation Tree (Audit 2026-04-14)

### Community 30 - "Resume Orchestration Skill"
Cohesion: 1.0
Nodes (1): Orchestrations README

### Community 31 - "Phase 3 Remediation Logs"
Cohesion: 1.0
Nodes (1): Phase 3 Completion & Vault Update

### Community 32 - "Parallel Dispatch Pattern"
Cohesion: 1.0
Nodes (1): Parallel Agent Dispatch Skill

### Community 33 - "Brand Config Module"
Cohesion: 1.0
Nodes (1): brand.__init__

### Community 34 - "Content Storyboard"
Cohesion: 1.0
Nodes (1): content.storyboard

### Community 35 - "Intelligence Rejection Logic"
Cohesion: 1.0
Nodes (1): intelligence.rejection

### Community 36 - "Content Requests Handler"
Cohesion: 1.0
Nodes (1): ContentGenerateRequest, ContentEditRequest, SynthesizeRequest, StrategyGenerateRequest

### Community 37 - "Selection Memory Update"
Cohesion: 1.0
Nodes (1): update_selection_memory

### Community 38 - "Suggestion Generator"
Cohesion: 1.0
Nodes (1): generate_suggestions

### Community 39 - "Skill Section Loader"
Cohesion: 1.0
Nodes (1): load_skill_sections

### Community 40 - "Content Init Module"
Cohesion: 1.0
Nodes (1): content.__init__

### Community 41 - "Intelligence Init"
Cohesion: 1.0
Nodes (1): intelligence.__init__

### Community 42 - "Storage Client Module"
Cohesion: 1.0
Nodes (1): Storage Client (Supabase)

### Community 43 - "Workflow API Module"
Cohesion: 1.0
Nodes (1): Workflow Service

### Community 44 - "Dashboard Page"
Cohesion: 1.0
Nodes (1): Tailwind CSS Configuration

### Community 45 - "Workflow Pages"
Cohesion: 1.0
Nodes (1): TypeScript Configuration

### Community 46 - "Shared Types Library"
Cohesion: 1.0
Nodes (1): TypeScript Type Definitions

## Knowledge Gaps
- **164 isolated node(s):** `Phase 3: Refinement (7 tasks remaining)`, `Phase 1: The Seed Brain (Current State)`, `Phase 2: Active Memory (Memory-First Injections)`, `Phase 3: The Narrative Vault`, `Orchestration Skill` (+159 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Session Logs (Apr 16)`** (2 nodes): `APScheduler Jobs Configuration`, `2026-04-13 Day 4 Final Hardening`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase 3 Complete Status`** (2 nodes): `Test Infrastructure: Offline Wall (Mock Supabase & Gemini)`, `Phase 2.5: Test Infrastructure`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Tasks & Findings Backlog`** (2 nodes): `Remotion Shared-Secret Authentication (T2.1)`, `T2.1 Remotion Authentication (Shared-Secret)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Verification Gate Pattern`** (2 nodes): `Verification Gate Function`, `Verification Before Completion`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Skill Writing Plans`** (2 nodes): `Writing Plans`, `Specification Coverage Self-Review`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase 2 Tasks`** (2 nodes): `Project Phase Status Tracking`, `MVP Completion Tasks`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Trend Detection Spikes`** (2 nodes): `detect_trend_spikes`, `intelligence.triggers`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scrape & Trending Workflows`** (2 nodes): `Workflow Pydantic Models`, `Workflow API Router`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Orchestrated Execution Skill`** (1 nodes): `Orchestration Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Gen Tree Module`** (1 nodes): `Actual Generation Tree (Audit 2026-04-14)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Resume Orchestration Skill`** (1 nodes): `Orchestrations README`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Phase 3 Remediation Logs`** (1 nodes): `Phase 3 Completion & Vault Update`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Parallel Dispatch Pattern`** (1 nodes): `Parallel Agent Dispatch Skill`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Brand Config Module`** (1 nodes): `brand.__init__`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Content Storyboard`** (1 nodes): `content.storyboard`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Intelligence Rejection Logic`** (1 nodes): `intelligence.rejection`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Content Requests Handler`** (1 nodes): `ContentGenerateRequest, ContentEditRequest, SynthesizeRequest, StrategyGenerateRequest`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Selection Memory Update`** (1 nodes): `update_selection_memory`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Suggestion Generator`** (1 nodes): `generate_suggestions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Skill Section Loader`** (1 nodes): `load_skill_sections`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Content Init Module`** (1 nodes): `content.__init__`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Intelligence Init`** (1 nodes): `intelligence.__init__`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Storage Client Module`** (1 nodes): `Storage Client (Supabase)`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workflow API Module`** (1 nodes): `Workflow Service`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Dashboard Page`** (1 nodes): `Tailwind CSS Configuration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Workflow Pages`** (1 nodes): `TypeScript Configuration`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Shared Types Library`** (1 nodes): `TypeScript Type Definitions`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.