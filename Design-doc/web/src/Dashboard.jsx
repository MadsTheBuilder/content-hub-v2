import { useCallback } from 'react';
import Icon from './Icons.jsx';
import { usePipelineSnapshot } from './hooks/usePipelineSnapshot.js';

const CARD_DEFS = [
  { id: "trends",   step: "01", name: "Trends",   icon: "TrendingUp",   color: "var(--stage-trends)",       cta: "Run Trends" },
  { id: "research", step: "02", name: "Research",  icon: "FlaskConical", color: "var(--stage-research)",     cta: "Run Research" },
  { id: "ideation", step: "03", name: "Ideation",  icon: "Lightbulb",   color: "var(--stage-ideation)",     cta: "Run Ideation" },
  { id: "outline",  step: "04", name: "Outline",   icon: "FileText",    color: "var(--stage-distribution)", cta: "View Outlines" },
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
  const handleNavigate = useCallback((target) => onNavigate(target), [onNavigate]);

  return (
    <div data-screen-label="Dashboard">

      {/* ── Header ── */}
      <header className="dash-ctrl-header">
        <div className="dash-ctrl-left">
          <div className="dash-ctrl-eyebrow">PRODUCTION OPS</div>
          <h1 className="dash-ctrl-title">Dashboard</h1>
          <p className="dash-ctrl-date">
            <span>{today}</span>
            {runningSet.size > 0 && (
              <span className="dash-ctrl-live">
                <span className="nav-status running" style={{ width: 6, height: 6 }} />
                {runningSet.size} active
              </span>
            )}
          </p>
        </div>
        <button className="dash-ctrl-new-btn" onClick={() => handleNavigate("trends")}>
          <Icon.Zap size={15} />
          <span>New Video</span>
        </button>
      </header>

      {/* ── Brain Banner ── */}
      <button
        className="brain-banner"
        onClick={() => handleNavigate("brain")}
        aria-label="Open Knowledge Brain"
      >
        <div className="brain-banner-icon"><Icon.Brain size={32} /></div>
        <div className="brain-banner-text">
          <div className="brain-banner-eyebrow">Knowledge Brain</div>
          <div className="brain-banner-title">The Brain</div>
          <div className="brain-banner-tagline">Feed me — and I'll spit analysis.</div>
        </div>
        <div className="brain-banner-cta">
          <span>Drop something in</span>
          <Icon.ArrowRight size={16} />
        </div>
        <div className="brain-banner-orb brain-banner-orb-1" aria-hidden="true" />
        <div className="brain-banner-orb brain-banner-orb-2" aria-hidden="true" />
      </button>

      {/* ── Pipeline strip ── */}
      <div className="dash-pipeline-strip">
        <div className="dash-pipeline-label">
          <Icon.Zap size={10} />
          PIPELINE
        </div>
        <div className="dash-pipeline-track">
          {CARD_DEFS.map((card, i) => (
            <span key={card.id} style={{ display: 'contents' }}>
              <span className="dash-pipeline-dot" style={{ '--stage-color': card.color }} />
              {i < CARD_DEFS.length - 1 && <span className="dash-pipeline-seg" />}
            </span>
          ))}
        </div>
        <div className="dash-pipeline-count">{CARD_DEFS.length} stages</div>
      </div>

      {/* ── Stage grid ── */}
      <div className="dash-stage-grid">
        {CARD_DEFS.map((card, idx) => {
          const IconCmp = Icon[card.icon];
          const items = recents[card.id] || [];
          const running = runningSet.has(card.id);
          const navigate = () => {
            if (card.id === "outline") {
              window.location.hash = "distribution/outline";
              handleNavigate("distribution");
            } else {
              handleNavigate(card.id);
            }
          };

          return (
            <div
              key={card.id}
              className={"dash-stage-card" + (running ? " running" : "")}
              style={{ "--stage-color": card.color, animationDelay: `${idx * 65}ms` }}
              onClick={navigate}
            >
              {/* Stage badge + running dot */}
              <div className="dash-stage-top">
                <span className="dash-stage-badge">{card.step}</span>
                {running && <span className="nav-status running" style={{ width: 7, height: 7 }} />}
              </div>

              {/* Icon + name */}
              <div className="dash-stage-identity">
                <div className="dash-stage-icon">
                  <IconCmp size={20} />
                </div>
                <div className="dash-stage-name">{card.name}</div>
              </div>

              {/* Recent files feed */}
              <ul className="dash-stage-feed">
                {items.length === 0 ? (
                  <li className="dash-feed-empty">No recent files</li>
                ) : items.map((item, i) => (
                  <li key={i} className="dash-feed-item">
                    <span className="dash-feed-name">{item.name}</span>
                    <span className="dash-feed-time">{formatRelative(item.modified)}</span>
                  </li>
                ))}
              </ul>

              {/* CTA */}
              <button
                className="dash-stage-cta"
                onClick={(e) => { e.stopPropagation(); navigate(); }}
              >
                <Icon.Play size={11} />
                {card.cta}
              </button>

              {/* Atmospheric glow orb */}
              <div className="dash-stage-orb" aria-hidden="true" />
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Dashboard;
