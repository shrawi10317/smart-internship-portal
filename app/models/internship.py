from app import db
from datetime import datetime

class Internship(db.Model):

    __tablename__ = "internships"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    stipend = db.Column(db.Integer)
    duration = db.Column(db.String(100))
    location = db.Column(db.String(200))
    posted_date = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ ADD THIS
    applications = db.relationship("Application", backref="internship", lazy=True)

    # company = db.relationship("Company", backref="internships")