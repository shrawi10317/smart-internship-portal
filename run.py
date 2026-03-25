from app import create_app,db
from flask_mail import Mail

app = create_app()


with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.cache_control.no_cache = True
    response.cache_control.must_revalidate = True
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    # Use 0.0.0.0 so Render can access your app
    app.run(host="0.0.0.0", port=5000, debug=False)