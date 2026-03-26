import os
from app import create_app, db

# ----------------- CREATE APP -----------------
app = create_app()

# ----------------- ENSURE INSTANCE FOLDER -----------------
instance_path = os.path.join(app.root_path, "instance")
os.makedirs(instance_path, exist_ok=True)

# ----------------- ENSURE DATABASE FILE -----------------
db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
if db_uri.startswith("sqlite:///"):
    db_file = db_uri.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_file)
    os.makedirs(db_dir, exist_ok=True)  # Ensure folder exists

# ----------------- CREATE DATABASE -----------------
with app.app_context():
    print("Creating database at:", app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()

# ----------------- DISABLE CACHE FOR DEV -----------------
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# ----------------- RUN APP -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)