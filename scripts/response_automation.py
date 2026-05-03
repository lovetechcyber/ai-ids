import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

import pandas as pd
from flask import Flask
import dashboard.models

# =========================
# APP SETUP
# =========================
app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-key-change-me")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'ids.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dashboard.models.db.init_app(app)

# =========================
# HELPERS
# =========================
def block_ip(ip):
    print(f"[SIMULATION] Blocking IP: {ip}")
    blocked = dashboard.models.BlockedIP(ip_address=ip)
    dashboard.models.db.session.add(blocked)

def save_alert(ip, severity, score, message):
    alert = dashboard.models.Alert(
        src_ip=ip,
        severity=severity,
        score=score,
        message=message
    )
    dashboard.models.db.session.add(alert)

# =========================
# MAIN PIPELINE
# =========================
def main():

    csv_path = os.path.join(BASE_DIR, "logs", "predictions.csv")

    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    with app.app_context():
        try:
            for _, row in df.iterrows():

                if row.get("anomaly", 0) == 1:

                    ip = row.get("src_ip", "unknown")
                    score = int(row.get("score", 50))

                    # =========================
                    # Severity Logic
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

                    save_alert(ip, severity, score, message)

                    if severity in ["High", "Critical"]:
                        block_ip(ip)

            dashboard.models.db.session.commit()
            print("✅ Alerts saved to dashboard (DB)")

        except Exception as e:
            dashboard.models.db.session.rollback()
            print(f"❌ Error occurred: {e}")

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()