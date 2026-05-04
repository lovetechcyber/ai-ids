import os
import pandas as pd
import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# =========================
# CONFIG (API INTEGRATION)
# =========================
DASHBOARD_API = os.environ.get(
    "DASHBOARD_API",
    "https://ai-ids-myxb.onrender.com/api/alerts"
)

API_KEY = os.environ.get("API_KEY", "dev-key-change-me")

# =========================
# SEND ALERT TO DASHBOARD
# =========================
def send_alert(ip, severity, score, message):

    payload = {
        "src_ip": ip,
        "severity": severity,
        "score": score,
        "message": message
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

    try:
        res = requests.post(DASHBOARD_API, json=payload, headers=headers)
        print(f"[API] {res.status_code} -> {res.text}")

    except Exception as e:
        print(f"[ERROR] API call failed: {e}")

# =========================
# MAIN PIPELINE
# =========================
def main():

    csv_path = os.path.join(BASE_DIR, "logs", "predictions.csv")

    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():

        if row.get("anomaly", 0) == 1:

            ip = row.get("src_ip", "unknown")
            score = int(row.get("score", 50))

            # =========================
            # SEVERITY ENGINE
            # =========================
            if score >= 80:
                severity = "Critical"
            elif score >= 60:
                severity = "High"
            elif score >= 30:
                severity = "Medium"
            else:
                severity = "Low"

            message = f"Suspicious activity detected from {ip}"

            # =========================
            # SEND TO DASHBOARD API
            # =========================
            send_alert(ip, severity, score, message)

            # Optional local response simulation
            if severity in ["High", "Critical"]:
                print(f"[ACTION] Would block IP: {ip}")

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()