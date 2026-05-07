---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/workflows/templates.py"
category: "Content Hub Source Code"
---

# templates.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
NICHE_TEMPLATES = {
    "fitness": {
        "name": "Fitness & Health",
        "description": "Workout routines, nutrition, mindset, transformations",
        "content_pillars": ["Workout Routines", "Nutrition Tips", "Mindset & Motivation", "Client Transformations"],
        "apify_search_config": {
            "tiktok": {"hashtags": ["fitness", "workout", "gym", "fitnesstips", "homeworkout"]},
            "youtube": {"keywords": ["workout routine", "fitness tips", "meal prep", "gym motivation"]},
            "instagram": {"hashtags": ["fitnessmotivation", "workoutroutine", "healthylifestyle"]},
        },
        "platform_defaults": ["tiktok", "instagram"],
        "strategy_group": "short_form",
        "script_style": "high_energy_motivational",
    },
    "real_estate": {
        "name": "Real Estate",
        "description": "Market insights, property tours, buyer/seller tips, investment",
        "content_pillars": ["Market Updates", "Property Tours", "Buyer Tips", "Investment Strategy"],
        "apify_search_config": {
            "tiktok": {"hashtags": ["realestate", "realtor", "homebuying", "realestatetips"]},
            "youtube": {"keywords": ["real estate investing", "home buying tips", "property tour"]},
            "instagram": {"hashtags": ["realestate", "realtor", "propertytour", "homesforsale"]},
        },
        "platform_defaults": ["instagram", "tiktok", "youtube"],
        "strategy_group": "mixed",
        "script_style": "professional_authoritative",
    },
    "software_dev": {
        "name": "Software Development",
        "description": "Coding tutorials, tech insights, career advice, project showcases",
        "content_pillars": ["Coding Tutorials", "Tech Industry Insights", "Career Advice", "Project Showcases"],
        "apify_search_config": {
            "tiktok": {"hashtags": ["coding", "programming", "developer", "techtok", "webdev"]},
            "youtube": {"keywords": ["coding tutorial", "software engineering", "programming tips"]},
            "linkedin": {"keywords": ["software development", "tech career", "engineering leadership"]},
        },
        "platform_defaults": ["linkedin", "twitter", "youtube"],
        "strategy_group": "professional",
        "script_style": "educational_concise",
    },
    "finance": {
        "name": "Finance & Investing",
        "description": "Market analysis, investing strategies, personal finance, crypto",
        "content_pillars": ["Market Analysis", "Investing Strategies", "Personal Finance", "Financial Literacy"],
        "apify_search_config": {
            "tiktok": {"hashtags": ["finance", "investing", "stocks", "personalfinance", "fintok"]},
            "youtube": {"keywords": ["stock market", "investing for beginners", "personal finance tips"]},
            "linkedin": {"keywords": ["financial markets", "investment strategy", "wealth management"]},
        },
        "platform_defaults": ["youtube", "linkedin", "twitter"],
        "strategy_group": "professional",
        "script_style": "data_driven_analytical",
    },
    "coaching": {
        "name": "Life & Business Coaching",
        "description": "Mindset, productivity, business growth, personal development",
        "content_pillars": ["Mindset Shifts", "Productivity Systems", "Business Growth", "Personal Stories"],
        "apify_search_config": {
            "tiktok": {"hashtags": ["coaching", "mindset", "personalgrowth", "entrepreneur"]},
            "youtube": {"keywords": ["life coaching", "business coaching", "personal development"]},
            "instagram": {"hashtags": ["lifecoach", "mindsetcoach", "personaldevelopment"]},
        },
        "platform_defaults": ["instagram", "tiktok", "youtube"],
        "strategy_group": "short_form",
        "script_style": "storytelling_inspirational",
    },
    "custom": {
        "name": "Custom Niche",
        "description": "Define your own niche with a guided questionnaire",
        "content_pillars": [],
        "apify_search_config": {},
        "platform_defaults": [],
        "strategy_group": "mixed",
        "script_style": "adaptive",
        "requires_questionnaire": True,
    },
}

GUIDED_QUESTIONNAIRE = [
    {"id": "niche_description", "question": "Describe your niche in 1-2 sentences. What topic do you create content about?", "type": "text"},
    {"id": "target_audience", "question": "Who is your ideal audience? (age range, interests, pain points)", "type": "text"},
    {"id": "content_goal", "question": "What's the primary goal of your content?", "type": "choice",
     "options": ["Grow audience / followers", "Generate leads / clients", "Build authority / thought leadership", "Educate / inform", "Entertain"]},
    {"id": "tone", "question": "How would you describe your tone?", "type": "choice",
     "options": ["Professional & authoritative", "Casual & conversational", "High-energy & motivational", "Educational & concise", "Storytelling & personal"]},
    {"id": "platforms", "question": "Which platforms do you post on?", "type": "multi_choice",
     "options": ["TikTok", "Instagram", "YouTube", "LinkedIn", "Twitter/X", "Facebook"]},
    {"id": "posting_frequency", "question": "How often do you want to post?", "type": "choice",
     "options": ["Daily", "3-5 times per week", "1-2 times per week", "A few times per month"]},
    {"id": "competitors", "question": "Name 2-3 creators in your niche whose content you admire (optional)", "type": "text"},
    {"id": "search_terms", "question": "What hashtags or keywords would someone use to find content like yours?", "type": "text"},
]

```
