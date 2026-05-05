import os
import pandas as pd
import requests

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

API_URL = "https://ai-ids-myxb.onrender.com/api/ingest"
API_KEY = "ids123"


def safe_int(value, default=0):
    try:
        return int(value)
    except:
        return default


def main():

    csv_path = os.path.join(BASE_DIR, "logs", "predictions.csv")

    if not os.path.exists(csv_path):
        print("❌ predictions.csv not found")
        return

    df = pd.read_csv(csv_path)

    logs = []
    alerts = []

    for _, row in df.iterrows():

        # =========================
        # SAFE TYPE CONVERSION
        # =========================
        src_ip = str(row.get("Source", row.get("src_ip", "unknown")))
        dst_ip = str(row.get("Destination", row.get("dest_ip", "unknown")))
        protocol = str(row.get("Protocol", row.get("protocol", "unknown")))

        packet_size = safe_int(row.get("Length", 0))
        
        # Isolation Forest output:
        # 1 = normal, -1 = anomaly
        anomaly_flag = row.get("Anomaly", 0)
        is_anomaly = 1 if anomaly_flag == -1 else 0

        # fake scoring (you can improve later with probability model)
        score = 80 if is_anomaly else 20

        # =========================
        # BUILD TRAFFIC LOG
        # =========================
        logs.append({
            "src_ip": src_ip,
            "dest_ip": dst_ip,
            "protocol": protocol,
            "packet_size": packet_size,
            "anomaly": is_anomaly
        })

        # =========================
        # BUILD ALERT
        # =========================
        if is_anomaly == 1:

            if score >= 80:
                severity = "Critical"
            elif score >= 60:
                severity = "High"
            elif score >= 30:
                severity = "Medium"
            else:
                severity = "Low"

            alerts.append({
                "src_ip": src_ip,
                "severity": severity,
                "score": score,
                "message": f"Suspicious activity detected from {src_ip}"
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
        res = requests.post(API_URL, json=payload, headers=headers, timeout=20)

        print("STATUS:", res.status_code)
        print("RESPONSE:", res.text)

    except Exception as e:
        print("❌ Failed to send data:", e)


if __name__ == "__main__":
    main()