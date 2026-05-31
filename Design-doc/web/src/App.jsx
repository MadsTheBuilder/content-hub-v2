import { useState, useEffect } from 'react';
import { useTweaks } from './TweaksPanel.jsx';
import Dashboard from './Dashboard.jsx';
import Sidebar from './Sidebar.jsx';
import StageWorkspace from './StageWorkspace.jsx';
import TweaksPanel, { TweakSection, TweakColor, TweakRadio, TweakToggle, TweakSelect } from './TweaksPanel.jsx';
import Brain from './Brain.jsx';
import DistributionWorkspace from './DistributionWorkspace.jsx';
import FullPipelinePage from './FullPipelinePage.jsx';

const TWEAK_DEFAULTS = {
  "accent": "#5B8DEF",
  "view": "dashboard",
  "sidebarCollapsed": false,
  "density": "comfortable"
};

function App() {
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const [view, setView] = useState(t.view || "dashboard");
  const [collapsed, setCollapsed] = useState(t.sidebarCollapsed);

  // Particle bootstrap
  useEffect(() => {
    import('./particles.js');
  }, []);

  // Apply accent override
  useEffect(() => {
    document.documentElement.style.setProperty("--accent", t.accent);
  }, [t.accent]);

  // Density
  useEffect(() => {
    document.documentElement.style.setProperty("--main-pad", t.density === "compact" ? "20px 28px 48px" : "32px 40px 64px");
  }, [t.density]);

  // Page accent — drives ambient gradient + particle color per view
  useEffect(() => {
    const accents = {
      dashboard: "#06B6D4",
      trends: "#F5A623",
      research: "#5B8DEF",
      ideation: "#A855F7",
      hooks: "#EC4899",
      distribution: "#3DD68C",
      "full-pipeline": "#06B6D4",
      brain: "#06B6D4",
      settings: t.accent,
    };
    document.documentElement.style.setProperty("--page-accent", accents[view] || t.accent);
  }, [view, t.accent]);

  const navigate = (v) => {
    setView(v);
    setTweak("view", v);
  };

  const toggleCollapsed = () => {
    setCollapsed((c) => {
      const next = !c;
      setTweak("sidebarCollapsed", next);
      return next;
    });
  };

  return (
    <div className={"app" + (collapsed ? " collapsed" : "")}>
      <Sidebar
        active={view}
        onNavigate={navigate}
        collapsed={collapsed}
        onToggleCollapse={toggleCollapsed}
      />
      <main className="main">
        <div className="main-inner" style={{ padding: "var(--main-pad, 32px 40px 64px)" }}>
          {view === "dashboard" && <Dashboard onNavigate={navigate} />}
          {view === "trends" && <StageWorkspace stageId="trends" onBack={() => navigate("dashboard")} />}
          {view === "research" && (
            <StageWorkspace
              stageId="research"
              onBack={() => navigate("dashboard")}
              initialState={{
                prompt: "Why do AI tutorial videos go viral? Focus on hook patterns and the first 30 seconds.",
                urls: ["https://youtube.com/watch?v=fireship-rag"],
              }}
            />
          )}
          {view === "ideation" && <StageWorkspace stageId="ideation" onBack={() => navigate("dashboard")} />}
          {view === "hooks" && (
            <StageWorkspace
              stageId="hooks"
              onBack={() => navigate("dashboard")}
              initialState={{
                prompt: "How to build a local RAG system in 20 minutes — for indie devs who want privacy and no API costs.",
              }}
            />
          )}
          {view === "distribution" && <DistributionWorkspace onBack={() => navigate("dashboard")} />}
          <div style={{ display: view === "full-pipeline" ? "" : "none" }}>
            <FullPipelinePage onBack={() => navigate("dashboard")} />
          </div>
          {view === "brain" && <Brain />}
          {view === "settings" && <SettingsPlaceholder />}
        </div>
      </main>

      <TweaksPanel title="Tweaks">
        <TweakSection title="Theme">
          <TweakColor
            label="Accent"
            value={t.accent}
            onChange={(v) => setTweak("accent", v)}
            options={["#5B8DEF", "#06B6D4", "#A855F7", "#3DD68C", "#F5A623"]}
          />
          <TweakRadio
            label="Density"
            value={t.density}
            onChange={(v) => setTweak("density", v)}
            options={[
              { value: "compact", label: "Compact" },
              { value: "comfortable", label: "Comfortable" },
            ]}
          />
        </TweakSection>
        <TweakSection title="Layout">
          <TweakToggle
            label="Sidebar collapsed"
            value={collapsed}
            onChange={(v) => { setCollapsed(v); setTweak("sidebarCollapsed", v); }}
          />
        </TweakSection>
        <TweakSection title="Jump to screen">
          <TweakSelect
            label="Active view"
            value={view}
            onChange={navigate}
            options={[
              { value: "dashboard", label: "Dashboard" },
              { value: "trends", label: "Trends workspace" },
              { value: "research", label: "Research (with results)" },
              { value: "ideation", label: "Ideation workspace" },
              { value: "hooks", label: "Hooks (with results)" },
              { value: "distribution", label: "Distribution workspace" },
              { value: "full-pipeline", label: "Full Pipeline (auto-run)" },
              { value: "brain", label: "Knowledge Brain (analysis open)" },
            ]}
          />
        </TweakSection>
      </TweaksPanel>
    </div>
  );
}

function SettingsPlaceholder() {
  return (
    <div data-screen-label="Settings">
      <header className="page-header">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">Account, models, vault paths, integrations.</p>
        </div>
      </header>
      <div style={{
        background: "var(--bg-surface)",
        border: "1px solid var(--border)",
        borderRadius: "var(--r-card)",
        padding: 40,
        textAlign: "center",
        color: "var(--text-muted)"
      }}>
        Settings screen — not part of the v1 scope brief.
      </div>
    </div>
  );
}

export default App;
