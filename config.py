import os

class Config:
    # Absolute path to instance folder (writable)
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "instance"))
    
    # Ensure instance folder exists
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    # SQLite database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "internship_portal.db")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev_secret_key_!@#1234567890"

    # Mail configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")