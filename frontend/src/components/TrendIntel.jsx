import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, Users, FileText, AlertCircle, Heart, Star, Flame, MessageCircle } from 'lucide-react';

export default function TrendIntel() {
  const [trends, setTrends] = useState([]);
  const [redditTopics, setRedditTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch('http://${import.meta.env.VITE_API_URL}/api/trends').then(res => res.json()),
      fetch('http://${import.meta.env.VITE_API_URL}/api/trends/reddit-topics').then(res => res.json())
    ])
      .then(([trendsData, redditData]) => {
        setTrends(trendsData);
        setRedditTopics(redditData);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching trends:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div className="skeleton" style={{ height: '40px', width: '200px' }} />
        <div className="skeleton" style={{ height: '350px', width: '100%' }} />
      </div>
    );
  }

  const risingTrends = trends.filter(t => t.momentum >= 0).sort((a, b) => b.momentum - a.momentum);
  const decliningTrends = trends.filter(t => t.momentum < 0).sort((a, b) => a.momentum - b.momentum);

  const renderTrendCard = (t, isDeclining) => {
    const isPositive = t.momentum >= 0;
    const accentColor = isPositive ? 'var(--accent-mint)' : 'var(--accent-coral)';
    const bgGradient = isPositive ? 'rgba(126,188,137,0.08)' : 'rgba(223,108,99,0.08)';
    const borderColor = isPositive ? 'rgba(126,188,137,0.15)' : 'rgba(223,108,99,0.3)';

    return (
      <div className="glass-panel" key={t.key} style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden', borderTop: `3px solid ${accentColor}` }}>
        <div className="glass-card-header" style={{ paddingBottom: '12px' }}>
          <div>
            <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{t.category}</span>
            <h3 style={{ fontSize: '18px', marginTop: '2px', color: isDeclining ? 'var(--accent-coral)' : 'var(--text-primary)' }}>{t.name}</h3>
          </div>
          
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '4px',
            color: accentColor,
            fontWeight: 'bold',
            fontSize: '16px',
            fontFamily: 'var(--font-display)',
            backgroundColor: bgGradient,
            padding: '6px 12px',
            borderRadius: '8px',
            border: `1px solid ${borderColor}`
          }}>
            {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
            <span>{isPositive ? '+' : ''}{t.momentum}%</span>
          </div>
        </div>
        
        <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px', flexGrow: 1 }}>
          {/* Google Trends Mini Area Chart */}
          <div style={{ width: '100%', height: '100px', marginTop: '4px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={t.history} margin={{ top: 5, bottom: 5, left: -20, right: 0 }}>
                <defs>
                  <linearGradient id={`colorGrad-${t.key}`} x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={accentColor} stopOpacity={0.2}/>
                    <stop offset="95%" stopColor={accentColor} stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="month" stroke="var(--text-muted)" fontSize={9} tickLine={false} />
                <YAxis stroke="var(--text-muted)" fontSize={9} tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip contentStyle={{ background: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '4px', color: '#fff' }} />
                <Area 
                  type="monotone" 
                  dataKey="interest" 
                  stroke={accentColor} 
                  strokeWidth={2}
                  fillOpacity={1} 
                  fill={`url(#colorGrad-${t.key})`} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          
          {/* Social Stats Row */}
          <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '16px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Users size={16} style={{ color: 'var(--accent-rose)' }} />
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{t.reddit_mentions.toLocaleString()}</span>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Reddit posts (+{t.reddit_growth}%)</span>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <FileText size={16} style={{ color: 'var(--accent-gold)' }} />
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <span style={{ fontSize: '12px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{t.news_mentions.toLocaleString()}</span>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>News articles</span>
              </div>
            </div>
          </div>

          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', lineHeight: '1.6', background: 'rgba(0,0,0,0.1)', padding: '10px', borderRadius: '8px', borderLeft: `2px solid ${accentColor}` }}>
            {t.summary}
          </p>
        </div>
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
      
      {/* Title */}
      <div>
        <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>Trend Intelligence</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
          Monitor search index momentum, rising skincare community topics, and clinical ingredient trends.
        </p>
      </div>

      {/* Grid of Trending Ingredients */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <h2 style={{ fontSize: '20px', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
           <TrendingUp size={20} style={{ color: 'var(--accent-mint)' }} />
           Top Rising Ingredients
        </h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
          {risingTrends.map(t => renderTrendCard(t, false))}
        </div>
      </div>

      {/* Grid of Declining Ingredients */}
      {decliningTrends.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <h2 style={{ fontSize: '20px', color: 'var(--accent-coral)', display: 'flex', alignItems: 'center', gap: '8px' }}>
             <TrendingDown size={20} />
             Declining Market Interest
          </h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
            {decliningTrends.map(t => renderTrendCard(t, true))}
          </div>
        </div>
      )}

      {/* Reddit Discussion Clusters */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', paddingBottom: '32px' }}>
        <h2 style={{ fontSize: '20px', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Users size={20} style={{ color: 'var(--accent-rose)' }} />
          Reddit Skincare Community Hotspots
        </h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
          {redditTopics.map((topic, index) => {
            const isNegative = topic.sentiment_score < 0;
            const urgencyColor = topic.urgency_score > 85 ? 'var(--accent-coral)' : (topic.urgency_score > 70 ? 'var(--accent-gold)' : 'var(--accent-mint)');
            
            return (
              <div className="glass-panel" key={index} style={{ borderLeft: `3px solid ${urgencyColor}` }}>
                <div className="glass-card-header" style={{ paddingBottom: '16px' }}>
                  <div>
                    <h3 style={{ fontSize: '16px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                       {topic.topic}
                    </h3>
                    <span style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
                       <MessageCircle size={12} /> {topic.posts_count} active discussion threads
                    </span>
                  </div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '6px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(0,0,0,0.2)', padding: '4px 8px', borderRadius: '12px' }}>
                       <Flame size={14} style={{ color: urgencyColor }} />
                       <span style={{ fontSize: '11px', color: 'var(--text-secondary)', fontWeight: '600' }}>Urgency: {topic.urgency_score}/100</span>
                    </div>
                    <span className={`badge ${isNegative ? 'badge-danger' : 'badge-success'}`}>
                      {isNegative ? 'Negative Sent' : 'Positive Sent'}
                    </span>
                  </div>
                </div>
                
                <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.5' }}>
                    {topic.description}
                  </p>
                  
                  {/* Tag Cloud */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '4px' }}>
                    {topic.top_words.map((word, wIdx) => (
                      <span key={wIdx} style={{ 
                        fontSize: '11px', 
                        padding: '4px 10px', 
                        borderRadius: '12px',
                        background: 'rgba(255,255,255,0.03)',
                        border: '1px solid rgba(255,255,255,0.05)',
                        color: 'var(--text-secondary)',
                        fontWeight: '500'
                      }}>
                        #{word}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
