import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { DollarSign, ShieldAlert, Sparkles, HelpCircle, CheckSquare, Settings, TrendingUp, Target, Activity } from 'lucide-react';

const COLORS = {
  marketing: '#d49a89',          // rose gold
  product_improvement: '#7ebc89' // mint
};

export default function BudgetAdvisor({ products, selectedProductId, setSelectedProductId }) {
  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!selectedProductId) return;
    setLoading(true);
    fetch(`${import.meta.env.VITE_API_URL}/api/budget/advise/${selectedProductId}`)
      .then(res => res.json())
      .then(data => {
        setAdvice(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching budget advice:", err);
        setLoading(false);
      });
  }, [selectedProductId]);

  if (loading && !advice) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div className="skeleton" style={{ height: '40px', width: '200px' }} />
        <div className="skeleton" style={{ height: '300px', width: '100%' }} />
      </div>
    );
  }

  const chartData = advice ? [
    { name: 'Marketing', value: advice.allocation.marketing, color: COLORS.marketing },
    { name: 'Product Improvement', value: advice.allocation.product_improvement, color: COLORS.product_improvement }
  ] : [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Title */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>Budget Allocation Advisor</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
            Get data-driven spend recommendations based on customer sentiment and market trends.
          </p>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Analyze Product:</label>
          <select 
            value={selectedProductId} 
            onChange={(e) => setSelectedProductId(e.target.value)}
            style={{ minWidth: '220px', padding: '10px' }}
          >
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>{p.product_name}</option>
            ))}
          </select>
        </div>
      </div>

      {advice && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', lgGridTemplateColumns: '1.2fr 1fr', gap: '24px', animation: 'fadeIn 0.4s ease' }}>
          
          {/* Left: Spend Recommendation Details */}
          <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
            <div className="glass-card-header" style={{ paddingBottom: '16px' }}>
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <DollarSign size={18} style={{ color: 'var(--accent-rose)' }} />
                Spend Advisor Report
              </h3>
              <span className={`badge ${advice.recommendation === 'Product Improvement' ? 'badge-danger' : advice.recommendation === 'Scale Marketing Spend' ? 'badge-success' : 'badge-warning'}`}>
                {advice.recommendation}
              </span>
            </div>
            
            <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '20px', flexGrow: 1 }}>
              
              {/* Product State summary info cards */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div style={{ padding: '16px', borderRadius: '12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: '600', textTransform: 'uppercase' }}>Product Sentiment</span>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px', marginTop: '8px' }}>
                    <span style={{ fontSize: '24px', fontWeight: 'bold', color: advice.positive_sentiment_percent >= 60 ? 'var(--accent-mint)' : 'var(--accent-coral)' }}>
                      {advice.positive_sentiment_percent}%
                    </span>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Positive review ratio</span>
                  </div>
                </div>

                <div style={{ padding: '16px', borderRadius: '12px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <span style={{ fontSize: '12px', color: 'var(--text-secondary)', fontWeight: '600', textTransform: 'uppercase' }}>Market Trend Momentum</span>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px', marginTop: '8px' }}>
                    <span style={{ fontSize: '24px', fontWeight: 'bold', color: advice.trend_momentum_percent >= 0 ? 'var(--accent-mint)' : 'var(--accent-coral)' }}>
                      {advice.trend_momentum_percent >= 0 ? '+' : ''}{advice.trend_momentum_percent}%
                    </span>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>for {advice.primary_ingredient}</span>
                  </div>
                </div>
              </div>

              {/* Narrative reasoning */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '12px', borderLeft: `4px solid ${advice.recommendation === 'Product Improvement' ? 'var(--accent-coral)' : (advice.recommendation === 'Scale Marketing Spend' ? 'var(--accent-mint)' : 'var(--accent-gold)')}` }}>
                <span style={{ fontSize: '13px', fontWeight: 'bold', color: 'var(--text-primary)' }}>Advisor Diagnostic Narrative</span>
                <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                  {advice.reasoning}
                </p>
              </div>

              {/* Recommended Actions checklist */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '8px' }}>
                <span style={{ fontSize: '14px', fontWeight: 'bold', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <CheckSquare size={16} style={{ color: 'var(--accent-rose)' }} /> Recommended Action Steps
                </span>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {advice.recommended_actions.map((act, idx) => (
                    <div key={idx} style={{ display: 'flex', gap: '12px', alignItems: 'flex-start', fontSize: '14px', color: 'var(--text-secondary)' }}>
                      <span style={{ color: 'var(--accent-rose)', marginTop: '2px' }}>✦</span>
                      <span style={{ lineHeight: '1.5' }}>{act}</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          </div>

          {/* Right: Allocation breakdown & Estimates */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            
            <div className="glass-panel" style={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <div className="glass-card-header">
                <h3>Budget Allocation Strategy</h3>
                <span className="badge badge-info">Capital efficiency</span>
              </div>
              
              <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px', justifyContent: 'center', flexGrow: 1 }}>
                
                <div style={{ width: '100%', height: '220px', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={90}
                        paddingAngle={6}
                        dataKey="value"
                        stroke="rgba(0,0,0,0)"
                      >
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                
                {/* Legend with percentages */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', width: '100%', padding: '0 20px', paddingBottom: '20px' }}>
                  
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px', paddingBottom: '12px', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--text-secondary)' }}>
                      <span style={{ width: '12px', height: '12px', borderRadius: '3px', backgroundColor: COLORS.marketing }} />
                      Marketing Campaign Focus
                    </span>
                    <span style={{ fontWeight: 'bold', color: 'var(--text-primary)', fontSize: '16px' }}>{advice.allocation.marketing}%</span>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '14px' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--text-secondary)' }}>
                      <span style={{ width: '12px', height: '12px', borderRadius: '3px', backgroundColor: COLORS.product_improvement }} />
                      Product Improvement (R&D)
                    </span>
                    <span style={{ fontWeight: 'bold', color: 'var(--text-primary)', fontSize: '16px' }}>{advice.allocation.product_improvement}%</span>
                  </div>

                </div>

              </div>
            </div>

            {/* Campaign Projections (Estimates) */}
            {advice.estimates && (
              <div className="glass-panel">
                <div className="glass-card-header">
                  <h3>Marketing Projections (Est.)</h3>
                </div>
                <div className="glass-card-body" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', textAlign: 'center' }}>
                   
                   <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
                     <TrendingUp size={18} style={{ margin: '0 auto', color: 'var(--accent-mint)' }} />
                     <span style={{ fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Est. ROI</span>
                     <span style={{ fontSize: '16px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{advice.estimates.roi}</span>
                   </div>

                   <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
                     <Target size={18} style={{ margin: '0 auto', color: 'var(--accent-gold)' }} />
                     <span style={{ fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Est. CAC</span>
                     <span style={{ fontSize: '16px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{advice.estimates.cac}</span>
                   </div>

                   <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
                     <Activity size={18} style={{ margin: '0 auto', color: 'var(--accent-rose)' }} />
                     <span style={{ fontSize: '12px', color: 'var(--text-secondary)', textTransform: 'uppercase' }}>Conversion</span>
                     <span style={{ fontSize: '16px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{advice.estimates.conversion_rate}</span>
                   </div>

                </div>
              </div>
            )}

          </div>

        </div>
      )}

    </div>
  );
}
