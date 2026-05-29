import { useCallback } from 'react';
import Icon from './Icons.jsx';
import { usePipelineSnapshot } from './hooks/usePipelineSnapshot.js';

const CARD_DEFS = [
  { id: "trends",   name: "Trends",   icon: "TrendingUp",   color: "var(--stage-trends)",      cta: "Run Trends" },
  { id: "research", name: "Research", icon: "FlaskConical",  color: "var(--stage-research)",    cta: "Run Research" },
  { id: "ideation", name: "Ideation", icon: "Lightbulb",    color: "var(--stage-ideation)",    cta: "Run Ideation" },
  { id: "outline",  name: "Outline",  icon: "FileText",     color: "var(--stage-distribution)", cta: "View Outlines" },
];

function formatRelative(isoString) {
  if (!isoString) return "";
  const diff = Date.now() - new Date(isoString).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return mins <= 1 ? "just now" : `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return days === 1 ? "yesterday" : `${days} days ago`;
}

function Dashboard({ onNavigate }) {
  const today = new Date().toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric" });
  const { recents, runningSet } = usePipelineSnapshot();

  const handleNavigate = useCallback((target) => {
    onNavigate(target);
  }, [onNavigate]);

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
        onClick={() => handleNavigate("brain")}
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
        {CARD_DEFS.map((card) => {
          const IconCmp = Icon[card.icon];
          const items = recents[card.id] || [];
          const running = runningSet.has(card.id);
          return (
            <div
              key={card.id}
              className={"dash-card" + (running ? " running" : "")}
              style={{ "--stage-color": card.color, fontWeight: "600", fontFamily: "Inter", backgroundColor: "rgb(26, 30, 38)" }}
              onClick={() => {
                if (card.id === "outline") {
                  window.location.hash = "distribution/outline";
                  handleNavigate("distribution");
                } else {
                  handleNavigate(card.id);
                }
              }}>

              <div className="dash-card-header">
                <div className="dash-card-icon"><IconCmp size={18} /></div>
                <div style={{ flex: 1 }}>
                  <div className="dash-card-name">{card.name}</div>
                </div>
                <div className="dash-card-open">
                  {running ?
                    <span className="nav-status running" style={{ width: 8, height: 8 }} /> :
                    <Icon.ArrowRight size={14} />
                  }
                </div>
              </div>

              <ul className="activity-list">
                {items.length === 0 ? (
                  <li className="activity-item" style={{ color: "var(--text-muted)" }}>No recent files</li>
                ) : items.map((item, i) => (
                  <li key={i} className="activity-item">
                    <span className="activity-text">{item.name}</span>
                    <span className="activity-time">{formatRelative(item.modified)}</span>
                  </li>
                ))}
              </ul>

              <button
                className="btn-stage"
                style={{ "--stage-color": card.color }}
                onClick={(e) => {
                  e.stopPropagation();
                  if (card.id === "outline") {
                    window.location.hash = "distribution/outline";
                    handleNavigate("distribution");
                  } else {
                    handleNavigate(card.id);
                  }
                }}>
                <Icon.Play size={12} />
                {card.cta}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Dashboard;
