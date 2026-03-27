import os

class Config:
    # ----------------- FLASK SECRET -----------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-dev-key")

    # ----------------- DATABASE -----------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(INSTANCE_DIR, exist_ok=True)

    DB_PATH = os.path.join(INSTANCE_DIR, "internship_portal.db")

    DATABASE_URL = os.environ.get("DATABASE_URL")

    # ✅ Fix for Render PostgreSQL
    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local fallback
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------------- MAIL -----------------
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False").lower() == "true"

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # Optional performance tweaks
    MAIL_MAX_EMAILS = None
    MAIL_TIMEOUT = 10

    # ----------------- OTHER -----------------
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"