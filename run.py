from app import create_app, db
import os

# Ensure instance folder exists
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance")
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app = create_app()

# Create tables
with app.app_context():
    db.create_all()

# Disable caching
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)