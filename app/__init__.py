from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail =Mail()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config.from_object("config.Config")

    # IMPORTANT: import models
    from . import models
    
    # MAIL CONFIG
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "your_email"
    app.config["MAIL_PASSWORD"] = "your_password"

    db.init_app(app)
    mail.init_app(app)   # ✅ initialize mail

    from .routes.main_routes import main
    app.register_blueprint(main)

    from .routes.auth_routes import auth_main
    app.register_blueprint(auth_main)

    from .routes.student_routes import student
    app.register_blueprint(student)

    from .routes.company_routes import company
    app.register_blueprint(company)
    

    return app
