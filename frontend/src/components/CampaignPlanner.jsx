import React, { useState } from 'react';
import { Target, Users, Calendar, Coins, TrendingUp, Activity, Share2, PlayCircle, Clock, Smartphone, MessageCircle } from 'lucide-react';

export default function CampaignPlanner({ products }) {
  const [productName, setProductName] = useState(products?.[0]?.product_name || 'Ultra Hydrating Water Cream');
  const [productType, setProductType] = useState('Moisturizers');
  const [audience, setAudience] = useState('Millennials');
  const [budget, setBudget] = useState(100000);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = () => {
    setLoading(true);

    fetch('http://${import.meta.env.VITE_API_URL}/api/campaign/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_name: productName,
        product_type: productType,
        target_audience: audience,
        budget: Number(budget)
      })
    })
      .then(res => res.json())
      .then(data => {
        setPlan(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error generating campaign:", err);
        setLoading(false);
      });
  };

  const getPlatformIcon = (platform) => {
    if (platform === 'Instagram') return <img src="https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg" width={16} height={16} style={{ filter: 'grayscale(1) brightness(1.5)' }} alt="IG"/>;
    if (platform === 'TikTok') return <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M19.589 6.686a4.793 4.793 0 01-3.975-4.685.035.035 0 00-.035-.034h-3.32a.035.035 0 00-.035.035v11.365a3.834 3.834 0 01-3.832 3.832 3.834 3.834 0 01-3.832-3.832 3.834 3.834 0 013.832-3.832c.16 0 .317.01.472.03v-3.41a7.228 7.228 0 00-.472-.016 7.234 7.234 0 00-7.232 7.232 7.234 7.234 0 007.232 7.232 7.234 7.234 0 007.233-7.232V7.91a8.163 8.163 0 004.168 1.144.035.035 0 00.035-.035V5.679a.035.035 0 00-.035-.035 4.815 4.815 0 01-1.204-.158z"/></svg>;
    if (platform === 'YouTube Shorts') return <PlayCircle size={16} />;
    return <Share2 size={16} />;
  };

  const getPlatformColor = (platform) => {
    if (platform === 'Instagram') return '#E1306C';
    if (platform === 'TikTok') return '#25F4EE';
    if (platform === 'YouTube Shorts') return '#FF0000';
    return '#888';
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>Campaign Planner</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
            Simulate influencer campaigns, optimize budget allocation, and estimate logistics.
          </p>
        </div>
      </div>

      {/* Input Parameters */}
      <div className="glass-panel" style={{ padding: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
          <Coins size={18} style={{ color: 'var(--accent-gold)' }} />
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: '600' }}>Campaign Parameters</h3>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', alignItems: 'end' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Target Product</label>
            <select value={productName} onChange={(e) => setProductName(e.target.value)} style={{ padding: '10px' }}>
              {products.map((p) => (
                <option key={p.product_id} value={p.product_name}>{p.product_name}</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Product Category</label>
            <select value={productType} onChange={(e) => setProductType(e.target.value)} style={{ padding: '10px' }}>
              <option value="Moisturizers">Moisturizers</option>
              <option value="Treatments">Treatments (Serums, Acids)</option>
              <option value="Cleansers">Cleansers</option>
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Target Audience</label>
            <select value={audience} onChange={(e) => setAudience(e.target.value)} style={{ padding: '10px' }}>
              <option value="Gen Z">Gen Z (18-24)</option>
              <option value="Millennials">Millennials (25-40)</option>
              <option value="Gen X / Boomers">Gen X / Boomers (40+)</option>
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Total Budget (₹)</label>
            <input 
              type="number" 
              value={budget} 
              onChange={(e) => setBudget(e.target.value)} 
              min="5000"
              step="5000"
              style={{ padding: '10px', fontSize: '14px' }}
            />
          </div>

          <button 
            className="btn-primary" 
            onClick={handleGenerate} 
            disabled={loading}
            style={{ padding: '12px', height: '42px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}
          >
            {loading ? (
              <div style={{ width: '16px', height: '16px', border: '2px solid rgba(255,255,255,0.3)', borderTopColor: '#fff', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
            ) : (
              <><Target size={16} /> Simulate</>
            )}
          </button>
        </div>
      </div>

      {plan && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', animation: 'fadeIn 0.4s ease' }}>
          
          {/* Top KPI Row */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
            <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', borderTop: '3px solid var(--accent-rose)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                 <Users size={14} /> Expected Reach
              </div>
              <span style={{ fontSize: '28px', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                {(plan.projections?.expected_reach || 0).toLocaleString()}
              </span>
              <span style={{ fontSize: '12px', color: 'var(--accent-mint)' }}>Unique Impressions</span>
            </div>

            <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', borderTop: '3px solid var(--accent-mint)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                 <Activity size={14} /> Engagements
              </div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
                <span style={{ fontSize: '28px', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                  {(plan.projections?.expected_engagement || 0).toLocaleString()}
                </span>
                <span className="badge badge-success" style={{ fontSize: '11px' }}>
                  {plan.projections?.avg_engagement_rate_percent}% ER
                </span>
              </div>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Likes, Comments, Shares</span>
            </div>

            <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', borderTop: '3px solid var(--accent-gold)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                 <TrendingUp size={14} /> Efficiency (CPM/CPE)
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '4px' }}>
                 <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span style={{ fontSize: '20px', fontWeight: 'bold', color: 'var(--text-primary)' }}>₹{plan.projections?.estimated_cpm}</span>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Cost Per 1k Views</span>
                 </div>
                 <div style={{ width: '1px', height: '30px', background: 'rgba(255,255,255,0.1)' }} />
                 <div style={{ display: 'flex', flexDirection: 'column' }}>
                    <span style={{ fontSize: '20px', fontWeight: 'bold', color: 'var(--text-primary)' }}>₹{plan.projections?.estimated_cpe}</span>
                    <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>Cost Per Engagement</span>
                 </div>
              </div>
            </div>

            <div className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', borderTop: '3px solid var(--border-color)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)', fontSize: '13px' }}>
                 <Coins size={14} /> Campaign Spend
              </div>
              <span style={{ fontSize: '28px', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                ₹{(plan.financial_summary?.total_spent || 0).toLocaleString()}
              </span>
              <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                Remaining Buffer: ₹{(plan.financial_summary?.remaining_buffer || 0).toLocaleString()}
              </span>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
            
            {/* Influencer Mix */}
            <div className="glass-panel">
              <div className="glass-card-header">
                <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Users size={18} style={{ color: 'var(--accent-mint)' }} />
                  Creator Roster Mix
                </h3>
              </div>
              <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {Object.entries(plan.influencer_mix || {}).map(([tier, data]) => {
                  if (data.count === 0) return null;
                  return (
                    <div key={tier} style={{ 
                      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                      padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)'
                    }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                           <span style={{ fontWeight: '600', textTransform: 'capitalize', color: 'var(--text-primary)', fontSize: '15px' }}>
                             {tier} Influencers
                           </span>
                           <span className="badge" style={{ fontSize: '10px', background: 'rgba(255,255,255,0.1)' }}>{data.count}x</span>
                        </div>
                        <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Avg Following: {data.followers_range}</span>
                        <span style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>{data.description}</span>
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '4px' }}>
                        <span style={{ fontWeight: 'bold', fontSize: '16px', color: 'var(--accent-mint)' }}>₹{(data.total_cost).toLocaleString()}</span>
                        <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>₹{data.pay_each.toLocaleString()} each</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
               {/* Logistics & Platform Split */}
               <div className="glass-panel">
                 <div className="glass-card-header">
                   <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                     <Share2 size={18} style={{ color: 'var(--accent-gold)' }} />
                     Platform Distribution
                   </h3>
                 </div>
                 <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                   
                   <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                     {Object.entries(plan.logistics?.platform_split || {}).map(([platform, percent]) => (
                        <div key={platform} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                           <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                             <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                                {getPlatformIcon(platform)}
                                <span style={{ fontSize: '14px', fontWeight: '500' }}>{platform}</span>
                             </div>
                             <span style={{ fontSize: '14px', fontWeight: 'bold' }}>{percent}%</span>
                           </div>
                           <div style={{ width: '100%', height: '6px', background: 'rgba(255,255,255,0.05)', borderRadius: '3px' }}>
                             <div style={{ width: `${percent}%`, height: '100%', background: getPlatformColor(platform), borderRadius: '3px' }} />
                           </div>
                        </div>
                     ))}
                   </div>
                   
                   <div style={{ display: 'flex', gap: '16px', paddingTop: '16px', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '4px' }}>
                         <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                           <Clock size={12} /> Duration
                         </span>
                         <span style={{ fontSize: '14px', fontWeight: '500', color: 'var(--text-primary)' }}>{plan.logistics?.campaign_duration}</span>
                      </div>
                      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '4px' }}>
                         <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                           <Calendar size={12} /> Best Times
                         </span>
                         <span style={{ fontSize: '13px', fontWeight: '500', color: 'var(--text-primary)' }}>
                           {plan.logistics?.best_posting_times?.join(', ')}
                         </span>
                      </div>
                   </div>

                 </div>
               </div>
               
               {/* Strategy & Content Angle */}
               <div className="glass-panel">
                 <div className="glass-card-header">
                   <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                     <Target size={18} style={{ color: 'var(--accent-rose)' }} />
                     Creative Strategy
                   </h3>
                 </div>
                 <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                       <span style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Strategic Focus</span>
                       <p style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: '1.5', background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px' }}>
                         {plan.strategy?.focus}
                       </p>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                       <span style={{ fontSize: '12px', fontWeight: '600', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Content Angle</span>
                       <p style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: '1.5', background: 'rgba(255,255,255,0.03)', padding: '12px', borderRadius: '8px' }}>
                         {plan.strategy?.content_angle}
                       </p>
                    </div>
                 </div>
               </div>

            </div>
          </div>
        </div>
      )}
    </div>
  );
}