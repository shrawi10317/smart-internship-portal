from app import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_name = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(200))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    logo = db.Column(db.String(200))  # company logo filename

    # Optional: explicit profile completion flag
    is_profile_complete = db.Column(db.Boolean, default=False)

    internships = db.relationship("Internship", backref="company", lazy=True)

    def check_profile_complete(self):
        """
        Returns True if profile is considered complete.
        You can adjust rules here — e.g., require website, logo, etc.
        """
        # Example: require name, website, location, description, and logo
        required_fields = [self.company_name, self.website, self.location, self.description, self.logo]
        return all(required_fields)