from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app import db
from app.models.forms import PatientForm
from app.models.medication import Prescription
from app.models.persons import Patient
from app.models.persons import User

bp = Blueprint("patients", __name__)


@bp.route("/patients")
@login_required
def patients():
    """
    Render patient cards for doctors to quickly monitor patients who are
    adhering and deviating.
    """
    return _render_patients_page("patients/patients.html")


@bp.route("/patients_deviating")
@login_required
def patients_deviating():
    """Render patients page of the list of patients."""
    return _render_patients_page("patients/patients_deviating.html")


@bp.route("/patients_unprescribed")
@login_required
def patients_unprescribed():
    """Render page listing unprescribed patients."""
    return _render_patients_page("patients/patients_unprescribed.html")


@bp.route("/patients_ontrack")
@login_required
def patients_ontrack():
    """Render page listing adhering patients."""
    return _render_patients_page("patients/patients_ontrack.html")


@bp.route("/patients/<int:patient_id>", methods=("GET", "POST"))
@login_required
def patient_profile(patient_id):
    """Detail view for a single patient patient."""
    patient = Patient.query.filter_by(id=patient_id).first()
    prescriptions = patient.prescriptions
    return render_template(
        "patients/patient_profile.html", patient=patient, prescriptions=prescriptions
    )


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
        return redirect(url_for(".patients"))
    return render_template("patients/add_patient.html", form=patient_form)


def _render_patients_page(template):
    """Render a template for one of ontrack, deviating, and all patients."""
    patients = User.query.filter_by(id=current_user.id).first().patients
    if len(patients) == 0:
        return render_template("patients/patients.html", patients=patients)
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
