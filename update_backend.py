files = {
"backend/mailer.py": """import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

GMAIL_USER = os.getenv("GMAIL_USER", "").strip()
GMAIL_PASS = os.getenv("GMAIL_PASS", "").strip()
ALERT_TO   = os.getenv("ALERT_TO", "").strip()

def send_threat_email(threat_count):
    if not GMAIL_USER or not GMAIL_PASS or not ALERT_TO:
        return
    try:
        msg = MIMEMultipart()
        msg["From"]    = GMAIL_USER
        msg["To"]      = ALERT_TO
        msg["Subject"] = f"[ALERT] {threat_count} threat(s) detected on your network!"
        body = f\"\"\"
Network Security Dashboard Alert

{threat_count} suspicious packet(s) were detected on your network.

Login to your dashboard to investigate:
https://net-security-dashboard.onrender.com

-- Network Security Dashboard
\"\"\"
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, ALERT_TO, msg.as_string())
        server.quit()
        print(f"Alert email sent to {ALERT_TO}")
    except Exception as e:
        print(f"Email error: {e}")
""",

"backend/app.py": """from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
import threading
import time
import random
from scanner import scan_ports
from threat import check_ip
from logger import init_db, log_event, get_logs
from mailer import send_threat_email

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()

USERS = {"admin": "cyber123", "yash": "secure456"}
email_cooldown = 0

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    if USERS.get(username) == password:
        return jsonify({"success": True, "token": "secure-token-" + username})
    return jsonify({"success": False, "message": "Invalid credentials"}), 401

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
    global email_cooldown
    while True:
        data = {
            "packets": random.randint(50, 300),
            "bandwidth": round(random.uniform(10, 200), 1),
            "threats": random.randint(0, 3),
            "timestamp": time.strftime("%H:%M:%S")
        }
        socketio.emit("traffic_update", data)
        if data["threats"] > 0:
            log_event("ALERT", f"Threat detected - {data['threats']} suspicious packet(s)")
            if time.time() - email_cooldown > 300:
                send_threat_email(data["threats"])
                email_cooldown = time.time()
        time.sleep(2)

@socketio.on("connect")
def on_connect():
    print("Client connected")
    thread = threading.Thread(target=broadcast_traffic, daemon=True)
    thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Written: {path}")

print("Backend updated!")