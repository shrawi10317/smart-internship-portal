from app import create_app, db

app = create_app()

# Ensure instance folder exists (safety check)
import os
instance_path = os.path.join(app.root_path, "instance")
os.makedirs(instance_path, exist_ok=True)

with app.app_context():
    print("Creating DB at:", app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()  # Creates SQLite DB if it doesn't exist

# Disable caching for dev
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)