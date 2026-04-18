import requests
import os

ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY", "").strip()

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
