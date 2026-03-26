from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object("config.Config")

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Import models (make sure you have models.py)
    from . import models

    # Register blueprints
    from .routes.main_routes import main
    app.register_blueprint(main)

    from .routes.auth_routes import auth_main
    app.register_blueprint(auth_main)

    from .routes.student_routes import student
    app.register_blueprint(student)

    from .routes.company_routes import company
    app.register_blueprint(company)

    # Test email route
    @app.route("/test_email")
    def test_email():
        from flask_mail import Message
        try:
            msg = Message(
                subject="Test Email",
                sender=app.config["MAIL_USERNAME"],
                recipients=[app.config["MAIL_USERNAME"]],
                body="This is a test email from Flask!"
            )
            mail.send(msg)
            return "Email sent successfully!"
        except Exception as e:
            return f"Email failed: {str(e)}"

    return app