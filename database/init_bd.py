from dashboard.app import app
from dashboard.models import db

with app.app_context():
    db.create_all()
    print("Database initialized!")