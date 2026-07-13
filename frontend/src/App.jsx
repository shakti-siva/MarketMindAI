import React, { useState, useEffect } from 'react';
import { 
  Smile, 
  Sparkles, 
  TrendingUp, 
  BrainCircuit, 
  Target, 
  DollarSign, 
  Bot,
  Activity,
  Layers
} from 'lucide-react';
import CustomerVoice from './components/CustomerVoice';
import IngredientIntel from './components/IngredientIntel';
import TrendIntel from './components/TrendIntel';
import PsychologyAnalyzer from './components/PsychologyAnalyzer';
import CampaignPlanner from './components/CampaignPlanner';
import BudgetAdvisor from './components/BudgetAdvisor';
import AIConsultant from './components/AIConsultant';
import './App.css';

export default function App() {
  const [activeTab, setActiveTab] = useState('voice');
  const [products, setProducts] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState('');
  const [loading, setLoading] = useState(true);

  // Fetch product list on mount
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/products`)
      .then(res => res.json())
      .then(data => {
        const productList = Array.isArray(data) ? data : [];
        setProducts(productList);
        if (productList.length > 0) {
          setSelectedProductId(productList[0].product_id);
        }
        setLoading(false);
      })
  }, []);

  const renderActiveView = () => {
    switch (activeTab) {
      case 'voice':
        return (
          <CustomerVoice 
            products={products} 
            selectedProductId={selectedProductId} 
            setSelectedProductId={setSelectedProductId} 
          />
        );
      case 'ingredients':
        return <IngredientIntel />;
      case 'trends':
        return <TrendIntel />;
      case 'psychology':
        return <PsychologyAnalyzer />;
      case 'campaign':
        return <CampaignPlanner products={products} />;
      case 'budget':
        return (
          <BudgetAdvisor 
            products={products} 
            selectedProductId={selectedProductId} 
            setSelectedProductId={setSelectedProductId} 
          />
        );
      case 'consultant':
        return <AIConsultant />;
      default:
        return <CustomerVoice products={products} selectedProductId={selectedProductId} setSelectedProductId={setSelectedProductId} />;
    }
  };

  const navItems = [
    { id: 'voice', label: 'Customer Voice', icon: <Smile size={18} /> },
    { id: 'ingredients', label: 'Ingredient Intel', icon: <Layers size={18} /> },
    { id: 'trends', label: 'Trend Intel', icon: <TrendingUp size={18} /> },
    { id: 'psychology', label: 'Psychology Analyzer', icon: <BrainCircuit size={18} /> },
    { id: 'campaign', label: 'Campaign Planner', icon: <Target size={18} /> },
    { id: 'budget', label: 'Budget Advisor', icon: <DollarSign size={18} /> },
    { id: 'consultant', label: 'AI Consultant', icon: <Bot size={18} /> }
  ];

  if (loading) {
    return (
      <div style={{ 
        width: '100vw', 
        height: '100vh', 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center', 
        background: 'var(--bg-primary)',
        color: 'var(--text-secondary)',
        gap: '16px'
      }}>
        <div style={{ 
          width: '32px', 
          height: '32px', 
          borderRadius: '50%', 
          border: '3px solid rgba(212, 154, 137, 0.15)', 
          borderTopColor: 'var(--accent-rose)', 
          animation: 'spin 1.2s linear infinite' 
        }} />
        <span style={{ fontSize: '13px', fontFamily: 'var(--font-display)' }}>Initializing MarketMind AI platforms...</span>
      </div>
    );
  }

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        
        {/* Sidebar Brand header */}
        <div style={{ 
          padding: '24px 32px', 
          borderBottom: '1px solid var(--border-color)', 
          display: 'flex', 
          alignItems: 'center', 
          gap: '12px',
          background: 'rgba(255,255,255,0.01)'
        }}>
          <Activity size={24} style={{ color: 'var(--accent-rose)', filter: 'drop-shadow(0 0 4px rgba(212,154,137,0.4))' }} />
          <div>
            <h2 style={{ fontSize: '18px', color: 'var(--text-primary)', fontFamily: 'var(--font-display)', fontWeight: '700', letterSpacing: '-0.01em' }}>
              MarketMind AI
            </h2>
            <span style={{ fontSize: '9px', color: 'var(--accent-gold)', textTransform: 'uppercase', letterSpacing: '0.1em', fontWeight: 'bold' }}>
              Skincare Intelligence
            </span>
          </div>
        </div>

        {/* Sidebar Links */}
        <nav style={{ padding: '24px 16px', display: 'flex', flexDirection: 'column', gap: '8px', flexGrow: 1 }}>
          {navItems.map((item) => {
            const isActive = activeTab === item.id;
            return (
              <div 
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px', 
                  padding: '12px 16px', 
                  borderRadius: '10px', 
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: isActive ? '600' : '400',
                  color: isActive ? 'var(--text-primary)' : 'var(--text-secondary)',
                  background: isActive ? 'linear-gradient(135deg, rgba(212, 154, 137, 0.12), rgba(231, 160, 128, 0.05))' : 'transparent',
                  border: isActive ? '1px solid rgba(212, 154, 137, 0.25)' : '1px solid transparent',
                  transition: 'all 0.2s ease-in-out'
                }}
                className="sidebar-link-hover"
              >
                <span style={{ color: isActive ? 'var(--accent-rose)' : 'var(--text-muted)' }}>{item.icon}</span>
                {item.label}
              </div>
            );
          })}
        </nav>

        {/* Footer info in sidebar */}
        <div style={{ padding: '20px 24px', borderTop: '1px solid var(--border-color)', fontSize: '11px', color: 'var(--text-muted)' }}>
          <div>Model: <span style={{ color: 'var(--text-secondary)' }}>Llama 3 / GPT-4</span></div>
          <div style={{ marginTop: '4px' }}>Platform Version 1.0.0</div>
        </div>

      </aside>

      {/* Main Panel Viewport */}
      <main className="main-content">
        <style>{`
          .sidebar-link-hover:hover {
            color: var(--text-primary) !important;
            background: rgba(255, 255, 255, 0.02) !important;
          }
          .table-row-hover:hover {
            background: rgba(255, 255, 255, 0.01) !important;
          }
        `}</style>
        {renderActiveView()}
      </main>
    </div>
  );
}
