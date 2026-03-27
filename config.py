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

    # ----------------- SENDGRID ----------------- 
    SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY") 
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "shrawaniofficial6@gmail.com")
    # ----------------- OTHER -----------------
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"