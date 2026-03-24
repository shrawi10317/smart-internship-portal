from flask_wtf import FlaskForm
from wtforms import DateField, StringField, RadioField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )

    role = RadioField(
        "Register As",
        choices=[("student", "Student"), ("company", "Company")],
        validators=[DataRequired()]
    )

    submit = SubmitField("Register")