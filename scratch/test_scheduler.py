"""
Day 4 - Task 4A: APScheduler verification script.
Run from the project root: python scratch/test_scheduler.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Minimal env setup to avoid import errors
os.environ.setdefault("SUPABASE_URL", "https://your-project.supabase.co")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "your-key-placeholder")
os.environ.setdefault("SUPABASE_ANON_KEY", "your-anon-key-placeholder")
os.environ.setdefault("GOOGLE_AI_STUDIO_KEY", "placeholder")
os.environ.setdefault("APIFY_API_KEY", "")
os.environ.setdefault("ANTHROPIC_API_KEY", "")

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Import jobs module and grab the scheduler + start function
from backend.scheduler.jobs import start_scheduler, scheduler

print("=" * 60)
print("APScheduler Job Verification — Day 4 Task 4A")
print("=" * 60)

# Start the scheduler (registers all jobs)
start_scheduler()

jobs = scheduler.get_jobs()
print(f"\nTotal jobs registered: {len(jobs)}\n")

expected = {
    "scrape_organic": {"day": "*/3", "hour": "5", "minute": "30"},
    "detect_trends":  {"day": "*/3", "hour": "6", "minute": "0"},
    "generate_suggestions": {"hour": "6", "minute": "30"},
    "weekly_embed":   {"day_of_week": "sun", "hour": "4", "minute": "0"},
    "flag_rejections":{"day_of_week": "sun", "hour": "6", "minute": "0"},
}

found_ids = set()
for job in jobs:
    found_ids.add(job.id)
    trigger = job.trigger
    print(f"  [OK] Job: {job.id}")
    print(f"     Function: {job.func_ref}")
    print(f"     Trigger:  {trigger}")
    print(f"     Next run: {job.next_run_time}")
    print()

print("\n--- Expected vs Found ---")
all_pass = True
for jid in expected:
    ok = jid in found_ids
    status = "[FOUND]" if ok else "[MISSING]"
    print(f"  {status}: {jid}")
    if not ok:
        all_pass = False

print()
print("=" * 60)
print(f"VERDICT: {'PASS - All 5 jobs registered' if all_pass else 'FAIL - Some jobs missing'}")
print("=" * 60)

# Cleanly shut down
scheduler.shutdown(wait=False)
