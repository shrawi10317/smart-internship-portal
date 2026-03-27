from flask import Blueprint, render_template, redirect, url_for, request, session
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.company import Company
from app.forms.register_form import RegistrationForm
from app.forms.login_form import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
import random
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import time

auth_main = Blueprint("auth_main", __name__)

# ------------------- LOCAL SMTP EMAIL -------------------
def send_email(to_email, subject, content, retries=3, delay=2):
    """Send email locally using Python SMTP (Gmail or local server)"""

    def send():
        for attempt in range(1, retries + 1):
            try:
                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                smtp_user = os.environ.get("MAIL_USERNAME")
                smtp_pass = os.environ.get("MAIL_PASSWORD")

                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = smtp_user
                msg["To"] = to_email
                msg.attach(MIMEText(content, "html"))

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, to_email, msg.as_string())

                print(f"✅ Email sent to {to_email}")
                break
            except Exception as e:
                print(f"❌ Attempt {attempt} failed: {e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    print(f"❌ Failed after {retries} attempts.")

    threading.Thread(target=send, daemon=True).start()


# ------------------- REGISTER -------------------
@auth_main.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            return render_template("register.html", form=form, alert_message="Email already registered", alert_type="error")

        hashed_password = generate_password_hash(form.password.data)
        user = User(name=form.name.data, email=form.email.data, password=hashed_password, role=form.role.data, is_verified=False)
        db.session.add(user)
        db.session.commit()

        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["verify_user_id"] = user.id

        # 🔹 Send OTP using local SMTP
        threading.Thread(target=send_email, args=(user.email, "OTP Verification - SmartInternship", f"<h2>Your OTP is: {otp}</h2>")).start()

        return redirect(url_for("auth_main.verify_otp"))

    return render_template("register.html", form=form)


# ------------------- LOGIN -------------------
@auth_main.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not check_password_hash(user.password, form.password.data):
            return render_template("login.html", form=form, alert_message="Invalid email or password", alert_type="error")
        if not user.is_verified:
            return render_template("login.html", form=form, alert_message="Verify your email first", alert_type="warning")

        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role

        if user.role == "company":
            company = Company.query.filter_by(user_id=user.id).first()
            if not company or not company.check_profile_complete():
                return redirect(url_for("company.create_company_profile", message="Please complete your company profile first.", category="warning"))
            session["company_id"] = company.id
            session["name"] = company.company_name
            return redirect(url_for("company.dashboard", message="Login successful!", category="success"))

        elif user.role == "student":
            student = Student.query.filter_by(user_id=user.id).first()
            if not student:
                student = Student(user_id=user.id, full_name="", email=user.email, degree="", college="", skills="", profile_pic=None)
                db.session.add(student)
                db.session.commit()
            session["student_id"] = student.id
            session["name"] = student.full_name or user.name
            if not student.full_name or not student.profile_pic:
                return redirect(url_for("student.create_profile", message="Please complete your profile first.", category="warning"))
            return redirect(url_for("student.dashboard", message="Login successful!", category="success"))

    return render_template("login.html", form=form)


# ------------------- LOGOUT -------------------
@auth_main.route("/logout")
def logout():
    session.clear()
    session['logout_message'] = "Logged out successfully"
    return redirect(url_for("main.home"))


# ------------------- FORGOT PASSWORD -------------------
@auth_main.route("/forgot_password", methods=["GET","POST"])
def forgot_password():
    message = None
    show_otp = False

    if request.method == "POST":
        if "email" in request.form:
            email = request.form.get("email")
            user = User.query.filter_by(email=email).first()
            if user:
                otp = str(random.randint(100000, 999999))
                session["reset_email"] = email
                session["reset_otp"] = otp

                threading.Thread(target=send_email, args=(email, "Your OTP Code", f"<h2>Your OTP is: {otp}</h2>")).start()
                message = "OTP sent to your email 📧"
                show_otp = True
            else:
                message = "Email not registered ❌"

        elif "otp" in request.form:
            entered_otp = request.form.get("otp")
            new_password = request.form.get("password")
            if entered_otp == session.get("reset_otp"):
                user = User.query.filter_by(email=session.get("reset_email")).first()
                user.password = generate_password_hash(new_password)
                db.session.commit()
                session.pop("reset_otp", None)
                session.pop("reset_email", None)
                message = "Password updated successfully ✅"
                show_otp = False
            else:
                message = "Invalid OTP ❌"
                show_otp = True

    return render_template("forgot_password.html", message=message, show_otp=show_otp)


# ------------------- VERIFY OTP -------------------
@auth_main.route("/verify-otp", methods=["GET","POST"])
def verify_otp():
    alert_message = None
    alert_type = None

    if request.method == "POST":
        entered_otp = request.form.get("otp")
        session_otp = session.get("otp")
        user_id = session.get("verify_user_id")

        if not user_id:
            return redirect(url_for("auth_main.login"))

        if entered_otp and session_otp and str(entered_otp) == str(session_otp):
            user = User.query.get(user_id)
            if user:
                user.is_verified = True
                db.session.commit()
            session.pop("otp", None)
            session.pop("verify_user_id", None)
            alert_message = "Account verified successfully! Please login."
            alert_type = "success"
            form = LoginForm()
            return render_template("login.html", form=form, alert_message=alert_message, alert_type=alert_type)
        else:
            alert_message = "Invalid OTP. Please try again."
            alert_type = "danger"

    return render_template("verify_otp.html", alert_message=alert_message, alert_type=alert_type)


# ------------------- RESEND OTP -------------------
@auth_main.route("/resend_otp", methods=["POST"])
def resend_otp():
    user_id = session.get("verify_user_id")
    if not user_id:
        return redirect(url_for("auth_main.login"))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for("auth_main.login"))

    otp = str(random.randint(100000, 999999))
    session["otp"] = otp
    threading.Thread(target=send_email, args=(user.email, "Your OTP - SmartInternship", f"<h2>Hello {user.name}, your new OTP is: {otp}</h2>")).start()
    return redirect(url_for("auth_main.verify_otp", otp_sent="true"))