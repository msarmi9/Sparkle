from io import StringIO
import os
from datetime import date, datetime, timedelta

from app import application, db
from app.utils import *
from app.classes import (
    User,
    Patient,
    Prescription,
    PrescriptionForm,
    Patient,
    PatientForm,
    RegistrationForm,
    LogInForm,
    UploadFileForm,
)

from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
import numpy as np


# Home / splash page --------------------------------------------------------
@application.route("/")
@application.route("/home")
def index():
    """
    Render splash/home page.
    """
    return render_template("splash.html", message="Welcome to Sparkle!")


# Dashboard - visible once a user logs in -----------------------------------
@application.route("/dashboard")
@login_required
def dashboard():
    """
    Render dashboard for doctors to get comprehensive view of patient 
    adherence trends and statistics.
    """
    patients = User.query.filter_by(id=current_user.id).first().patients
    if len(patients) == 0:
        return render_template("dashboard.html", patients=patients)
    n_adherent = len(list(filter(lambda p: p.is_adherent(), patients)))
    patient_adherence = round(n_adherent / len(patients) * 100)

    rxs = Prescription.query.all()
    if len(rxs) == 0:
        rx_adherence = 1.0
    else:
        adherent_rxs = list(filter(lambda rx: rx.is_adherent(), rxs))
        rx_adherence = round(len(adherent_rxs) / len(rxs) * 100)

    adhering_patients = list(
        filter(lambda p: p.is_adherent() and len(p.prescriptions) != 0, patients)
    )
    nonadhering_patients = list(
        filter(lambda p: not p.is_adherent() and len(p.prescriptions) != 0, patients)
    )
    unprescribed_patients = list(filter(lambda p: len(p.prescriptions) == 0, patients))
    return render_template(
        "dashboard.html",
        patients=patients,
        patient_adherence=patient_adherence,
        rx_adherence=rx_adherence,
        adhering_patients=adhering_patients,
        nonadhering_patients=nonadhering_patients,
        unprescribed_patients=unprescribed_patients,
    )


# Patient profile -----------------------------------------------------------
@application.route("/patients/<int:patient_id>", methods=("GET", "POST"))
@login_required
def patient_profile(patient_id):
    """
    'Detail' view for a particular patient.
    """
    patient = Patient.query.filter_by(id=patient_id).first()
    prescriptions = patient.prescriptions
    return render_template(
        "patient_profile.html", patient=patient, prescriptions=prescriptions
    )


# New prescription for patient ----------------------------------------------
@application.route(
    "/patients/<int:patient_id>/new-prescription", methods=("GET", "POST")
)
@login_required
def add_prescription(patient_id):
    """
    Route to add a prescription from a form.
    """
    rx_form = PrescriptionForm()
    patient = Patient.query.filter_by(id=patient_id).first()

    if request.method == "POST":
        f = request.form

        # Basic data directly from form input
        rx_fields = {
            "drug": f.get("drug"),
            "desc": f.get("desc"),
            "strength": int(f.get("strength")),
            "strength_unit": f.get("strength_unit"),
            "quantity": int(f.get("quantity")),
            "form": f.get("drug_form"),
            "amount": int(f.get("amount")),
            "route": f.get("route"),
            "duration": int(f.get("duration")),
            "duration_unit": f.get("duration_unit")[:-1],
            "refills": int(f.get("refills")),
            "time_of_day": f"{f.get('time_of_day_am')}, {f.get('time_of_day_pm')}",
            "start_date": datetime.strptime(f.get("start_date"), "%Y-%m-%d"),
        }

        # Time of day
        if f.get("time_of_day_am"):
            if f.get("time_of_day_pm"):
                tod = "AM, PM"
            else:
                tod = "AM"
        elif f.get("time_of_day_pm"):
            tod = "PM"
        else:
            tod = None
        rx_fields["time_of_day"] = tod

        # Translate dosage to frequency info
        freq_info = DOSAGE_TO_FREQ[f.get("dosage")]
        rx_fields["freq"] = freq_info["freq"]
        rx_fields["freq_repeat"] = freq_info["freq_repeat"]
        rx_fields["freq_repeat_unit"] = freq_info["freq_repeat_unit"]

        # Non-form data; autofilled
        rx_fields["created"] = datetime.now()
        rx_fields["refill_num"] = 0
        rx_fields["last_refill_date"] = rx_fields["start_date"]
        rx_fields["patient"] = patient

        # Next refill day, days until next refill
        next_refill_date = get_next_refill_date(
            rx_fields["start_date"],
            rx_fields["duration"],
            rx_fields["duration_unit"],
            rx_fields["refills"],
            rx_fields["refill_num"],
        )
        rx_fields["next_refill_date"] = next_refill_date

        days_until_refill = get_days_until_refill(datetime.now(), next_refill_date)
        rx_fields["days_until_refill"] = days_until_refill

        for k, v in rx_fields.items():
            print(f"{k}: {v}")

        # Create Rx
        rx = Prescription(**rx_fields)
        db.session.add(rx)
        db.session.commit()

        return redirect(url_for("patient_profile", patient_id=patient_id))
    print(rx_form.errors)
    return render_template("add_prescription.html", patient=patient, form=rx_form)


# New patient ---------------------------------------------------------------
@application.route("/new-patient", methods=("GET", "POST"))
@login_required
def add_patient():
    patient_form = PatientForm()
    if patient_form.validate_on_submit():
        firstname = patient_form.firstname.data
        lastname = patient_form.lastname.data
        email = patient_form.email.data
        age = patient_form.age.data
        weight = patient_form.weight.data

        patient = Patient(
            firstname=firstname,
            lastname=lastname,
            email=email,
            age=age,
            weight=weight,
            user=current_user,
        )
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_patient.html", form=patient_form)


# New user registration -----------------------------------------------------
@application.route("/register", methods=("GET", "POST"))
def register():
    """
    Registers a user from form data.
    """
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        firstname = registration_form.firstname.data
        lastname = registration_form.lastname.data
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = (
            User.query.filter_by(username=username).count()
            + User.query.filter_by(email=email).count()
        )
        if user_count > 0:
            return "<h1>Error - Existing user : " + username + " OR " + email + "</h1>"
        else:
            user = User(firstname, lastname, username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html", form=registration_form)


# User login ------------------------------------------------------------------
@application.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs in a user.
    """
    login_form = LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = User.query.filter_by(username=username).first()

        # Login and validate the user; take them to dashboard page.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard"))
    return render_template("login.html", form=login_form)


# User logout ------------------------------------------------------------------
@application.route("/logout")
def logout():
    """
    Logs out a user.
    """
    logout_user()
    return redirect(url_for("index"))


# File upload ---------------------------------------------------------------
@application.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Upload a file from the client machine.
    """
    file = UploadFileForm()
    if file.validate_on_submit():
        f = file.file_selector.data
        filename = f.filename

        file_dir_path = os.path.join(application.instance_path, "files")
        file_path = os.path.join(file_dir_path, filename)
        f.save(file_path)
        return redirect(url_for("index"))
    return render_template("upload.html", form=file)


# Data receiving endpoint ---------------------------------------------------
def adherence_model(data):
    """
    takes in gyroscope data as a string
    and makes binary prediction about whether or not medication
    was consumed
    """
    gyro_data = np.genfromtxt(StringIO(data), delimiter=",", skip_header=1)
    global_mean = np.abs(gyro_data).mean(axis=1).mean(axis=0)
    print(global_mean)
    if global_mean > 0.5:
        pred_string = "You just took your medication!"
    else:
        pred_string = "It does not appear you took any medication."
    return {"pred_string": pred_string, "pred": global_mean}


@application.route("/send-data", methods=["POST"])
def send_data():
    """
    Json in and json out
    """
    content = request.get_json()
    data = content["data"]
    print(f"data received: {data}")
    model_pred_dict = adherence_model(data)

    # TODO: store metadata in DB
    return jsonify(model_pred_dict)
