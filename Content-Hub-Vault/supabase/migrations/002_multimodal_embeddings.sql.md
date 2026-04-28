---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "supabase/migrations/002_multimodal_embeddings.sql"
category: "Content Hub Source Code"
---

# 002_multimodal_embeddings.sql

**Description:** Supabase database schema definitions and Row Level Security policies.

---

```sql
-- Migration 002: Upgrade to multimodal embeddings (Gemini Embedding 2, 1536-dim)
-- Safe to run: content_embeddings has 0 rows, no backfill needed.

-- 1. Drop IVFFlat index (can't ALTER column type while index references it)
DROP INDEX IF EXISTS content_embeddings_embedding_idx;

-- 2. Drop existing match_embeddings RPC (signature has vector(768))
DROP FUNCTION IF EXISTS match_embeddings;

-- 3. Upgrade embedding column from 768-dim to 1536-dim
ALTER TABLE public.content_embeddings ALTER COLUMN embedding TYPE vector(1536);

-- 4. Expand source_type constraint for multimodal content
ALTER TABLE public.content_embeddings DROP CONSTRAINT IF EXISTS content_embeddings_source_type_check;
ALTER TABLE public.content_embeddings ADD CONSTRAINT content_embeddings_source_type_check
  CHECK (source_type IN ('trending_content', 'published_script', 'slide_image'));

-- 5. Add thumbnail_url to trending_content (Phase 2 prep)
ALTER TABLE public.trending_content ADD COLUMN IF NOT EXISTS thumbnail_url text DEFAULT '';

-- 6. Create content_calendar table (was missing from migration 001)
CREATE TABLE IF NOT EXISTS public.content_calendar (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id uuid REFERENCES public.content_items(id) ON DELETE CASCADE,
    workflow_id uuid NOT NULL REFERENCES public.workflows(id) ON DELETE CASCADE,
    scheduled_at timestamptz NOT NULL,
    platform text NOT NULL,
    status text DEFAULT 'scheduled',
    created_at timestamptz DEFAULT now()
);

-- 7. Recreate match_embeddings RPC with vector(1536)
CREATE OR REPLACE FUNCTION match_embeddings(
    query_embedding vector(1536),
    match_workflow_id uuid,
    match_count int DEFAULT 5,
    match_source_type text DEFAULT NULL
)
RETURNS TABLE (
    id uuid,
    source_type text,
    source_id uuid,
    content_text text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        ce.id,
        ce.source_type,
        ce.source_id,
        ce.content_text,
        ce.metadata,
        1 - (ce.embedding <=> query_embedding) AS similarity
    FROM content_embeddings ce
    WHERE ce.workflow_id = match_workflow_id
      AND (match_source_type IS NULL OR ce.source_type = match_source_type)
    ORDER BY ce.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 8. HNSW index (works with 0 rows; IVFFlat needs lists*10 minimum rows)
CREATE INDEX ON public.content_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

```
