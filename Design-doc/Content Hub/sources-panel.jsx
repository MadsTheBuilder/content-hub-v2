// SourcesPanel — the "behind page" with vault files, folders, and sources used.
// Clicking a file or source opens an in-panel viewer.

const VAULT_DATA = {
  trends: {
    accent: "var(--stage-trends)",
    folder: "trends/",
    tree: [
    { type: "folder", name: "trends/", count: 18 },
    { type: "file", name: "2026-05-week3-ai-dev.md", meta: "2.1 kb · today", current: true, depth: 1, kind: "trends-output" },
    { type: "file", name: "2026-05-week2-ai-dev.md", meta: "1.8 kb · 6d", depth: 1, kind: "trends-prev" },
    { type: "file", name: "2026-05-week1-creator-tools.md", meta: "2.4 kb · 13d", depth: 1, kind: "trends-creator" },
    { type: "file", name: "2026-04-monthly-roundup.md", meta: "4.7 kb · 19d", depth: 1, kind: "trends-monthly" },
    { type: "folder", name: "topics/", count: 7 },
    { type: "file", name: "ai-tools.json", meta: "tag index", depth: 1, kind: "json-tag-ai" },
    { type: "file", name: "local-llm.json", meta: "tag index", depth: 1, kind: "json-tag-llm" }],

    sources: [
    { host: "RD", title: "r/LocalLLaMA — top this week", url: "reddit.com/r/LocalLLaMA/top", meta: "412 posts" },
    { host: "HN", title: "Hacker News — AI-tagged stories", url: "news.ycombinator.com/from?site=ai", meta: "186 stories" },
    { host: "YT", title: "YouTube — dev channel uploads (7d)", url: "youtube.com/results?sp=…", meta: "1240 videos" },
    { host: "X", title: "X — AI dev tools list", url: "x.com/i/lists/ai-dev", meta: "320 posts" }]

  },
  research: {
    accent: "var(--stage-research)",
    folder: "research/",
    tree: [
    { type: "folder", name: "research/", count: 24 },
    { type: "file", name: "viral-ai-tutorials.md", meta: "8.2 kb · today", current: true, depth: 1, kind: "research-output" },
    { type: "file", name: "dev-yt-economics.md", meta: "5.1 kb · 1d", depth: 1, kind: "research-econ" },
    { type: "file", name: "hook-patterns-1M+.md", meta: "12.4 kb · 4d", depth: 1, kind: "research-hooks" },
    { type: "folder", name: "raw/", count: 12 },
    { type: "file", name: "transcripts.zip", meta: "48 mb", depth: 1, kind: "binary-zip" },
    { type: "file", name: "retention-curves.csv", meta: "2.1 mb", depth: 1, kind: "csv-retention" },
    { type: "folder", name: "sources/", count: 33 }],

    sources: [
    { host: "YT", title: "YouTube Data API — 1,240 sample videos, 90d", url: "developers.google.com/youtube/v3", meta: "n=1240" },
    { host: "TB", title: "Tubular — AI/dev retention curves", url: "tubular.com/dashboard/retention", meta: "8 channels" },
    { host: "📝", title: "Channel interviews · Fireship, Theo, NetChuck", url: "vault://research/raw/interviews", meta: "4 transcripts" },
    { host: "📊", title: "Google Trends — AI tutorial 24mo", url: "trends.google.com/explore", meta: "long view" },
    { host: "RD", title: "r/SubsAreSlaughter — creator threads", url: "reddit.com/r/SubsAreSlaughter", meta: "27 threads" }]

  },
  ideation: {
    accent: "var(--stage-ideation)",
    folder: "ideation/",
    tree: [
    { type: "folder", name: "ideation/", count: 31 },
    { type: "file", name: "may-batch-12.md", meta: "3.2 kb · today", current: true, depth: 1, kind: "ideation-output" },
    { type: "file", name: "april-batch-09.md", meta: "2.8 kb · 14d", depth: 1, kind: "ideation-prev" },
    { type: "folder", name: "scored/", count: 88 },
    { type: "file", name: "9.0+.md", meta: "11 ideas", depth: 1, kind: "ideation-9" },
    { type: "file", name: "8.0-9.0.md", meta: "34 ideas", depth: 1, kind: "ideation-8" },
    { type: "folder", name: "channel-signal/", count: 3 },
    { type: "file", name: "ctr-baseline.json", meta: "6 months", depth: 1, kind: "json-ctr" }],

    sources: [
    { host: "📊", title: "Channel analytics — last 6 months", url: "vault://analytics/6mo.csv", meta: "primary" },
    { host: "📄", title: "Research · viral-ai-tutorials.md", url: "vault://research/viral-ai…", meta: "linked" },
    { host: "📄", title: "Trends · 2026-05-week3-ai-dev.md", url: "vault://trends/2026-05…", meta: "linked" }]

  },
  hooks: {
    accent: "var(--stage-hooks)",
    folder: "hooks/",
    tree: [
    { type: "folder", name: "hooks/", count: 47 },
    { type: "file", name: "local-rag-20min.md", meta: "1.4 kb · today", current: true, depth: 1, kind: "hooks-output" },
    { type: "file", name: "cursor-vs-cline.md", meta: "1.1 kb · 3d", depth: 1, kind: "hooks-cursor" },
    { type: "folder", name: "templates/", count: 12 },
    { type: "file", name: "demo-first.md", meta: "channel default", depth: 1, kind: "tpl-demo" },
    { type: "file", name: "contrarian.md", meta: "high CTR", depth: 1, kind: "tpl-contra" },
    { type: "file", name: "object-first.md", meta: "low risk", depth: 1, kind: "tpl-object" }],

    sources: [
    { host: "📄", title: "Research · hook-patterns-1M+.md", url: "vault://research/hook-patterns…", meta: "linked" },
    { host: "🎬", title: "Channel · top-performing-openings", url: "vault://channel/top-openings.md", meta: "personal" },
    { host: "📊", title: "Hook A/B history (52 weeks)", url: "vault://hooks/ab-log.csv", meta: "52 wks" }]

  },
  distribution: {
    accent: "var(--stage-distribution)",
    folder: "distribution/",
    tree: [
    { type: "folder", name: "distribution/", count: 14 },
    { type: "file", name: "local-rag-20min.kit.md", meta: "today", current: true, depth: 1, kind: "dist-output" },
    { type: "folder", name: "outlines/", count: 12 },
    { type: "file", name: "local-rag-20min.outline.md", meta: "8 sections", depth: 1, kind: "outline-rag" },
    { type: "file", name: "cursor-vs-cline.outline.md", meta: "in progress", depth: 1, kind: "outline-cursor" },
    { type: "folder", name: "thumbnails/", count: 36 },
    { type: "file", name: "brief-template.md", meta: "channel style", depth: 1, kind: "thumb-brief" }],

    sources: [
    { host: "📄", title: "Outline · local-rag-20min.outline.md", url: "vault://outlines/local-rag…", meta: "primary" },
    { host: "📄", title: "Hooks · local-rag-20min.md", url: "vault://hooks/local-rag…", meta: "linked" },
    { host: "🎬", title: "Thumbnail brief template", url: "vault://thumbnails/brief.md", meta: "channel" }]

  },
  brain: {
    accent: "var(--brain)",
    folder: "brain/",
    tree: [
    { type: "folder", name: "brain/", count: 142 },
    { type: "file", name: "vision-pro-teardown.md", meta: "today", current: true, depth: 1, kind: "brain-current" },
    { type: "file", name: "fireship-svelte-rant.md", meta: "yesterday", depth: 1, kind: "brain-prev1" },
    { type: "file", name: "marques-segment-cuts.md", meta: "2d", depth: 1, kind: "brain-prev2" },
    { type: "folder", name: "techniques/", count: 37 },
    { type: "file", name: "authority-claim.md", meta: "8 examples", depth: 1, kind: "tech-authority" },
    { type: "file", name: "timestamp-promise.md", meta: "12 examples", depth: 1, kind: "tech-timestamp" },
    { type: "folder", name: "raw-imports/", count: 88 }],

    sources: [
    { host: "YT", title: "Vision Pro teardown — original video", url: "youtube.com/watch?v=demo-tear-down", meta: "input" },
    { host: "📝", title: "Pasted transcript (3,420 words)", url: "session://pasted-1", meta: "input" },
    { host: "📚", title: "Technique library cross-references", url: "vault://brain/techniques/", meta: "linked" }]

  },
  title: {
    accent: "var(--stage-title)",
    folder: "titles/",
    tree: [
    { type: "folder", name: "titles/", count: 22 },
    { type: "file", name: "local-rag-20min.titles.md", meta: "today", current: true, depth: 1, kind: "title-output" },
    { type: "file", name: "cursor-vs-cline.titles.md", meta: "3d", depth: 1, kind: "title-cursor" },
    { type: "folder", name: "patterns/", count: 8 },
    { type: "file", name: "i-built-X-in-Y.md", meta: "highest CTR", depth: 1, kind: "title-pattern-built" },
    { type: "file", name: "contrarian-claim.md", meta: "high variance", depth: 1, kind: "title-pattern-contra" },
    { type: "file", name: "number-prefix.md", meta: "safe floor", depth: 1, kind: "title-pattern-num" },
    { type: "folder", name: "ab-history/", count: 96 }],

    sources: [
    { host: "📄", title: "Hook · local-rag-20min.md", url: "vault://hooks/local-rag…", meta: "linked" },
    { host: "📄", title: "Ideation · may-batch-12.md", url: "vault://ideation/may-batch-12.md", meta: "linked" },
    { host: "📊", title: "Channel · title CTR history (12mo)", url: "vault://analytics/titles-12mo.csv", meta: "primary" }]

  },
  outline: {
    accent: "var(--stage-outline)",
    folder: "outlines/",
    tree: [
    { type: "folder", name: "outlines/", count: 17 },
    { type: "file", name: "local-rag-20min.outline.md", meta: "8 sections", current: true, depth: 1, kind: "outline-rag" },
    { type: "file", name: "cursor-vs-cline.outline.md", meta: "in progress", depth: 1, kind: "outline-cursor" },
    { type: "folder", name: "templates/", count: 6 },
    { type: "file", name: "how-to-tutorial.md", meta: "default", depth: 1, kind: "outline-tpl-howto" },
    { type: "file", name: "opinion-essay.md", meta: "channel style", depth: 1, kind: "outline-tpl-opinion" },
    { type: "folder", name: "retention-shapes/", count: 4 }],

    sources: [
    { host: "📄", title: "Hook · local-rag-20min.md", url: "vault://hooks/local-rag…", meta: "linked" },
    { host: "📄", title: "Title · local-rag-20min.titles.md", url: "vault://titles/local-rag…", meta: "linked" },
    { host: "📊", title: "Channel · retention shapes (top 20)", url: "vault://analytics/retention-top20.csv", meta: "reference" }]

  }
};

// Inline markdown-ish content per file. Keep it tight + scannable.
const FILE_CONTENT = {
  // Trends
  "trends-output":
  <>
      <h1>AI dev-tools — week of May 19</h1>
      <p>Three signals broke containment this week. The strongest is a <strong>frustration arc around AI IDEs</strong> — Cursor users hitting context limits, Cline picking up the spillover.</p>
      <h2>Top signals</h2>
      <ol>
        <li><strong>"Cline vs Cursor"</strong> — 4.2× volume vs last week.</li>
        <li><strong>Llama 3.3 + 24GB consumer GPUs</strong> — viral on r/LocalLLaMA.</li>
        <li><strong>v0 + product-engineer hybrid</strong> — "is the senior PM dead?"</li>
        <li><strong>Bun 1.2</strong> — Node-killer framing (overblown but trending).</li>
      </ol>
      <h2>Angles to ship within 4 days</h2>
      <ul>
        <li>"I tried Cline for a week. Here's why I'm switching."</li>
        <li>"You can run Llama on a $400 GPU now. Here's the build."</li>
        <li>"v0 made my whole team uncomfortable."</li>
      </ul>
    </>,

  "trends-prev":
  <>
      <h1>AI dev-tools — week of May 12</h1>
      <p>Quiet week. Two signals worth tracking: a slow build around <strong>agent eval harnesses</strong> and the start of a backlash around <em>"AI coding influencer fatigue"</em>.</p>
      <ul>
        <li>r/MachineLearning weekly thread — 2.1× engagement on eval-related comments.</li>
        <li>Three high-engagement YT vids on "I'm done with AI demos".</li>
      </ul>
    </>,

  "trends-creator":
  <>
      <h1>Creator tools — week of May 5</h1>
      <p>Descript pricing change drove a 6-day discourse spike. ScreenStudio + CleanShot bundles being shared.</p>
    </>,

  "trends-monthly":
  <>
      <h1>April monthly roundup</h1>
      <p>The story of April: <strong>local-first AI</strong> went from niche to general-purpose. Ollama download numbers, lm-studio enterprise pivot, and three notable open-weight releases.</p>
    </>,

  "json-tag-ai":
  <>
      <h1>ai-tools.json</h1>
      <pre><code>{`{
  "tag": "ai-tools",
  "tracked": ["Cursor","Cline","Claude Code","v0","Lovable","Windsurf"],
  "scan_freq": "6h",
  "last_run": "2026-05-22T07:14:00Z",
  "volume_7d": 14820,
  "growth_7d": 0.42
}`}</code></pre>
    </>,

  "json-tag-llm":
  <>
      <h1>local-llm.json</h1>
      <pre><code>{`{
  "tag": "local-llm",
  "tracked": ["llama.cpp","Ollama","lm-studio","mlx"],
  "scan_freq": "12h",
  "volume_7d": 6210
}`}</code></pre>
    </>,


  // Research
  "research-output":
  <>
      <h1>Why AI tutorial videos go viral</h1>
      <p>Across 1,240 sample videos &gt;500k views, viral AI tutorials share four structural traits. None are about production quality. All are about <em>compression</em>.</p>
      <h2>1 · First 11 seconds make or break</h2>
      <p>78% open with a working demo, not a face cam.</p>
      <h2>2 · Tooling specificity outperforms abstract concepts</h2>
      <p>Specific tool names beat generic terms by <strong>3.4×</strong> on impressions-to-CTR.</p>
      <h2>3 · "Lazy build" template dominates</h2>
      <p>61% lean on "I built X in Y minutes/lines/hours". The constraint is load-bearing.</p>
      <h2>4 · Mid-roll friction is the new outro</h2>
      <p>Top channels park CTAs at ~55% of runtime. Converts at 2.1× end-of-video CTAs.</p>
    </>,

  "research-econ":
  <>
      <h1>The economics of dev-tool YouTube</h1>
      <p>CPMs in the dev/AI vertical run 2.4× the YouTube average. Sponsor inventory is the real story — channels under 50k subs are placing $4–8k packages.</p>
    </>,

  "research-hooks":
  <>
      <h1>Hook patterns of 1M+ view AI videos</h1>
      <p>Sample: 84 videos. Three patterns own 71% of them: <strong>demo-first</strong> (38%), <strong>contrarian-claim</strong> (19%), <strong>object-first</strong> (14%).</p>
    </>,

  "csv-retention":
  <>
      <h1>retention-curves.csv</h1>
      <pre><code>{`channel,video_id,t0,t30,t60,t120,avd
fireship,fhg-mZ,1.00,0.91,0.84,0.71,0.62
theo,abc-12,1.00,0.88,0.79,0.65,0.58
ai-jason,xyz-7,1.00,0.93,0.87,0.78,0.69
... (1240 rows)`}</code></pre>
      <p style={{ color: "var(--text-muted)", fontSize: 12 }}>Open in CSV preview · 2.1 MB · 1,240 rows</p>
    </>,

  "binary-zip":
  <>
      <h1>transcripts.zip</h1>
      <p style={{ color: "var(--text-secondary)" }}>Binary archive · 48 MB · 1,240 transcript files</p>
      <ul>
        <li>fireship-recent-90d/</li>
        <li>theo-recent-90d/</li>
        <li>ai-jason-recent-90d/</li>
        <li>networkchuck-recent-90d/</li>
      </ul>
    </>,


  // Ideation
  "ideation-output":
  <>
      <h1>12 ideas — May batch</h1>
      <ol>
        <li><strong>Local RAG in 20 minutes (no API).</strong> Predicted 340k views.</li>
        <li><strong>Cursor lost me. Here's the 4-tool setup I use now.</strong></li>
        <li><strong>The smallest LLM that's actually useful for code.</strong></li>
        <li><strong>Why your AI agent is bad (and 3 prompts that fix it).</strong></li>
        <li><strong>I gave Claude my entire codebase. Here's what it found.</strong></li>
      </ol>
    </>,

  "ideation-prev":
  <>
      <h1>April batch — 9 ideas</h1>
      <p>Mixed bag. One breakout idea ("Why I switched to Bun") shipped and pulled 580k. Others scored under 7.0 and weren't built.</p>
    </>,

  "ideation-9":
  <>
      <h1>Ideas scoring 9.0+</h1>
      <ul>
        <li>Local RAG in 20 minutes (9.4)</li>
        <li>You can run Llama on a $400 GPU (9.2)</li>
        <li>I gave Claude my entire codebase (9.0)</li>
      </ul>
    </>,

  "ideation-8":
  <>
      <h1>Ideas scoring 8.0–9.0</h1>
      <p>34 ideas. Strong mid-tier. Most fit either "demo-first" or "I tried X for a week" templates.</p>
    </>,

  "json-ctr":
  <>
      <h1>ctr-baseline.json</h1>
      <pre><code>{`{
  "window_months": 6,
  "median_ctr": 0.078,
  "p25_ctr": 0.054,
  "p75_ctr": 0.106,
  "avd_baseline": 0.61
}`}</code></pre>
    </>,


  // Hooks
  "hooks-output":
  <>
      <h1>5 hooks — "Local RAG in 20 min"</h1>
      <ol>
        <li>"I just built a RAG system that runs on my laptop. No API calls. No subscription. Here's the entire thing in twenty minutes." (9.1)</li>
        <li>"Everyone is paying for AI coding tools. I'm not. And after today, you won't either." (8.7)</li>
        <li>"This is the file every developer should have. It's 47 lines. It replaces $200 of subscriptions." (8.4)</li>
        <li>"What you're looking at is running entirely offline." (8.0)</li>
        <li>"I spent six months on this so you don't have to." (7.6)</li>
      </ol>
    </>,

  "hooks-cursor":
  <>
      <h1>5 hooks — "Cursor vs Cline"</h1>
      <ol>
        <li>"I switched from Cursor to Cline three weeks ago. Here's what I wish I'd known." (8.9)</li>
        <li>"Cursor's pricing change pushed me out. The replacement is free." (8.5)</li>
      </ol>
    </>,

  "tpl-demo":
  <>
      <h1>Template — Demo-first</h1>
      <p>Opens with the working result on screen, no face cam, no setup. Narration starts at ~3 seconds.</p>
      <pre><code>{`[0:00] visual: completed demo running
[0:03] narrator: one-sentence claim
[0:08] narrator: precise constraint`}</code></pre>
    </>,

  "tpl-contra":
  <>
      <h1>Template — Contrarian</h1>
      <p>Opens with a statement that pre-frames the audience as smart for clicking. Higher CTR, slightly higher unsub risk.</p>
    </>,

  "tpl-object":
  <>
      <h1>Template — Object-first</h1>
      <p>Opens on a single object/file/screen. "This is the file…" Lower-risk, broadly applicable.</p>
    </>,


  // Distribution
  "dist-output":
  <>
      <h1>Distribution kit — Local RAG in 20 min</h1>
      <h2>Titles</h2>
      <ol>
        <li>I built a RAG that runs on my laptop. In 20 minutes.</li>
        <li>You don't need an API. (Local RAG, 47 lines)</li>
        <li>This RAG runs offline. It cost me $0 to build.</li>
      </ol>
      <h2>Chapters · 7</h2>
      <h2>Thumbnail brief</h2>
      <p>Laptop with terminal open, "OFFLINE" label glowing. Face cam mild shock. Top text: <code>20 MIN. NO API.</code></p>
    </>,

  "outline-rag":
  <>
      <h1>Outline — Local RAG in 20 min</h1>
      <ol>
        <li>The setup (00:00)</li>
        <li>Why local matters (01:30)</li>
        <li>Embedding model: nomic-embed-text (04:12)</li>
        <li>Vector store: sqlite-vss (07:40)</li>
        <li>Putting it together (11:05)</li>
        <li>Live demo on my codebase (16:20)</li>
        <li>Where it breaks (18:45)</li>
        <li>Outro + next video tease (20:10)</li>
      </ol>
    </>,

  "outline-cursor":
  <>
      <h1>Outline — Cursor vs Cline</h1>
      <p style={{ color: "var(--warning)" }}>⚠ In progress — 4 of 8 sections drafted.</p>
    </>,

  "thumb-brief":
  <>
      <h1>Thumbnail brief template</h1>
      <p>Channel style guide: high-contrast object/face split, max 4 words of text, yellow accent on the number.</p>
    </>,


  // Brain
  "brain-current":
  <>
      <h1>Vision Pro teardown — analysis</h1>
      <p><strong>Hook Quality:</strong> 8.4/10 · <strong>Structure:</strong> 7.9/10 · <strong>Triggers:</strong> 5</p>
      <p>The opening does three jobs in eleven seconds. Authority claim, payoff promise, antagonist frame. Active watching pattern.</p>
    </>,

  "brain-prev1":
  <>
      <h1>Fireship — Svelte rant</h1>
      <p><strong>Hook Quality:</strong> 9.1/10. Heavy reliance on the contrarian-claim pattern. Audience pre-flattered as "smart enough to disagree".</p>
    </>,

  "brain-prev2":
  <>
      <h1>Marques — segment cuts breakdown</h1>
      <p><strong>Structure:</strong> 9.4/10. Cuts at exact retention dips. CTA lives at the 47% mark.</p>
    </>,

  "tech-authority":
  <>
      <h1>Technique — Authority Claim</h1>
      <p>Place an unjustified expertise assertion in the first 3 seconds. Don't introduce yourself; assume it.</p>
      <h2>8 examples</h2>
      <ul>
        <li>"The first second I saw this, I knew…"</li>
        <li>"I've been building this for 12 years…"</li>
        <li>"Most people will get this wrong…"</li>
      </ul>
    </>,

  "tech-timestamp":
  <>
      <h1>Technique — Timestamp Promise</h1>
      <p>Reference a specific later moment in the video. "Watch what happens at 0:23." Locks in a forward-looking attention contract.</p>
    </>,

  // Title stage
  "title-output":
  <>
      <h1>Title candidates — Local RAG in 20 min</h1>
      <ol>
        <li><strong>I built a RAG that runs on my laptop. In 20 minutes.</strong> <em>(predicted CTR 9.4%)</em></li>
        <li><strong>You don't need an API. (Local RAG, 47 lines)</strong> <em>(9.1%)</em></li>
        <li><strong>This RAG runs offline. It cost me $0 to build.</strong> <em>(8.7%)</em></li>
        <li><strong>20 minutes. 47 lines. No API key.</strong> <em>(8.5%)</em></li>
        <li><strong>I gave Claude my entire codebase… locally.</strong> <em>(7.9%)</em></li>
      </ol>
      <h2>Why these work</h2>
      <ul>
        <li>Constraints up front (numbers, scope) outperform abstract titles by 3.4×.</li>
        <li>"No API" wins the search-driven traffic from cost-sensitive devs.</li>
        <li>First-person framing ("I built") outperforms 2nd person on this channel.</li>
      </ul>
    </>,

  "title-cursor":
  <>
      <h1>Title candidates — Cursor vs Cline</h1>
      <ol>
        <li>Cursor lost me. Here's the 4-tool setup I use now. <em>(9.0%)</em></li>
        <li>I switched from Cursor to Cline. No regrets. <em>(8.6%)</em></li>
        <li>The Cursor pricing change pushed me out. <em>(8.2%)</em></li>
      </ol>
    </>,

  "title-pattern-built":
  <>
      <h1>Pattern — I built X in Y</h1>
      <p>Highest-CTR title template on this channel. Pairs a verb ("built", "shipped", "deployed") with a constraint (time, lines, dollars).</p>
      <ul>
        <li>I built a RAG in 20 minutes.</li>
        <li>I shipped a CLI in 47 lines.</li>
        <li>I deployed an AI agent for $0.</li>
      </ul>
    </>,

  "title-pattern-contra":
  <>
      <h1>Pattern — Contrarian claim</h1>
      <p>Higher variance. When it lands it dominates; when it misses it underperforms baseline by ~30%.</p>
    </>,

  "title-pattern-num":
  <>
      <h1>Pattern — Number-prefix</h1>
      <p>"3 prompts that fix…", "5 hooks that…". Safe floor, low ceiling. Use when you need dependable mid-range performance.</p>
    </>,

  // Outline stage
  "outline-rag":
  <>
      <h1>Outline — Local RAG in 20 min</h1>
      <ol>
        <li><strong>The setup (00:00–01:30)</strong> — demo on screen, narrate the claim.</li>
        <li><strong>Why local matters (01:30–04:12)</strong> — cost + privacy framing.</li>
        <li><strong>Embedding model: nomic-embed-text (04:12–07:40)</strong> — install + first query.</li>
        <li><strong>Vector store: sqlite-vss (07:40–11:05)</strong> — schema + insert path.</li>
        <li><strong>Putting it together (11:05–16:20)</strong> — wiring + retrieval loop.</li>
        <li><strong>Live demo on my codebase (16:20–18:45)</strong> — real query, real answer.</li>
        <li><strong>Where it breaks (18:45–20:10)</strong> — honest failure modes.</li>
        <li><strong>Outro + next video tease (20:10–end)</strong></li>
      </ol>
      <h2>Retention shape target</h2>
      <p>Demo at 0:02. Pre-pay the hook at 0:30. CTA at the 11-minute mark (≈55% of runtime).</p>
    </>,

  "outline-tpl-howto":
  <>
      <h1>Template — How-to tutorial</h1>
      <ol>
        <li>Working demo on screen</li>
        <li>Why it matters (cost / risk / time)</li>
        <li>The 3–4 building blocks, one at a time</li>
        <li>Wiring them together</li>
        <li>Live demo</li>
        <li>Failure modes</li>
        <li>CTA loop + next video</li>
      </ol>
    </>,

  "outline-tpl-opinion":
  <>
      <h1>Template — Opinion essay</h1>
      <ol>
        <li>Claim, no setup</li>
        <li>Single piece of evidence</li>
        <li>Counter-objection acknowledged + refuted</li>
        <li>Stakes / who this changes things for</li>
        <li>Concrete next action</li>
      </ol>
    </>

};

function generateSourcePreview(s) {
  return (
    <>
      <div className="viewer-empty-meta">
        <div><span className="viewer-empty-meta-key">URL · </span><span className="viewer-empty-meta-val">{s.url}</span></div>
        <div><span className="viewer-empty-meta-key">Type · </span><span className="viewer-empty-meta-val">{s.host === "YT" ? "Video source" : s.host === "RD" ? "Forum thread" : s.host === "HN" ? "Forum thread" : s.host === "X" ? "Microblog" : "Document"}</span></div>
        <div><span className="viewer-empty-meta-key">Scope · </span><span className="viewer-empty-meta-val">{s.meta}</span></div>
      </div>
      <h1>{s.title}</h1>
      <p style={{ color: "var(--text-secondary)" }}>
        Source preview cached locally. Click "Open externally" to load the live page in your browser.
      </p>
      {s.host === "YT" &&
      <>
          <h2>Why this was cited</h2>
          <p>This video's first-30-second retention curve was used as a calibration anchor for the "demo-first" pattern detection. Notable: the AVD at the 0:55 mark exceeds the channel's 30-day baseline by 14 points.</p>
          <h2>Captured signals</h2>
          <ul>
            <li>Working demo on screen at 0:02</li>
            <li>Specific tool name in first sentence</li>
            <li>Constraint stated by 0:08 ("in 47 lines")</li>
            <li>Mid-roll CTA at 11:12 (54% of runtime)</li>
          </ul>
        </>
      }
      {(s.host === "RD" || s.host === "HN") &&
      <>
          <h2>Sampled threads</h2>
          <ul>
            <li>Thread 1 — top sentiment cluster: "context limits"</li>
            <li>Thread 2 — top cluster: "pricing changes"</li>
            <li>Thread 3 — top cluster: "model selection UI"</li>
          </ul>
          <h2>Signal density</h2>
          <p>{s.meta} matched the topic filter. 38% were keep-worthy after dedup. The kept set was passed to the synthesis pass.</p>
        </>
      }
      {s.host === "X" &&
      <>
          <h2>List composition</h2>
          <p>Curated list of 84 accounts active on AI dev tools. Posts were filtered by engagement-to-follower ratio &gt; 2% to remove low-signal noise.</p>
        </>
      }
      {s.host === "📊" &&
      <>
          <h2>Snapshot</h2>
          <pre><code>{`series,scope,value
median_ctr,6mo,0.078
avd_baseline,6mo,0.61
top_video,6mo,"Local RAG in 20 min"`}</code></pre>
        </>
      }
      {s.host === "📝" &&
      <>
          <h2>Preview</h2>
          <p>Local transcript file. Stored in <code>vault://research/raw/interviews</code>.</p>
        </>
      }
      {s.host === "📚" &&
      <>
          <h2>Cross-references</h2>
          <ul>
            <li>authority-claim.md (8 examples)</li>
            <li>timestamp-promise.md (12 examples)</li>
            <li>contrarian-frame.md (6 examples)</li>
          </ul>
        </>
      }
      {s.host === "🎬" &&
      <>
          <h2>Channel index</h2>
          <p>Curated set of your own top-performing video openings. Used to calibrate hook generation against your channel's voice.</p>
        </>
      }
    </>);

}

function TreeRow({ row, onClick }) {
  const folderIcon =
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6Z" />
    </svg>;

  const fileIcon =
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>;

  const clickable = row.type === "file";
  return (
    <div
      className={"tree-row " + (row.type === "folder" ? "is-folder " : "") + (row.current ? "is-current " : "") + (clickable ? "is-clickable" : "")}
      onClick={clickable ? onClick : undefined}
      role={clickable ? "button" : undefined}
      tabIndex={clickable ? 0 : undefined}>
      
      {row.depth ? <span className="tree-indent" /> : null}
      <span className="tree-icon">{row.type === "folder" ? folderIcon : fileIcon}</span>
      <span className="tree-name">{row.name}</span>
      {row.type === "folder" && <span className="tree-meta">{row.count} items</span>}
      {row.type === "file" && <span className="tree-meta">{row.meta}</span>}
    </div>);

}

function FileViewer({ item, onBack, folder, totalCount }) {
  const isSource = item._kind === "source";
  const content = isSource ?
  generateSourcePreview(item) :
  FILE_CONTENT[item.kind] || <p style={{ color: "var(--text-muted)" }}>Preview not yet generated for this file.</p>;

  return (
    <div className="sources-panel">
      {totalCount !== undefined && <VaultBookmark count={totalCount} />}
      <div className="viewer-toolbar">
        <button className="viewer-back" onClick={onBack}>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="15 18 9 12 15 6" />
          </svg>
          Files
        </button>
        <div className="viewer-path">
          {isSource ?
          <>session://sources/<span className="viewer-path-name">{item.url}</span></> :
          <>~/content-hub/{folder}<span className="viewer-path-name">{item.name}</span></>
          }
        </div>
        {isSource ?
        <button className="viewer-external">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              <polyline points="15 3 21 3 21 9" />
              <line x1="10" y1="14" x2="21" y2="3" />
            </svg>
            Open externally
          </button> :

        <span className="viewer-meta-pill">{item.current ? "current run" : "vault file"}</span>
        }
      </div>
      <div className="viewer-body md">
        {content}
      </div>
    </div>);

}

function SourcesPanel({ stageId }) {
  const data = VAULT_DATA[stageId] || VAULT_DATA.research;
  const [selected, setSelected] = useState(null);
  const filesCount = data.tree.filter((r) => r.type === "file").length;
  const totalCount = filesCount + data.sources.length;

  if (selected) {
    return <FileViewer item={selected} onBack={() => setSelected(null)} folder={data.folder} totalCount={totalCount} />;
  }

  return (
    <div className="sources-panel">
      <VaultBookmark count={totalCount} />
      <div className="sources-meta">
        <div className="sources-meta-left">
          <span className="sources-meta-eyebrow">Vault</span>
          <span>~/content-hub/{data.folder}</span>
        </div>
        <span>local-first · synced</span>
      </div>
      <div className="sources-body">
        <div className="sources-section">
          <h3 className="sources-section-title">
            Files & folders
            <span className="sources-section-count">{data.tree.filter((r) => r.type === "file").length} files</span>
          </h3>
          <div className="tree">
            {data.tree.map((row, i) =>
            <TreeRow key={i} row={row} onClick={() => setSelected({ ...row, _kind: "file" })} />
            )}
          </div>
        </div>
        <div className="sources-section">
          <h3 className="sources-section-title">
            Sources cited by this run
            <span className="sources-section-count">{data.sources.length}</span>
          </h3>
          <div>
            {data.sources.map((s, i) =>
            <button key={i} className="source-link" onClick={() => setSelected({ ...s, _kind: "source" })}>
                <div className="source-link-favicon">{s.host}</div>
                <div className="source-link-body">
                  <div className="source-link-title">{s.title}</div>
                  <div className="source-link-url">{s.url}</div>
                </div>
                <div className="source-link-meta">{s.meta}</div>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>);

}

// StackedPanel — two faces, swap on click of the back card. No tabs.
function StackedPanel({ front, back }) {
  const [frontIsActive, setFrontIsActive] = useState(true);
  const swap = () => setFrontIsActive((v) => !v);

  return (
    <div className="stacked-panel">
      <div
        className={"stacked-face " + (frontIsActive ? "is-front" : "is-back")}
        onClick={frontIsActive ? undefined : swap}>
        
        {front}
      </div>
      <div
        className={"stacked-face " + (!frontIsActive ? "is-front" : "is-back")}
        onClick={!frontIsActive ? undefined : swap}>
        
        {back}
      </div>
    </div>);

}

// VaultBookmark — always-visible vertical tab on the right edge of
// the SourcesPanel. Reads as a folder bookmark; when the panel is in
// the back position, this is the visible affordance the user clicks.
function VaultBookmark({ count }) {
  return (
    <div className="vault-bookmark" aria-hidden="true">
      <div className="vault-bookmark-icon">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
          <path d="M2 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6Z" />
        </svg>
      </div>
      <div className="vault-bookmark-text">Vault · Sources</div>
      <div className="vault-bookmark-count">{count}</div>
    </div>);

}

window.SourcesPanel = SourcesPanel;
window.StackedPanel = StackedPanel;