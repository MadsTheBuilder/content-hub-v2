---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "supabase/migrations/003_evolution_columns.sql"
category: "Content Hub Source Code"
---

# 003_evolution_columns.sql

**Description:** Supabase database schema definitions and Row Level Security policies.

---

```sql
-- Migration 003: Evolution columns for Voice Engine + Content Synthesis
-- Adds brand_profile to workflows, content_analysis + relevance_score to trending_content

-- 1. Parsed brand persona (audience, style, accounts) — populated by Voice Engine
ALTER TABLE public.workflows ADD COLUMN IF NOT EXISTS brand_profile jsonb DEFAULT '{}'::jsonb;

-- 2. Gemini "why it works" analysis per trending post
ALTER TABLE public.trending_content ADD COLUMN IF NOT EXISTS content_analysis jsonb DEFAULT NULL;

-- 3. Weighted relevance score (replaces organic_score as primary ranking)
ALTER TABLE public.trending_content ADD COLUMN IF NOT EXISTS relevance_score float DEFAULT 0.0;

```
