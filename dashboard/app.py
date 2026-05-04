from flask import Flask, render_template, redirect, url_for
from flask_login import login_required
from dashboard.models import db, TrafficLog, Alert, BlockedIP
from dashboard.auth import auth_bp, login_manager, bcrypt
import os

# =========================
# APP CONFIG
# =========================
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-insecure-key")

# =========================
# DATABASE CONFIG
# =========================
basedir = os.path.abspath(os.path.dirname(__file__))

database_url = os.environ.get("DATABASE_URL")

# Fix Render postgres URL (important if you switch later)
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or \
    "sqlite:///" + os.path.join(basedir, "ids.db")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =========================
# INIT EXTENSIONS
# =========================
db.init_app(app)
login_manager.init_app(app)
bcrypt.init_app(app)

# =========================
# REGISTER BLUEPRINTS
# =========================
app.register_blueprint(auth_bp)

# =========================
# AUTO CREATE TABLES (CRITICAL FIX)
# =========================
with app.app_context():
    db.create_all()

# =========================
# SECURITY HEADERS
# =========================
@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
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
    try:
        logs = TrafficLog.query.all()
        alerts = Alert.query.all()
        blocked_ips = BlockedIP.query.all()

        total_traffic = len(logs)
        anomaly_count = len([log for log in logs if getattr(log, "anomaly", 0) == 1])

        top_ips = {}
        for log in logs:
            ip = getattr(log, "src_ip", "unknown")
            top_ips[ip] = top_ips.get(ip, 0) + 1

        return render_template(
            "index.html",
            total_traffic=total_traffic,
            anomaly_count=anomaly_count,
            top_ips=top_ips,
            alerts=alerts,
            blocked_ips=blocked_ips
        )

    except Exception as e:
        # Prevent full crash in production
        return f"Dashboard error: {str(e)}", 500

@app.route("/alerts/<level>")
@login_required
def filter_alerts(level):
    alerts = Alert.query.filter_by(severity=level.capitalize()).all()
    return render_template("alerts.html", alerts=alerts)

# =========================
# HEALTH CHECK (FOR RENDER)
# =========================
@app.route("/health")
def health():
    return {"status": "ok"}, 200

# =========================
# ENTRY POINT (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )