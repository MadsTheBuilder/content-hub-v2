import { useState, useEffect } from 'react';
import Icon from './Icons.jsx';
import { usePipelineSnapshot } from './hooks/usePipelineSnapshot.js';
import { getHealth } from './api.js';

const PIPELINE = [
  { id: "trends",       label: "Trends",       icon: "TrendingUp",  color: "var(--stage-trends)" },
  { id: "research",     label: "Research",     icon: "FlaskConical", color: "var(--stage-research)" },
  { id: "ideation",     label: "Ideation",     icon: "Lightbulb",   color: "var(--stage-ideation)" },
  { id: "hooks",        label: "Hooks",        icon: "Zap",         color: "var(--stage-hooks)" },
  { id: "distribution", label: "Distribution", icon: "Share2",      color: "var(--stage-distribution)" },
];

function Sidebar({ active, onNavigate, collapsed, onToggleCollapse }) {
  const { sidebarStatuses } = usePipelineSnapshot();
  const [health, setHealth] = useState(null);

  useEffect(() => {
    getHealth().then((h) => setHealth(h.status === "ok" ? "ok" : "error"));
  }, []);

  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark"></div>
        <div className="brand-text">
          <span className="brand-name">Content Hub</span>
          <span className="brand-version">v2.1.0</span>
        </div>
      </div>

      <div className="sidebar-section-label">Pipeline</div>
      <nav className="sidebar-nav">
        {PIPELINE.map((item) => {
          const IconCmp = Icon[item.icon];
          const isActive = active === item.id;
          const status = sidebarStatuses[item.id] || "idle";
          return (
            <button
              key={item.id}
              className={"nav-item" + (isActive ? " active" : "")}
              style={{ "--stage-color": item.color }}
              onClick={() => onNavigate(item.id)}>
              <span className="nav-icon"><IconCmp size={18} /></span>
              <span className="nav-label">{item.label}</span>
              <span className={"nav-status " + status} />
              <span className="nav-tooltip">{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="sidebar-divider" />

      <nav className="sidebar-nav">
        <button
          className={"nav-item" + (active === "brain" ? " active" : "")}
          style={{ "--stage-color": "var(--brain)" }}
          onClick={() => onNavigate("brain")}>
          <span className="nav-icon"><Icon.Brain size={20} /></span>
          <span className="nav-label">Knowledge Brain</span>
          <span className="nav-tooltip">Knowledge Brain</span>
        </button>
      </nav>

      <div className="sidebar-divider" />

      <nav className="sidebar-nav">
        <button
          className={"nav-item" + (active === "settings" ? " active" : "")}
          onClick={() => onNavigate("settings")}>
          <span className="nav-icon" style={{ color: "var(--text-secondary)" }}>
            <Icon.Settings size={18} />
          </span>
          <span className="nav-label" style={{ color: "var(--text-secondary)" }}>Settings</span>
          <span className="nav-tooltip">Settings</span>
        </button>
      </nav>

      <div className="sidebar-bottom">
        {health !== null && (
          <div className="sidebar-health" title={health === "ok" ? "Backend connected" : "Backend unavailable"}>
            <span
              className="nav-status"
              style={{
                width: 8,
                height: 8,
                background: health === "ok" ? "var(--stage-ideation, #3DD68C)" : "#EF4444",
                flexShrink: 0,
              }}
            />
            <span className="sidebar-bottom-label" style={{ fontSize: 11, color: "var(--text-muted)" }}>
              {health === "ok" ? "Backend up" : "Backend down"}
            </span>
          </div>
        )}
        <button className="collapse-toggle" onClick={onToggleCollapse} title={collapsed ? "Expand sidebar" : "Collapse sidebar"}>
          <span className="chevron-icon" style={{ display: "grid", placeItems: "center" }}>
            <Icon.ChevronLeft size={16} />
          </span>
          <span className="sidebar-bottom-label">Collapse</span>
        </button>
      </div>
    </aside>
  );
}

export { PIPELINE };
export default Sidebar;
