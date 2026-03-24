from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class CompanyProfileForm(FlaskForm):

    company_name = StringField(
        "Company Name",
        validators=[DataRequired(), Length(max=200)]
    )

    website = StringField("Website")

    location = StringField("Location")

    description = TextAreaField("Description")

    logo = FileField(
        "Company Logo",
        validators=[FileAllowed(['jpg','png','jpeg'], 'Images only!')]
    )

    submit = SubmitField("Save Profile")