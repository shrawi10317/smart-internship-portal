from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load config first
    app.config.from_object("config.Config")

    # Override with environment variables (Render)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

    # DATABASE FIX
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or app.config.get("SQLALCHEMY_DATABASE_URI")

    # MAIL CONFIG
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True  
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

    db.init_app(app)
    mail.init_app(app)

    from . import models

    from .routes.main_routes import main
    app.register_blueprint(main)

    from .routes.auth_routes import auth_main
    app.register_blueprint(auth_main)

    from .routes.student_routes import student
    app.register_blueprint(student)

    from .routes.company_routes import company
    app.register_blueprint(company)

    return app