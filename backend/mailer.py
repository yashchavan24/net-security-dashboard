import smtplib
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
        body = f"""
Network Security Dashboard Alert

{threat_count} suspicious packet(s) were detected on your network.

Login to your dashboard to investigate:
https://net-security-dashboard.onrender.com

-- Network Security Dashboard
"""
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, ALERT_TO, msg.as_string())
        server.quit()
        print(f"Alert email sent to {ALERT_TO}")
    except Exception as e:
        print(f"Email error: {e}")
