from flask import Blueprint , render_template,session,flash,redirect,url_for,request
from app import db
from app.models.application import Application
from app.models.internship import Internship
from werkzeug.utils import secure_filename
from app.models.user import User
import os
from flask import current_app
from app.forms.application_form import InternshipApplicationForm
from app.models.student import Student
from functools import wraps
from app import create_app
import uuid
from app.utils.decorators import login_required
student = Blueprint("student",__name__, url_prefix="/student")

# UPLOAD_FOLDER = os.path.join("static", "uploads", "student_profile")
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)




# Decorator to ensure profile exists
def student_profile_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("role") != "student":
            return redirect(url_for("auth_main.login"))
        student_obj = Student.query.filter_by(user_id=session.get("user_id")).first()
        if not student_obj:
            return redirect(url_for("student.create_profile"))
        return f(*args, **kwargs)
    return decorated

@student.route("/dashboard")
@login_required(role="student")
@student_profile_required
def dashboard():

    if session.get("role") != "student":
        return redirect(url_for("auth_main.login"))

    student_id = session.get("user_id")   # 🔥 FIXED

    internships = Internship.query.all()

    total_applications = Application.query.filter_by(
        student_id=student_id
    ).count()

    accepted = Application.query.filter_by(
        student_id=student_id,
        status="accepted"
    ).count()

    pending = Application.query.filter_by(
        student_id=student_id,
        status="pending"
    ).count()

    rejected = Application.query.filter_by(
        student_id=student_id,
        status="rejected"
    ).count()

    applied_ids = [
        app.internship_id
        for app in Application.query.filter_by(student_id=student_id).all()
    ]

    return render_template(
        "student_dashboard.html",
        internships=internships,
        applied_ids=applied_ids,
        total_applications=total_applications,
        accepted=accepted,
        pending=pending,
        rejected=rejected
    )


@student.route("/my_applications")
@login_required(role="student")
def my_applications():

    applications = Application.query.filter_by(
        student_id=session["user_id"]
    ).all()

    return render_template(
        "my_applications.html",
        applications=applications
    )

@student.route("/apply/<int:id>", methods=["GET", "POST"])
@login_required(role="student")
def apply_internship(id):

    # ✅ Check login FIRST
    if "user_id" not in session:
        return redirect(url_for("auth_main.login", login_required="true"))

    # ✅ Check role
    if session.get("role") != "student":
        return redirect(url_for("main.home", student_only="true"))

    student_id = session.get("user_id")
    internship = Internship.query.get_or_404(id)
    form = InternshipApplicationForm()

    if form.validate_on_submit():

        existing = Application.query.filter_by(
            student_id=student_id,
            internship_id=id
        ).first()

        if existing:
            return redirect(url_for("main.internships", already_applied="true"))

        file = form.resume.data
        filename = secure_filename(file.filename)

        filepath = os.path.join(
            current_app.root_path,
            "static/uploads/resumes",
            filename
        )

        file.save(filepath)

        application = Application(
            student_id=student_id,
            internship_id=id,
            full_name=form.full_name.data,
            email=form.email.data,
            degree=form.degree.data,
            college=form.college.data,
            skills=form.skills.data,
            cover_letter=form.cover_letter.data,
            resume=filename,
            status="pending"
        )

        db.session.add(application)
        db.session.commit()

        # ✅ Redirect with query parameter instead of flash
        return redirect(url_for("student.dashboard", applied="true"))

    return render_template(
        "apply_internship.html",
        form=form,
        internship=internship
    )


# ✅ Correct BASE DIR (project root)
BASE_DIR = os.getcwd()

# ✅ Correct upload folder (must match static path)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "app/static/uploads/student_profile")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@student.route("/create_profile", methods=["GET", "POST"])
@login_required(role="student")
def create_profile():

    if session.get("role") != "student":
        return redirect(url_for("auth_main.login"))

    student_obj = Student.query.filter_by(user_id=session["user_id"]).first()

    if not student_obj:
        student_obj = Student(user_id=session["user_id"])
        db.session.add(student_obj)
        db.session.commit()

    if request.method == "POST":

        # ✅ Save form data
        student_obj.full_name = request.form.get("full_name")
        student_obj.email = request.form.get("email")
        student_obj.degree = request.form.get("degree")
        student_obj.college = request.form.get("college")
        student_obj.skills = request.form.get("skills")

        # ✅ Handle file upload
        profile_pic_file = request.files.get("profile_pic")

        if profile_pic_file and profile_pic_file.filename != "":
            filename = str(uuid.uuid4()) + "_" + secure_filename(profile_pic_file.filename)

            file_path = os.path.join(UPLOAD_FOLDER, filename)

            print("Saving image to:", file_path)  # DEBUG

            profile_pic_file.save(file_path)

            # ✅ Save filename in DB
            student_obj.profile_pic = filename

            print("Saved filename:", filename)  # DEBUG

        db.session.commit()

        # ✅ IMPORTANT FIX: reload same page
        return redirect(url_for("student.create_profile", profile_updated="true"))

    return render_template("create_student_profile.html", student=student_obj)


@student.route("/profile", methods=["GET", "POST"])
@login_required(role="student")
@student_profile_required
def profile():
    if session.get("role") != "student":
        return redirect(url_for("auth_main.login"))

    student_id = session.get("student_id")
    if not student_id:
        return redirect(url_for("auth_main.login"))

    student_data = Student.query.get(student_id)
    if not student_data:
        return redirect(url_for("student.create_profile"))

    show_popup = False
    popup_message = ""

    # ✅ Correct upload folder (IMPORTANT FIX)
    upload_folder = os.path.join(current_app.root_path, "static", "uploads", "student_profile")
    os.makedirs(upload_folder, exist_ok=True)

    if request.method == "POST":
        student_data.full_name = request.form.get("full_name")
        student_data.email = request.form.get("email")
        student_data.degree = request.form.get("degree")
        student_data.college = request.form.get("college")
        student_data.skills = request.form.get("skills")

        file = request.files.get("profile_pic")

        if file and file.filename != "":
            filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            student_data.profile_pic = filename

        db.session.commit()

        show_popup = True
        popup_message = "Profile updated successfully!"

    # ✅ fallback image
    profile_img = student_data.profile_pic if student_data.profile_pic else "default_profile.png"

    return render_template(
        "student_profile.html",
        student=student_data,
        profile_img=profile_img,
        show_popup=show_popup,
        popup_message=popup_message
    )