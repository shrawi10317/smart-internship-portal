from wtforms import IntegerField,StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm

class InternshipForm(FlaskForm):

    title = StringField(
        "Internship Title",
        validators=[DataRequired(), Length(max=200)]
    )

    description = TextAreaField(
        "Internship Description",
        validators=[DataRequired()]
    )

    stipend = IntegerField("Stipend")

    duration = StringField("Duration")

    location = StringField("Location")

    submit = SubmitField("Post Internship")