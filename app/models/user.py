from app import db

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200),nullable=False)
    role = db.Column(db.String(20))
    is_verified = db.Column(db.Boolean, default=False)