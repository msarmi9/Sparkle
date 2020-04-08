from app import application, db
from app.classes import *
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
import logging
import os


# Home / splash page --------------------------------------------------------
@application.route('/')
@application.route('/home')
def index():
    return render_template('splash.html', message='Welcome to Sparkle!')	

# Dashboard - visible once a doc logs in ------------------------------------
@application.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', patients=['TODO'])	

# Data receiving endpoint ---------------------------------------------------
@application.route('/send-data', methods=['POST'])
def send_data():

	pid = request.args.get('patient_id')
	timestamp = request.args.get('timestamp')
	data = request.args.get('data')

	# TODO: store metadata in DB
	return f"Received patient ID {pid} at {timestamp}\nData:\n{data}"


# New user registration -----------------------------------------------------
@application.route('/register',  methods=('GET', 'POST'))
def register():
    registration_form = RegistrationForm()
    # print('in register')
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
            return redirect(url_for('index'))
    # print('rendering register')
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
# @login_required
def logout():
    before_logout = '<h1> Before logout - is_autheticated : ' \
                    + str(current_user.is_authenticated) + '</h1>'

    logout_user()

    after_logout = '<h1> After logout - is_autheticated : ' \
                   + str(current_user.is_authenticated) + '</h1>'
    return before_logout + after_logout


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