from flask_wtf import FlaskForm
from flask_login import UserMixin
from flask_wtf.file import FileRequired
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import (
    FileField,
    PasswordField,
    StringField,
    SubmitField,
    IntegerField,
    TextAreaField,
)
from wtforms.validators import DataRequired

from app import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    patients = db.relationship("Patient", backref="user", lazy=True)

    def __init__(self, firstname, lastname, username, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=True)
    age = db.Column(db.Integer, unique=False, nullable=False)
    weight = db.Column(db.Integer, unique=False, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    prescriptions = db.relationship("Prescription", backref="patient", lazy=True)


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drug = db.Column(db.String(100), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=False)
    freq = db.Column(db.Integer, unique=False, nullable=False)
    cycle_n = db.Column(db.Integer, unique=False, nullable=False)
    cycle_unit = db.Column(db.String(50), unique=False, nullable=False)

    # freq = number of times per cycle e.g. 2 (twice), 1 (once)
    # cycle_n = every n <unit>
    # cycle_unit = unit of repeat e.g. day, week, month
    # Example Rx: "twice daily" --> freq=2, cycle_n=1, cycle_unit=day
    # Example Rx: "once every other day" --> freq=1, cycle_n=2, cycle_unit=day

    start_pills = db.Column(db.Integer, unique=False, nullable=False)
    remaining_pills = db.Column(db.Integer, unique=False, nullable=False)
    last_refill_date = db.Column(db.String(20), unique=False, nullable=False)
    next_refill_date = db.Column(db.String(20), unique=False, nullable=False)

    # start_pills = starting number of pills for this refill cycle
    # remaining_pills = remaining number of pills for this refill cycle
    # last_refill_date = when the Rx was last refilled (if first time, then date of first fill)
    # next_refill_date = when the Rx will be next refilled

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)


class PatientForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email")
    age = IntegerField("Age", validators=[DataRequired()])
    weight = IntegerField("Weight", validators=[DataRequired()])


class PrescriptionForm(FlaskForm):
    drug = StringField("Drug name", validators=[DataRequired()])
    desc = StringField("Purpose / description", validators=[DataRequired()])
    freq = IntegerField("Frequency", validators=[DataRequired()])
    cycle_n = IntegerField("Cycle number", validators=[DataRequired()])
    cycle_unit = StringField("Cycle unit", validators=[DataRequired()])
    start_pills = IntegerField("Starting number of pills", validators=[DataRequired()])
    # remaining_pills automatically populated in new_prescription route
    last_refill_date = StringField("Latest refill date", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LogInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UploadFileForm(FlaskForm):
    file_selector = FileField("File", validators=[FileRequired()])
    submit = SubmitField("Submit")


db.create_all()
db.session.commit()

# user_loader :
# This callback is used to reload the user object
# from the user ID stored in the session.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
