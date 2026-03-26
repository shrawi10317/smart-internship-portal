from app import create_app, db
import os

# Ensure instance folder exists
if not os.path.exists("instance"):
    os.makedirs("instance")

# Create Flask app
app = create_app()

# Create all database tables if they don't exist
with app.app_context():
    db.create_all()

# Disable caching for dynamic pages
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    # Use 0.0.0.0 and PORT environment variable for deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)