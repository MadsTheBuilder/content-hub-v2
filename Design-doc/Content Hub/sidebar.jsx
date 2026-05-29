// Sidebar component
const { useState, useEffect, useRef } = React;

const PIPELINE = [
{ id: "trends", label: "Trends", icon: "TrendingUp", color: "var(--stage-trends)", status: "done" },
{ id: "research", label: "Research", icon: "FlaskConical", color: "var(--stage-research)", status: "running" },
{ id: "ideation", label: "Ideation", icon: "Lightbulb", color: "var(--stage-ideation)", status: "done" },
{ id: "hooks", label: "Hooks", icon: "Zap", color: "var(--stage-hooks)", status: "idle" },
{ id: "title", label: "Title", icon: "Type", color: "var(--stage-title)", status: "idle" },
{ id: "outline", label: "Outline", icon: "ListTree", color: "var(--stage-outline)", status: "idle" },
{ id: "distribution", label: "Distribution", icon: "Share2", color: "var(--stage-distribution)", status: "idle" }];


function Sidebar({ active, onNavigate, collapsed, onToggleCollapse }) {
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
          return (
            <button
              key={item.id}
              className={"nav-item" + (isActive ? " active" : "")}
              style={{ "--stage-color": item.color }}
              onClick={() => onNavigate(item.id)}>
              
              <span className="nav-icon"><IconCmp size={18} /></span>
              <span className="nav-label">{item.label}</span>
              <span className={"nav-status " + item.status} />
              <span className="nav-tooltip">{item.label}</span>
            </button>);

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
        <button className="collapse-toggle" onClick={onToggleCollapse} title={collapsed ? "Expand sidebar" : "Collapse sidebar"}>
          <span className="chevron-icon" style={{ display: "grid", placeItems: "center" }}>
            <Icon.ChevronLeft size={16} />
          </span>
          <span className="sidebar-bottom-label">Collapse</span>
        </button>
      </div>
    </aside>);

}

window.Sidebar = Sidebar;
window.PIPELINE = PIPELINE;