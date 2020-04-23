from app.utils import *
from collections import defaultdict
from flask_wtf import FlaskForm
from flask_login import UserMixin
from flask_wtf.file import FileRequired
import numpy as np
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import (
    FileField,
    PasswordField,
    StringField,
    SubmitField,
    IntegerField,
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

    # One-to-many relationship
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

    # Foreign key
    doctor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # One-to-many relationship
    prescriptions = db.relationship("Prescription", backref="patient", lazy=True)

    def all_intakes(self, start=None, end=None):
        """
        Return Intake objects associated with this Patient.
        start: datetime - optional start date for filtering
        end: datetime - optional end date for filtering

        TODO: Implement start, end filtering
        NOTE: There's probably a better way of doing this.  Perhaps setting Patient
              as a foreign key in Intake?
        """
        all_intakes = []
        for rx in self.prescriptions:
            all_intakes += rx.intakes
        return all_intakes

    def adherence_stats(self):
        """
        Return adherence statistics on a per-Prescription basis.
        return: dict - <prescription ID>: <details>
        Example:
        {
            1: {
                'frac_on_time': 0.932,
                'frac_required_intakes': 0.976
            },
            19: {
                'frac_on_time': 0.389,
                'frac_required_intakes': 1.0
            },
            ...
        }
        """
        stats = defaultdict(lambda: defaultdict(float))
        for rx in self.prescriptions:
            stats[rx.id]["frac_on_time"] = rx.frac_on_time()
            stats[rx.id]["frac_required_intakes"] = rx.frac_required_intakes()
        return dict(stats)

    def frac_adhering_prescriptions(
        self, on_time_threshold=0.9, required_intakes_threshold=0.9
    ):
        if len(self.prescriptions) == 0:
            return {}
        adherence = {}
        frac_on_time_by_rx = []
        frac_required_intakes_by_rx = []
        stats = self.adherence_stats()
        for rx_id, details in stats.items():
            frac_on_time_by_rx.append(details["frac_on_time"])
            frac_required_intakes_by_rx.append(details["frac_required_intakes"])

        adherence["on_time"] = np.sum(
            np.array(frac_on_time_by_rx) >= on_time_threshold
        ) / len(frac_on_time_by_rx)

        adherence["required_intakes"] = np.sum(
            np.array(frac_required_intakes_by_rx) >= required_intakes_threshold
        ) / len(frac_required_intakes_by_rx)
        return adherence

    def is_adherent(self, on_time_threshold=0.9, required_intakes_threshold=0.9):
        stats = self.adherence_stats()
        for rx_id, details in stats.items():
            if (
                details["frac_on_time"] <= on_time_threshold
                or details["frac_required_intakes"] <= required_intakes_threshold
            ):
                return False
        return True


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

    # One-to-many relationship
    intakes = db.relationship("Intake", backref="prescription", lazy=True)

    def has_started(self):
        return datetime.now() >= self.start_date

    def is_adherent(self, on_time_threshold=0.9, required_intakes_threshold=0.9):
        return (
            self.frac_on_time() >= on_time_threshold
            and self.frac_required_intakes() >= required_intakes_threshold
        )

    def frac_on_time(self):
        """
        Return fraction of intakes that were on time, out of all recorded
        intakes.
        """
        if len(self.intakes) == 0:
            return 1.0
        on_time = Intake.query.filter_by(prescription_id=self.id, on_time=True).all()
        return len(on_time) / len(self.intakes)

    def frac_required_intakes(self):
        """
        Return fraction of recorded intakes, out of total number of intakes
        that are supposed to be recorded by this time.
        """

        # start of treatment until yesterday
        days_since_start = (datetime.now() - self.start_date).days - 1
        if days_since_start <= 0:
            return 1.0
        pills_per_day = int(
            self.amount
            * self.freq
            / (self.freq_repeat * DAY_STD[self.freq_repeat_unit])
        )
        n_required_intakes = days_since_start * pills_per_day

        if n_required_intakes == 0:
            return 1.0
        return len(self.intakes) / n_required_intakes


class Intake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s3_url = db.Column(db.String(500), unique=True, nullable=True)
    recording_data = db.Column(db.JSON(), unique=False, nullable=True)
    timestamp = db.Column(db.DateTime(), unique=False, nullable=False)
    on_time = db.Column(db.Boolean(), unique=False, nullable=False)

    # Foreign key
    prescription_id = db.Column(
        db.Integer, db.ForeignKey("prescription.id"), nullable=False
    )


class PatientForm(FlaskForm):
    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email")
    age = IntegerField("Age", validators=[DataRequired()])
    weight = IntegerField("Weight", validators=[DataRequired()])


class PrescriptionForm(FlaskForm):
    # TODO: We technically don't need these wtf/Flask forms.
    #       The only reason why we have them now is to provide the CSRF token
    #       to the frontend/templates when rendering the form.
    #       At least one field is needed for this FlaskForm so
    #       that's why `drug` is still here.
    drug = StringField("Drug name", validators=[DataRequired()])


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
