from flask import Flask, jsonify
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
