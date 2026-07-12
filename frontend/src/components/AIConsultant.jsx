import React, { useState } from 'react';
import { Sparkles, MessageSquare, Send, Bot, RefreshCw, Copy, Download, CheckCircle2 } from 'lucide-react';

const SUGGESTIONS = [
  {
    label: "Niacinamide Underperforming?",
    query: "Why is my niacinamide serum underperforming? Analyze reviews, trends, and competitor ingredient performance."
  },
  {
    label: "Retinol Strategy Adjustment?",
    query: "How should we adjust our Retinol marketing and formulation strategy given negative skin irritation feedback?"
  },
  {
    label: "Next Trending Ingredient?",
    query: "Which ingredients are worth formulating next based on Google Trends momentum and Reddit skin barrier topics?"
  }
];

export default function AIConsultant() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleConsult = (targetQuery) => {
    const activeQuery = targetQuery || query;
    if (!activeQuery.trim()) return;

    setLoading(true);
    setResponse('');
    setCopied(false);
    
    fetch('http://${import.meta.env.VITE_API_URL}/api/consult', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: activeQuery })
    })
      .then(res => res.json())
      .then(data => {
        setResponse(data.response);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error during consultation:", err);
        setResponse("### Error\n⚠️ Connection error: Make sure the FastAPI backend is running on http://${import.meta.env.VITE_API_URL}.");
        setLoading(false);
      });
  };

  const handleCopy = () => {
    if (!response) return;
    navigator.clipboard.writeText(response);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExport = () => {
    if (!response) return;
    const blob = new Blob([response], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `marketmind-ai-report-${new Date().toISOString().split('T')[0]}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Advanced Markdown-like formatter to render structured HTML
  const formatReportText = (text) => {
    if (!text) return null;

    const lines = text.split('\n');
    let inList = false;
    let listItems = [];
    const elements = [];

    const flushList = () => {
      if (inList && listItems.length > 0) {
        elements.push(
          <ul key={`ul-${elements.length}`} style={{ paddingLeft: '20px', marginBottom: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {listItems}
          </ul>
        );
        listItems = [];
        inList = false;
      }
    };

    lines.forEach((line, idx) => {
      const trimmed = line.trim();
      
      if (trimmed.startsWith('### ')) {
        flushList();
        let color = 'var(--text-primary)';
        const headingText = trimmed.replace('### ', '');
        
        if (headingText.includes('Executive Summary')) color = 'var(--accent-mint)';
        else if (headingText.includes('Key Findings')) color = 'var(--accent-gold)';
        else if (headingText.includes('Recommendations')) color = 'var(--accent-rose)';
        else if (headingText.includes('Expected Impact')) color = 'var(--accent-coral)';
        else if (headingText.includes('Confidence Score')) color = '#a388ee';

        elements.push(
          <h3 key={idx} style={{ 
            fontSize: '18px', 
            color: color, 
            marginTop: idx === 0 ? '0' : '28px', 
            marginBottom: '14px',
            fontFamily: 'var(--font-display)',
            borderBottom: `1px solid ${color}33`,
            paddingBottom: '8px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            {headingText}
          </h3>
        );
        return;
      }
      
      if (trimmed.startsWith('#### ')) {
        flushList();
        elements.push(
          <h4 key={idx} style={{ 
            fontSize: '15px', 
            color: 'var(--text-primary)', 
            marginTop: '20px', 
            marginBottom: '10px',
            fontFamily: 'var(--font-display)',
            fontWeight: '600'
          }}>
            {trimmed.replace('#### ', '')}
          </h4>
        );
        return;
      }

      if (trimmed.startsWith('* ') || trimmed.startsWith('- ') || /^\d+\.\s/.test(trimmed)) {
        inList = true;
        const isNumbered = /^\d+\.\s/.test(trimmed);
        const itemText = isNumbered ? trimmed.replace(/^\d+\.\s/, '') : trimmed.substring(2);
        
        listItems.push(
          <li key={idx} style={{ 
            fontSize: '14px', 
            color: 'var(--text-secondary)',
            lineHeight: '1.6',
            listStyleType: isNumbered ? 'decimal' : 'disc'
          }}>
            {parseInlineStyling(itemText)}
          </li>
        );
        return;
      }

      if (trimmed.length > 0) {
        flushList();
        elements.push(
          <p key={idx} style={{ 
            fontSize: '14px', 
            color: 'var(--text-secondary)', 
            lineHeight: '1.7', 
            marginBottom: '16px' 
          }}>
            {parseInlineStyling(trimmed)}
          </p>
        );
        return;
      }
    });

    flushList();
    return elements;
  };

  const parseInlineStyling = (text) => {
    // Bold
    let parts = text.split(/\*\*([^*]+)\*\*/g);
    let result = parts.map((part, index) => {
      if (index % 2 === 1) {
        return <strong key={`b-${index}`} style={{ color: 'var(--text-primary)', fontWeight: '600' }}>{part}</strong>;
      }
      return part;
    });

    // Italics (simplified)
    const newResult = [];
    result.forEach((part, i) => {
      if (typeof part === 'string') {
        let subParts = part.split(/\*([^*]+)\*/g);
        subParts.forEach((subPart, j) => {
          if (j % 2 === 1) {
             newResult.push(<em key={`i-${i}-${j}`} style={{ fontStyle: 'italic', color: 'var(--text-primary)' }}>{subPart}</em>);
          } else {
             newResult.push(subPart);
          }
        });
      } else {
        newResult.push(part);
      }
    });

    return newResult;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px', height: '100%' }}>
      
      {/* Title */}
      <div>
        <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>AI Marketing Consultant</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
          Consult the LLM reasoning layer to diagnose campaign performance, address review anomalies, and plan next actions.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px', flexGrow: 1 }}>
        
        {/* Left Side: Consultation Input */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', height: 'fit-content' }}>
          <div className="glass-card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Bot size={18} style={{ color: 'var(--accent-rose)' }} />
              Consultation Console
            </h3>
            <span className="badge badge-success" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Sparkles size={11} /> Ready
            </span>
          </div>
          
          <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            
            {/* Quick Suggestions Cards */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <span style={{ fontSize: '13px', color: 'var(--text-secondary)', fontWeight: '500' }}>Diagnostic Presets:</span>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {SUGGESTIONS.map((s, idx) => (
                  <div 
                    key={idx} 
                    onClick={() => {
                      setQuery(s.query);
                      handleConsult(s.query);
                    }}
                    style={{ 
                      padding: '14px 16px', 
                      borderRadius: '10px', 
                      background: 'rgba(255,255,255,0.02)', 
                      border: '1px solid rgba(255,255,255,0.05)', 
                      cursor: 'pointer',
                      fontSize: '13px',
                      color: 'var(--text-secondary)',
                      transition: 'all 0.2s',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px'
                    }}
                    onMouseEnter={(e) => {
                       e.currentTarget.style.borderColor = 'var(--accent-rose)';
                       e.currentTarget.style.background = 'rgba(224, 168, 153, 0.05)';
                    }}
                    onMouseLeave={(e) => {
                       e.currentTarget.style.borderColor = 'rgba(255,255,255,0.05)';
                       e.currentTarget.style.background = 'rgba(255,255,255,0.02)';
                    }}
                  >
                    <MessageSquare size={16} style={{ color: 'var(--accent-gold)', flexShrink: 0 }} />
                    <span style={{ fontWeight: '500', color: 'var(--text-primary)', lineHeight: '1.4' }}>{s.label}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Custom Input */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <label style={{ fontSize: '13px', color: 'var(--text-secondary)', fontWeight: '500' }}>Type Custom Question:</label>
              <textarea 
                value={query} 
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about underperforming serums, emerging ingredient trends, skin barrier marketing..."
                style={{ 
                  width: '100%', 
                  minHeight: '140px', 
                  resize: 'none',
                  background: 'rgba(0,0,0,0.2)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '10px',
                  padding: '16px',
                  color: 'var(--text-primary)',
                  fontFamily: 'inherit',
                  fontSize: '14px',
                  lineHeight: '1.5'
                }}
              />
            </div>

            {/* Actions */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
              <button 
                className="btn-secondary" 
                onClick={() => {
                  setQuery('');
                  setResponse('');
                }}
                disabled={loading}
              >
                Clear
              </button>
              <button 
                className="btn-primary" 
                onClick={() => handleConsult()}
                disabled={loading || !query.trim()}
                style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 24px' }}
              >
                {loading ? 'Consulting...' : <>Generate Report <Send size={16} /></>}
              </button>
            </div>

          </div>
        </div>

        {/* Right Side: Consultation Output */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', minHeight: '500px' }}>
          <div className="glass-card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>Strategic Report</h3>
            
            {response && !loading && (
              <div style={{ display: 'flex', gap: '8px' }}>
                 <button 
                   onClick={handleCopy}
                   title="Copy to Clipboard"
                   style={{ background: 'transparent', border: 'none', color: copied ? 'var(--accent-mint)' : 'var(--text-secondary)', cursor: 'pointer', padding: '6px', borderRadius: '4px', transition: 'all 0.2s', display: 'flex', alignItems: 'center', gap: '4px' }}
                 >
                   {copied ? <CheckCircle2 size={16} /> : <Copy size={16} />}
                 </button>
                 <button 
                   onClick={handleExport}
                   title="Export as Markdown"
                   style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: '6px', borderRadius: '4px', transition: 'all 0.2s' }}
                 >
                   <Download size={16} />
                 </button>
                 <button 
                   onClick={() => handleConsult()}
                   title="Regenerate"
                   style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: '6px', borderRadius: '4px', transition: 'all 0.2s' }}
                 >
                   <RefreshCw size={16} />
                 </button>
              </div>
            )}
          </div>
          
          <div className="glass-card-body" style={{ flexGrow: 1, overflowY: 'auto', padding: '32px' }}>
            {loading ? (
              <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '24px', color: 'var(--text-secondary)' }}>
                <div style={{ position: 'relative', width: '60px', height: '60px' }}>
                  <div style={{ 
                    position: 'absolute', inset: 0,
                    borderRadius: '50%', 
                    border: '3px solid rgba(212, 154, 137, 0.1)', 
                    borderTopColor: 'var(--accent-rose)',
                    animation: 'spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite'
                  }} />
                  <div style={{ 
                    position: 'absolute', inset: '10px',
                    borderRadius: '50%', 
                    border: '3px solid rgba(224, 168, 153, 0.1)', 
                    borderRightColor: 'var(--accent-gold)',
                    animation: 'spin 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite reverse'
                  }} />
                </div>
                <style>{`
                  @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                  }
                `}</style>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '15px', color: 'var(--text-primary)', fontWeight: '500' }}>Synthesizing Intelligence...</span>
                  <span style={{ fontSize: '13px' }}>Cross-referencing reviews, trends, and market data</span>
                </div>
              </div>
            ) : response ? (
              <div style={{ animation: 'fadeIn 0.4s ease-out' }}>
                <style>{`
                  @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                  }
                `}</style>
                <div style={{
                   background: 'rgba(0,0,0,0.1)',
                   borderRadius: '12px',
                   padding: '24px',
                   border: '1px solid rgba(255,255,255,0.05)'
                }}>
                   {formatReportText(response)}
                </div>
              </div>
            ) : (
              <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', textAlign: 'center', gap: '16px' }}>
                <div style={{ 
                  width: '64px', height: '64px', borderRadius: '50%', 
                  background: 'rgba(255,255,255,0.02)', display: 'flex', alignItems: 'center', justifyContent: 'center' 
                }}>
                  <Bot size={32} strokeWidth={1.5} style={{ color: 'var(--text-secondary)' }} />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <span style={{ fontSize: '15px', color: 'var(--text-primary)', fontWeight: '500' }}>Awaiting Query</span>
                  <span style={{ fontSize: '13px', maxWidth: '280px' }}>Select a preset or ask a custom question to generate a strategic report.</span>
                </div>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
