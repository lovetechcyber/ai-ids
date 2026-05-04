import os
import pandas as pd
import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

API_URL = "https://ai-ids-myxb.onrender.com/api/ingest"
API_KEY = "ids123"


def main():

    csv_path = os.path.join(BASE_DIR, "logs", "predictions.csv")

    if not os.path.exists(csv_path):
        print("❌ predictions.csv not found")
        return

    df = pd.read_csv(csv_path)

    logs = []
    alerts = []

    for _, row in df.iterrows():

        # ✅ Convert EVERYTHING to safe Python types
        ip = str(row.get("src_ip", "unknown"))
        dest_ip = str(row.get("dest_ip", "unknown"))
        protocol = str(row.get("protocol", "unknown"))

        score = int(row.get("score", 50))
        anomaly = int(row.get("anomaly", 0))
        packet_size = int(row.get("Length", 0))

        # =========================
        # BUILD TRAFFIC LOG
        # =========================
        logs.append({
            "src_ip": ip,
            "dest_ip": dest_ip,
            "protocol": protocol,
            "packet_size": packet_size,
            "anomaly": anomaly
        })

        # =========================
        # BUILD ALERT
        # =========================
        if anomaly == 1:

            if score >= 80:
                severity = "Critical"
            elif score >= 60:
                severity = "High"
            elif score >= 30:
                severity = "Medium"
            else:
                severity = "Low"

            alerts.append({
                "src_ip": ip,
                "severity": severity,
                "score": score,
                "message": f"Suspicious activity detected from {ip}"
            })

    payload = {
        "logs": logs,
        "alerts": alerts
    }

    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": API_KEY
    }

    try:
        res = requests.post(API_URL, json=payload, headers=headers)
        print("STATUS:", res.status_code)
        print("RESPONSE:", res.text)

    except Exception as e:
        print("❌ Failed to send data:", e)


if __name__ == "__main__":
    main()