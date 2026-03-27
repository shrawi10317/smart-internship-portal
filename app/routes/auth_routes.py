from flask import Blueprint, render_template, redirect, url_for,request,flash,session
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.company import Company
from app.forms.register_form import  RegistrationForm
from werkzeug.security import generate_password_hash,check_password_hash
from app.forms.login_form import LoginForm
from app.models.user import User
# from flask_mail import Message
import random
from app import mail
from flask import current_app
import time
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import threading





auth_main=Blueprint('auth_main',__name__)

def send_email(to_email, subject, content):
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))

        message = Mail(
            from_email=("Smart Internship", "shrawaniofficial6@gmail.com"),
            to_emails=to_email,
            subject=subject,
            html_content=content
        )

        # 🔥 IMPORTANT (Gmail trust fix)
        message.reply_to = "shrawaniofficial6@gmail.com"

        sg.send(message)
        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Email error: {str(e)}")
    

@auth_main.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            return render_template(
                "register.html",
                form=form,
                alert_message="Email already registered",
                alert_type="error",
                redirect_url=""
            )

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
            is_verified=False
        )

        db.session.add(user)
        db.session.commit()

        # 🔹 DO NOT create Student object here
        # Students will create profile after first login

        # 🔐 GENERATE OTP
        otp = str(random.randint(100000, 999999))
        session["otp"] = otp
        session["verify_user_id"] = user.id

        # 📩 SEND EMAIL
        send_email(
        user.email,
        "OTP Verification - SmartInternship",
        f"<h2>Your OTP is: {otp}</h2>"
        )

        return redirect(url_for("auth_main.verify_otp"))

    return render_template("register.html", form=form)

@auth_main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # ❌ Invalid credentials
        if not user or not check_password_hash(user.password, form.password.data):
            return render_template(
                "login.html",
                form=form,
                alert_message="Invalid email or password",
                alert_type="error"
            )

        # 🚫 Email not verified
        if not user.is_verified:
            return render_template(
                "login.html",
                form=form,
                alert_message="Verify your email first",
                alert_type="warning"
            )

        # ✅ Login success
        session.clear()
        session["user_id"] = user.id
        session["role"] = user.role

        # ================= COMPANY =================
        if user.role == "company":
            company = Company.query.filter_by(user_id=user.id).first()

            # ❗ No profile or incomplete
            if not company or not company.check_profile_complete():
                return redirect(url_for(
                    "company.create_company_profile",
                    message="Please complete your company profile first.",
                    category="warning"
                ))

            session["company_id"] = company.id
            session["name"] = company.company_name

            return redirect(url_for(
                "company.dashboard",
                message="Login successful!",
                category="success"
            ))

        # ================= STUDENT =================
        elif user.role == "student":
            student = Student.query.filter_by(user_id=user.id).first()

            # Create profile if not exists
            if not student:
                student = Student(
                    user_id=user.id,
                    full_name="",
                    email=user.email,
                    degree="",
                    college="",
                    skills="",
                    profile_pic=None
                )
                db.session.add(student)
                db.session.commit()

            session["student_id"] = student.id
            session["name"] = student.full_name or user.name

            # ❗ Incomplete profile
            if not student.full_name or not student.profile_pic:
                return redirect(url_for(
                    "student.create_profile",
                    message="Please complete your profile first.",
                    category="warning"
                ))

            return redirect(url_for(
                "student.dashboard",
                message="Login successful!",
                category="success"
            ))

    return render_template("login.html", form=form)

@auth_main.route("/logout")
def logout():
    session.clear()
    # store the message in session
    session['logout_message'] = "Logged out successfully"
    return redirect(url_for("main.home"))


@auth_main.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():

    message = None
    show_otp = False

    if request.method == "POST":

        # STEP 1: EMAIL SUBMIT
        if "email" in request.form:
            email = request.form.get("email")
            user = User.query.filter_by(email=email).first()

            if user:
                otp = str(random.randint(100000, 999999))

                session["reset_email"] = email
                session["reset_otp"] = otp

                # 📧 Send OTP
                send_email(
                email,
                "Your OTP Code",
                f"<h2>Your OTP is: {otp}</h2>"
                )
                message = "OTP sent to your email 📧"
                show_otp = True

            else:
                message = "Email not registered ❌"

        # STEP 2: VERIFY OTP + RESET
        elif "otp" in request.form:
            entered_otp = request.form.get("otp")
            new_password = request.form.get("password")

            if entered_otp == session.get("reset_otp"):

                user = User.query.filter_by(email=session.get("reset_email")).first()

                from werkzeug.security import generate_password_hash
                user.password = generate_password_hash(new_password)

                db.session.commit()

                # clear session
                session.pop("reset_otp", None)
                session.pop("reset_email", None)

                message = "Password updated successfully ✅"
                show_otp = False

            else:
                message = "Invalid OTP ❌"
                show_otp = True

    return render_template(
        "forgot_password.html",
        message=message,
        show_otp=show_otp
    )


@auth_main.route("/verify-otp", methods=["GET", "POST"])
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

            form = LoginForm()  # ✅ Pass form object here
            return render_template(
                "login.html",
                form=form,
                alert_message=alert_message,
                alert_type=alert_type
            )
        else:
            alert_message = "Invalid OTP. Please try again."
            alert_type = "danger"

    return render_template(
        "verify_otp.html",
        alert_message=alert_message,
        alert_type=alert_type
    )

@auth_main.route("/resend_otp", methods=["POST"])
def resend_otp():
    user_id = session.get("verify_user_id")
    if not user_id:
        return redirect(url_for("auth_main.login"))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for("auth_main.login"))

    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp

    # Send OTP
    send_email(
    user.email,
    "Your OTP - SmartInternship",
    f"<h2>Hello {user.name}, your new OTP is: {otp}</h2>"
    )

    # Redirect back to verify OTP page with popup
    return redirect(url_for("auth_main.verify_otp", otp_sent="true"))





    # test route
@auth_main.route("/init-test-user")
def init_test_user():
    try:
        # 🔍 Check if user already exists
        user = User.query.filter_by(email="autotest@gmail.com").first()

        if not user:
            new_user = User(
                name="Auto Test User",   # ✅ correct column
                email="autotest@gmail.com",
                password=generate_password_hash("123456"),
                role="student",
                is_verified=True        # optional but useful
            )

            db.session.add(new_user)
            db.session.commit()

            return "✅ Test user created successfully!"

        return "⚠️ User already exists!"

    except Exception as e:
        db.session.rollback()
        return f"❌ Error: {str(e)}"
    

