from datetime import datetime
from datetime import timedelta

import numpy as np

from app import db
from app import login_manager
from app.adherence import DAY_STD
from app.models.persons import User


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
    last_refill_date = date of most recent refill
    next_refill = date of next refill; auto-filled field
    days_until_refill = days until next refill; auto-filled field

    patient_id = patient ID for which this Prescription is for
    intakes = collection of Intakes for this Prescription (one to many field)
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
        """
        Whether this Prescription is active, according to start date.
        """
        return datetime.now() >= self.start_date

    def is_adherent(
        self, on_time_threshold=0.9, required_intakes_threshold=0.9, date=datetime.now()
    ):
        """
        Whether this Prescription is adhered to by the Patient.
        """
        return (
            self.frac_on_time(date=date) >= on_time_threshold
            and self.frac_required_intakes(date=date) >= required_intakes_threshold
        )

    def frac_on_time(self, date=datetime.now()):
        """
        Return fraction of intakes that were on time, out of all recorded
        intakes.
        date: datetime - get fraction on time intakes on or before this date
        """
        intakes = list(filter(lambda i: i.timestamp <= date, self.intakes))
        if len(intakes) == 0:
            return 0.0
        on_time = Intake.query.filter(
            Intake.prescription_id == self.id, Intake.on_time, Intake.timestamp <= date,
        ).all()
        return len(on_time) / len(intakes)

    def frac_required_intakes(self, date=datetime.now()):
        """
        Return fraction of recorded intakes, out of total number of intakes
        that are supposed to be recorded by this time.
        date: datetime - get fraction on track intakes on or before this date
        """

        # start of treatment until specified date
        days_since_start = (date - self.start_date).days - 1
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

    def next_refill_date(self):
        """
        Return next refill date based on most recent (last) refill date
        and dosage information.
        """
        if self.refill_num == self.refills or self.refills == 0:
            return None
        days_per_cycle = np.floor(
            self.duration * DAY_STD[self.duration_unit] / (self.refills + 1)
        )
        return self.last_refill_date + timedelta(days=days_per_cycle)

    def days_until_refill(self):
        """
        Return number of days until next refill.
        If curr_date > next_refill_date, for instance, if refill was not fulfilled
            in time, then days until refill is still 0.
        """
        if self.next_refill_date() is None:
            return None
        return max([(self.next_refill_date() - datetime.now()).days, 0])

    def generate_schedule(self):
        """
        Generates the schedule which is a list of rx's, where each
        rx is a list of dictionaries with key being the date and value being
        another dictionary of metadata.

        Currently only works for the case when freq_repeat = 1 and
        freq_repeat_unit = day
        """
        dates = [self.start_date + timedelta(days=i) for i in range(self.duration)]
        schedule = [
            {
                date: {
                    "timestamp": date + timedelta(hours=8)
                    if self.time_of_day == "AM"
                    else date + timedelta(hours=20),
                    "drug": self.drug,
                    "desc": self.desc,
                    "amount": self.amount,
                    "route": self.route,
                }
            }
            for date in dates
        ]
        return schedule


class Intake(db.Model):
    """
    Intake model. Intakes are created when the app receives a recording,
    indicating that a patient has taken medication.
    """

    id = db.Column(db.Integer, primary_key=True)
    s3_url = db.Column(db.String(500), unique=True, nullable=True)
    recording_data = db.Column(db.JSON(), unique=False, nullable=True)
    timestamp = db.Column(db.DateTime(), unique=False, nullable=False)
    on_time = db.Column(db.Boolean(), unique=False, nullable=False)

    # Foreign key
    prescription_id = db.Column(
        db.Integer, db.ForeignKey("prescription.id"), nullable=False
    )


db.create_all()
db.session.commit()
