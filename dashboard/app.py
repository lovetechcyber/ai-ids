from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required
from models import db, TrafficLog, Alert, BlockedIP
from auth import auth_bp, login_manager
import os

# =========================
# APP CONFIG (PRODUCTION)
# =========================
app = Flask(__name__)

# 🔐 SECRET KEY (NEVER hardcode in production)
app.config['SECRET_KEY'] = os.environ.get(
    "SECRET_KEY",
    "dev-fallback-insecure-key"
)

# =========================
# DATABASE CONFIG
# =========================
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///" + os.path.join(basedir, "ids.db")
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =========================
# INIT EXTENSIONS
# =========================
db.init_app(app)
login_manager.init_app(app)

# Register auth blueprint
app.register_blueprint(auth_bp)

# =========================
# SECURITY HEADERS (BASIC HARDENING)
# =========================
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

@app.route("/dashboard")
@login_required
def dashboard():
    logs = TrafficLog.query.all()
    alerts = Alert.query.all()
    blocked_ips = BlockedIP.query.all()

    total_traffic = len(logs)
    anomaly_count = len([log for log in logs if log.anomaly == 1])

    top_ips = {}
    for log in logs:
        top_ips[log.src_ip] = top_ips.get(log.src_ip, 0) + 1

    return render_template(
        "index.html",
        total_traffic=total_traffic,
        anomaly_count=anomaly_count,
        top_ips=top_ips,
        alerts=alerts,
        blocked_ips=blocked_ips
    )

@app.route("/alerts/<level>")
@login_required
def filter_alerts(level):
    alerts = Alert.query.filter_by(severity=level.capitalize()).all()
    return render_template("alerts.html", alerts=alerts)

# =========================
# APP ENTRY POINT
# =========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False  # ❌ NEVER True in production
    )