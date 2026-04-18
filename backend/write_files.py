files = {
"app.py": """from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
import random
from scanner import scan_ports
from threat import check_ip
from logger import init_db, log_event, get_logs

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()

@app.route("/api/scan/<ip>")
def scan(ip):
    ports = scan_ports(ip)
    return jsonify({"ip": ip, "open_ports": ports})

@app.route("/api/threat/<ip>")
def threat(ip):
    result = check_ip(ip)
    return jsonify(result)

@app.route("/api/logs")
def logs():
    return jsonify(get_logs())

def broadcast_traffic():
    while True:
        data = {
            "packets": random.randint(50, 300),
            "bandwidth": round(random.uniform(10, 200), 1),
            "threats": random.randint(0, 3),
            "timestamp": time.strftime("%H:%M:%S")
        }
        socketio.emit("traffic_update", data)
        if data["threats"] > 0:
            log_event("ALERT", f"Threat detected - {data['threats']} packet(s)")
        time.sleep(2)

@socketio.on("connect")
def on_connect():
    print("Client connected")
    thread = threading.Thread(target=broadcast_traffic, daemon=True)
    thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
""",

"scanner.py": """import socket

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 8080, 8443]

def scan_ports(ip, timeout=0.5):
    open_ports = []
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service = get_service_name(port)
                open_ports.append({"port": port, "service": service, "status": "open"})
            sock.close()
        except Exception:
            pass
    return open_ports

def get_service_name(port):
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 3306: "MySQL", 5432: "PostgreSQL",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt"
    }
    return services.get(port, "Unknown")
""",

"threat.py": """import requests
import os

ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY", "")

def check_ip(ip):
    if not ABUSEIPDB_KEY:
        return simulate_threat(ip)
    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json().get("data", {})
        return {
            "ip": ip,
            "abuse_score": data.get("abuseConfidenceScore", 0),
            "country": data.get("countryCode", "Unknown"),
            "total_reports": data.get("totalReports", 0),
            "is_threat": data.get("abuseConfidenceScore", 0) > 50
        }
    except Exception as e:
        return {"ip": ip, "error": str(e)}

def simulate_threat(ip):
    known = {
        "192.168.4.211": {"abuse_score": 95, "country": "CN", "total_reports": 42, "is_threat": True},
        "10.0.0.87":     {"abuse_score": 80, "country": "RU", "total_reports": 18, "is_threat": True},
        "172.16.33.5":   {"abuse_score": 60, "country": "BR", "total_reports": 7,  "is_threat": True},
    }
    result = known.get(ip, {"abuse_score": 0, "country": "US", "total_reports": 0, "is_threat": False})
    result["ip"] = ip
    return result
""",

"logger.py": """import sqlite3
import time

DB = "events.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_event(level, message):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO events (level, message, timestamp) VALUES (?, ?, ?)",
        (level, message, time.strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_logs(limit=50):
    conn = sqlite3.connect(DB)
    cursor = conn.execute(
        "SELECT level, message, timestamp FROM events ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = [{"level": r[0], "message": r[1], "timestamp": r[2]} for r in cursor.fetchall()]
    conn.close()
    return rows
"""
}

for filename, content in files.items():
    with open(filename, "w") as f:
        f.write(content)
    print(f"Written: {filename}")

print("All files written successfully!")