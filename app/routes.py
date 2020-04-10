from app import application, db
from app.classes import *
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, login_required, logout_user
import logging
import os
import numpy as np
from io import StringIO


# Home / splash page --------------------------------------------------------
@application.route('/home')
@application.route('/')
def index():
    """
    Home page of our site. Many other pages redirect here.
    """
    return render_template('splash.html', message='Welcome to Sparkle!')

# Dashboard - visible once a user logs in -----------------------------------
@application.route('/dashboard')
@login_required
def dashboard():
    """
    The main dashboard for our site, only made visible to the user once logged
    in.
    """
    return render_template('dashboard.html', patients=['TODO'])


# New user registration -----------------------------------------------------
@application.route('/register',  methods=('GET', 'POST'))
def register():
    """
    Page that allows users to register an account on our site.
    """
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        password = registration_form.password.data
        email = registration_form.email.data

        user_count = User.query.filter_by(username=username).count() \
            + User.query.filter_by(email=email).count()
        if (user_count > 0):
            return '<h1>Error - Existing user : ' + username \
                   + ' OR ' + email + '</h1>'
        else:
            user = User(username, email, password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=registration_form)


# User login ------------------------------------------------------------------
@application.route('/login', methods=['GET', 'POST'])
def login():
    """
    Page that allows registered users to log-in to our site.
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
            return redirect(url_for('dashboard'))
    else:
        print(login_form.errors)

    return render_template('login.html', form=login_form)


# User logout ---------------------------------------------------------------
@application.route('/logout')
def logout():
    """
    Page that allows logged-in users to logout.
    """
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
    Post route that receives and responds with json data.
    Currently set up to receive smart watch sensor data from Apple Watch.
    """
    content = request.get_json()
    data = content["data"]
    print(f"data received: {data}")
    model_pred_dict = adherence_model(data)

    # TODO: store metadata in DB
    return jsonify(model_pred_dict)
