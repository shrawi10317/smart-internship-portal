from flask import Blueprint,render_template
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.internship import Internship
from app import db
from flask import current_app
import os
from werkzeug.utils import secure_filename
from app.forms.internship_form import InternshipForm
from app.forms.company_form import CompanyProfileForm
from app.models.company import Company
from app.models.application import Application
from app.models.student import Student
from app.forms.internship_form import InternshipForm
# from flask_mail import Message
from flask import current_app
from datetime import datetime, timedelta
# from app import mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email
from sqlalchemy import func
from functools import wraps
from flask import session, redirect, url_for
from app.utils.decorators import login_required
import threading
import os
import time

company = Blueprint("company",__name__,url_prefix="/company")

def send_email(to_email, subject, content, retries=3, delay=5):
    """
    Send email via SendGrid API with retry logic.
    """

    message = Mail(
        from_email=Email(os.environ.get("MAIL_USERNAME"), "Smart Internship"),  # Verified Gmail
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    message.reply_to = Email(os.environ.get("MAIL_USERNAME"), "Smart Internship")

    for attempt in range(1, retries + 1):
        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(f"✅ Email sent to {to_email}, Status Code: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {str(e)}")
            if attempt < retries:
                print(f"⏳ Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return False

# ================= Decorator =================
# Decorator to ensure company profile exists and is complete
from functools import wraps
from flask import session, redirect, url_for
from urllib.parse import urlencode

def company_profile_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # ❌ Not logged in
        if session.get("role") != "company":
            return redirect(url_for("auth_main.login"))

        company_id = session.get("company_id")

        if not company_id:
            query = urlencode({
                "alert_message": "Please create your company profile first.",
                "alert_type": "warning"
            })
            return redirect(url_for("company.create_company_profile") + "?" + query)

        company_obj = Company.query.get(company_id)

        if not company_obj or not company_obj.check_profile_complete():
            query = urlencode({
                "alert_message": "Please complete your company profile first.",
                "alert_type": "warning"
            })
            return redirect(url_for("company.create_company_profile") + "?" + query)

        return f(*args, **kwargs)

    return decorated_function
# ✅ COMPANY DASHBOARD




@company.route("/dashboard")
@login_required(role="company")
@company_profile_required
def dashboard():
    company_id = session.get("company_id")
    company_obj = Company.query.get(company_id)

    # Fetch internships for this company
    internships = Internship.query.filter_by(company_id=company_obj.id).all()

    # Total applicants for all internships
    total_applicants = db.session.query(func.count(Application.id))\
        .join(Internship)\
        .filter(Internship.company_id == company_obj.id)\
        .scalar() or 0

    active_count = len(internships)

    return render_template(
        "company_dashboard.html",
        internships=internships,
        company_name=company_obj.company_name,
        total_applicants=total_applicants,
        active_count=active_count
    )


@company.route("/post_internship", methods=["GET","POST"])
@login_required(role="company")
def post_internship():

    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    form = InternshipForm()
    success = False

    if form.validate_on_submit():

        # ✅ ALWAYS GET COMPANY FROM DB
        company = Company.query.filter_by(user_id=session["user_id"]).first()

        if not company:
            return "Company profile not found", 404

        internship = Internship(
            company_id=company.id,   # ✅ FIXED
            title=form.title.data,
            description=form.description.data,
            stipend=form.stipend.data,
            duration=form.duration.data,
            location=form.location.data
        )

        db.session.add(internship)
        db.session.commit()

        success = True

    return render_template("post_internship.html", form=form, success=success)


@company.route("/edit_internship/<int:id>", methods=["GET","POST"])
@login_required(role="company")
def edit_internship(id):

    internship = Internship.query.get_or_404(id)
    form = InternshipForm(obj=internship)

    if form.validate_on_submit():

        internship.title = form.title.data
        internship.description = form.description.data
        internship.stipend = form.stipend.data
        internship.duration = form.duration.data
        internship.location = form.location.data

        db.session.commit()

        # 🔥 send popup data instead of flash
        return render_template(
            "edit_internship.html",
            form=form,
            alert_message="Internship updated successfully",
            alert_type="success",
            redirect_url=url_for("company.dashboard")
        )

    return render_template(
        "edit_internship.html",
        form=form
    )



@company.route("/delete_internship/<int:id>")
@login_required(role="company")
def delete_internship(id):
    internship = Internship.query.get_or_404(id)
    db.session.delete(internship)
    db.session.commit()
    
    # Redirect with a query parameter indicating deletion
    return redirect(url_for("company.dashboard", deleted="true"))


@company.route("/applicants/<int:internship_id>")
@login_required(role="company")
def view_applicants(internship_id):

    if session.get("role") != "company":
        return redirect(url_for("main.home"))

    applications = Application.query.filter_by(
        internship_id=internship_id
    ).all()

    return render_template(
        "view_applicants.html",
        applications=applications
    )

# ACCEPT APPLICATION
@company.route("/accept_application/<int:id>")
@login_required(role="company")
def accept_application(id):
    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    application = Application.query.get_or_404(id)

    # 🔒 SECURITY CHECK
    if application.internship.company_id != session.get("company_id"):
        return "Unauthorized", 403

    application.status = "accepted"
    db.session.commit()

    # ✅ SEND EMAIL
    # ✅ SEND EMAIL (non-blocking)
    threading.Thread(
    target=send_email,
    args=(
        application.student.email,
        "Internship Application Accepted",
        f"""
        <p>Hello {application.student.name},</p>
        <p><b>Congratulations!</b></p>
        <p>Your application for <b>{application.internship.title}</b> has been ACCEPTED.</p>
        <br>
        <p>Best Regards,<br>Smart Internship Portal</p>
        """
    )
    ).start()

    # Redirect with query param instead of flash
    return redirect(url_for("company.applications", accepted="true"))


# REJECT APPLICATION
@company.route("/reject_application/<int:id>")
@login_required(role="company")
def reject_application(id):
    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    application = Application.query.get_or_404(id)

    # 🔒 SECURITY CHECK
    if application.internship.company_id != session.get("company_id"):
        return "Unauthorized", 403

    application.status = "rejected"
    db.session.commit()

    # ✅ SEND EMAIL
    # ✅ SEND EMAIL (non-blocking)
    threading.Thread(
    target=send_email,
    args=(
        application.student.email,
        "Internship Application Update",
        f"""
        <p>Hello {application.student.name},</p>
        <p>We regret to inform you that your application for 
        <b>{application.internship.title}</b> was not selected.</p>
        <br>
        <p>Best Regards,<br>Smart Internship Portal</p>
        """
    )
    ).start()

    # Redirect with query param instead of flash
    return redirect(url_for("company.applications", rejected="true"))


@company.route("/applications")
@login_required(role="company")
@company_profile_required
def applications():
    # Only company can access
    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    company_id = session.get("company_id")

    # Fetch all applications for this company's internships
    applications = Application.query.join(Application.internship).filter(
        Internship.company_id == company_id
    ).order_by(Application.applied_date.desc()).all()

    if not applications:
        message = "No applications yet for your internships."
        return render_template("company_applications.html", message=message)

    return render_template("company_applications.html", applications=applications)

@company.route("/student/<int:student_id>")
@login_required(role="company")
def view_student(student_id):
    # Only allow company access
    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    # Try to fetch the latest application
    application = Application.query.filter_by(student_id=student_id).order_by(Application.applied_date.desc()).first()

    # If no application found, keep application as None
    alert_message = None
    if not application:
        application = None
        alert_message = "Student has not applied to any internships."

    # Always pass BOTH variables
    return render_template(
        "view_student.html",
        application=application,
        alert_message=alert_message
    )




@company.route("/create_company_profile", methods=["GET", "POST"])
def create_company_profile():
    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    existing_profile = Company.query.filter_by(user_id=session["user_id"]).first()
    if existing_profile:
        # Pass message directly to template instead of flash
        return redirect(url_for("company.company_profile", message="You already have a profile. Redirecting to edit page.", category="info"))

    form = CompanyProfileForm()

    if form.validate_on_submit():
        if not form.logo.data:
            return render_template(
                "create_company_profile.html",
                form=form,
                message="Logo is required.",
                category="error"
            )

        file = form.logo.data
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(current_app.root_path, "static/uploads/logos")
        os.makedirs(upload_folder, exist_ok=True)
        file.save(os.path.join(upload_folder, filename))

        company = Company(
            user_id=session["user_id"],
            company_name=form.company_name.data,
            website=form.website.data,
            location=form.location.data,
            description=form.description.data,
            logo=filename
        )

        db.session.add(company)
        db.session.commit()

        session["company_id"] = company.id
        session["name"] = company.company_name

        return redirect(url_for("company.dashboard", message="Company profile created successfully!", category="success"))

    return render_template("create_company_profile.html", form=form)


@company.route("/company_profile", methods=["GET", "POST"])
def company_profile():
    if session.get("role") != "company":
        return redirect(url_for("auth_main.login"))

    form = CompanyProfileForm()
    company_profile = Company.query.filter_by(user_id=session["user_id"]).first()

    if not company_profile:
        # Pass message via query parameters instead of flash
        return redirect(url_for(
            "company.create_company_profile",
            message="No profile found. Please create your profile first.",
            category="warning"
        ))

    # Prefill form on GET
    if request.method == "GET":
        form.company_name.data = company_profile.company_name
        form.website.data = company_profile.website
        form.location.data = company_profile.location
        form.description.data = company_profile.description

    if form.validate_on_submit():
        # Optional logo update
        if form.logo.data:
            file = form.logo.data
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, "static/uploads/logos")
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))
            company_profile.logo = filename

        # Update profile data
        company_profile.company_name = form.company_name.data
        company_profile.website = form.website.data
        company_profile.location = form.location.data
        company_profile.description = form.description.data

        db.session.commit()

        # Update session name
        session["name"] = company_profile.company_name

        # ✅ Redirect back to same page with pop-up
        return redirect(url_for(
            "company.company_profile",  # redirect to same page
            message="Profile updated successfully!",
            category="success"
        ))

    return render_template(
        "company_profile.html",
        form=form,
        company=company_profile
    )