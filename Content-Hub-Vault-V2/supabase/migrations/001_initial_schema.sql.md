---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "supabase/migrations/001_initial_schema.sql"
category: "Content Hub Source Code"
---

# 001_initial_schema.sql

**Description:** Supabase database schema definitions and Row Level Security policies.

---

```sql
-- Content Hub Database Schema
-- 9 tables + pgvector + RLS policies
-- No public.users table — auth.users is the source of truth
-- Backend uses service_role key → bypasses RLS entirely

-- Enable pgvector extension
create extension if not exists vector;

-- 1. Workflows
create table public.workflows (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null,  -- plain uuid, no FK to public.users
    name text not null,
    template_type text not null check (template_type in ('fitness', 'real_estate', 'software_dev', 'finance', 'coaching', 'custom')),
    brand_voice text default '',
    content_pillars jsonb default '[]'::jsonb,
    platforms jsonb default '[]'::jsonb,
    posting_cadence jsonb default '{}'::jsonb,
    competitors jsonb default '[]'::jsonb,
    apify_search_config jsonb default '{}'::jsonb,
    questionnaire_answers jsonb default null,
    is_active boolean default true,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
alter table public.workflows enable row level security;
create policy "Users can CRUD own workflows" on public.workflows for all using (auth.uid() = user_id);

-- 2. Content Items
create table public.content_items (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    user_id uuid not null,  -- plain uuid, no FK to public.users
    content_type text not null check (content_type in ('slides', 'topic', 'short_form', 'talking_head')),
    platform text not null,
    title text default '',
    script_text text default '',
    published_script text default null,
    storyboard jsonb default null,
    asset_urls jsonb default '[]'::jsonb,
    status text not null default 'generating' check (status in ('generating', 'scripting', 'rendering', 'ready', 'failed', 'posted')),
    rejection_flag boolean default false,
    generation_metadata jsonb default '{}'::jsonb,
    error_message text default null,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
alter table public.content_items enable row level security;
create policy "Users can CRUD own content" on public.content_items for all using (auth.uid() = user_id);

-- 3. Trending Content (service_role writes, anon reads)
create table public.trending_content (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    platform text not null,
    post_url text default '',
    author_username text default '',
    author_followers integer default 0,
    title text default '',
    description text default '',
    hashtags jsonb default '[]'::jsonb,
    view_count bigint default 0,
    like_count bigint default 0,
    comment_count bigint default 0,
    share_count bigint default 0,
    save_count bigint default 0,
    organic_score float default 0.0,
    content_age_days integer default 0,
    scraped_at timestamptz default now(),
    created_at timestamptz default now()
);
alter table public.trending_content enable row level security;
create policy "Users can read own trending" on public.trending_content for select
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- 4. Content Triggers (backend needs full CRUD)
create table public.content_triggers (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    trigger_type text not null check (trigger_type in ('trend_spike', 'competitor_post', 'content_gap')),
    title text default '',
    description text default '',
    source_data jsonb default '{}'::jsonb,
    is_acted_on boolean default false,
    created_at timestamptz default now()
);
alter table public.content_triggers enable row level security;
create policy "Users can CRUD own triggers" on public.content_triggers for all
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- 5. Content Style Profiles (learning loop needs full CRUD)
create table public.content_style_profiles (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null unique references public.workflows(id) on delete cascade,
    tone_descriptors jsonb default '[]'::jsonb,
    avg_sentence_length float default 0.0,
    vocabulary_level text default 'conversational',
    common_phrases jsonb default '[]'::jsonb,
    formatting_preferences jsonb default '{}'::jsonb,
    updated_at timestamptz default now()
);
alter table public.content_style_profiles enable row level security;
create policy "Users can CRUD own profiles" on public.content_style_profiles for all
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- 6. Content Edit History
create table public.content_edit_history (
    id uuid primary key default gen_random_uuid(),
    content_item_id uuid not null references public.content_items(id) on delete cascade,
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    original_text text not null,
    edited_text text not null,
    diff_summary text default '',
    created_at timestamptz default now()
);
alter table public.content_edit_history enable row level security;
create policy "Users can CRUD own edit history" on public.content_edit_history for all
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- 7. Brand Configs
create table public.brand_configs (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null unique references public.workflows(id) on delete cascade,
    primary_color text default '#C9A96E',
    secondary_color text default '#0F172A',
    accent_color text default '#FFFFFF',
    font_family text default 'Inter',
    logo_url text default null,
    watermark_enabled boolean default false,
    watermark_text text default '',
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
alter table public.brand_configs enable row level security;
create policy "Users can CRUD own brand config" on public.brand_configs for all
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- 8. Content Publication Memory (learning system needs full CRUD)
create table public.content_publication_memory (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null unique references public.workflows(id) on delete cascade,
    published_count integer default 0,
    content_type_distribution jsonb default '{}'::jsonb,
    avg_script_length jsonb default '{}'::jsonb,
    preferred_hook_styles jsonb default '{}'::jsonb,
    topics_published jsonb default '[]'::jsonb,
    platform_content_map jsonb default '{}'::jsonb,
    generation_without_publish jsonb default '{}'::jsonb,
    rejection_patterns jsonb default '{}'::jsonb,
    updated_at timestamptz default now()
);
alter table public.content_publication_memory enable row level security;
create policy "Users can CRUD own memory" on public.content_publication_memory for all
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- 9. Content Embeddings (RAG — service_role writes, anon reads)
create table public.content_embeddings (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    source_type text not null check (source_type in ('trending_content', 'published_script')),
    source_id uuid not null,
    embedding vector(768),
    content_text text default '',
    metadata jsonb default '{}'::jsonb,
    created_at timestamptz default now()
);
alter table public.content_embeddings enable row level security;
create policy "Users can read own embeddings" on public.content_embeddings for select
    using (workflow_id in (select id from public.workflows where user_id = auth.uid()));

-- Vector similarity search index
create index on public.content_embeddings using ivfflat (embedding vector_cosine_ops) with (lists = 100);

-- Performance indexes
create index idx_content_items_workflow on public.content_items(workflow_id, status);
create index idx_content_items_user on public.content_items(user_id, created_at desc);
create index idx_trending_workflow on public.trending_content(workflow_id, organic_score desc);
create index idx_triggers_workflow on public.content_triggers(workflow_id, created_at desc);
create index idx_embeddings_workflow on public.content_embeddings(workflow_id, source_type);

-- RPC function for vector similarity search
create or replace function match_embeddings(
    query_embedding vector(768),
    match_workflow_id uuid,
    match_count int default 5,
    match_source_type text default null
)
returns table (
    id uuid,
    source_type text,
    source_id uuid,
    content_text text,
    metadata jsonb,
    similarity float
)
language plpgsql
as $$
begin
    return query
    select
        ce.id,
        ce.source_type,
        ce.source_id,
        ce.content_text,
        ce.metadata,
        1 - (ce.embedding <=> query_embedding) as similarity
    from content_embeddings ce
    where ce.workflow_id = match_workflow_id
      and (match_source_type is null or ce.source_type = match_source_type)
    order by ce.embedding <=> query_embedding
    limit match_count;
end;
$$;

```
