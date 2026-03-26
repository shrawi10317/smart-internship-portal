import os
from pathlib import Path

basedir = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "my_secret_key")
    
    db_folder = basedir / "instance"
    os.makedirs(db_folder, exist_ok=True)

    db_path = db_folder / "internship_portal.db"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path.as_posix()}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")