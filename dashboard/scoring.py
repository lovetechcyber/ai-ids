from models import TrafficLog

def calculate_score(data):
    score = 0

    if data.get("anomaly") == 1:
        score += 50

    if data.get("packet_size", 0) > 1000:
        score += 20

    if data.get("port") in [22, 23, 3389]:
        score += 20

    ip_count = TrafficLog.query.filter_by(src_ip=data.get("src_ip")).count()
    if ip_count > 10:
        score += 10

    return score

def get_severity(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 30:
        return "Medium"
    return "Low"