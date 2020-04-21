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
    """
    Prescription model.

    drug = name of drug
    desc = purpose/description of drug/prescription (aka "indication")
    strength = how much of the drug per tablet (e.g. 30mg)
    strength_unit = unit for strength (e.g. mg, ug)
    quantity = number of tablets per fill cycle
    form = form factor of pill (for now, only tablet aka 'tab')
    amount = number of units taken per intake
    route = how it gets into the body (only oral for now)
    freq = how many times per freq_repeat_unit
    freq_repeat = every <freq_repeat> <freq_repeat_unit>
    freq_repeat_unit = how often a day of intake repeats (e.g. every 3 days)
    duration = length of entire treatment
    refills = number of expected refills throughout duration
    time_of_day = time pill(s) should be taken (e.g. AM, PM)

    created = date this Prescription was created; auto-filled
    start_date = start date of first intake (regardless of refill)
    next_refill = date of next refill; auto-filled
    days_remaining = days until next refill; auto-filled nightly
    """
    id = db.Column(db.Integer, primary_key=True)

    # Prescription-related
    drug = db.Column(db.String(100), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=False)
    strength = db.Column(db.Integer, unique=False, nullable=False)
    strength_unit = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    form = db.Column(db.String(20), unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    route = db.Column(db.String(10), unique=False, nullable=False)
    freq = db.Column(db.Integer, unique=False, nullable=False)
    freq_repeat = db.Column(db.Integer, unique=False, nullable=False)
    freq_repeat_unit = db.Column(db.String(10), unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    duration_unit = db.Column(db.String(10), unique=False, nullable=False)
    refills = db.Column(db.Integer, unique=False, nullable=False)
    time_of_day = db.Column(db.String(10), unique=False, nullable=True)
    
    # Metadata
    start_date = db.Column(db.DateTime(), unique=False, nullable=False)
    created = db.Column(db.DateTime(), unique=False, nullable=False)
    last_refill_date = db.Column(db.DateTime(), unique=False, nullable=True)
    next_refill_date = db.Column(db.DateTime(), unique=False, nullable=True)
    refill_num = db.Column(db.Integer, unique=False, nullable=True)
    days_until_refill = db.Column(db.Integer, unique=False, nullable=True)

    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)


class PatientForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email")
    age = IntegerField("Age", validators=[DataRequired()])
    weight = IntegerField("Weight", validators=[DataRequired()])


class PrescriptionForm(FlaskForm):
    drug = StringField("Drug name", validators=[DataRequired()])
    # desc = StringField("Purpose / description", validators=[DataRequired()])
    # strength = IntegerField("Strength", validators=[DataRequired()])
    # strength_unit = StringField("Strength unit", validators=[DataRequired()])
    # quantity = IntegerField("Quantity", validators=[DataRequired()])
    # form = StringField("Form", validators=[DataRequired()])
    # amount = IntegerField("Amount", validators=[DataRequired()])
    # route = StringField("Route", validators=[DataRequired()])
    # duration = IntegerField("Duration", validators=[DataRequired()])
    # duration_unit = StringField("Duration unit", validators=[DataRequired()])
    # refills = IntegerField("# Refills", validators=[DataRequired()])
    # dosage = StringField("Dosage", validators=[DataRequired()])
    # # time_of_day_am = 


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
