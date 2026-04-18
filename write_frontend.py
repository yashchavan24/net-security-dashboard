import os

os.makedirs("frontend/src", exist_ok=True)

files = {
"frontend/src/App.js": """import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';
import './App.css';

const socket = io('http://127.0.0.1:5000');
const API = 'http://127.0.0.1:5000';

export default function App() {
  const [traffic, setTraffic] = useState([]);
  const [stats, setStats] = useState({ packets: 0, bandwidth: 0, threats: 0 });
  const [logs, setLogs] = useState([]);
  const [scanIP, setScanIP] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [threatIP, setThreatIP] = useState('');
  const [threatResult, setThreatResult] = useState(null);

  const threats_list = [
    { ip: '192.168.4.211', type: 'Port scan', risk: 'High' },
    { ip: '10.0.0.87', type: 'Brute force', risk: 'High' },
    { ip: '172.16.33.5', type: 'DDoS', risk: 'Medium' },
    { ip: '203.0.113.44', type: 'Recon', risk: 'Low' },
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

  const riskColor = (risk) => {
    if (risk === 'High') return '#e24b4a';
    if (risk === 'Medium') return '#ef9f27';
    return '#1d9e75';
  };

  return (
    <div className="app">
      <div className="header">
        <div className="header-left">
          <span className="pulse-dot"></span>
          <h1>Network Security Dashboard</h1>
        </div>
        <div className="header-time">{new Date().toLocaleTimeString()}</div>
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
            <input
              className="ip-input"
              value={scanIP}
              onChange={e => setScanIP(e.target.value)}
              placeholder="Enter IP (e.g. 127.0.0.1)"
            />
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
            <input
              className="ip-input"
              value={threatIP}
              onChange={e => setThreatIP(e.target.value)}
              placeholder="Enter IP (e.g. 192.168.4.211)"
            />
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
            ? <div className="log-empty">No events yet — events appear as threats are detected.</div>
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
""",

"frontend/src/App.css": """* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0f1117; color: #e2e2e2; font-family: -apple-system, sans-serif; font-size: 14px; }
.app { max-width: 1100px; margin: 0 auto; padding: 1.5rem; }
.header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.header-left { display: flex; align-items: center; gap: 10px; }
h1 { font-size: 18px; font-weight: 500; }
.pulse-dot { width: 10px; height: 10px; border-radius: 50%; background: #1d9e75; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
.header-time { font-size: 12px; color: #888; font-family: monospace; }
.metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.metric-card { background: #1a1d27; border: 0.5px solid #2a2d3a; border-radius: 10px; padding: 1rem; }
.metric-label { font-size: 11px; color: #888; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em; }
.metric-value { font-size: 24px; font-weight: 500; }
.metric-value.blue { color: #378add; }
.metric-value.red { color: #e24b4a; }
.metric-value.orange { color: #ef9f27; }
.panels { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 1.5rem; }
.panel { background: #1a1d27; border: 0.5px solid #2a2d3a; border-radius: 10px; padding: 1.25rem; }
.panel-title { font-size: 11px; font-weight: 500; color: #888; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 1rem; display: flex; align-items: center; gap: 10px; }
.threat-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.threat-table th { text-align: left; color: #666; font-weight: 400; padding: 4px 0; border-bottom: 0.5px solid #2a2d3a; }
.threat-table td { padding: 7px 0; border-bottom: 0.5px solid #1e2130; }
.mono { font-family: monospace; font-size: 12px; }
.badge { font-size: 11px; padding: 2px 8px; border-radius: 99px; color: #fff; font-weight: 500; }
.input-row { display: flex; gap: 8px; margin-bottom: 12px; }
.ip-input { flex: 1; background: #0f1117; border: 0.5px solid #2a2d3a; border-radius: 8px; padding: 7px 10px; color: #e2e2e2; font-size: 13px; }
.ip-input:focus { outline: none; border-color: #378add; }
.btn { background: transparent; border: 0.5px solid #378add; color: #378add; border-radius: 8px; padding: 7px 16px; cursor: pointer; font-size: 13px; }
.btn:hover { background: #378add22; }
.result-box { background: #0f1117; border-radius: 8px; padding: 12px; font-size: 13px; line-height: 2; }
.port-row { display: flex; gap: 10px; align-items: center; }
.service { color: #888; }
.open-badge { background: #1d9e7522; color: #1d9e75; font-size: 11px; padding: 1px 6px; border-radius: 4px; }
.safe-text { color: #1d9e75; }
.log-box { max-height: 200px; overflow-y: auto; font-family: monospace; font-size: 12px; }
.log-entry { display: flex; gap: 12px; padding: 5px 0; border-bottom: 0.5px solid #1e2130; }
.log-time { color: #555; min-width: 140px; }
.log-level { min-width: 50px; font-weight: 500; }
.log-entry.alert .log-level { color: #e24b4a; }
.log-entry.warn .log-level { color: #ef9f27; }
.log-entry.ok .log-level { color: #1d9e75; }
.log-empty { color: #555; font-style: italic; }
.refresh-btn { background: transparent; border: 0.5px solid #2a2d3a; color: #888; border-radius: 6px; padding: 2px 8px; cursor: pointer; font-size: 11px; }
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {path}")

print("All frontend files written!")