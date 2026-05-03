from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TrafficLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src_ip = db.Column(db.String(50))
    dest_ip = db.Column(db.String(50))
    protocol = db.Column(db.String(10))
    packet_size = db.Column(db.Integer)
    anomaly = db.Column(db.Integer)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    src_ip = db.Column(db.String(50))
    message = db.Column(db.String(255))
    severity = db.Column(db.String(20))
    score = db.Column(db.Integer)

class BlockedIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))