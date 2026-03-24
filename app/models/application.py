from app import db
from datetime import datetime


class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'))

    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    degree = db.Column(db.String(150))
    college = db.Column(db.String(150))
    skills = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)
    resume = db.Column(db.String(200))
    status = db.Column(db.String(20), default="pending")
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", backref="applications")

    __table_args__ = (
        db.UniqueConstraint('student_id', 'internship_id', name='unique_application'),
    )