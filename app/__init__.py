from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    # Create Flask app
    app = Flask(__name__, instance_relative_config=True)

    # Load default config
    app.config.from_object("config.Config")

    # Load .env file (for local development)
    load_dotenv()

    # SECRET KEY
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY") or "dev_secret_key_!@#1234567890"

    # MAIL CONFIG (works locally and in deployment)
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USE_SSL"] = False
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # Import models
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

    # Optional: test email route
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