---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "frontend/lib/types.ts"
category: "Content Hub Source Code"
---

# types.ts

**Description:** Frontend shared utilities, API clients, or TypeScript type definitions.

---

```typescript
export interface User {
  id: string;
  email: string;
  display_name?: string;
}

export interface Workflow {
  id: string;
  user_id: string;
  name: string;
  template_type: string;
  brand_voice: string;
  content_pillars: string[];
  platforms: string[];
  posting_cadence: Record<string, unknown>;
  competitors: string[];
  brand_profile: Record<string, unknown>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ContentItem {
  id: string;
  workflow_id: string;
  user_id: string;
  content_type: "slides" | "topic" | "short_form" | "talking_head";
  platform: string;
  title: string;
  script_text: string;
  published_script: string | null;
  storyboard: Record<string, unknown> | null;
  asset_urls: string[];
  status: "generating" | "scripting" | "refining" | "rendering" | "ready" | "failed" | "posted";
  rejection_flag: boolean;
  generation_metadata: Record<string, unknown>;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface TrendingContent {
  id: string;
  workflow_id: string;
  platform: string;
  post_url: string;
  author_username: string;
  author_followers: number;
  title: string;
  description: string;
  hashtags: string[];
  view_count: number;
  like_count: number;
  comment_count: number;
  share_count: number;
  save_count: number;
  organic_score: number;
  relevance_score: number;
  thumbnail_url: string;
  content_analysis: Record<string, unknown> | null;
}

export interface Suggestion {
  type: string;
  topic: string;
  platform: string;
  organic_score: number;
  source_url: string;
  recommended_type: string;
  warning?: string;
}

export interface BrandConfig {
  id: string;
  workflow_id: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  font_family: string;
  logo_url: string | null;
  watermark_enabled: boolean;
  watermark_text: string;
}

export interface NicheTemplate {
  name: string;
  description: string;
  content_pillars: string[];
  platform_defaults: string[];
  strategy_group: string;
  requires_questionnaire?: boolean;
}

export interface QuestionnaireItem {
  id: string;
  question: string;
  type: "text" | "choice" | "multi_choice";
  options?: string[];
}

export interface StrategyAlternative {
  content_angle: string;
  hypothesis: string;
  differentiation: string;
}

export interface StrategyDocument {
  content_angle: string;
  why_this_angle: string;
  target_platform: string;
  recommended_format: {
    type: string;
    length: string;
    hook_style: string;
    pacing: string;
    cta_style: string;
  };
  inspired_by: { post_title: string; technique_borrowed: string }[];
  differentiation: string;
  user_notes: string;
  alternatives?: StrategyAlternative[];
}

```
