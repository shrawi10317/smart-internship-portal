from functools import wraps
from flask import session, redirect, url_for

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:
                return redirect(url_for("auth_main.login"))

            if role and session.get("role") != role:
                return redirect(url_for("auth_main.login"))

            return f(*args, **kwargs)
        return wrapper
    return decorator