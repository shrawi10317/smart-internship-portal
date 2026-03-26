# app/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Load config
    from config import Config
    app.config.from_object(Config)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Ensure database folder exists (for SQLite)
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_uri.startswith("sqlite:///"):
        db_file = db_uri.replace("sqlite:///", "")
        db_dir = os.path.dirname(db_file)
        os.makedirs(db_dir, exist_ok=True)  # Very important for deployment

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    # ----------------- BLUEPRINTS -----------------
    from app.routes.auth_routes import auth_main
    from app.routes.student_routes import student
    from app.routes.company_routes import company
    from app.routes.main_routes import main

    app.register_blueprint(auth_main)
    app.register_blueprint(student)
    app.register_blueprint(company)
    app.register_blueprint(main)

    # ----------------- ERROR HANDLERS -----------------
    @app.errorhandler(404)
    def page_not_found(e):
        return "Page not found 404", 404

    @app.errorhandler(500)
    def internal_error(e):
        return "Internal server error 500", 500

    # ----------------- CREATE DATABASE IF NOT EXISTS -----------------
    with app.app_context():
        print("Creating database at:", app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()

    return app