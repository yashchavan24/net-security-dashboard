# 🔐 Network Security Dashboard

A real-time network security monitoring dashboard built with Python and React. Detects threats, scans ports, checks IP reputation, and sends email alerts.

![Dashboard](https://net-security-dashboard.vercel.app)

## 🌐 Live Demo
- **Frontend:** https://net-security-dashboard.vercel.app
- **Backend API:** https://net-security-dashboard.onrender.com

## ✨ Features
- 🔴 Real-time live traffic monitoring via WebSockets
- 🔍 Port scanner — scan any IP for open ports
- 🌍 IP threat checker using AbuseIPDB API (real country, abuse score, reports)
- 📧 Email alerts when threats are detected
- 🔐 Login page with authentication
- 📋 Event log with timestamped threat entries
- 🚀 Deployed on Render (backend) + Vercel (frontend)

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-SocketIO, Flask-CORS |
| Frontend | React, Recharts, Socket.IO, Axios |
| Database | SQLite |
| APIs | AbuseIPDB (IP reputation) |
| Deployment | Render (backend), Vercel (frontend) |
| Version Control | Git, GitHub |

## 📁 Project Structure