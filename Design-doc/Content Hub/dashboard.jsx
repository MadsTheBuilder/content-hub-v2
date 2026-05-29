// Dashboard view - 4-card grid

const dashCards = [
{
  id: "trends",
  name: "Trends",
  title: "Trends",
  icon: "TrendingUp",
  color: "var(--stage-trends)",
  running: false,
  activity: [
  { text: <><span className="topic-pill" style={{ "--stage-color": "var(--stage-trends)" }}>#AITools</span>Cline vs Cursor adoption split</>, time: "2h ago" },
  { text: <><span className="topic-pill" style={{ "--stage-color": "var(--stage-trends)" }}>#LocalLLM</span>Llama 3.3 on consumer GPUs</>, time: "yesterday" },
  { text: <><span className="topic-pill" style={{ "--stage-color": "var(--stage-trends)" }}>#DevTools</span>v0 hitting product-engineer ceiling</>, time: "3 days ago" }],

  cta: "Run Trends"
},
{
  id: "research",
  name: "Research",
  title: "Research",
  icon: "FlaskConical",
  color: "var(--stage-research)",
  running: true,
  activity: [
  { text: "Why AI tutorial videos go viral", badge: "12 sources" },
  { text: "The economics of dev-tool YouTube", badge: "8 sources" },
  { text: "Hook patterns of 1M+ view AI videos", badge: "21 sources" }],

  cta: "Run Research"
},
{
  id: "ideation",
  name: "Ideation",
  title: "Ideation",
  icon: "Lightbulb",
  color: "var(--stage-ideation)",
  running: false,
  activity: [
  { text: "Build a local RAG in 20 minutes", score: 9.2 },
  { text: "Why I quit Cursor (and what I use now)", score: 8.7 },
  { text: "The fastest way to ship an AI side project", score: 7.4 }],

  cta: "Run Ideation"
},
{
  id: "outline",
  name: "Outline",
  title: "Outline",
  icon: "FileText",
  color: "var(--stage-distribution)",
  running: false,
  activity: [
  { text: "Local RAG in 20 min — final draft", status: "8 sections" },
  { text: "Why I quit Cursor — v2", status: "In Progress", inProgress: true },
  { text: "Shipping AI side projects fast", status: "6 sections" }],

  cta: "View Outlines"
}];


function Dashboard({ onNavigate }) {
  const today = new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
  return (
    <div data-screen-label="Dashboard">
      <header className="page-header">
        <div>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-subtitle">{today} · 4 active stages · last run 12 minutes ago</p>
        </div>
        <button className="btn btn-primary">
          <Icon.Plus size={14} />
          New Video
        </button>
      </header>

      <button
        className="brain-banner"
        onClick={() => onNavigate("brain")}
        aria-label="Open Knowledge Brain"
      >
        <div className="brain-banner-icon">
          <Icon.Brain size={32} />
        </div>
        <div className="brain-banner-text">
          <div className="brain-banner-eyebrow">Knowledge Brain</div>
          <div className="brain-banner-title">The Brain</div>
          <div className="brain-banner-tagline">Feed me — and I'll spit analysis.</div>
        </div>
        <div className="brain-banner-stats">
          <div className="brain-banner-stat">
            <span className="brain-banner-stat-value">142</span>
            <span className="brain-banner-stat-label">decoded</span>
          </div>
          <div className="brain-banner-stat">
            <span className="brain-banner-stat-value">8.1</span>
            <span className="brain-banner-stat-label">avg hook /10</span>
          </div>
          <div className="brain-banner-stat">
            <span className="brain-banner-stat-value">37</span>
            <span className="brain-banner-stat-label">techniques saved</span>
          </div>
        </div>
        <div className="brain-banner-cta">
          <span>Drop something in</span>
          <Icon.ArrowRight size={16} />
        </div>
        <div className="brain-banner-orb brain-banner-orb-1" aria-hidden="true" />
        <div className="brain-banner-orb brain-banner-orb-2" aria-hidden="true" />
      </button>

      <div className="dash-grid">
        {dashCards.map((card) => {
          const IconCmp = Icon[card.icon];
          return (
            <div
              key={card.id}
              className={"dash-card" + (card.running ? " running" : "")}
              style={{ "--stage-color": card.color, fontWeight: "600", fontFamily: "Inter", backgroundColor: "rgb(26, 30, 38)" }}
              onClick={() => onNavigate(card.id === "outline" ? "distribution" : card.id)}>
              
              <div className="dash-card-header">
                <div className="dash-card-icon"><IconCmp size={18} /></div>
                <div style={{ flex: 1 }}>
                  <div className="dash-card-name">{card.name}</div>
                </div>
                <div className="dash-card-open">
                  {card.running ?
                  <span className="nav-status running" style={{ width: 8, height: 8 }} /> :

                  <Icon.ArrowRight size={14} />
                  }
                </div>
              </div>

              <ul className="activity-list">
                {card.activity.map((a, i) =>
                <li key={i} className="activity-item">
                    <span className="activity-text">{a.text}</span>
                    {a.badge && <span className="source-badge">{a.badge}</span>}
                    {a.score !== undefined &&
                  <>
                        <span className="relevance-bar"><span className="relevance-bar-fill" style={{ width: `${a.score * 10}%` }} /></span>
                        <span className="activity-time">{a.score.toFixed(1)}</span>
                      </>
                  }
                    {a.status &&
                  <span className={"status-chip" + (a.inProgress ? " in-progress" : "")}>{a.status}</span>
                  }
                    {a.time && <span className="activity-time">{a.time}</span>}
                  </li>
                )}
              </ul>

              <button
                className="btn-stage"
                style={{ "--stage-color": card.color }}
                onClick={(e) => {e.stopPropagation();onNavigate(card.id === "outline" ? "distribution" : card.id);}}>
                
                <Icon.Play size={12} />
                {card.cta}
              </button>
            </div>);

        })}
      </div>
    </div>);

}

window.Dashboard = Dashboard;