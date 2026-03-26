from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[
        DataRequired(message="Name is required"),
        Length(min=2, max=50, message="Name must be between 2 and 50 characters")
    ])
    email = StringField("Email", validators=[
        DataRequired(message="Email is required"),
        Email(message="Enter a valid email address")
    ])
    password = PasswordField("Password", validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters")
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(message="Confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    role = SelectField("Role", choices=[("student", "Student"), ("company", "Company")], validators=[DataRequired()])
    submit = SubmitField("Register")