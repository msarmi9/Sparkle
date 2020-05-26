from datetime import datetime

from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_required

from app import db
from app.models.forms import PrescriptionForm
from app.models.medication import Prescription
from app.models.persons import Patient
from app.utils import adherence


bp = Blueprint("prescriptions", __name__)


@bp.route("/patients/<int:patient_id>/new-prescription", methods=("GET", "POST"))
@login_required
def add_prescription(patient_id):
    """Route to add a patient prescription via a form."""
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
            "drug_form": f.get("drug_form"),
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
        freq_info = adherence.DOSAGE_TO_FREQ[f.get("dosage")]
        rx_fields["freq"] = freq_info["freq"]
        rx_fields["freq_repeat"] = freq_info["freq_repeat"]
        rx_fields["freq_repeat_unit"] = freq_info["freq_repeat_unit"]

        # Non-form data; autofilled
        rx_fields["created"] = datetime.now()
        rx_fields["refill_num"] = 0
        rx_fields["last_refill_date"] = rx_fields["start_date"]
        rx_fields["patient"] = patient

        # Next refill day, days until next refill
        next_refill_date = adherence.get_next_refill_date(
            rx_fields["start_date"],
            rx_fields["duration"],
            rx_fields["duration_unit"],
            rx_fields["refills"],
            rx_fields["refill_num"],
        )
        rx_fields["next_refill_date"] = next_refill_date

        days_until_refill = adherence.get_days_until_refill(
            datetime.now(), next_refill_date
        )
        rx_fields["days_until_refill"] = days_until_refill

        for k, v in rx_fields.items():
            print(f"{k}: {v}")

        # Create Rx
        rx = Prescription(**rx_fields)
        db.session.add(rx)
        db.session.commit()

        return redirect(url_for("patients.profile", patient_id=patient_id))
    print(rx_form.errors)
    return render_template(
        "prescriptions/add_prescription.html", patient=patient, form=rx_form
    )
