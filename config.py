import os

class Config:
    # ----------------- FLASK SECRET -----------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-dev-key")

    # ----------------- DATABASE -----------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    DB_PATH = os.path.join(INSTANCE_DIR, "internship_portal.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------------- DEBUG -----------------
    DEBUG = True
    PORT = 5000

    # ----------------- EMAIL (GMAIL SMTP) -----------------
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True") == "True"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # your Gmail
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # Gmail app password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)