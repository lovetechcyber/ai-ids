from dashboard.models import db, TrafficLog, Alert, BlockedIP
from dashboard.scoring import calculate_score, get_severity
from dashboard.app import app

def process(data):
    with app.app_context():
        log = TrafficLog(**data)
        db.session.add(log)

        score = calculate_score(data)
        severity = get_severity(score)

        alert = Alert(
            src_ip=data['src_ip'],
            message="Suspicious activity",
            severity=severity,
            score=score
        )
        db.session.add(alert)

        if severity in ["High", "Critical"]:
            db.session.add(BlockedIP(ip_address=data['src_ip']))

        db.session.commit()