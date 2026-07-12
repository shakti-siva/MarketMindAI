import React, { useState } from 'react';
import { BrainCircuit, Sparkles, Send, RefreshCw, CheckCircle2, Target, AlertTriangle } from 'lucide-react';

const PRESETS = [
  {
    title: "Clinical & Limited",
    text: "Our dermatologist-recommended and clinically-proven Vitamin C serum is back! Made in exclusive micro-batches. Hurry, we only have 45 bottles left in this restock vault!"
  },
  {
    title: "Viral TikTok Proof",
    text: "The viral peptide serum everyone on TikTok is talking about! Over 50,000+ five-star reviews. Don't miss out on joining the waitlist for the next big thing in skincare."
  },
  {
    title: "Flash Urgency",
    text: "Flash sale ends tonight! Clock is ticking. Get 30% off our best-selling hydrating water cream. Buy now before the deal expires!"
  }
];

export default function PsychologyAnalyzer() {
  const [copyText, setCopyText] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = (textToAnalyze) => {
    const targetText = textToAnalyze || copyText;
    if (!targetText.trim()) return;

    setLoading(true);
    fetch('http://${import.meta.env.VITE_API_URL}/api/psychology/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: targetText })
    })
      .then(res => res.json())
      .then(data => {
        setAnalysis(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error analyzing copy:", err);
        setLoading(false);
      });
  };

  const getTriggerColor = (trigger) => {
    switch (trigger) {
      case 'Authority': return 'var(--accent-gold)';
      case 'Scarcity': return 'var(--accent-rose)';
      case 'Urgency': return 'var(--accent-coral)';
      case 'Social Proof': return 'var(--accent-mint)';
      case 'FOMO': return '#ad7ebc';
      default: return 'var(--text-muted)';
    }
  };

  const renderCircularScore = (score) => {
    const radius = 36;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;
    const color = score > 75 ? 'var(--accent-mint)' : (score > 40 ? 'var(--accent-gold)' : 'var(--accent-coral)');

    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px', padding: '16px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
        <div style={{ position: 'relative', width: '80px', height: '80px', flexShrink: 0 }}>
          <svg width="80" height="80" viewBox="0 0 80 80" style={{ transform: 'rotate(-90deg)' }}>
            <circle cx="40" cy="40" r={radius} fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="6" />
            <circle 
              cx="40" cy="40" r={radius} fill="none" stroke={color} strokeWidth="6"
              strokeDasharray={circumference} strokeDashoffset={strokeDashoffset}
              strokeLinecap="round" style={{ transition: 'stroke-dashoffset 1s ease' }}
            />
          </svg>
          <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
            <span style={{ fontSize: '22px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{score}</span>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
          <span style={{ fontSize: '15px', fontWeight: '600', color: 'var(--text-primary)' }}>Overall Persuasion Score</span>
          <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Based on presence and intensity of psychological triggers</span>
        </div>
      </div>
    );
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Title */}
      <div>
        <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>Consumer Psychology Analyzer</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
          Evaluate marketing copy and identify psychological triggers to optimize ad conversions and brand authority.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', lgGridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        
        {/* Left Card: Input Textarea */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="glass-card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <BrainCircuit size={18} style={{ color: 'var(--accent-rose)' }} />
              Marketing Copy Tester
            </h3>
            <span className="badge badge-info">Copy Sandbox</span>
          </div>
          
          <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '20px', flexGrow: 1 }}>
            
            {/* Presets */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Load Template:</span>
              <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                {PRESETS.map((p, idx) => (
                  <button 
                    key={idx} 
                    className="btn-secondary" 
                    style={{ padding: '6px 12px', fontSize: '12px' }}
                    onClick={() => {
                      setCopyText(p.text);
                      handleAnalyze(p.text);
                    }}
                  >
                    {p.title}
                  </button>
                ))}
              </div>
            </div>

            {/* Main Textarea */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flexGrow: 1 }}>
              <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Enter Headline or Ad Body:</label>
              <textarea 
                value={copyText} 
                onChange={(e) => setCopyText(e.target.value)}
                placeholder="E.g. Dermatologist recommended serum that sells out every hour! Click here to grab your bottle..."
                style={{ width: '100%', minHeight: '180px', flexGrow: 1, resize: 'none' }}
              />
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
              <button 
                className="btn-secondary" 
                onClick={() => setCopyText('')}
                style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                <RefreshCw size={14} /> Clear
              </button>
              <button 
                className="btn-primary" 
                onClick={() => handleAnalyze()}
                disabled={loading || !copyText.trim()}
                style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
              >
                {loading ? 'Analyzing...' : <>Analyze <Send size={14} /></>}
              </button>
            </div>

          </div>
        </div>

        {/* Right Card: Trigger analysis display */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="glass-card-header">
            <h3>Persuasion Breakdown</h3>
            {analysis && (
              <span className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Sparkles size={11} /> {analysis.dominant_trigger} Dominant
              </span>
            )}
          </div>
          
          <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '24px', flexGrow: 1, justifyContent: 'center' }}>
            {!analysis ? (
              <div style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '40px 0', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
                <BrainCircuit size={48} strokeWidth={1} style={{ color: 'var(--border-color)' }} />
                <span>Enter and analyze your copywriting to review psychological impact scores.</span>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                
                {/* Overall Score */}
                {renderCircularScore(analysis.overall_score || 0)}

                {/* Direct Recommendations */}
                {analysis.recommendations && analysis.recommendations.length > 0 && (
                  <div style={{ 
                    background: 'rgba(212,154,137,0.05)', 
                    border: '1px solid rgba(212,154,137,0.15)', 
                    padding: '16px', 
                    borderRadius: '12px',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                  }}>
                    <span style={{ fontSize: '13px', fontWeight: 'bold', color: 'var(--accent-rose)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <Target size={16} /> Copywriter Action Items
                    </span>
                    <ul style={{ margin: 0, paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                       {analysis.recommendations.map((rec, i) => (
                         <li key={i} style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{rec}</li>
                       ))}
                    </ul>
                  </div>
                )}

                {/* Visual Progress Bars */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', marginTop: '8px' }}>
                  <h4 style={{ fontSize: '14px', color: 'var(--text-primary)', margin: 0 }}>Trigger Intensity</h4>
                  {analysis.breakdown.map((item) => {
                    const color = getTriggerColor(item.trigger);
                    return (
                      <div key={item.trigger} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                          <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{item.trigger}</span>
                          <span style={{ fontWeight: 'bold', color: color }}>{item.score}%</span>
                        </div>
                        
                        <div style={{ width: '100%', height: '8px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '4px', overflow: 'hidden' }}>
                          <div style={{ 
                            width: `${item.score}%`, 
                            height: '100%', 
                            backgroundColor: color, 
                            borderRadius: '4px',
                            boxShadow: `0 0 8px ${color}80`,
                            transition: 'width 0.5s ease'
                          }} />
                        </div>
                        
                        {item.matches.length > 0 && (
                          <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>
                            Trigger words: {item.matches.map(m => `"${m}"`).join(', ')}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>

              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
