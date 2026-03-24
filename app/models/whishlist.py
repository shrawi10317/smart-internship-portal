from app import db
class Wishlist(db.Model):
    __tablename__ = "wishlist"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    internship_id = db.Column(db.Integer, db.ForeignKey("internships.id"))