import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';
import { Smile, Frown, AlertCircle, Sparkles, Star, Calendar, User } from 'lucide-react';

const COLORS = {
  positive: '#7ebc89',
  neutral: '#cfa87b',
  negative: '#df6c63'
};

const StarRating = ({ rating }) => {
  return (
    <div style={{ display: 'flex', gap: '2px' }}>
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          size={12}
          fill={star <= rating ? "#FFD700" : "transparent"}
          color={star <= rating ? "#FFD700" : "rgba(255,255,255,0.2)"}
        />
      ))}
    </div>
  );
};

export default function CustomerVoice({ products, selectedProductId, setSelectedProductId }) {
  const [productData, setProductData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!selectedProductId) return;

    setLoading(true);

    fetch(`http://${import.meta.env.VITE_API_URL}/api/customer-voice/${selectedProductId}`)
      .then(res => {
        if (!res.ok) {
          setProductData(null);
          setLoading(false);
          return null;
        }
        return res.json();
      })
      .then(data => {
        if (data) setProductData(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching product voice:", err);
        setLoading(false);
      });
  }, [selectedProductId]);

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div className="skeleton" style={{ height: '40px', width: '200px' }} />
        <div className="skeleton" style={{ height: '100px', width: '100%' }} />
        <div style={{ display: 'flex', gap: '24px' }}>
          <div className="skeleton" style={{ height: '300px', flex: 1 }} />
          <div className="skeleton" style={{ height: '300px', flex: 1 }} />
        </div>
      </div>
    );
  }

  if (!productData || !productData.sentiment_percentages) {
    return (
      <div className="glass-panel" style={{ padding: '24px' }}>
        <h2>Customer Voice Intelligence</h2>
        <div style={{ marginTop: '16px' }}>
          <label style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Target Product:</label>
          <select
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(e.target.value)}
            style={{ minWidth: '260px', marginLeft: '12px' }}
          >
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>{p.product_name}</option>
            ))}
          </select>
        </div>
        <p style={{ marginTop: '24px', color: 'var(--text-secondary)' }}>
          No review data available for this product. Please select another product.
        </p>
      </div>
    );
  }

  const productSentimentChartData = [
    { name: 'Positive', value: productData.sentiment_percentages.positive || 0, color: COLORS.positive },
    { name: 'Neutral', value: productData.sentiment_percentages.neutral || 0, color: COLORS.neutral },
    { name: 'Negative', value: productData.sentiment_percentages.negative || 0, color: COLORS.negative }
  ];

  const complaintEntries = Object.entries(productData.complaints || {});
  const hasComplaints = complaintEntries.some(([_, data]) => data.count > 0);

  const complaintChartData = complaintEntries.map(([name, data]) => ({
    name: name.replaceAll('_', ' ').replace(/\b\w/g, c => c.toUpperCase()),
    count: data.percentage || 0
  })).filter(d => d.count > 0);

  const praiseEntries = Object.entries(productData.praises || {});
  const hasPraises = praiseEntries.some(([_, data]) => data.count > 0);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <h1 style={{ fontSize: '28px', color: 'var(--text-primary)' }}>Customer Voice Intelligence</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            Analyze reviews, extract pain points, and monitor skin reaction alerts.
          </p>
          <div style={{ marginTop: '12px', display: 'flex', alignItems: 'center', gap: '12px' }}>
             <span className="badge badge-info" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '13px', padding: '4px 10px' }}>
                <User size={14} />
                Analyzed from {productData.total_reviews?.toLocaleString()} reviews
             </span>
             {(productData.total_reviews_available > productData.total_reviews) && (
               <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                 (out of {productData.total_reviews_available?.toLocaleString()} total)
               </span>
             )}
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'flex-end' }}>
          <label style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Target Product:</label>
          <select
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(e.target.value)}
            style={{ minWidth: '220px' }}
          >
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>{p.product_name}</option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        {productSentimentChartData.map(sentiment => (
          <div key={sentiment.name} className="glass-panel" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '8px', borderTop: `3px solid ${sentiment.color}` }}>
             <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>{sentiment.name} Sentiment</span>
             <span style={{ fontSize: '28px', fontWeight: 'bold', color: sentiment.color }}>{sentiment.value}%</span>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
        <div className="glass-panel">
          <div className="glass-card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Smile size={18} style={{ color: 'var(--accent-rose)' }} />
              Sentiment Distribution
            </h3>
          </div>

          <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
            <div style={{ width: '100%', height: '220px' }}>
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={productSentimentChartData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {productSentimentChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => `${value}%`} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="glass-panel">
          <div className="glass-card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Frown size={18} style={{ color: 'var(--accent-coral)' }} />
              Skincare Complaint Trends
            </h3>
          </div>

          <div className="glass-card-body">
            {!hasComplaints || complaintChartData.length === 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)', padding: '40px 0' }}>
                <Sparkles size={32} style={{ color: 'var(--accent-mint)', marginBottom: '12px', opacity: 0.8 }} />
                <span style={{ fontSize: '16px', fontWeight: '500' }}>No complaints detected</span>
                <span style={{ fontSize: '13px', marginTop: '4px' }}>Customers are generally satisfied in these categories.</span>
              </div>
            ) : (
              <div style={{ width: '100%', height: '260px', minHeight: '260px' }}>
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={complaintChartData} layout="vertical" margin={{ left: 20, right: 20 }}>
                    <XAxis type="number" domain={[0, 100]} />
                    <YAxis dataKey="name" type="category" stroke="var(--text-secondary)" width={130} fontSize={12} tickLine={false} />
                    <Tooltip formatter={(value) => `${value}%`} />
                    <Bar dataKey="count" fill="#df6c63" radius={[0, 4, 4, 0]} barSize={20} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '24px' }}>
        <div className="glass-panel">
          <div className="glass-card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-mint)' }}>
              <Sparkles size={18} />
              What Customers Love
            </h3>
          </div>

          <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {!hasPraises && (
               <div style={{ color: 'var(--text-secondary)', fontStyle: 'italic', padding: '20px 0' }}>No specific praise trends detected in this dataset.</div>
            )}
            
            {praiseEntries.filter(([_, data]) => data.count > 0).sort((a, b) => b[1].count - a[1].count).map(([key, data]) => {
              const isTopPraise = productData.top_praise === key;
              return (
              <div key={key} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontWeight: '600', textTransform: 'capitalize', fontSize: '15px' }}>{key.replaceAll('_', ' ')}</span>
                    {isTopPraise && <span className="badge badge-success" style={{ fontSize: '10px', padding: '2px 6px' }}>Top Praise</span>}
                  </div>
                  <span style={{ color: 'var(--accent-mint)', fontSize: '14px', fontWeight: '500' }}>{data.percentage}% of reviews</span>
                </div>

                <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '3px' }}>
                  <div style={{ width: `${data.percentage}%`, height: '100%', backgroundColor: 'var(--accent-mint)', borderRadius: '3px' }} />
                </div>

                {data.samples?.length > 0 && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '4px' }}>
                    {data.samples.slice(0, 2).map((sample, idx) => (
                      <div key={idx} style={{ 
                        background: 'rgba(126, 188, 137, 0.05)', 
                        padding: '16px', 
                        borderRadius: '12px', 
                        border: '1px solid rgba(126, 188, 137, 0.1)',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                           <StarRating rating={sample.rating} />
                           {sample.date && sample.date !== 'N/A' && (
                             <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--text-muted)' }}>
                               <Calendar size={10} /> {sample.date}
                             </span>
                           )}
                        </div>
                        <span style={{ fontSize: '13px', color: 'var(--text-primary)', fontStyle: 'italic', lineHeight: '1.4' }}>
                          "{sample.text}"
                        </span>
                        <span style={{ fontSize: '11px', color: 'var(--text-muted)', textAlign: 'right' }}>
                          — {sample.author}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )})}
          </div>
        </div>

        <div className="glass-panel">
          <div className="glass-card-header">
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-coral)' }}>
              <AlertCircle size={18} />
              Pain Points & Complaints
            </h3>
          </div>

          <div className="glass-card-body" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            {!hasComplaints && (
               <div style={{ color: 'var(--text-secondary)', fontStyle: 'italic', padding: '20px 0' }}>No significant complaints detected.</div>
            )}
            
            {complaintEntries.filter(([_, data]) => data.count > 0).sort((a, b) => b[1].count - a[1].count).map(([key, data]) => {
              const isTopComplaint = productData.top_complaint === key;
              return (
              <div key={key} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontWeight: '600', textTransform: 'capitalize', fontSize: '15px' }}>{key.replaceAll('_', ' ')}</span>
                    {isTopComplaint && <span className="badge badge-danger" style={{ fontSize: '10px', padding: '2px 6px' }}>Top Complaint</span>}
                  </div>
                  <span style={{ color: data.percentage > 10 ? 'var(--accent-coral)' : 'var(--text-secondary)', fontSize: '14px', fontWeight: '500' }}>
                    {data.percentage}% {data.percentage > 10 && '⚠️'}
                  </span>
                </div>

                <div style={{ width: '100%', height: '6px', backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: '3px' }}>
                  <div style={{ width: `${data.percentage}%`, height: '100%', backgroundColor: 'var(--accent-coral)', borderRadius: '3px' }} />
                </div>

                {data.samples?.length > 0 && (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '4px' }}>
                    {data.samples.slice(0, 2).map((sample, idx) => (
                      <div key={idx} style={{ 
                        background: 'rgba(223, 108, 99, 0.05)', 
                        padding: '16px', 
                        borderRadius: '12px', 
                        border: '1px solid rgba(223, 108, 99, 0.1)',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '8px'
                      }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                           <StarRating rating={sample.rating} />
                           {sample.date && sample.date !== 'N/A' && (
                             <span style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', color: 'var(--text-muted)' }}>
                               <Calendar size={10} /> {sample.date}
                             </span>
                           )}
                        </div>
                        <span style={{ fontSize: '13px', color: 'var(--text-primary)', fontStyle: 'italic', lineHeight: '1.4' }}>
                          "{sample.text}"
                        </span>
                        <span style={{ fontSize: '11px', color: 'var(--text-muted)', textAlign: 'right' }}>
                          — {sample.author}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )})}
          </div>
        </div>
      </div>
    </div>
  );
}