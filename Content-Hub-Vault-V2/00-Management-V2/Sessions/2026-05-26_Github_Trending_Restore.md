---
date: 2026-05-26
tags: [bugfix, restore, github-trending, pipeline]
description: "Recovered github_trending.py after it was incorrectly deleted during the 8GB cleanup. Fixed V1→V2 vault path on restore."
---

# GitHub Trending Restore

## What Happened

During [[2026-05-26_8GB_Shed_Cleanup]], `github_trending.py` and `run_github_trending.bat` were incorrectly categorised as orphaned V1 scripts and deleted.

Post-cleanup verification of the session log surfaced the error: `skills/researcher.py` reads `TRENDS_FILE = .../Content-Hub-Vault-V2/04-Trends/github_trending.md` as step 1 of every research run. That file is the direct output of `github_trending.py`. Without the script, trend data cannot be refreshed.

## Recovery

Both files recovered from git (`git show 6c15663:github_trending.py`, `git show b11e5f4:run_github_trending.bat`) and restored to project root.

## Bug Fixed on Restore

The original `OUTPUT` path in `github_trending.py` still pointed at the V1 vault:

```python
# Before (wrong — V1 path)
OUTPUT = ROOT.parent / "Content Hub" / "Content-Hub-Vault" / "04-Trends" / "github_trending.md"

# After (correct — V2 path)
OUTPUT = ROOT / "Content-Hub-Vault-V2" / "04-Trends" / "github_trending.md"
```

The script had been writing to the V1 vault location. The V2 vault's `04-Trends/` had existing content (repo deep-dive folders from prior runs) but those would have come from manual syncs. Going forward the script writes directly to the correct V2 location.

## Pipeline Role

```
github_trending.py
  → Content-Hub-Vault-V2/04-Trends/github_trending.md   (daily refresh)
  → Content-Hub-Vault-V2/04-Trends/<owner>_<repo>/      (per-repo deep dives)

skills/researcher.py
  ← reads github_trending.md at TRENDS_FILE (step 1 of every /researcher run)
```

Run manually: `python github_trending.py`
Scheduled: `run_github_trending.bat` via Windows Task Scheduler at 08:00 daily.

---

Modifies: [[github_trending.py]]
References: [[2026-05-26_8GB_Shed_Cleanup]], [[skills/researcher.py]]
