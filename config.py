import os

class Config:
    # ----------------- FLASK SECRET -----------------
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-dev-key")

    # ----------------- DATABASE -----------------
    # Absolute path to instance folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    os.makedirs(INSTANCE_DIR, exist_ok=True)  # Ensure folder exists

    # SQLite database file path
    DB_PATH = os.path.join(INSTANCE_DIR, "internship_portal.db")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH}"  # Use absolute path
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ----------------- MAIL -----------------
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "False").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # ----------------- OTHER SETTINGS -----------------
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"