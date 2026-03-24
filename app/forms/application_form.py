from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileRequired, FileAllowed

class InternshipApplicationForm(FlaskForm):

    full_name = StringField("Full Name", validators=[DataRequired()])

    email = StringField("Email", validators=[DataRequired(), Email()])

    degree = StringField("Degree", validators=[DataRequired()])

    college = StringField("College / University", validators=[DataRequired()])

    skills = StringField("Skills", validators=[DataRequired()])

    cover_letter = TextAreaField("Cover Letter")

    resume = FileField(
        "Upload Resume",
        validators=[
            FileRequired(),
            FileAllowed(["pdf","doc","docx"], "Resume must be PDF or DOC")
        ]
    )

    submit = SubmitField("Apply Internship")