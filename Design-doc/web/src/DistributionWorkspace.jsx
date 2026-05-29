import { useState, useEffect } from 'react';
import Icon from './Icons.jsx';
import OutlineTab from './DistributionTabs/OutlineTab.jsx';
import TitleTab from './DistributionTabs/TitleTab.jsx';
import CascadeTab from './DistributionTabs/CascadeTab.jsx';
import ShortFormTab from './DistributionTabs/ShortFormTab.jsx';
import VoiceCleanupTab from './DistributionTabs/VoiceCleanupTab.jsx';

const TABS = [
  { slug: 'outline',       label: 'Outline',        component: OutlineTab },
  { slug: 'title',         label: 'Title',           component: TitleTab },
  { slug: 'cascade',       label: 'Cascade',         component: CascadeTab },
  { slug: 'short-form',    label: 'Short-form',      component: ShortFormTab },
  { slug: 'voice-cleanup', label: 'Voice-cleanup',   component: VoiceCleanupTab },
];

const VALID_SLUGS = new Set(TABS.map((t) => t.slug));

function getTabFromHash() {
  const m = window.location.hash.match(/^#distribution\/(.+)$/);
  const slug = m ? m[1] : null;
  return VALID_SLUGS.has(slug) ? slug : 'outline';
}

export default function DistributionWorkspace({ onBack }) {
  const [activeTab, setActiveTab] = useState(getTabFromHash);

  useEffect(() => {
    const handler = () => setActiveTab(getTabFromHash());
    window.addEventListener('hashchange', handler);
    return () => window.removeEventListener('hashchange', handler);
  }, []);

  const navigate = (slug) => {
    /* eslint-disable-next-line react-hooks/immutability */
    window.location.hash = `distribution/${slug}`;
    setActiveTab(slug);
  };

  const ActiveTab = TABS.find((t) => t.slug === activeTab)?.component;

  return (
    <div data-screen-label="Distribution" style={{ '--stage-color': 'var(--stage-distribution)' }}>
      <div className="stage-banner">
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, position: 'relative', zIndex: 1 }}>
          <button className="back-btn" onClick={onBack} title="Back to Dashboard">
            <Icon.ArrowLeft size={16} />
          </button>
          <div className="stage-banner-icon"><Icon.Share2 size={28} /></div>
        </div>
        <div className="stage-banner-text">
          <div className="stage-banner-eyebrow">Pipeline · 07</div>
          <h1 className="stage-banner-title">Distribution</h1>
          <p className="stage-banner-tagline">Outline → Titles → Cascade → Short-form → Voice-cleanup.</p>
        </div>
        <div className="stage-banner-orb stage-banner-orb-1" aria-hidden="true" />
        <div className="stage-banner-orb stage-banner-orb-2" aria-hidden="true" />
      </div>

      <div className="dist-tab-bar">
        {TABS.map((tab) => (
          <button
            key={tab.slug}
            className={'dist-tab' + (activeTab === tab.slug ? ' is-active' : '')}
            onClick={() => navigate(tab.slug)}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="dist-tab-content">
        {ActiveTab && <ActiveTab />}
      </div>
    </div>
  );
}
