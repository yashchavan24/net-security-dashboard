import React, { useState } from 'react';
import axios from 'axios';

const API = 'https://net-security-dashboard.onrender.com';

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError]       = useState('');
  const [loading, setLoading]   = useState(false);

  const handleLogin = async () => {
    if (!username || !password) { setError('Please enter both fields.'); return; }
    setLoading(true);
    try {
      const res = await axios.post(API + '/api/login', { username, password });
      if (res.data.success) {
        localStorage.setItem('token', res.data.token);
        onLogin();
      }
    } catch {
      setError('Invalid username or password.');
    }
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: '100vh', background: '#0f1117',
      display: 'flex', alignItems: 'center', justifyContent: 'center'
    }}>
      <div style={{
        background: '#1a1d27', border: '0.5px solid #2a2d3a',
        borderRadius: 14, padding: '2.5rem 2rem', width: 360
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: '2rem' }}>
          <div style={{ width: 10, height: 10, borderRadius: '50%', background: '#1d9e75' }}></div>
          <h1 style={{ color: '#e2e2e2', fontSize: 18, fontWeight: 500 }}>Network Security Dashboard</h1>
        </div>

        <p style={{ color: '#888', fontSize: 12, marginBottom: '1.5rem' }}>Sign in to access the dashboard</p>

        <div style={{ marginBottom: 12 }}>
          <label style={{ color: '#888', fontSize: 11, display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Username</label>
          <input
            style={{ width: '100%', background: '#0f1117', border: '0.5px solid #2a2d3a', borderRadius: 8, padding: '8px 12px', color: '#e2e2e2', fontSize: 14 }}
            value={username}
            onChange={e => setUsername(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="admin"
          />
        </div>

        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ color: '#888', fontSize: 11, display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Password</label>
          <input
            type="password"
            style={{ width: '100%', background: '#0f1117', border: '0.5px solid #2a2d3a', borderRadius: 8, padding: '8px 12px', color: '#e2e2e2', fontSize: 14 }}
            value={password}
            onChange={e => setPassword(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="••••••••"
          />
        </div>

        {error && <div style={{ color: '#e24b4a', fontSize: 13, marginBottom: 12 }}>{error}</div>}

        <button
          onClick={handleLogin}
          disabled={loading}
          style={{
            width: '100%', padding: '10px', background: '#378add22',
            border: '0.5px solid #378add', color: '#378add',
            borderRadius: 8, fontSize: 14, cursor: 'pointer', fontWeight: 500
          }}
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>

        <div style={{ marginTop: '1.5rem', padding: '12px', background: '#0f1117', borderRadius: 8, fontSize: 12, color: '#555' }}>
          Demo credentials:<br/>
          <span style={{ color: '#888' }}>admin / cyber123</span><br/>
          <span style={{ color: '#888' }}>yash / secure456</span>
        </div>
      </div>
    </div>
  );
}
