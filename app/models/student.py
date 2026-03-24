from app import db

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    degree = db.Column(db.String(100), nullable=True)
    college = db.Column(db.String(150), nullable=True)
    skills = db.Column(db.String(300), nullable=True)
    profile_pic = db.Column(db.String(300), nullable=True)  # optional

    user = db.relationship("User", backref="student_profile", uselist=False)