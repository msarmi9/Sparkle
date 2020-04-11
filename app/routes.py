from app import application, db
from app.classes import *
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
import logging
import os
import numpy as np
from io import StringIO


# Home / splash page --------------------------------------------------------
@application.route('/')
@application.route('/home')
def index():
    return render_template('splash.html', message='Welcome to Sparkle!')    

# Dashboard - visible once a user logs in -----------------------------------
@application.route('/dashboard')
@login_required
def dashboard():
    patients = User.query.filter_by(id=current_user.id).first().patients
    return render_template('dashboard.html', patients=patients)


# Patient profile -----------------------------------------------------------
@application.route('/patients/<int:patient_id>', methods=('GET', 'POST'))
@login_required
def patient_profile(patient_id):
    patient = Patient.query.filter_by(id=patient_id).first()
    prescriptions = patient.prescriptions
    return render_template('patient_profile.html',
                           patient=patient, prescriptions=prescriptions)


# New prescription for patient ----------------------------------------------
@application.route('/patients/<int:patient_id>/new-prescription',
                   methods=('GET', 'POST'))
@login_required
def add_prescription(patient_id):
    rx_form = PrescriptionForm()
    patient = Patient.query.filter_by(id=patient_id).first()
    if rx_form.validate_on_submit():
        drug = rx_form.drug.data
        desc = rx_form.desc.data 
        freq = rx_form.freq.data
        cycle_n = rx_form.cycle_n.data
        cycle_unit = rx_form.cycle_unit.data
        start_pills = rx_form.start_pills.data
        last_refill_date = rx_form.last_refill_date.data
        remaining_pills = start_pills  # No pills taken yet at this point

        rx = Prescription(drug=drug, desc=desc, freq=freq, cycle_n=cycle_n,
                          cycle_unit=cycle_unit, start_pills=start_pills,
                          last_refill_date=last_refill_date,
                          remaining_pills=remaining_pills,
                          next_refill_date='2020-05-10', patient=patient)

        # TODO: latest, next refill dates should be date fields.
        # TODO: calculate next refill date based on freq, cycle_n, cycle_units
        # and number of starting pills.

        db.session.add(rx)
        db.session.commit()
        return redirect(url_for('patient_profile', patient_id=patient_id))
    return render_template('add_prescription.html',
                           patient=patient, form=rx_form)


# New patient ---------------------------------------------------------------
@application.route('/new-patient',  methods=('GET', 'POST'))
@login_required
def add_patient():
    patient_form = PatientForm()
    if patient_form.validate_on_submit():
        firstname = patient_form.firstname.data
        lastname = patient_form.lastname.data 
        email = patient_form.email.data
        age = patient_form.age.data
        weight = patient_form.weight.data

        patient = Patient(firstname=firstname, lastname=lastname, email=email,
                          age=age, weight=weight, user=current_user)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_patient.html', form=patient_form)


# New user registration -----------------------------------------------------
@application.route('/register',  methods=('GET', 'POST'))
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        firstname = registration_form.firstname.data
        lastname = registration_form.lastname.data 
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = User.query.filter_by(username=username).count() \
                     + User.query.filter_by(email=email).count()
        if (user_count > 0):
            return '<h1>Error - Existing user : ' + username \
                   + ' OR ' + email + '</h1>'
        else:
            user = User(firstname, lastname, username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


# User login ------------------------------------------------------------------
@application.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LogInForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        # Look for it in the database.
        user = User.query.filter_by(username=username).first()

        # Login and validate the user; take them to dashboard page.
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=login_form)


# User logout ------------------------------------------------------------------
@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# File upload ---------------------------------------------------------------
@application.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Upload a file from the client machine.
    """
    file = UploadFileForm()
    if file.validate_on_submit():
        f = file.file_selector.data
        filename = f.filename

        file_dir_path = os.path.join(application.instance_path, 'files')
        file_path = os.path.join(file_dir_path, filename)
        f.save(file_path)
        return redirect(url_for('index'))
    return render_template('upload.html', form=file)

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


@application.route('/send-data', methods=['POST'])
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
