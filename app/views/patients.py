from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app.models.forms import PatientForm
from app.models.persons import Patient


bp = Blueprint("patients", __name__)


@bp.route("/patients")
@login_required
def patients():
    """Render page listing unprescribed, deviating, and adhering patients. """
    patients = current_user.patients
    return render_template("patients/patients.html", patients=patients)


@bp.route("/patients_unprescribed")
@login_required
def patients_unprescribed():
    """Render page listing unprescribed patients."""
    patients = current_user.patients
    unprescribed = [p for p in patients if not p.prescriptions]
    return render_template("patients/patients.html", patients=unprescribed)


@bp.route("/patients_deviating")
@login_required
def patients_deviating():
    """Render page listing deviating patients."""
    patients = current_user.patients
    deviating = [p for p in patients if p.prescriptions and not p.is_adherent()]
    return render_template("patients/patients.html", patients=deviating)


@bp.route("/patients_ontrack")
@login_required
def patients_ontrack():
    """Render page listing adhering patients."""
    patients = current_user.patients
    adhering = [p for p in patients if p.prescriptions and p.is_adherent()]
    return render_template("patients/patients.html", patients=adhering)


@bp.route("/patients/search")
@login_required
def search():
    """Redirect to a patient profile page given first and last names."""
    try:
        first, last = request.args.get("name").split()
        patient_id = Patient.query.filter_by(firstname=first, lastname=last).first().id
    except:
        return redirect(url_for(".patients"))
    return redirect(url_for(".profile", patient_id=patient_id))


@bp.route("/patients/<int:patient_id>", methods=("GET", "POST"))
@login_required
def profile(patient_id):
    """Detail view for a single patient patient."""
    patient = Patient.query.filter_by(id=patient_id).first()
    rxs = patient.prescriptions
    return render_template("patients/profile.html", patient=patient, prescriptions=rxs)


@bp.route("/new-patient", methods=("GET", "POST"))
@login_required
def add_patient():
    patient_form = PatientForm()
    if patient_form.validate_on_submit():
        firstname = patient_form.firstname.data
        lastname = patient_form.lastname.data
        email = patient_form.email.data
        age = patient_form.age.data
        weight = patient_form.weight.data

        patient = Patient(firstname, lastname, email, age, weight, user=current_user)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for(".patients"))
    return render_template("patients/add_patient.html", form=patient_form)
