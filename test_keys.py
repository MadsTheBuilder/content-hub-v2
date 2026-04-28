#!/usr/bin/env python3
"""Test which API keys in .env are valid and working."""

import os
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Store results
results = {}

print("=" * 70)
print("TESTING API KEYS")
print("=" * 70)

# ─────────────────────────────────────────────────────────────────────────
# 1. SUPABASE
# ─────────────────────────────────────────────────────────────────────────
print("\n[1] SUPABASE")
try:
    import supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url or not key:
        print("   [FAIL] Missing SUPABASE_URL or SUPABASE_SERVICE_KEY")
        results["supabase"] = False
    else:
        client = supabase.create_client(url, key)
        # Try a simple query
        response = client.table("workflows").select("count", count="exact").execute()
        print("[OK] SUPABASE connected. Workflows count: {}".format(response.count))
        results["supabase"] = True
except Exception as e:
    print("[FAIL] SUPABASE error: {}".format(str(e)[:100]))
    results["supabase"] = False

# ─────────────────────────────────────────────────────────────────────────
# 2. GOOGLE GEMINI (GOOGLE_AI_STUDIO_KEY)
# ─────────────────────────────────────────────────────────────────────────
print("\n[2] GOOGLE GEMINI")
try:
    import google.generativeai as genai
    api_key = os.getenv("GOOGLE_AI_STUDIO_KEY")

    if not api_key:
        print("   [FAIL] Missing GOOGLE_AI_STUDIO_KEY")
        results["gemini"] = False
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content("Say 'Hello' in one word")
        print("[OK] GEMINI working. Response: {}".format(response.text[:50]))
        results["gemini"] = True
except Exception as e:
    print("[FAIL] GEMINI error: {}".format(str(e)[:100]))
    results["gemini"] = False

# ─────────────────────────────────────────────────────────────────────────
# 3. APIFY
# ─────────────────────────────────────────────────────────────────────────
print("\n[3] APIFY")
try:
    from apify_client import ApifyClient
    api_token = os.getenv("APIFY_API_TOKEN")

    if not api_token:
        print("   [FAIL] Missing APIFY_API_TOKEN")
        results["apify"] = False
    else:
        client = ApifyClient(api_token)
        me = client.user().get()
        print("[OK] APIFY connected. Account: {}".format(me.get('id', 'unknown')[:20]))
        results["apify"] = True
except Exception as e:
    print("[FAIL] APIFY error: {}".format(str(e)[:100]))
    results["apify"] = False

# ─────────────────────────────────────────────────────────────────────────
# 4. YOUTUBE DATA API
# ─────────────────────────────────────────────────────────────────────────
print("\n[4] YOUTUBE DATA API")
try:
    from googleapiclient.discovery import build
    api_key = os.getenv("YOUTUBE_API_KEY")

    if not api_key:
        print("   [FAIL] Missing YOUTUBE_API_KEY")
        results["youtube"] = False
    else:
        service = build("youtube", "v3", developerKey=api_key)
        request = service.videos().list(part="snippet", chart="mostPopular", regionCode="US", maxResults=1)
        response = request.execute()
        count = len(response.get("items", []))
        print("[OK] YOUTUBE API working. Got {} video(s)".format(count))
        results["youtube"] = True
except Exception as e:
    print("[FAIL] YOUTUBE API error: {}".format(str(e)[:100]))
    results["youtube"] = False

# ─────────────────────────────────────────────────────────────────────────
# 5. PEXELS
# ─────────────────────────────────────────────────────────────────────────
print("\n[5] PEXELS")
try:
    import requests
    api_key = os.getenv("PEXELS_API_KEY")

    if not api_key:
        print("   [FAIL] Missing PEXELS_API_KEY")
        results["pexels"] = False
    else:
        headers = {"Authorization": api_key}
        resp = requests.get("https://api.pexels.com/v1/curated", headers=headers, params={"per_page": 1})
        resp.raise_for_status()
        print("[OK] PEXELS working. Status: {}".format(resp.status_code))
        results["pexels"] = True
except Exception as e:
    print("[FAIL] PEXELS error: {}".format(str(e)[:100]))
    results["pexels"] = False

# ─────────────────────────────────────────────────────────────────────────
# 6. ANTHROPIC
# ─────────────────────────────────────────────────────────────────────────
print("\n[6] ANTHROPIC")
try:
    from anthropic import Anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key or api_key == "your-anthropic-api-key":
        print("   [FAIL] ANTHROPIC_API_KEY is placeholder/missing")
        results["anthropic"] = False
    else:
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=10,
            messages=[{"role": "user", "content": "Say 'Hi'"}]
        )
        print("[OK] ANTHROPIC working")
        results["anthropic"] = True
except Exception as e:
    print("[FAIL] ANTHROPIC error: {}".format(str(e)[:100]))
    results["anthropic"] = False

# ─────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
for name, working in sorted(results.items()):
    status = "[OK]" if working else "[FAIL]"
    print("{:20} {}".format(name.upper(), status))

working_count = sum(results.values())
print("\nTotal: {}/{} keys working".format(working_count, len(results)))
