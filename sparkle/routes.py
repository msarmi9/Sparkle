import io
import json
import os
from datetime import date
from datetime import datetime

import numpy as np
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from modeling.preprocessing import *
from sparkle import application
from sparkle import db
from sparkle.forms import LoginForm
from sparkle.forms import PatientForm
from sparkle.forms import PrescriptionForm
from sparkle.forms import RegistrationForm
from sparkle.forms import UploadFileForm
from sparkle.medication import Intake
from sparkle.medication import Prescription
from sparkle.persons import Patient
from sparkle.persons import User
from sparkle.utils import *


# Home / splash page --------------------------------------------------------
@application.route("/")
@application.route("/home")
def index():
    """
    Render splash/home page.
    """
    return render_template("splash.html", message="Welcome to Sparkle!")


# About page --------------------------------------------------------
@application.route("/about")
def about():
    """
    Render about i.e. learn more page.
    """
    return render_template("about.html")


# Dashboard - visible once a user logs in -----------------------------------
@application.route("/dashboard")
@login_required
def dashboard():
    """
    Render dashboard page which includes plots/analytics of adherence trends
    and statistics.
    """
    patients = Patient.query.filter_by(doctor_id=current_user.id).all()
    rxs = []
    for p in patients:
        rxs += p.prescriptions
    adh_over_time = plot_adherence_rates_over_time(patients, rxs)
    top_general_adh = plot_top_general_adherence_by_drug_name(rxs, n=5)
    top_ontime_adh = plot_top_ontime_adherence_by_drug_name(rxs, n=5)

    return render_template(
        "dashboard.html",
        adh_over_time=adh_over_time,
        top_general_adh=top_general_adh,
        top_ontime_adh=top_ontime_adh,
    )


def _render_patients_page(template):
    """Render a template for one of ontrack, deviating, and all patients."""
    patients = User.query.filter_by(id=current_user.id).first().patients
    if len(patients) == 0:
        return render_template("patients.html", patients=patients)
    n_adherent = len(list(filter(lambda p: p.is_adherent(), patients)))
    patient_adherence = round(n_adherent / len(patients) * 100)

    rxs = Prescription.query.all()
    if len(rxs) == 0:
        rx_adherence = 100
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
        template,
        patients=patients,
        patient_adherence=patient_adherence,
        rx_adherence=rx_adherence,
        adhering_patients=adhering_patients,
        nonadhering_patients=nonadhering_patients,
        unprescribed_patients=unprescribed_patients,
    )


# Patient cards display -----------------------------------------------------
@application.route("/patients")
@login_required
def patients():
    """
    Render patient cards for doctors to quickly monitor patients who are
    adhering and deviating.
    """
    return _render_patients_page("patients.html")


# Patients_deviating - visible once a user logs in -----------------------------------
@application.route("/patients_deviating")
@login_required
def patients_deviating():
    """Render patients page of the list of patients."""
    return _render_patients_page("patients_deviating.html")


# Patients_unprescribed - visible once a user logs in -----------------------------------
@application.route("/patients_unprescribed")
@login_required
def patients_unprescribed():
    """Render page listing unprescribed patients."""
    return _render_patients_page("patients_unprescribed.html")


# Patients_ontrack - visible once a user logs in -----------------------------------
@application.route("/patients_ontrack")
@login_required
def patients_ontrack():
    """Render page listing adhering patients."""
    return _render_patients_page("patients_ontrack.html")


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
            "start_date": datetime.strptime(f.get("start_date"), "%m/%d/%Y"),
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
        return redirect(url_for("patients"))
    return render_template("add_patient.html", form=patient_form)


# New user registration -----------------------------------------------------
@application.route("/register", methods=("GET", "POST"))
def register():
    """Registers a new doctor (user) from form data."""
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
    """Logs in a returning doctor (user)."""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = User.query.filter_by(username=username).first()

        # Login and validate the user; take them to dashboard page.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for("patients"))
    return render_template("login.html", form=login_form)


# User logout ------------------------------------------------------------------
@application.route("/logout")
def logout():
    """
    Logs out a user.
    """
    logout_user()
    return redirect(url_for("index"))


# Forgot password ------------------------------------------------------------------
@application.route("/forgot_password")
def forgot_password():
    """
    Redirects to 'forgot_password' page.
    """

    return render_template("forgot_password.html")


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
def adherence_model(
    data,
    classifier_path="./modeling/classifier.pkl",
    regressor_path="./modeling/regressor.pkl",
):
    """
    takes in accelerometer and gyroscope data as a string.
    """

    # run the pill classifier process
    X = preprocess(io.StringIO(data), regression=False)
    classifier = pickle.load(open(classifier_path, "rb"))
    classifier_pred = classifier.predict(X).item()

    if classifier_pred == 0:
        pred_string = "It does not appear you took any medication."
        return {
            "pred_string": pred_string,
            "pred_type": "classification",
            "pred": classifier_pred,
        }
    else:
        # run the regression process
        X = preprocess(io.StringIO(data), regression=True)

        regressor = pickle.load(open(regressor_path, "rb"))
        predicted_pills = regressor.predict(X).round().item()
        predicted_pills = max(min(predicted_pills, 30), 1)

        pred_string = f"It looks like you have {predicted_pills - 1} pills remaining."
        return {
            "pred_string": pred_string,
            "pred_type": "regression",
            "pred": predicted_pills,
        }


@application.route("/send-data", methods=["POST"])
def send_data():
    """
    Json in and json out
    """
    content = request.get_json()

    # retrieving data for Intake table from json
    id = content["id"]  # request.headers["User-Agent"]
    s3_url = content["s3_url"]
    recording_data = content["recording_data"]
    timestamp = datetime.strptime(content["timestamp"], "%Y-%m-%d_%H:%M:%S")
    on_time = bool(int(content["on_time"]))
    print(f"data received: {recording_data}")

    # saving data to Intake table
    # rx = Prescription.query.filter_by(id=my_prescription_id).first()
    # note: this _requires_ there to be a prescription already in db!
    intake = Intake(
        s3_url=s3_url,
        recording_data=json.dumps(content),
        timestamp=timestamp,
        on_time=on_time,
        prescription_id=id,
    )
    db.session.add(intake)
    db.session.commit()

    model_pred_dict = adherence_model(recording_data)

    return jsonify(model_pred_dict)


# mobile login  --------------------------------------------------------
@application.route("/mobile-login", methods=["POST"])
def mobile_login():
    """
    login from web app
    today's schedule returns a list of dictionaries with metadata
    """
    # retrieving data from json request
    content = request.get_json()
    patient_id = content["patient_id"]

    # getting all prescriptions for all schedules
    rxs = Prescription.query.filter_by(patient_id=patient_id).all()
    schedules = [rx.generate_schedule() for rx in rxs]

    # getting only prescription for today (this can probably be optimized)
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    todays_schedule = [
        [metadata for date, metadata in day.items() if date == today]
        for schedule in schedules
        for day in schedule
    ]

    # getting name from Patient Table
    firstname = Patient.query.filter_by(id=patient_id).first().firstname

    # flattening and transforming datetime object to string
    todays_schedule = [
        metadata for rx in todays_schedule for metadata in rx if metadata
    ]
    for schedule in todays_schedule:
        schedule["timestamp"] = schedule["timestamp"].strftime("%Y-%m-%d_%H:%M:%S")
        schedule["firstname"] = firstname

    return jsonify(todays_schedule)