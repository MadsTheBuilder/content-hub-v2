---
slug: phase0a-twitter-data-layer
created: 2026-05-07
status: complete
current_group: null
groups_complete: []
specialists_involved: [research-agent, db-agent]
---

# Orchestration: Phase 0a — Twitter Data Layer

## Recon summary

- `backend/research/apify_client.py` exists with TikTok, YouTube, Instagram scrapers (actors in `ACTOR_MAP` and `PROFILE_ACTOR_MAP`). Functions: `scrape_platform`, `scrape_profiles`, `scrape_general_trending`, `scrape_workflow`, plus private helpers `_build_actor_input`, `_build_profile_input`, `_normalize_post`, etc.
- Settings accessed via `backend.config.settings`; `.env` contains both `APIFY_API_TOKEN` and `APIFY_API_KEY` — agent must check `backend/config/settings.py` for the exact attribute name used.
- `skills/data/` directory does NOT exist; `skills/` directory does exist at project root.
- Supabase project: `fuvtjsivfngzrmyxeuug` (ap-southeast-1); credentials available in `.env`.
- `Content-Hub-Vault-V2/00-Management-V2/Orchestrations/` exists (previous state files present).
- AGENTS.md defines 6 specialists; research-agent owns `backend/research/*`, db-agent owns Supabase MCP operations.

## Execution plan

**Tasks:** 3 across 1 group
**Specialists:** research-agent, db-agent

### Group 1 (all parallel — no cross-dependencies)

- [research-agent | MEDIUM] Add `scrape_twitter` function to `apify_client.py`
  Files: `backend/research/apify_client.py` (append only)
  Read for context: `backend/config/settings.py`
  Criteria:
  1. Function signature: `async def scrape_twitter(keywords: list[str], accounts: list[str], max_results: int = 60) -> list[dict]`
  2. Tries actor `quacker~twitter-scraper` first, falls back to `apify~twitter-scraper`
  3. Normalizes output to: {tweet_id, text, author_username, author_followers, like_count, reply_count, retweet_count, created_at (ISO 8601), url}
  4. Test run logged: keywords=["AI content creator", "YouTube growth"], accounts=["nateherk", "ChaseHAI"], max_results=10
  5. If both actors fail, logs clear error message and returns [] — does NOT raise (external blocker, not a bug)
  6. Zero modifications to any existing code above the new function

- [research-agent | EASY] Create `skills/data/twitter_config.json`
  Files: `skills/data/twitter_config.json` (new file, new directory)
  Criteria:
  1. Directory `skills/data/` created
  2. File contains exact JSON: {"keywords": ["AI content creator", "YouTube automation", "faceless YouTube", "AI video"], "accounts": ["nateherk", "ChaseHAI"], "max_results": 60, "min_composite_score": 0.5}

- [db-agent | MEDIUM] Apply Supabase migration for tweets and tweet_actions
  Files: Supabase MCP only (no local files)
  Criteria:
  1. Table `tweets` created with all specified columns (tweet_id, author_username, author_followers, text, like_count, reply_count, retweet_count, created_at, url, velocity_score, authority_score, opportunity_score, replyability_score, composite_score, seen_at DEFAULT now(), actioned DEFAULT false)
  2. Table `tweet_actions` created with all specified columns (id uuid PK DEFAULT gen_random_uuid(), tweet_id FK → tweets.tweet_id, action_type text, actioned_at DEFAULT now())
  3. Both tables verified with SELECT COUNT(*) returning 0 rows (not an error)

## Agent prompts

### Task: research-agent: Add scrape_twitter to apify_client.py

- description: "research-agent: Add scrape_twitter to apify_client.py"
- model: sonnet
- prompt: |
    You are the research-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Append a `scrape_twitter` function to `backend/research/apify_client.py`.
    Do NOT modify any existing code — append only.

    ## Scope
    Read for context: `backend/research/apify_client.py`, `backend/config/settings.py`
    Modify: `backend/research/apify_client.py` (append only — do not touch existing lines)
    Create: nothing

    IMPORTANT: Only touch the files listed above. Other agents are working on other
    files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Implementation spec

    Function signature:
    ```python
    async def scrape_twitter(keywords: list[str], accounts: list[str], max_results: int = 60) -> list[dict]:
    ```

    Actor try order:
    1. `quacker~twitter-scraper` (primary)
    2. `apify~twitter-scraper` (fallback)

    Use the same Apify polling pattern as `scrape_platform` (poll loop, check status, fetch dataset).
    Check `backend/config/settings.py` to find the exact attribute name for the Apify API key (likely `APIFY_API_KEY` or `APIFY_API_TOKEN`).

    Normalized output schema per tweet:
    ```python
    {
        "tweet_id": str,
        "text": str,
        "author_username": str,
        "author_followers": int,
        "like_count": int,
        "reply_count": int,
        "retweet_count": int,
        "created_at": str,  # ISO 8601
        "url": str,
    }
    ```

    If both actors fail:
    - Log a clear error: `logger.error("Both Twitter actors failed: <actor1>: <err1>, <actor2>: <err2>. External blocker.")`
    - Return `[]` — do NOT raise an exception

    After implementing, run a test:
    ```python
    asyncio.run(scrape_twitter(
        keywords=["AI content creator", "YouTube growth"],
        accounts=["nateherk", "ChaseHAI"],
        max_results=10
    ))
    ```
    Log whether it succeeded or both actors failed. Either outcome is acceptable — just report clearly.

    ## Acceptance Criteria
    1. Function appended at end of file with correct signature
    2. Tries quacker~twitter-scraper first, apify~twitter-scraper as fallback
    3. Returns list of dicts matching the 9-field normalized schema
    4. Returns [] (not raise) if both actors fail, with a clear log line
    5. Zero lines changed above the new function
    6. Test run executed and result logged

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and the test result.

---

### Task: research-agent: Create skills/data/twitter_config.json

- description: "research-agent: Create skills/data/twitter_config.json"
- model: haiku
- prompt: |
    You are the research-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `skills/data/twitter_config.json` with exact content.

    ## Scope
    Read for context: nothing
    Modify: nothing
    Create: `skills/data/twitter_config.json` (create directory `skills/data/` first if needed)

    IMPORTANT: Only touch the files listed above. Other agents are working on other
    files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Exact file content
    ```json
    {
      "keywords": ["AI content creator", "YouTube automation", "faceless YouTube", "AI video"],
      "accounts": ["nateherk", "ChaseHAI"],
      "max_results": 60,
      "min_composite_score": 0.5
    }
    ```

    ## Acceptance Criteria
    1. Directory `skills/data/` exists
    2. File `skills/data/twitter_config.json` exists with exactly the content above
    3. Valid JSON (parseable)

    ## When done
    Report your status:
    - DONE: All criteria met
    - STUCK: Cannot proceed (explain what blocks you)

    Include a summary of what you created.

---

### Task: db-agent: Apply Supabase migration for tweets and tweet_actions

- description: "db-agent: Apply Supabase migration for tweets and tweet_actions"
- model: sonnet
- prompt: |
    You are the db-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Apply a Supabase migration that creates the `tweets` and `tweet_actions` tables,
    then verify both exist.

    ## Scope
    Read for context: nothing
    Modify: nothing (Supabase MCP only)
    Create: nothing local

    IMPORTANT: Use Supabase MCP tools only. Do not touch any local files.

    ## Migration SQL

    ```sql
    CREATE TABLE tweets (
        tweet_id text PRIMARY KEY,
        author_username text,
        author_followers int,
        text text,
        like_count int,
        reply_count int,
        retweet_count int,
        created_at timestamptz,
        url text,
        velocity_score float,
        authority_score float,
        opportunity_score float,
        replyability_score float,
        composite_score float,
        seen_at timestamptz DEFAULT now(),
        actioned boolean DEFAULT false
    );

    CREATE TABLE tweet_actions (
        id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
        tweet_id text REFERENCES tweets(tweet_id),
        action_type text,
        actioned_at timestamptz DEFAULT now()
    );
    ```

    ## Verification
    After applying the migration, run:
    ```sql
    SELECT COUNT(*) FROM tweets;
    SELECT COUNT(*) FROM tweet_actions;
    ```
    Both should return 0 (empty tables — that is correct).

    ## Acceptance Criteria
    1. `tweets` table created with all 16 columns
    2. `tweet_actions` table created with 4 columns, FK to tweets
    3. Both SELECT COUNT(*) queries return 0

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include the SELECT COUNT(*) output as confirmation.

## Status log
- 2026-05-07 created, status=awaiting-approval
- 2026-05-07 approved by user; dispatching Group 1 in parallel
- 2026-05-07 Group 1 complete; post-dispatch bugs found and fixed (status guard, int casting); verification passed; status=complete
