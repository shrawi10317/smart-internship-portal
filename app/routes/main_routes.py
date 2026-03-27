from flask import Blueprint, render_template,session,flash,redirect,url_for,request
from app.models.internship import Internship
from app.models.application import Application
from app.models.company import Company
from app.models.whishlist import Wishlist
# from app.routes.company_routes import dashboard
# from flask_mail import Message
# from app import mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail,Email
import time
import os
from app import db
from flask import current_app

import threading
main = Blueprint('main', __name__)

import threading

def send_email(to_email, subject, content, retries=3, delay=5):
    """Send email via SendGrid asynchronously with retry logic."""


    def send():
        for attempt in range(1, retries + 1):
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                message = Mail(
                    from_email=Email(os.environ.get("MAIL_USERNAME"), "Smart Internship"),
                    to_emails=to_email,
                    subject=subject,
                    html_content=content
                )
                message.reply_to = Email(os.environ.get("MAIL_USERNAME"), "Smart Internship")
                response = sg.send(message)
                print(f"✅ Email sent to {to_email}, Status: {response.status_code}")
                break
            except Exception as e:
                print(f"❌ Attempt {attempt} failed: {str(e)}")
                if attempt < retries:
                    print(f"⏳ Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"❌ Failed to send email after {retries} attempts.")

    # Run in a separate thread to avoid blocking
    threading.Thread(target=send).start()

@main.route("/")
def home():
    # Pop message safely
    logout_message = session.pop('logout_message', None)

    if "user_id" in session:
        if session.get("role") == "company":
            return redirect(url_for("company.dashboard"))
        elif session.get("role") == "student":
            return redirect(url_for("student.dashboard"))

    return render_template("index.html", logout_message=logout_message)

@main.route("/apply-redirect")
def apply_redirect():
    session["next_page"] = "internships"
    return redirect(url_for("auth_main.login"))

@main.route("/internships")
def internships():

    search = request.args.get("search")
    location = request.args.get("location")
    duration = request.args.get("duration")
    sort = request.args.get("sort")

    query = Internship.query

    # 🔍 FILTERS
    if search:
        query = query.filter(Internship.title.ilike(f"%{search}%"))

    if location:
        query = query.filter(Internship.location == location)

    # ✅ FIXED DURATION FILTER
    if duration:
        query = query.filter(Internship.duration == duration)

    # 🔽 SORTING
    if sort == "stipend_high":
        query = query.order_by(Internship.stipend.desc())
    elif sort == "stipend_low":
        query = query.order_by(Internship.stipend.asc())

    internships = query.all()

    # 📊 APPLY COUNT
    for internship in internships:
        internship.apply_count = Application.query.filter_by(
            internship_id=internship.id
        ).count()

    # ❤️ WISHLIST + APPLIED
    wishlist_ids = []
    applied_ids = []

    if session.get("role") == "student":
        user_id = session.get("user_id")

        wishlist = Wishlist.query.filter_by(student_id=user_id).all()
        wishlist_ids = [w.internship_id for w in wishlist]

        applied = Application.query.filter_by(student_id=user_id).all()
        applied_ids = [a.internship_id for a in applied]

    # 📍 DISTINCT LOCATIONS
    locations = db.session.query(Internship.location).distinct().all()
    locations = [loc[0] for loc in locations]

    # ⏱ DISTINCT DURATIONS
    durations = db.session.query(Internship.duration).distinct().all()
    durations = [dur[0] for dur in durations]

    return render_template(
        "internships.html",
        internships=internships,
        wishlist_ids=wishlist_ids,
        applied_ids=applied_ids,
        locations=locations,
        durations=durations
    )


@main.route("/companies")
def companies():
    page = request.args.get("page", 1, type=int)
    per_page = 6
    search = request.args.get("search", "", type=str)
    location = request.args.get("location", "", type=str)

    query = Company.query.filter(Company.company_name.isnot(None))  # only complete profiles

    if search:
        query = query.filter(Company.company_name.ilike(f"%{search}%"))
    if location:
        query = query.filter(Company.location == location)

    companies_paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "companies.html",
        companies=companies_paginated,
        search=search,
        location=location
    )


@main.route("/about")
def about():
    return render_template("about_us.html")

from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route("/contact", methods=["GET", "POST"])
def contact():
    sent = request.args.get("sent")
    error = request.args.get("error")

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color:#333;">
            <h2 style="color:#ff6b00;">New Message from SmartInternship Contact Form</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong><br>{message}</p>
            <hr>
            <p style="font-size:12px; color:#777;">
                This message was sent via SmartInternship Portal
            </p>
        </body>
        </html>
        """

        try:
            send_email(
                "shrawaniofficial6@gmail.com",  # ✅ your verified email
                "New Contact Message - SmartInternship",
                html_content
            )
            return redirect(url_for("main.contact", sent="true"))

        except Exception as e:
            return redirect(url_for("main.contact", error=str(e)))

    return render_template("contact.html", sent=sent, error=error)

# student.py (or main routes)

@main.route("/toggle-wishlist/<int:id>")
def toggle_wishlist(id):
    if session.get("role") != "student":
        return redirect(url_for("auth_main.login"))

    user_id = session.get("user_id")

    existing = Wishlist.query.filter_by(
        student_id=user_id,
        internship_id=id
    ).first()

    if existing:
        db.session.delete(existing)
    else:
        new_item = Wishlist(
            student_id=user_id,
            internship_id=id
        )
        db.session.add(new_item)

    db.session.commit()
    return redirect(request.referrer)

@main.route("/company/<int:id>")
def company_details(id):

    company = Company.query.get_or_404(id)

    internships = Internship.query.filter_by(company_id=id).all()

    applied_ids = []

    if session.get("user_id"):
        applied_ids = [
            a.internship_id
            for a in Application.query.filter_by(
                student_id=session.get("user_id")   # ✅ FIXED HERE
            ).all()
        ]

    return render_template(
        "company_details.html",
        company=company,
        internships=internships,
        applied_ids=applied_ids
    )

@main.route("/internship/<int:id>")
def internship_detail(id):

    internship = Internship.query.get_or_404(id)

    # 📊 Apply count
    apply_count = Application.query.filter_by(internship_id=id).count()

    # ❤️ Wishlist & Applied
    wishlist_ids = []
    applied_ids = []

    if session.get("role") == "student":
        user_id = session.get("user_id")

        wishlist = Wishlist.query.filter_by(student_id=user_id).all()
        wishlist_ids = [w.internship_id for w in wishlist]

        applied = Application.query.filter_by(student_id=user_id).all()
        applied_ids = [a.internship_id for a in applied]

    # 🔥 GET SKILLS FROM APPLICATION TABLE
    applications = Application.query.filter_by(internship_id=id).all()

    skills_list = []

    for app in applications:
        if app.skills:
            for skill in app.skills.split(','):
                if skill.strip():
                    skills_list.append(skill.strip())

    # remove duplicates
    skills_list = list(set(skills_list))

    return render_template(
        "internship_detail.html",
        internship=internship,
        apply_count=apply_count,
        wishlist_ids=wishlist_ids,
        applied_ids=applied_ids,
        skills_list=skills_list   # ✅ PASS
    )


@main.route("/test-email")
def test_email():
    """Route to send a test email to shrawaniw03@gmail.com"""
    try:
        send_email(
            "shrawaniw03@gmail.com",
            "🚀 Test Email from SmartInternship",
            """
            <h2 style='color:#ff6b00;'>SendGrid Test Email</h2>
            <p>If you see this message, SendGrid email is working correctly!</p>
            """
        )
        return "<h3>✅ Test email sent! Check your inbox (or spam) shortly.</h3>"
    except Exception as e:
        import traceback
        return f"<h3>❌ Test email failed:</h3><pre>{traceback.format_exc()}</pre>"