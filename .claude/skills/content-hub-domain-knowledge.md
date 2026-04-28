# Content Hub Developer Guide

<description>
This skill provides the core domain knowledge for the Content Hub repository. It includes the commands to run the backend and frontend servers, an overview of the code organization and file structure, and the visual design system tokens (colors, fonts, component styles) needed for UI work. Use this skill when you need to start the app, understand directory layouts, or when designing UI components.
</description>

## Dev commands
```bash
# Backend
cd "C:\Users\madhu\Claude cowork\Content Hub"
uvicorn backend.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm run dev   # runs on port 3003

# Playwright (one-time setup)
playwright install chromium
```

## File structure highlights
```
content-hub/
├── backend/
│   ├── main.py              # FastAPI app + /api/v1/status endpoint
│   ├── config.py            # loads .env
│   ├── database.py          # Supabase client + mock fallback
│   ├── auth/                # signup/login/me
│   ├── workflows/           # CRUD + scrape + trending + suggestions
│   ├── content/             # generate + status poll + edit + publish + calendar
│   ├── brand/               # brand config per workflow
│   ├── research/            # Apify scraping + RAG + organic scoring
│   ├── intelligence/        # memory + rejection + suggestions + triggers
│   ├── scheduler/           # APScheduler jobs
│   └── storage/             # Supabase Storage client
├── frontend/
│   ├── app/
│   │   ├── dashboard/       # workflow grid
│   │   ├── workflows/new/   # 5-step wizard
│   │   ├── workflows/[id]/  # trending + suggestions tabs
│   │   ├── brand/[wfId]/    # brand config editor
│   │   ├── content/new/     # 3-step generation wizard
│   │   ├── content/library/ # filtered content grid
│   │   ├── content/[id]/    # content detail + download + publish
│   │   ├── content/[id]/edit/ # side-by-side script editor
│   │   └── content/calendar/  # scheduled content calendar
│   ├── components/
│   │   └── Sidebar.tsx      # fixed sidebar + mock-mode banner
│   └── lib/
│       ├── api.ts           # all API calls
│       └── types.ts         # TypeScript types
├── supabase/migrations/
│   └── 001_initial_schema.sql  # canonical schema (corrected)
└── .env                     # secrets — never commit
```

## Design system
- Background: `#0F172A` (dark navy)
- Accent: `#C9A96E` (gold) → `#8E744A` (gradient end)
- Borders: `#334155` / `#1E293B`
- Font: Black/extrabold weight, uppercase tracking for labels
- Components: rounded-2xl, glassmorphism panels, gold glow shadows
