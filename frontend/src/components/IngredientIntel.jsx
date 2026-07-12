import React, { useState, useEffect } from 'react';
import { Star, ShieldAlert, Sparkles, CheckCircle2, AlertTriangle, XCircle, Heart } from 'lucide-react';

export default function IngredientIntel() {
  const [ingredients, setIngredients] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Pairing states
  const [ing1, setIng1] = useState('niacinamide');
  const [ing2, setIng2] = useState('zinc pca');
  const [compatibility, setCompatibility] = useState(null);
  const [compLoading, setCompLoading] = useState(false);

  // Fetch ingredient analytics
  useEffect(() => {
    fetch('http://${import.meta.env.VITE_API_URL}/api/ingredients')
      .then(res => res.json())
      .then(data => {
        setIngredients(data);
        setLoading(false);
      })
      .catch(err => console.error("Error fetching ingredients:", err));
  }, []);

  // Check pairing compatibility
  useEffect(() => {
    if (!ing1 || !ing2) return;
    setCompLoading(true);
    fetch(`http://${import.meta.env.VITE_API_URL}/api/ingredients/compatibility?ing1=${ing1}&ing2=${ing2}`)
      .then(res => res.json())
      .then(data => {
        setCompatibility(data);
        setCompLoading(false);
      })
      .catch(err => {
        console.error("Error checking compatibility:", err);
        setCompLoading(false);
      });
  }, [ing1, ing2]);

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'Synergistic': return 'badge-success';
      case 'Compatible': return 'badge-info';
      case 'Precaution': return 'badge-warning';
      case 'Incompatible': return 'badge-danger';
      default: return 'badge-info';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Synergistic': return <Sparkles size={16} style={{ color: 'var(--accent-mint)' }} />;
      case 'Compatible': return <CheckCircle2 size={16} style={{ color: 'var(--accent-gold)' }} />;
      case 'Precaution': return <AlertTriangle size={16} style={{ color: 'var(--accent-peach)' }} />;
      case 'Incompatible': return <XCircle size={16} style={{ color: 'var(--accent-coral)' }} />;
      default: return null;
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div className="skeleton" style={{ height: '40px', width: '200px' }} />
        <div className="skeleton" style={{ height: '400px', width: '100%' }} />
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      
      {/* Title */}
      <div>
        <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>Ingredient Intelligence</h1>
        <p style={{ color: 'var(--text-secondary)', marginTop: '4px' }}>
          Evaluate active ingredients by consumer success ratings, formulation counts, and check combination risk alerts.
        </p>
      </div>

      {/* Main Grid: Left is Table, Right is Compatibility checker */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr', lgGridTemplateColumns: '3fr 2fr', gap: '24px' }}>
        
        {/* Ingredient Performance Table */}
        <div className="glass-panel" style={{ overflow: 'hidden' }}>
          <div className="glass-card-header">
            <h3>Top Performing Ingredients</h3>
            <span className="badge badge-info">Weighted Scores</span>
          </div>
          <div className="glass-card-body" style={{ overflowX: 'auto', padding: 0 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', minWidth: '600px' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-secondary)', fontSize: '12px', textTransform: 'uppercase' }}>
                  <th style={{ padding: '16px 24px' }}>Ingredient</th>
                  <th style={{ padding: '16px 24px' }}>Category</th>
                  <th style={{ padding: '16px 24px' }}>Products</th>
                  <th style={{ padding: '16px 24px' }}>Avg Rating</th>
                  <th style={{ padding: '16px 24px', textAlign: 'center' }}>Popularity</th>
                  <th style={{ padding: '16px 24px', textAlign: 'center' }}>Success Score</th>
                </tr>
              </thead>
              <tbody>
                {ingredients.map((ing) => (
                  <tr key={ing.key} style={{ borderBottom: '1px solid rgba(224, 168, 153, 0.05)', fontSize: '14px', transition: 'background 0.2s' }} className="table-row-hover">
                    <td style={{ padding: '16px 24px' }}>
                      <div style={{ display: 'flex', flexDirection: 'column' }}>
                        <span style={{ fontWeight: '600', color: 'var(--text-primary)' }}>{ing.name}</span>
                        <span style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px', maxWidth: '280px', textOverflow: 'ellipsis', overflow: 'hidden', whiteSpace: 'nowrap' }} title={ing.description}>
                          {ing.description}
                        </span>
                      </div>
                    </td>
                    <td style={{ padding: '16px 24px', color: 'var(--text-secondary)' }}>{ing.category}</td>
                    <td style={{ padding: '16px 24px', color: 'var(--text-secondary)' }}>{ing.product_count}</td>
                    <td style={{ padding: '16px 24px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--accent-gold)' }}>
                        <Star size={14} fill="var(--accent-gold)" />
                        <span>{ing.avg_rating}</span>
                      </div>
                    </td>
                    <td style={{ padding: '16px 24px', textAlign: 'center' }}>
                      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <span style={{ fontWeight: '500' }}>{ing.popularity_score}</span>
                        <div style={{ width: '50px', height: '4px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '2px', marginTop: '4px' }}>
                          <div style={{ width: `${ing.popularity_score}%`, height: '100%', backgroundColor: 'var(--accent-peach)', borderRadius: '2px' }} />
                        </div>
                      </div>
                    </td>
                    <td style={{ padding: '16px 24px', textAlign: 'center' }}>
                      <span style={{ 
                        padding: '4px 8px', 
                        borderRadius: '6px', 
                        backgroundColor: 'rgba(212, 154, 137, 0.08)',
                        border: '1px solid rgba(212, 154, 137, 0.2)',
                        color: 'var(--accent-rose)', 
                        fontWeight: 'bold',
                        fontFamily: 'var(--font-display)' 
                      }}>
                        {ing.success_score}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Compatibility Checker */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          <div className="glass-panel">
            <div className="glass-card-header">
              <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <ShieldAlert size={18} style={{ color: 'var(--accent-rose)' }} />
                Combination Checker
              </h3>
              <span className="badge badge-info">Dermatological Guidance</span>
            </div>
            <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              
              {/* Selectors */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>First Active Ingredient:</label>
                <select value={ing1} onChange={(e) => setIng1(e.target.value)}>
                  {ingredients.map(i => (
                    <option key={i.key} value={i.key}>{i.name}</option>
                  ))}
                </select>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <label style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Second Active Ingredient:</label>
                <select value={ing2} onChange={(e) => setIng2(e.target.value)}>
                  {ingredients.map(i => (
                    <option key={i.key} value={i.key} disabled={i.key === ing1}>{i.name}</option>
                  ))}
                </select>
              </div>

              {/* Compatibility Result */}
              {compLoading ? (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px' }}>
                  <div className="skeleton" style={{ height: '30px', width: '120px' }} />
                  <div className="skeleton" style={{ height: '80px', width: '100%' }} />
                </div>
              ) : compatibility ? (
                <div style={{ 
                  marginTop: '16px', 
                  padding: '20px', 
                  borderRadius: '12px', 
                  background: 'rgba(255,255,255,0.01)',
                  border: '1px solid rgba(255,255,255,0.03)',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '16px'
                }}>
                  
                  {/* Status & Index Row */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {getStatusIcon(compatibility.status)}
                      <span className={`badge ${getStatusBadgeClass(compatibility.status)}`} style={{ fontSize: '12px' }}>
                        {compatibility.status}
                      </span>
                    </div>
                    
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                      <span style={{ fontSize: '20px', fontWeight: 'bold', color: 'var(--text-primary)', fontFamily: 'var(--font-display)' }}>
                        {compatibility.compatibility_index}%
                      </span>
                      <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Compatibility index</span>
                    </div>
                  </div>

                  {/* Compatibility Progress bar */}
                  <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '3px' }}>
                    <div style={{ 
                      width: `${compatibility.compatibility_index}%`, 
                      height: '100%', 
                      backgroundColor: compatibility.status === 'Incompatible' ? 'var(--accent-coral)' : 
                                      compatibility.status === 'Precaution' ? 'var(--accent-peach)' : 
                                      compatibility.status === 'Compatible' ? 'var(--accent-gold)' : 'var(--accent-mint)', 
                      borderRadius: '3px' 
                    }} />
                  </div>

                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', lineHeight: '1.6' }}>
                    {compatibility.description}
                  </p>
                </div>
              ) : null}

            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
}
