files = {
"frontend/src/Login.js": """import React, { useState } from 'react';
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
""",

"frontend/src/App.js": """import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import Login from './Login';
import './App.css';

const socket = io('https://net-security-dashboard.onrender.com');
const API = 'https://net-security-dashboard.onrender.com';

export default function App() {
  const [loggedIn, setLoggedIn]       = useState(!!localStorage.getItem('token'));
  const [traffic, setTraffic]         = useState([]);
  const [stats, setStats]             = useState({ packets: 0, bandwidth: 0, threats: 0 });
  const [logs, setLogs]               = useState([]);
  const [scanIP, setScanIP]           = useState('');
  const [scanResult, setScanResult]   = useState(null);
  const [threatIP, setThreatIP]       = useState('');
  const [threatResult, setThreatResult] = useState(null);

  const threats_list = [
    { ip: '192.168.4.211', type: 'Port scan',   risk: 'High'   },
    { ip: '10.0.0.87',     type: 'Brute force', risk: 'High'   },
    { ip: '172.16.33.5',   type: 'DDoS',        risk: 'Medium' },
    { ip: '203.0.113.44',  type: 'Recon',       risk: 'Low'    },
  ];

  useEffect(() => {
    socket.on('traffic_update', (data) => {
      setStats(data);
      setTraffic(prev => [...prev.slice(-20), data]);
    });
    fetchLogs();
    return () => socket.off('traffic_update');
  }, []);

  const fetchLogs = async () => {
    const res = await axios.get(API + '/api/logs');
    setLogs(res.data);
  };

  const handleScan = async () => {
    if (!scanIP) return;
    const res = await axios.get(API + '/api/scan/' + scanIP);
    setScanResult(res.data);
  };

  const handleThreat = async () => {
    if (!threatIP) return;
    const res = await axios.get(API + '/api/threat/' + threatIP);
    setThreatResult(res.data);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setLoggedIn(false);
  };

  const riskColor = (risk) => {
    if (risk === 'High')   return '#e24b4a';
    if (risk === 'Medium') return '#ef9f27';
    return '#1d9e75';
  };

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />;

  return (
    <div className="app">
      <div className="header">
        <div className="header-left">
          <span className="pulse-dot"></span>
          <h1>Network Security Dashboard</h1>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div className="header-time">{new Date().toLocaleTimeString()}</div>
          <button onClick={handleLogout} style={{
            background: 'transparent', border: '0.5px solid #2a2d3a',
            color: '#888', borderRadius: 8, padding: '4px 12px',
            cursor: 'pointer', fontSize: 12
          }}>Logout</button>
        </div>
      </div>

      <div className="metrics">
        <div className="metric-card">
          <div className="metric-label">Packets received</div>
          <div className="metric-value">{stats.packets.toLocaleString()}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Bandwidth (Mbps)</div>
          <div className="metric-value blue">{stats.bandwidth}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Threats detected</div>
          <div className="metric-value red">{stats.threats}</div>
        </div>
        <div className="metric-card">
          <div className="metric-label">Active threats</div>
          <div className="metric-value orange">{threats_list.length}</div>
        </div>
      </div>

      <div className="panels">
        <div className="panel">
          <div className="panel-title">Live traffic (Mbps)</div>
          <ResponsiveContainer width="100%" height={180}>
            <LineChart data={traffic}>
              <XAxis dataKey="timestamp" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 10 }} />
              <Tooltip />
              <Line type="monotone" dataKey="bandwidth" stroke="#378add" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="panel">
          <div className="panel-title">Suspicious IPs</div>
          <table className="threat-table">
            <thead>
              <tr><th>IP Address</th><th>Type</th><th>Risk</th></tr>
            </thead>
            <tbody>
              {threats_list.map((t, i) => (
                <tr key={i}>
                  <td className="mono">{t.ip}</td>
                  <td>{t.type}</td>
                  <td><span className="badge" style={{ background: riskColor(t.risk) }}>{t.risk}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="panels">
        <div className="panel">
          <div className="panel-title">Port scanner</div>
          <div className="input-row">
            <input className="ip-input" value={scanIP} onChange={e => setScanIP(e.target.value)} placeholder="Enter IP (e.g. 127.0.0.1)" />
            <button className="btn" onClick={handleScan}>Scan</button>
          </div>
          {scanResult && (
            <div className="result-box">
              <div className="mono">IP: {scanResult.ip}</div>
              {scanResult.open_ports.length === 0
                ? <div className="safe-text">No open ports found</div>
                : scanResult.open_ports.map((p, i) => (
                    <div key={i} className="port-row">
                      <span className="mono">:{p.port}</span>
                      <span className="service">{p.service}</span>
                      <span className="open-badge">OPEN</span>
                    </div>
                  ))
              }
            </div>
          )}
        </div>

        <div className="panel">
          <div className="panel-title">IP threat checker</div>
          <div className="input-row">
            <input className="ip-input" value={threatIP} onChange={e => setThreatIP(e.target.value)} placeholder="Enter IP (e.g. 192.168.4.211)" />
            <button className="btn" onClick={handleThreat}>Check</button>
          </div>
          {threatResult && (
            <div className="result-box">
              <div className="mono">IP: {threatResult.ip}</div>
              <div>Country: {threatResult.country}</div>
              <div>Abuse score: <span style={{ color: threatResult.abuse_score > 50 ? '#e24b4a' : '#1d9e75' }}>{threatResult.abuse_score}</span></div>
              <div>Reports: {threatResult.total_reports}</div>
              <div>Status: <span style={{ color: threatResult.is_threat ? '#e24b4a' : '#1d9e75', fontWeight: 500 }}>{threatResult.is_threat ? 'THREAT' : 'CLEAN'}</span></div>
            </div>
          )}
        </div>
      </div>

      <div className="panel">
        <div className="panel-title">Event log <button className="refresh-btn" onClick={fetchLogs}>Refresh</button></div>
        <div className="log-box">
          {logs.length === 0
            ? <div className="log-empty">No events yet.</div>
            : logs.map((l, i) => (
                <div key={i} className={"log-entry " + l.level.toLowerCase()}>
                  <span className="log-time">{l.timestamp}</span>
                  <span className="log-level">{l.level}</span>
                  <span>{l.message}</span>
                </div>
              ))
          }
        </div>
      </div>
    </div>
  );
}
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {path}")

print("Frontend updated!")