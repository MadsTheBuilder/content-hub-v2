---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "supabase/migrations/004_memory_rpc.sql"
category: "Content Hub Source Code"
---

# 004_memory_rpc.sql

**Description:** Supabase database schema definitions and Row Level Security policies.

---

```sql
-- RPC function to atomically increment selection memory counts
create or replace function increment_selection_memory(
    target_workflow_id uuid,
    hook_updates jsonb,
    style_updates jsonb,
    weight float
)
returns void
language plpgsql
security definer
as $$
declare
    current_memory_row record;
    new_hook_styles jsonb := '{}'::jsonb;
    new_sel_prefs jsonb := '{"hook_styles": {}, "content_styles": {}}'::jsonb;
    k text;
    v numeric;
begin
    -- Upsert the baseline row if it doesn't exist to prevent "cold start" loss
    insert into public.content_publication_memory (workflow_id)
    values (target_workflow_id)
    on conflict (workflow_id) do nothing;

    -- Fetch current memory row
    select * into current_memory_row 
    from public.content_publication_memory 
    where workflow_id = target_workflow_id;

    if current_memory_row.preferred_hook_styles is not null then
        new_hook_styles := current_memory_row.preferred_hook_styles;
    end if;
    
    if current_memory_row.selection_preferences is not null then
        new_sel_prefs := current_memory_row.selection_preferences;
    end if;

    if not new_sel_prefs ? 'hook_styles' then
        new_sel_prefs := jsonb_set(new_sel_prefs, '{hook_styles}', '{}'::jsonb);
    end if;
    
    if not new_sel_prefs ? 'content_styles' then
        new_sel_prefs := jsonb_set(new_sel_prefs, '{content_styles}', '{}'::jsonb);
    end if;

    -- Iterate and update hook styles (blended weighted updates)
    for k, v in select * from jsonb_each_text(hook_updates)
    loop
        -- Update preferred_hook_styles
        new_hook_styles := jsonb_set(
            new_hook_styles, 
            array[k], 
            to_jsonb(coalesce((new_hook_styles->>k)::numeric, 0) + (weight * v))
        );
        -- Update selection_preferences
        new_sel_prefs := jsonb_set(
            new_sel_prefs, 
            array['hook_styles', k], 
            to_jsonb(coalesce((new_sel_prefs->'hook_styles'->>k)::numeric, 0) + v)
        );
    end loop;

    -- Iterate and update content styles
    for k, v in select * from jsonb_each_text(style_updates)
    loop
        new_sel_prefs := jsonb_set(
            new_sel_prefs, 
            array['content_styles', k], 
            to_jsonb(coalesce((new_sel_prefs->'content_styles'->>k)::numeric, 0) + v)
        );
    end loop;

    -- Commit update
    update public.content_publication_memory
    set 
        preferred_hook_styles = new_hook_styles,
        selection_preferences = new_sel_prefs,
        updated_at = now()
    where workflow_id = target_workflow_id;

end;
$$;

```
